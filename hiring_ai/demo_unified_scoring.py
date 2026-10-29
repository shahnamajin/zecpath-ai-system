import json

from hiring_ai.candidate_score_builder import CandidateScoreBuilder


def main():
    builder = CandidateScoreBuilder()

    candidate = builder.build(
        candidate_id="CAND_1001",
        job_id="JOB_2001",
        ats_score=83.34,
        screening_score=72.92,
        hr_interview_score=89.02,
        role_type="technical"
    )

    print("=" * 55)
    print("ZECPath AI - UNIFIED SCORING ENGINE")
    print("=" * 55)
    print(json.dumps(candidate, indent=4))
    print("=" * 55)
    print(
        "Hiring Fit:",
        f'{candidate["hiring_fit_percentage"]:.2f}%'
    )
    print("Demo completed successfully.")


if __name__ == "__main__":
    main()