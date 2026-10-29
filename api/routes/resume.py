from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
from uuid import uuid4

from pypdf import PdfReader

from api.schemas import (
    ResumeUploadResponse,
    ResumeParseRequest
)

from parsers.information_extractor import InformationExtractor


router = APIRouter(
    prefix="/api/resume",
    tags=["Resume"]
)


# -----------------------------------------
# Upload directory
# -----------------------------------------

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# -----------------------------------------
# Information Extractor
# -----------------------------------------

information_extractor = InformationExtractor()


# -----------------------------------------
# Resume Upload API
# -----------------------------------------

@router.post(
    "/upload",
    response_model=ResumeUploadResponse
)
async def upload_resume(
    file: UploadFile = File(...)
):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file was provided."
        )

    allowed_extensions = {
        ".pdf",
        ".docx",
        ".txt"
    }

    extension = Path(file.filename).suffix.lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, DOCX and TXT files are supported."
        )

    candidate_id = f"CAND-{uuid4().hex[:8].upper()}"

    saved_filename = f"{candidate_id}{extension}"

    file_path = UPLOAD_DIR / saved_filename

    contents = await file.read()

    with open(file_path, "wb") as output_file:
        output_file.write(contents)

    return ResumeUploadResponse(
        success=True,
        candidate_id=candidate_id,
        filename=file.filename,
        status="uploaded"
    )


# -----------------------------------------
# Extract Text From PDF
# -----------------------------------------

def extract_pdf_text(file_path):

    reader = PdfReader(str(file_path))

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


# -----------------------------------------
# Resume Parsing API
# -----------------------------------------

@router.post("/parse")
async def parse_resume(
    request: ResumeParseRequest
):

    candidate_id = request.candidate_id

    # -----------------------------------------
    # Find candidate resume
    # -----------------------------------------

    matching_files = list(
        UPLOAD_DIR.glob(
            f"{candidate_id}.*"
        )
    )

    if not matching_files:

        raise HTTPException(
            status_code=404,
            detail="Resume not found for this candidate."
        )

    file_path = matching_files[0]

    # -----------------------------------------
    # Read resume
    # -----------------------------------------

    extension = file_path.suffix.lower()

    if extension == ".pdf":

        text = extract_pdf_text(file_path)

    elif extension == ".txt":

        text = file_path.read_text(
            encoding="utf-8"
        )

    else:

        raise HTTPException(
            status_code=400,
            detail="Parsing currently supports PDF and TXT files."
        )

    # -----------------------------------------
    # Validate extracted text
    # -----------------------------------------

    if not text.strip():

        raise HTTPException(
            status_code=422,
            detail="No readable text found in the resume."
        )

    # -----------------------------------------
    # Existing ATS parser
    # -----------------------------------------

    candidate = information_extractor.extract(
        text
    )

    # Keep upload candidate ID
    candidate["candidate_id"] = candidate_id

    # -----------------------------------------
    # API response
    # -----------------------------------------

    return {
        "success": True,
        "candidate_id": candidate_id,
        "status": "parsed",
        "candidate": candidate
    }
