from transformers import pipeline

class NLPService:
    def __init__(self):
        self.nlp = pipeline("question-answering")

    def answer_question(self, question, context):
        return self.nlp(question=question, context=context)
