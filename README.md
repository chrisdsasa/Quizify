# PDF Quiz Generator

A web application that allows teachers to upload PDF documents and automatically generate interactive quizzes for their students. Powered by Flask and LangChain.

## Features

- **PDF Upload**: Teachers can upload educational PDF documents
- **AI-Generated Quizzes**: Automatically creates multiple-choice questions based on the PDF content
- **Shareable Quizzes**: Teachers can share a unique link with students to access the quiz
- **Student Responses**: Tracks student answers and provides scores
- **Results Dashboard**: Teachers can view individual and aggregate results

## Technology Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS (Bootstrap 5), JavaScript
- **Database**: SQLite (using SQLAlchemy)
- **AI Integration**: LangChain + LLM APIs (OpenAI)
- **PDF Processing**: PyPDF2, pdfplumber

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pdf-quiz-generator.git
cd pdf-quiz-generator
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root directory with the following variables:
```
SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-api-key
```

5. Initialize the database:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

6. Run the application:
```bash
flask run
```

The application will be available at http://127.0.0.1:5000/

## Project Structure

```
pdf-quiz-generator/
├── app/
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── uploads/  # PDF storage
│   ├── templates/    # HTML templates
│   ├── __init__.py   # Flask application factory
│   ├── models.py     # Database models
│   └── routes.py     # Application routes
├── migrations/       # Database migrations
├── instance/         # SQLite database
├── .env              # Environment variables
├── config.py         # Application configuration
├── requirements.txt  # Python dependencies
└── run.py            # Application entry point
```

## Usage

### For Teachers

1. Register for an account
2. Login and navigate to "Upload PDF"
3. Upload a PDF document and configure quiz options
4. Wait for the AI to generate quiz questions
5. Share the generated quiz link with students
6. View student responses in the dashboard

### For Students

1. Access the quiz using the shared link
2. Enter your name and email
3. Answer the multiple-choice questions
4. Submit your answers and view your score
5. Results are automatically sent to the teacher

## Future Enhancements

- Question editing for teachers
- Additional question types (short answer, true/false)
- PDF annotation for more targeted quizzes
- Student accounts for tracking progress
- Integration with learning management systems (LMS)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
