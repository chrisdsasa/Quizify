import os
import json
from typing import List, Dict, Any
import PyPDF2
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import logging

logger = logging.getLogger(__name__)

class PDFProcessor:
    def __init__(self, api_key: str = None):
        """Initialize the PDF processor.
        
        Args:
            api_key (str, optional): OpenAI API key. Defaults to None (will use environment variable).
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set the OPENAI_API_KEY environment variable or pass it as a parameter.")
        
        # Initialize LLM
        callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
        self.llm = ChatOpenAI(
            temperature=0.7,
            model_name="gpt-3.5-turbo",
            openai_api_key=self.api_key,
            callback_manager=callback_manager,
            verbose=True
        )
        
        # Text splitter for long documents
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=200,
            length_function=len,
        )
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from a PDF file.
        
        Args:
            pdf_path (str): Path to the PDF file.
            
        Returns:
            str: Extracted text from the PDF.
        """
        try:
            text = ""
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    text += page.extract_text()
            return text
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            raise
    
    def generate_quiz_questions(self, text: str, num_questions: int = 5) -> List[Dict[str, Any]]:
        """Generate quiz questions from the extracted text.
        
        Args:
            text (str): Text extracted from PDF.
            num_questions (int, optional): Number of questions to generate. Defaults to 5.
            
        Returns:
            List[Dict[str, Any]]: List of generated questions with options and correct answers.
        """
        # Split text into chunks if it's too long
        if len(text) > 4000:
            chunks = self.text_splitter.split_text(text)
            logger.info(f"Split text into {len(chunks)} chunks")
        else:
            chunks = [text]
        
        questions = []
        questions_per_chunk = max(1, num_questions // len(chunks))
        
        # Create prompt template
        prompt_template = """
        You are a helpful assistant that creates educational multiple-choice quiz questions based on the content below.
        
        Content: {text}
        
        Please generate {num_questions} multiple-choice quiz questions based on the most important concepts in the text. 
        Each question should have 4 options with only one correct answer.
        Make sure the questions test understanding rather than just factual recall.
        
        Format your response as a JSON array where each question is an object with the following structure:
        {{
            "question_text": "The question text",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct_answer": 0 // Index of the correct answer (0-3)
        }}
        
        Make sure your response is properly formatted JSON that can be parsed, with no extra text before or after the JSON.
        """
        
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["text", "num_questions"]
        )
        
        llm_chain = LLMChain(
            llm=self.llm,
            prompt=prompt,
        )
        
        for i, chunk in enumerate(chunks):
            # For the last chunk, use remaining number of questions
            if i == len(chunks) - 1:
                remaining = num_questions - len(questions)
                num_to_generate = remaining if remaining > 0 else 1
            else:
                num_to_generate = questions_per_chunk
            
            try:
                response = llm_chain.invoke({"text": chunk, "num_questions": num_to_generate})
                # Extract JSON from the response
                json_str = self._extract_json_from_response(response['text'])
                chunk_questions = json.loads(json_str)
                questions.extend(chunk_questions)
                
                # If we have enough questions, break
                if len(questions) >= num_questions:
                    questions = questions[:num_questions]
                    break
                    
            except Exception as e:
                logger.error(f"Error generating questions for chunk {i}: {str(e)}")
                continue
        
        return questions
    
    def _extract_json_from_response(self, response: str) -> str:
        """Extract JSON from the LLM response.
        
        Args:
            response (str): Response from the LLM.
            
        Returns:
            str: Extracted JSON string.
        """
        # Find the first '[' and the last ']'
        start_idx = response.find('[')
        end_idx = response.rfind(']')
        
        if start_idx == -1 or end_idx == -1 or start_idx > end_idx:
            # If we can't find proper JSON array markers, try to find object markers
            start_idx = response.find('{')
            end_idx = response.rfind('}')
            
            if start_idx == -1 or end_idx == -1 or start_idx > end_idx:
                raise ValueError(f"Could not extract JSON from response: {response}")
            
            # Wrap the single object in an array
            return f"[{response[start_idx:end_idx+1]}]"
        
        return response[start_idx:end_idx+1]
    
    def process_pdf_and_generate_questions(self, pdf_path: str, num_questions: int = 5) -> List[Dict[str, Any]]:
        """Extract text from PDF and generate quiz questions.
        
        Args:
            pdf_path (str): Path to the PDF file.
            num_questions (int, optional): Number of questions to generate. Defaults to 5.
            
        Returns:
            List[Dict[str, Any]]: List of generated questions with options and correct answers.
        """
        text = self.extract_text_from_pdf(pdf_path)
        return self.generate_quiz_questions(text, num_questions) 