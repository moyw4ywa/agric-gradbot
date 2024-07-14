# gemini_api.py

import os
import json
from dotenv import load_dotenv
from google.cloud import aiplatform_v1
from google.oauth2 import service_account
import google.generativeai as genai

load_dotenv()

class GeminiAPI:
    def __init__(self):
        self.client = None
        self.model = None
        self.project_id = None
        self.endpoint = None

        # Load API key JSON from environment variables
        api_key_json = os.getenv("GOOGLE_API_KEY_JSON")
        if api_key_json:
            self.setup_aiplatform_client(api_key_json)
        else:
            # Fallback to genai if GOOGLE_API_KEY_JSON is not present
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY_JSON or GEMINI_API_KEY not found in environment variables")
            self.setup_genai_model(api_key)

    def setup_aiplatform_client(self, api_key_json):
        # Parse the JSON key to dictionary
        api_key = json.loads(api_key_json)

        # Create credentials from the service account info
        credentials = service_account.Credentials.from_service_account_info(api_key)

        # Initialize the AI Platform Prediction Service Client
        self.client = aiplatform_v1.PredictionServiceClient(credentials=credentials)
        
        # Set the project ID and model endpoint
        self.project_id = api_key['project_id']
        self.endpoint = "projects/{}/locations/us-central1/endpoints/YOUR_ENDPOINT_ID".format(self.project_id)

    def setup_genai_model(self, api_key):
        # Configure genai with the provided API key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def generate_response(self, prompt):
        if self.client:
            try:
                # Prepare the request
                instances = [{"content": prompt}]
                parameters = {}
                request = aiplatform_v1.PredictRequest(endpoint=self.endpoint, instances=instances, parameters=parameters)

                # Make the prediction request
                response = self.client.predict(request=request)
                
                # Extract the response text
                response_text = response.predictions[0].get('content', '')
                
                # Process the response to add more details
                detailed_response = self.process_response(response_text)
                
                return detailed_response
            except Exception as e:
                return str(e)
        elif self.model:
            # Fallback to genai model if aiplatform client is not set up
            content = self.model.generate_content(prompt)
            response_text = content.text
            
            # Process the response to add more details
            detailed_response = self.process_response(response_text)
            
            return detailed_response
        else:
            raise ValueError("No API configuration found.")

    def process_response(self, response_text):
        # Example of adding more details or formatting the response
        processed_response = f"Generated Response:\n{response_text}\n\nAdditional details could be added here."
        
        return processed_response
