from fastapi import FastAPI
from .routers import auth, helpdesk
from .utils.database import engine
from .models.models import Base

app = FastAPI()

# Include routers
app.include_router(auth.router)
app.include_router(helpdesk.router)

# Create database tables
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
