
import uvicorn
from fastapi import FastAPI

from app.api.open_food_facts.routes import router as off_router
from app.config.logging import setup_logging
from app.config.middlewares import RequestIdFilter, add_locale_translator, request_id_middleware

# Setup logging
logger = setup_logging()
logger.addFilter(RequestIdFilter())

# Create FastAPI app
app = FastAPI(title="Suffering Footprint API")

# Add request ID middleware
app.middleware("http")(request_id_middleware)

# Add locale translator middleware
app.middleware("http")(add_locale_translator)

# Include API routes
app.include_router(off_router, prefix="/off/v1", tags=["Open Food Facts"])


# Go in the app folder and run the server with: uvicorn main:app --reload
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
