from fastapi import (
    APIRouter,
    BackgroundTasks,
    HTTPException
)

from pathlib import Path
from uuid import uuid4

from pypdf import PdfReader

from api.schemas import (
    ParseJobRequest,
    JobCreateResponse,
    JobStatusResponse
)

from parsers.information_extractor import InformationExtractor


router = APIRouter(
    prefix="/api/jobs",
    tags=["Async Jobs"]
)


# =========================================
# Upload Directory
# =========================================

BASE_DIR = Path(__file__).resolve().parents[2]

UPLOAD_DIR = BASE_DIR / "data" / "uploads"


# =========================================
# Job Storage
# =========================================

jobs = {}


# =========================================
# Information Extractor
# =========================================

information_extractor = InformationExtractor()


# =========================================
# Extract PDF Text
# =========================================

def extract_pdf_text(file_path):

    reader = PdfReader(str(file_path))

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:

            text += page_text + "\n"

    return text


# =========================================
# Background Parsing Task
# =========================================

def process_parse_job(
    job_id,
    candidate_id
):

    try:

        # ---------------------------------
        # Update status
        # ---------------------------------

        jobs[job_id]["status"] = "processing"

        # ---------------------------------
        # Find uploaded resume
        # ---------------------------------

        matching_files = list(
            UPLOAD_DIR.glob(
                f"{candidate_id}.*"
            )
        )

        if not matching_files:

            raise FileNotFoundError(
                "Resume not found for this candidate."
            )

        file_path = matching_files[0]

        # ---------------------------------
        # Check file type
        # ---------------------------------

        extension = file_path.suffix.lower()

        if extension != ".pdf":

            raise ValueError(
                "Async parsing currently supports PDF files."
            )

        # ---------------------------------
        # Extract text
        # ---------------------------------

        text = extract_pdf_text(
            file_path
        )

        if not text.strip():

            raise ValueError(
                "No readable text found in resume."
            )

        # ---------------------------------
        # Existing ATS parser
        # ---------------------------------

        candidate = information_extractor.extract(
            text
        )

        # Keep original candidate ID
        candidate["candidate_id"] = candidate_id

        # ---------------------------------
        # Save result
        # ---------------------------------

        jobs[job_id]["result"] = candidate

        jobs[job_id]["status"] = "completed"

    except Exception as error:

        jobs[job_id]["status"] = "failed"

        jobs[job_id]["error"] = str(error)


# =========================================
# Create Async Parse Job
# =========================================

@router.post(
    "/parse",
    response_model=JobCreateResponse
)
async def create_parse_job(
    request: ParseJobRequest,
    background_tasks: BackgroundTasks
):

    # -------------------------------------
    # Check candidate resume
    # -------------------------------------

    matching_files = list(
        UPLOAD_DIR.glob(
            f"{request.candidate_id}.*"
        )
    )

    if not matching_files:

        raise HTTPException(
            status_code=404,
            detail="Resume not found for this candidate."
        )

    # -------------------------------------
    # Generate Job ID
    # -------------------------------------

    job_id = (
        f"JOB-{uuid4().hex[:8].upper()}"
    )

    # -------------------------------------
    # Create job record
    # -------------------------------------

    jobs[job_id] = {

        "job_id": job_id,

        "candidate_id": request.candidate_id,

        "status": "queued",

        "result": None,

        "error": None

    }

    # -------------------------------------
    # Add background task
    # -------------------------------------

    background_tasks.add_task(

        process_parse_job,

        job_id,

        request.candidate_id

    )

    # -------------------------------------
    # Return immediately
    # -------------------------------------

    return {

        "success": True,

        "job_id": job_id,

        "candidate_id": request.candidate_id,

        "status": "queued"

    }


# =========================================
# Get Job Status
# =========================================

@router.get(
    "/{job_id}",
    response_model=JobStatusResponse
)
async def get_job_status(
    job_id: str
):

    if job_id not in jobs:

        raise HTTPException(
            status_code=404,
            detail="Job not found."
        )

    job = jobs[job_id]

    return {

        "success": True,

        "job_id": job["job_id"],

        "candidate_id": job["candidate_id"],

        "status": job["status"],

        "result": job["result"],

        "error": job["error"]

    }