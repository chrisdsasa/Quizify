from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app, jsonify
from flask_login import login_user, logout_user, current_user, login_required
import os
from werkzeug.utils import secure_filename
from app import db
from app.models import User, Quiz, Question, QuizResult
from app.utils.pdf_processor import PDFProcessor
import json
import logging

main = Blueprint('main', __name__)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Helper functions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@main.route('/')
def index():
    return render_template('index.html', title='PDF Quiz Generator')

@main.route('/dashboard')
@login_required
def dashboard():
    quizzes = Quiz.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', title='Dashboard', quizzes=quizzes, QuizResult=QuizResult)

@main.route('/upload_pdf', methods=['GET', 'POST'])
@login_required
def upload_pdf():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'pdf_file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
            
        file = request.files['pdf_file']
        
        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_folder = current_app.config['UPLOAD_FOLDER']
            
            # Create upload folder if it doesn't exist
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
                
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)
            
            # Create a new quiz
            quiz = Quiz(
                title=request.form.get('title', 'Untitled Quiz'),
                description=request.form.get('description', ''),
                pdf_path=filepath,
                user_id=current_user.id
            )
            db.session.add(quiz)
            db.session.commit()
            
            # Process the PDF and generate questions
            try:
                # Get the number of questions from the form, default to 5
                num_questions = int(request.form.get('num_questions', 5))
                
                flash('PDF uploaded successfully! Generating quiz questions...', 'info')
                
                # Redirect to generate questions with the specified number
                return redirect(url_for('main.generate_questions', quiz_id=quiz.id, num_questions=num_questions))
            except Exception as e:
                logger.error(f"Error processing PDF: {str(e)}")
                flash(f'Error processing PDF: {str(e)}', 'danger')
                return redirect(url_for('main.dashboard'))
            
        else:
            flash('File type not allowed. Please upload a PDF.', 'danger')
            
    return render_template('upload.html', title='Upload PDF')

@main.route('/quiz/<int:quiz_id>')
@login_required
def view_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    # Ensure the current user is the owner of the quiz
    if quiz.user_id != current_user.id:
        flash('You do not have permission to view this quiz', 'danger')
        return redirect(url_for('main.dashboard'))
        
    questions = quiz.questions.all()
    
    # If there are no questions yet, generate them
    if not questions and quiz.pdf_path:
        return redirect(url_for('main.generate_questions', quiz_id=quiz.id))
        
    return render_template('quiz_detail.html', title=quiz.title, quiz=quiz, questions=questions)

@main.route('/quiz/<int:quiz_id>/generate')
@login_required
def generate_questions(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    
    # Ensure the current user is the owner of the quiz
    if quiz.user_id != current_user.id:
        flash('You do not have permission to modify this quiz', 'danger')
        return redirect(url_for('main.dashboard'))
        
    if not quiz.pdf_path or not os.path.exists(quiz.pdf_path):
        flash('PDF file not found', 'danger')
        return redirect(url_for('main.view_quiz', quiz_id=quiz.id))
    
    try:
        # Get the OpenAI API key from config
        api_key = current_app.config.get('OPENAI_API_KEY')
        
        # Process the PDF and generate questions
        pdf_processor = PDFProcessor(api_key=api_key)
        
        # Get the number of questions to generate, default to 5
        num_questions = request.args.get('num_questions', 5, type=int)
        
        # Generate questions
        generated_questions = pdf_processor.process_pdf_and_generate_questions(
            quiz.pdf_path, 
            num_questions=num_questions
        )
        
        # Delete existing questions for this quiz
        Question.query.filter_by(quiz_id=quiz.id).delete()
        
        # Add the new questions to the database
        for q_data in generated_questions:
            question = Question(
                quiz_id=quiz.id,
                question_text=q_data['question_text'],
                correct_answer=q_data['correct_answer']
            )
            # Set options as JSON
            question.set_options(q_data['options'])
            db.session.add(question)
        
        db.session.commit()
        flash('Quiz questions generated successfully!', 'success')
    except Exception as e:
        logger.error(f"Error generating questions: {str(e)}")
        flash(f'Error generating questions: {str(e)}', 'danger')
    
    return redirect(url_for('main.view_quiz', quiz_id=quiz.id))

@main.route('/quiz/<int:quiz_id>/regenerate', methods=['POST'])
@login_required
def regenerate_questions(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    
    # Ensure the current user is the owner of the quiz
    if quiz.user_id != current_user.id:
        return jsonify({"success": False, "error": "Permission denied"})
    
    try:
        # Redirect to generate questions
        return redirect(url_for('main.generate_questions', quiz_id=quiz.id))
    except Exception as e:
        logger.error(f"Error regenerating questions: {str(e)}")
        return jsonify({"success": False, "error": str(e)})

@main.route('/question/<int:question_id>/delete', methods=['POST'])
@login_required
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    quiz = Quiz.query.get(question.quiz_id)
    
    # Ensure the current user is the owner of the quiz
    if quiz.user_id != current_user.id:
        return jsonify({"success": False, "error": "Permission denied"})
    
    try:
        db.session.delete(question)
        db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        logger.error(f"Error deleting question: {str(e)}")
        return jsonify({"success": False, "error": str(e)})

@main.route('/quiz/<int:quiz_id>/share')
@login_required
def share_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    # Ensure the current user is the owner of the quiz
    if quiz.user_id != current_user.id:
        flash('You do not have permission to share this quiz', 'danger')
        return redirect(url_for('main.dashboard'))
        
    # Generate a unique code for accessing the quiz if it doesn't exist
    if not quiz.access_code:
        import random
        import string
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        quiz.access_code = code
        db.session.commit()
        
    share_url = url_for('main.take_quiz', access_code=quiz.access_code, _external=True)
    return render_template('share_quiz.html', title='Share Quiz', quiz=quiz, share_url=share_url)

@main.route('/take_quiz/<string:access_code>', methods=['GET', 'POST'])
def take_quiz(access_code):
    quiz = Quiz.query.filter_by(access_code=access_code).first_or_404()
    questions = quiz.questions.all()
    
    if request.method == 'POST':
        student_name = request.form.get('student_name')
        student_email = request.form.get('student_email')
        
        if not student_name or not student_email:
            flash('Please provide your name and email', 'danger')
            return redirect(request.url)
        
        # Process quiz answers
        answers = {}
        score = 0
        
        for question in questions:
            answer_key = f'question_{question.id}'
            if answer_key in request.form:
                selected_answer = int(request.form[answer_key])
                answers[str(question.id)] = selected_answer
                if selected_answer == question.correct_answer:
                    score += 1
        
        # Save the quiz result
        result = QuizResult(
            quiz_id=quiz.id,
            student_name=student_name,
            student_email=student_email,
            score=score,
            max_score=len(questions)
        )
        result.set_answers(answers)
        db.session.add(result)
        db.session.commit()
        
        return render_template('quiz_results.html', 
                               title='Quiz Results', 
                               quiz=quiz, 
                               result=result, 
                               questions=questions)
    
    return render_template('take_quiz.html', 
                           title=f'Quiz: {quiz.title}', 
                           quiz=quiz, 
                           questions=questions)

@main.route('/quiz/<int:quiz_id>/delete', methods=['POST'])
@login_required
def delete_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    
    # Ensure the current user is the owner of the quiz
    if quiz.user_id != current_user.id:
        return jsonify({"success": False, "error": "Permission denied"})
    
    try:
        # Delete the PDF file if it exists
        if quiz.pdf_path and os.path.exists(quiz.pdf_path):
            os.remove(quiz.pdf_path)
        
        # Delete the quiz (cascade will delete associated questions and results)
        db.session.delete(quiz)
        db.session.commit()
        
        logger.info(f"Quiz {quiz_id} deleted successfully by user {current_user.id}")
        return jsonify({"success": True})
    except Exception as e:
        logger.error(f"Error deleting quiz {quiz_id}: {str(e)}")
        return jsonify({"success": False, "error": str(e)})
