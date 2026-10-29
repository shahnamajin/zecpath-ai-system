from fastapi import FastAPI

from api.routes.resume import router as resume_router
from api.routes.scoring import router as scoring_router
from api.routes.shortlisting import router as shortlisting_router
from api.routes.jobs import router as jobs_router


app = FastAPI(
    title="Zecpath AI ATS API",
    description="AI-powered Applicant Tracking System API",
    version="1.0.0"
)


# =========================================
# Register API Routes
# =========================================

app.include_router(
    resume_router
)

app.include_router(
    scoring_router
)

app.include_router(
    shortlisting_router
)

app.include_router(
    jobs_router
)


# =========================================
# Root API
# =========================================

@app.get("/")
def root():

    return {

        "message": "Zecpath AI ATS API",

        "status": "running"

    }