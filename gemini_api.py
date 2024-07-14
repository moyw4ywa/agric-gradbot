import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class GeminiAPI:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def generate_response(self, prompt):
        content = self.model.generate_content(prompt)
        response_text = content.text
        
        # Process the response to add more details
        detailed_response = self.process_response(response_text)
        
        return detailed_response

    def process_response(self, response_text):
        # Example of adding more details or formatting the response
        processed_response = f"Generated Response:\n{response_text}\n\nAdditional details could be added here."
        
        return processed_response
