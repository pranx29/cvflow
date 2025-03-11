from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import job_application
from app.core.config import settings

# Create FastAPI app
app = FastAPI(
    title="Job Application Processing Pipeline",
    version="1.0.0",
)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

# Include routers
app.include_router(job_application.router, prefix="/api")

