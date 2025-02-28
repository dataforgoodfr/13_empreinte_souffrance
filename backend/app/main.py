import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.open_food_facts.routes import router as off_router
from app.config.logging import setup_logging
from app.config.middlewares import (
    GlobalExceptionMiddleware,
    add_locale_translator,
)

# Setup logging
setup_logging()

# Create FastAPI app
app = FastAPI(
    title="Suffering Footprint API",
    description="API for calculating and displaying the suffering footprint of food products",
    version="0.1.0",
)


# Add locale translator middleware
app.middleware("http")(add_locale_translator)

# Add global exception middleware
app.add_middleware(GlobalExceptionMiddleware)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(off_router, prefix="/off/v1", tags=["Open Food Facts"])


# Go in the app folder and run the server with: uvicorn main:app --reload
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
