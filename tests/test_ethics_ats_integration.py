import json

from ats_engine.ats_scorer import ATSScorer


def test_demographic_fields_do_not_change_ats_score(tmp_path):
    job = {
        "job_id": "JOB-TEST",
        "required_skills": ["python", "sql"]
    }

    job_path = tmp_path / "job.json"
    job_path.write_text(json.dumps(job), encoding="utf-8")

    candidate = {
        "candidate_id": "CAND-001",
        "skills": ["Python", "SQL"],
        "education": ["MCA"],
        "projects": ["Project A", "Project B"],
        "experience": [],
        "certifications": []
    }

    candidate_with_demographics = {
        **candidate,
        "race": "example",
        "religion": "example",
        "gender_identity": "example",
        "date_of_birth": "2000-01-01"
    }

    scorer = ATSScorer()

    original_result = scorer.score(candidate, job_path)
    demographic_result = scorer.score(
        candidate_with_demographics,
        job_path
    )

    assert (
        original_result["overall_score"]
        == demographic_result["overall_score"]
    )

    assert (
        original_result["recommendation"]
        == demographic_result["recommendation"]
    )


def test_ats_does_not_modify_original_candidate(tmp_path):
    job = {
        "job_id": "JOB-TEST",
        "required_skills": ["python"]
    }

    job_path = tmp_path / "job.json"
    job_path.write_text(json.dumps(job), encoding="utf-8")

    candidate = {
        "candidate_id": "CAND-002",
        "skills": ["Python"],
        "education": ["MCA"],
        "projects": [],
        "experience": [],
        "certifications": [],
        "religion": "example"
    }

    scorer = ATSScorer()
    scorer.score(candidate, job_path)

    assert "religion" in candidate