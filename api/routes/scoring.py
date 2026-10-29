from fastapi import APIRouter, HTTPException

from api.schemas import (
    ScoringRequest,
    ScoreResponse
)

from engines.ats_scoring_engine import ATSScoringEngine


router = APIRouter(
    prefix="/api",
    tags=["ATS Scoring"]
)


# -----------------------------------------
# ATS Scoring Engine
# -----------------------------------------

scoring_engine = ATSScoringEngine()


# -----------------------------------------
# Calculate ATS Score
# -----------------------------------------

@router.post(
    "/score",
    response_model=ScoreResponse
)
async def calculate_score(
    request: ScoringRequest
):

    try:

        # ---------------------------------
        # Call existing ATS engine
        # ---------------------------------

        result = scoring_engine.calculate(

            role=request.role,

            skill_match=request.skill_match,

            experience_relevance=request.experience_relevance,

            education_alignment=request.education_alignment,

            semantic_similarity=request.semantic_similarity

        )

        # ---------------------------------
        # Return API response
        # ---------------------------------

        return {

            "success": True,

            "candidate_id": request.candidate_id,

            "job_id": request.job_id,

            "role": result["role"],

            "final_score": result["final_score"],

            "recommendation": result["recommendation"],

            "breakdown": result["breakdown"]

        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"ATS scoring failed: {str(error)}"
        )