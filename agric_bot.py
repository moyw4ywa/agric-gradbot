import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import os

class AgricultureBot:
    def __init__(self):
        # Load agricultural data from CSV
        if not os.path.exists('agriculture_data.csv'):
            raise FileNotFoundError("The file 'agriculture_data.csv' was not found. Please make sure it exists in the directory.")
        
        self.agriculture_data = pd.read_csv('agriculture_data.csv')

        # Initialize SentenceTransformer model for encoding advice texts
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        self.index = self.create_faiss_index()

    def create_faiss_index(self):
        # Convert advice texts to vectors
        advice_vectors = self.model.encode(self.agriculture_data['advice_text'].tolist())
        # Create a FAISS index
        index = faiss.IndexFlatL2(advice_vectors.shape[1])
        index.add(advice_vectors)
        return index  # Return the newly created index

    def get_agricultural_advice(self, user_input):
        # Convert user input to a vector
        user_vector = self.model.encode([user_input])
        # Search the FAISS index
        _, advice_ids = self.index.search(user_vector, k=1)
        # Retrieve the most relevant advice
        most_relevant_advice = self.agriculture_data.iloc[advice_ids[0][0]]['advice_text']

        # Additional processing to make the response more precise
        precise_advice = self.process_advice(most_relevant_advice)

        return precise_advice

    def process_advice(self, advice):
        # Example of processing to make the advice more precise
        if "Rotate crops to prevent soil depletion and improve yield." in advice:
            advice += "\nConsider integrating cover crops like legumes to enhance soil fertility."

        return advice
