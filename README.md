# PDF Quiz Generator

A web application that allows teachers to upload PDF documents and automatically generate quizzes using AI. Students can take these quizzes and get immediate feedback.

## Features

- User authentication (register, login, logout)
- PDF document upload
- Automatic quiz generation from PDF content using AI
- Quiz sharing via unique URLs
- Quiz taking and automatic grading
- Result tracking and visualization

## Technology Stack

- **Backend**: Flask, SQLAlchemy, Flask-Login
- **Frontend**: Bootstrap 5, JavaScript
- **Database**: SQLite (development), PostgreSQL (production)
- **AI**: OpenAI GPT-3.5 via LangChain
- **PDF Processing**: PyPDF2

## Getting Started

### Prerequisites

- Python 3.8 or higher
- OpenAI API key

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd AIPdf
   ```

2. Create and activate a virtual environment:
   ```
   # Using conda
   conda create -n aipdf_env python=3.8
   conda activate aipdf_env
   
   # Or using venv
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```
   cp .env.example .env
   ```
   Edit the `.env` file and add your OpenAI API key and other settings.

5. Initialize the database:
   ```
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. Run the application:
   ```
   flask run
   ```

The application will be available at `http://127.0.0.1:5000`.

## Usage

1. **Register and Log In**:
   - Create a new account by clicking on the Register link
   - Log in with your credentials

2. **Upload a PDF**:
   - Navigate to "Upload PDF" in the navigation bar
   - Fill in the quiz title and description
   - Select a PDF file from your computer
   - Click "Upload and Generate Quiz"

3. **View and Share Quiz**:
   - View the generated quiz on the dashboard
   - Click on a quiz to see details and questions
   - Use the "Share Quiz" button to get a shareable link

4. **Take a Quiz**:
   - Access the quiz using the shared link
   - Enter your name and email
   - Answer all questions
   - Submit to see your results

## Development

### Project Structure

```
AIPdf/
├── app/
│   ├── __init__.py          # Application factory
│   ├── models.py            # Database models
│   ├── routes.py            # Main routes
│   ├── auth/                # Authentication blueprint
│   │   ├── __init__.py
│   │   ├── forms.py
│   │   └── routes.py
│   ├── static/              # Static files
│   │   ├── css/
│   │   ├── js/
│   │   └── uploads/         # Uploaded PDFs
│   ├── templates/           # Jinja2 templates
│   │   ├── auth/
│   │   ├── base.html
│   │   └── ...
│   └── utils/               # Utility functions
│       ├── __init__.py
│       └── pdf_processor.py
├── migrations/              # Database migrations
├── instance/                # Instance-specific data
│   └── app.db               # SQLite database
├── config.py                # Configuration settings
├── run.py                   # Application entry point
├── .env                     # Environment variables
└── requirements.txt         # Dependencies
```

### Database Models

- **User**: Authentication and user information
- **Quiz**: Represents a quiz created from a PDF
- **Question**: Multiple-choice questions for each quiz
- **QuizResult**: Student results for each quiz attempt

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [Bootstrap](https://getbootstrap.com/)
- [LangChain](https://github.com/hwchase17/langchain)
- [OpenAI](https://openai.com/)
