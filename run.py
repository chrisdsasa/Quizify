from app import create_app, db
from app.models import User, Quiz, Question, QuizResult

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db, 
        'User': User, 
        'Quiz': Quiz, 
        'Question': Question, 
        'QuizResult': QuizResult
    }

if __name__ == '__main__':
    app.run(debug=True)
