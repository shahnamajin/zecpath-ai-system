from pydantic import BaseModel, Field
from typing import Optional, List


# =========================================
# Resume Parsing Request
# =========================================

class ResumeParseRequest(BaseModel):

    candidate_id: str = Field(
        ...,
        min_length=1
    )


# =========================================
# Resume Upload Response
# =========================================

class ResumeUploadResponse(BaseModel):

    success: bool

    candidate_id: str

    filename: str

    status: str


# =========================================
# ATS Scoring Request
# =========================================

class ScoringRequest(BaseModel):

    candidate_id: str = Field(
        ...,
        min_length=1
    )

    job_id: str = Field(
        ...,
        min_length=1
    )

    role: str = Field(
        ...,
        min_length=1
    )

    skill_match: Optional[float] = 0

    experience_relevance: Optional[float] = 0

    education_alignment: Optional[float] = 0

    semantic_similarity: Optional[float] = 0


# =========================================
# ATS Scoring Response
# =========================================

class ScoreResponse(BaseModel):

    success: bool

    candidate_id: str

    job_id: str

    role: str

    final_score: float

    recommendation: str

    breakdown: dict


# =========================================
# Candidate Score
# =========================================

class CandidateScore(BaseModel):

    candidate_id: str

    score: float


# =========================================
# Shortlisting Request
# =========================================

class ShortlistingRequest(BaseModel):

    job_id: str

    candidates: List[CandidateScore]


# =========================================
# Ranked Candidate
# =========================================

class RankedCandidate(BaseModel):

    candidate_id: str

    rank: int

    score: float

    status: str


# =========================================
# Shortlisting Response
# =========================================

class ShortlistingResponse(BaseModel):

    job_id: str

    candidates: List[RankedCandidate]


# =========================================
# Job Status Response
# =========================================

class JobStatusResponse(BaseModel):

    job_id: str

    status: str

# =========================================
# Shortlisting Candidate
# =========================================

class ShortlistCandidate(BaseModel):

    candidate_id: str = Field(
        ...,
        min_length=1
    )

    score: float = Field(
        ...,
        ge=0,
        le=100
    )


# =========================================
# Shortlisting Request
# =========================================

class ShortlistingRequest(BaseModel):

    job_id: str = Field(
        ...,
        min_length=1
    )

    candidates: List[ShortlistCandidate]


# =========================================
# Ranked/Shortlisted Candidate
# =========================================

class ShortlistedCandidate(BaseModel):

    candidate_id: str

    score: float

    status: str


# =========================================
# Shortlisting Response
# =========================================

class ShortlistingResponse(BaseModel):

    success: bool

    job_id: str

    candidates: List[ShortlistedCandidate]


# =========================================
# Async Parse Job Request
# =========================================

class ParseJobRequest(BaseModel):

    candidate_id: str = Field(
        ...,
        min_length=1
    )


# =========================================
# Async Job Response
# =========================================

class JobCreateResponse(BaseModel):

    success: bool

    job_id: str

    candidate_id: str

    status: str


# =========================================
# Async Job Status
# =========================================

class JobStatusResponse(BaseModel):

    success: bool

    job_id: str

    candidate_id: str

    status: str

    result: Optional[dict] = None

    error: Optional[str] = None