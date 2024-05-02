#nlp_services.py

import logging
from transformers import pipeline
import asyncio

# Set up basic configuration for logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NLPServices:
    def __init__(self, model="distilbert-base-cased-distilled-squad"):
        self.model = model
        self.nlp = self.load_pipeline()

    def load_pipeline(self):
        """Loads the NLP pipeline based on the specified model."""
        try:
            return pipeline("question-answering", model=self.model)
        except Exception as e:
            logger.error(f"Failed to load model {self.model}: {e}")
            return None

    async def answer_question(self, question, context):
        """Asynchronously processes a question with the given context using the NLP pipeline."""
        if not self.nlp:
            logger.error("Pipeline is not initialized.")
            return "Pipeline is not initialized."
        
        loop = asyncio.get_running_loop()
        
        try:
            # Use a lambda to pass the method call to run_in_executor
            return await loop.run_in_executor(None, lambda: self.nlp(question=question, context=context))
        except Exception as e:
            logger.error(f"Error during question answering: {e}")
            return None

