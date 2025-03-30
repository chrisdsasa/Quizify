# PDF Quiz Generator

A Flask web application that uses AI to automatically generate quiz questions from PDF documents. Perfect for teachers and educators who want to create quizzes quickly and efficiently.

## Features

- **PDF Upload**: Upload any educational PDF document
- **AI-Powered Question Generation**: Automatically generates multiple-choice questions from PDF content using OpenAI
- **Quiz Management**: Create, view, share, and delete quizzes
- **Student Responses**: Track student results and performance
- **Responsive Design**: Works on desktop and mobile devices

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- OpenAI API key (get one at [OpenAI's platform](https://platform.openai.com/))

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/AIPdf.git
   cd AIPdf
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables by creating a `.env` file:
   ```
   cp .env.example .env
   ```

5. Edit the `.env` file with your secure information:
   ```
   # Generate a secure random string for SECRET_KEY
   # You can use: python -c "import secrets; print(secrets.token_hex(32))"
   SECRET_KEY=your-generated-secure-key
   
   # Add your OpenAI API key
   OPENAI_API_KEY=your-api-key-here
   
   # For production, consider using a different database:
   # DATABASE_URL=postgresql://username:password@localhost/dbname
   ```

6. Create the database:
   ```
   flask shell
   >>> from app import db
   >>> db.create_all()
   >>> exit()
   ```

7. Start the application:
   ```
   flask run
   ```

The application will be available at `http://localhost:5000`

### Security Considerations

- **Never commit your `.env` file** to version control
- Regularly rotate your `SECRET_KEY` in production
- Consider setting up rate limiting for API requests
- Use HTTPS in production
- Implement proper user authentication and authorization

### AI Configuration (OpenAI)

The application uses the OpenAI API to generate quiz questions. You need to:

1. Create an account at [OpenAI](https://platform.openai.com/)
2. Generate an API key in your account settings
3. Add the API key to your `.env` file as shown above
4. Be aware of API usage costs - the application uses GPT-3.5-Turbo by default

#### Customizing the AI Model

You can change the model in `app/utils/pdf_processor.py` if you prefer to use a different model. Look for the following line:

```python
self.llm = ChatOpenAI(
    temperature=0.7,
    model_name="gpt-3.5-turbo",  # Change this to use a different model
    openai_api_key=self.api_key,
    callback_manager=callback_manager,
    verbose=True
)
```

## Usage

1. **Register/Login**: Create an account or log in
2. **Upload PDF**: Go to the "Create Quiz" page and upload a PDF document
3. **Configure Options**: Set the number of questions, difficulty level, etc.
4. **Generate Quiz**: The AI will process the PDF and generate questions
5. **Review & Edit**: Review the generated questions and edit if needed
6. **Share Quiz**: Share the quiz link with students
7. **Track Results**: View student responses and results on your dashboard

## Tips for Best Results

- Use high-quality PDFs with clear, searchable text
- PDFs with structured content (headings, paragraphs) work best
- 5-20 page PDFs tend to produce more focused quizzes
- You can regenerate individual questions if needed

## Customizing AI Generation

The question generation is handled by the `PDFProcessor` class in `app/utils/pdf_processor.py`. You can customize:

- The prompt template for generating questions
- The number of questions per chunk of text
- The OpenAI model used (e.g., switch to GPT-4 for higher quality)
- Temperature and other model parameters

## Deployment

For production deployment:
1. Use a production WSGI server like Gunicorn
2. Set up a reverse proxy with Nginx
3. Configure proper HTTPS
4. Use environment variables instead of .env files
5. Consider using a proper database like PostgreSQL

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you have any questions or need help, please open an issue on GitHub.
