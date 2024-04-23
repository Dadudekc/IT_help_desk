from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..utils.database import get_db
from ..services.nlp_service import NLPServices


router = APIRouter()

nlp_service = NLPServices()  # Initialize NLP service

@router.post("/ask")
def ask_question(question: str, db: Session = Depends(get_db)):
    # Example context (usually, you'd fetch this from your database)
    context = "The IT Help Desk handles issues like password resets, software installations, and hardware troubleshooting."
    answer = nlp_service.answer_question(question, context)
    return answer

@router.get("/faqs")
def read_faqs(db: Session = Depends(get_db)):
    # Placeholder for fetching FAQs from the database
    # Example response structure
    faqs = [
        {"question": "How do I reset my password?", "answer": "Click on 'Forgot password' link on the login page."},
        {"question": "What is my user ID?", "answer": "Your user ID is typically your registered email address."},
    ]
    return faqs

@router.post("/reset-password")
def reset_password(username: str, db: Session = Depends(get_db)):
    # Placeholder for password reset logic
    # You would add logic here to verify the user's identity and initiate a password reset
    # Example response
    return {"message": "Password reset instructions have been sent to your registered email address."}

@router.get("/retrieve-username")
def retrieve_username(email: str, db: Session = Depends(get_db)):
    # Placeholder for retrieving a username by email
    # You would implement logic to verify the email and send the username to it
    # Example response
    return {"message": "Your username has been sent to your registered email address."}
