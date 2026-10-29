from fastapi import APIRouter, HTTPException

from api.schemas import (
    ShortlistingRequest,
    ShortlistingResponse
)

from engines.shortlisting_engine import ShortlistingEngine


router = APIRouter(
    prefix="/api",
    tags=["Shortlisting"]
)


# -----------------------------------------
# Shortlisting Engine
# -----------------------------------------

shortlisting_engine = ShortlistingEngine()


# -----------------------------------------
# Shortlisting API
# -----------------------------------------

@router.post(
    "/shortlist",
    response_model=ShortlistingResponse
)
async def shortlist_candidates(
    request: ShortlistingRequest
):

    try:

        # ---------------------------------
        # Convert request candidates
        # into engine-compatible format
        # ---------------------------------

        candidates = []

        for candidate in request.candidates:

            candidates.append({

                "candidate_id": candidate.candidate_id,

                "score": candidate.score

            })

        # ---------------------------------
        # Apply existing Day 14 engine
        # ---------------------------------

        result = shortlisting_engine.apply(
            candidates
        )

        # ---------------------------------
        # Return API response
        # ---------------------------------

        return {

            "success": True,

            "job_id": request.job_id,

            "candidates": result

        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Shortlisting failed: {str(error)}"
        )