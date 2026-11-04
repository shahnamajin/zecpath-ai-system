"""ZECPath Day 56 - Full System Simulation.

Runs the existing ATS, screening, HR, technical, unified scoring,
and final recommendation engines.

Important:
- HR data is a predefined simulation fixture.
- Technical ratings are sample evaluator-provided inputs.
- Machine-test ratings are sample inputs based on a design-only rubric.
- This script does not claim autonomous technical or machine-test grading.
"""

import json
import sys
import time
from pathlib import Path
from datetime import datetime, timezone

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from ats_engine.ats_scorer import ATSScorer
from screening_ai.screening_scoring_engine import ScreeningScoringEngine
from interview_ai.hr_interview_simulator import HRInterviewSimulator
from interview_ai.technical_scoring_engine import TechnicalScoringEngine
from hiring_ai.unified_scoring_engine import UnifiedScoringEngine
from hiring_ai.final_recommendation_engine import FinalRecommendationEngine


DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = DATA_DIR / "day56"
REPORT_DIR = PROJECT_ROOT / "docs" / "day56"


def load_json(path):
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_json(data, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def run_ats(candidate_data):
    """Normalize the parsed resume and run the existing ATS scorer."""

    candidate = {
        "candidate_id": candidate_data["candidate_id"],
        "skills": candidate_data.get("skills", []),
        "education": candidate_data.get("education", []),
        "projects": candidate_data.get("projects", []),
        "experience": candidate_data.get("experience", []),
        "certifications": candidate_data.get("certifications", []),
    }

    job_path = DATA_DIR / "job_descriptions" / "backend_developer.json"
    result = ATSScorer().score(candidate, job_path)

    return {
        "score": result["overall_score"],
        "recommendation": result["recommendation"],
        "engine_report": result,
        "input_provenance": "Existing parsed resume mapped to ATS input schema",
    }


def run_screening(candidate_id):
    """Run the existing screening scorer on a labelled sample answer."""

    engine = ScreeningScoringEngine()

    answer_data = {
        "answer": {
            "raw_text": (
                "I have used Python, Django and SQL in academic "
                "and personal software projects."
            ),
            "intent": "skills",
        },
        "entities": {
            "skills": ["Python", "Django", "SQL"],
            "experience": {},
            "availability": {},
            "salary_expectation": {},
        },
        "quality": {
            "is_missing": False,
            "is_vague": False,
            "is_off_topic": False,
        },
    }

    result = engine.score_question(
        candidate_id=candidate_id,
        job_id="JOB-1001",
        question_id="DAY56-SAMPLE-SCREENING-001",
        question_category="skills",
        answer_data=answer_data,
    )

    final_result = engine.calculate_final_score(
        candidate_id=candidate_id,
        job_id="JOB-1001",
        question_results=[result],
    )

    return {
        "score": final_result["final_screening_score"],
        "engine_report": final_result,
        "input_provenance": (
            "Sample structured answer supplied to the existing "
            "rule-based screening engine"
        ),
    }


def run_hr_simulation():
    """Run all existing HR fixtures and select one labelled fixture."""

    simulator = HRInterviewSimulator()
    all_results = simulator.run_all()
    comparisons = simulator.compare_manual_evaluation()
    metrics = simulator.evaluation_metrics()

    # SIM_001 is used only as a sample input for the unified pipeline.
    selected_fixture = next(
        item for item in all_results
        if item["session_id"] == "SIM_001"
    )

    return {
        "pipeline_score": selected_fixture["ai_score"],
        "pipeline_fixture": selected_fixture,
        "all_session_count": len(all_results),
        "manual_comparison": comparisons,
        "evaluation_metrics": metrics,
        "inconsistencies": simulator.identify_inconsistencies(),
        "recommendations": simulator.recommendations(),
        "input_provenance": (
            "Predefined HR simulation fixture SIM_001; "
            "not a real interview record for C001"
        ),
    }


def run_technical(candidate_id):
    """Aggregate explicitly supplied sample evaluator ratings."""

    engine = TechnicalScoringEngine()

    question = {
        "question_id": "DAY56-TECH-SAMPLE-001",
        "skill_domain": "python",
        "section": "conceptual",
        "question_type": "conceptual",
        "difficulty": "easy",
        "prompt": "Explain a core Python concept and give an example.",
    }

    evaluator_ratings = {
        "accuracy": 3,
        "depth": 3,
        "logical_reasoning": 3,
        "real_world_applicability": 3,
    }

    scored_answer = engine.score_answer(
        question=question,
        dimension_scores=evaluator_ratings,
        evidence_coverage=0.75,
        evidence_notes={
            "accuracy": "Sample evaluator rating",
            "depth": "Sample evaluator rating",
            "logical_reasoning": "Sample evaluator rating",
            "real_world_applicability": "Sample evaluator rating",
        },
        evaluator_id="DAY56_SAMPLE_EVALUATOR",
        evaluator_version="1.0",
    )

    report = engine.build_report(
        candidate_id=candidate_id,
        job_id="JOB-1001",
        session_id="DAY56-TECH-SAMPLE-SESSION",
        role_id="backend_developer",
        experience_years=0,
        scored_answers=[scored_answer],
        evaluator_summary={
            "source": "Sample evaluator-provided dimension ratings",
        },
    )

    return {
        "score": report["overall_score"],
        "engine_report": report,
        "input_provenance": (
            "Sample evaluator-provided ratings; "
            "not autonomous raw-answer evaluation"
        ),
    }


def run_machine_test():
    """Calculate a sample score using the design-only machine-test rubric."""

    rubric_path = DATA_DIR / "machine_test_ai" / "machine_test_scoring_model.json"
    rubric = load_json(rubric_path)

    task_type = "coding"
    weights = rubric["task_type_weights"][task_type]

    # Explicit sample ratings, not results from an executed coding test.
    ratings = {
        "correctness": 3,
        "efficiency": 3,
        "code_quality": 3,
        "problem_solving": 3,
    }

    score = sum(
        (ratings[dimension] / 4) * weight * 100
        for dimension, weight in weights.items()
    )

    return {
        "score": round(score, 2),
        "task_type": task_type,
        "dimension_ratings": ratings,
        "weights": weights,
        "rubric_version": rubric.get("model_version"),
        "rubric_status": "design_only_unvalidated",
        "input_provenance": (
            "Sample evaluator-provided ratings calculated using "
            "the design-only machine-test rubric; no coding task executed"
        ),
    }


def run_incomplete_evaluation_test(unified_engine, recommendation_engine):
    """Verify that missing stages lead to human review."""

    partial = unified_engine.calculate({
        "ats": 80,
        "screening": 75,
        "hr_interview": 82,
        "technical_interview": 78,
        # machine_test intentionally omitted
    })

    recommendation = recommendation_engine.recommend(partial)

    return {
        "unified_result": partial,
        "recommendation": recommendation,
        "passed": (
            partial["status"] == "incomplete"
            and "machine_test" in partial["missing_stages"]
            and recommendation["recommendation"] == "hold_review"
            and recommendation["requires_human_review"] is True
        ),
    }


def main():
    start = time.perf_counter()
    timestamp = datetime.now(timezone.utc).isoformat()

    print("=" * 65)
    print("ZECPath Day 56 - Full System Simulation")
    print("=" * 65)

    candidate_path = DATA_DIR / "parsed_resumes" / "arjun.json"
    candidate_data = load_json(candidate_path)

    candidate_id = candidate_data["candidate_id"]
    candidate_name = candidate_data.get("name", "Unknown")

    print(f"\nCandidate: {candidate_name} ({candidate_id})")

    stages = {}

    print("\n[1/6] Running ATS...")
    stages["ats"] = run_ats(candidate_data)
    print(f"ATS score: {stages['ats']['score']}")

    print("\n[2/6] Running screening...")
    stages["screening"] = run_screening(candidate_id)
    print(f"Screening score: {stages['screening']['score']}")

    print("\n[3/6] Running HR simulation...")
    stages["hr_interview"] = run_hr_simulation()
    print(f"HR fixture score: {stages['hr_interview']['pipeline_score']}")
    print(
        "HR comparison decision agreement: "
        f"{stages['hr_interview']['evaluation_metrics']['decision_accuracy']}%"
    )

    print("\n[4/6] Running technical scoring...")
    stages["technical_interview"] = run_technical(candidate_id)
    print(f"Technical sample score: {stages['technical_interview']['score']}")

    print("\n[5/6] Calculating machine-test sample...")
    stages["machine_test"] = run_machine_test()
    print(f"Machine-test sample score: {stages['machine_test']['score']}")

    scores = {
        "ats": stages["ats"]["score"],
        "screening": stages["screening"]["score"],
        "hr_interview": stages["hr_interview"]["pipeline_score"],
        "technical_interview": stages["technical_interview"]["score"],
        "machine_test": stages["machine_test"]["score"],
    }

    unified_engine = UnifiedScoringEngine(
        config_dir=DATA_DIR / "unified_scoring"
    )
    recommendation_engine = FinalRecommendationEngine(
        config_path=PROJECT_ROOT / "config" / "recommendation_policy.json"
    )

    print("\n[6/6] Running unified scoring and final recommendation...")
    unified_result = unified_engine.calculate(
        scores,
        role_type="technical",
    )
    final_recommendation = recommendation_engine.recommend(unified_result)

    incomplete_test = run_incomplete_evaluation_test(
        unified_engine,
        recommendation_engine,
    )

    elapsed_ms = round((time.perf_counter() - start) * 1000, 3)

    result = {
        "report_type": "day56_full_system_simulation",
        "report_version": "1.0",
        "generated_at": timestamp,
        "candidate": {
            "candidate_id": candidate_id,
            "name": candidate_name,
            "job_id": "JOB-1001",
            "job_title": "Backend Python Developer",
            "resume_source": str(candidate_path.relative_to(PROJECT_ROOT)),
        },
        "stages": stages,
        "unified_scores": scores,
        "unified_result": unified_result,
        "final_recommendation": final_recommendation,
        "incomplete_evaluation_test": incomplete_test,
        "performance": {
            "total_execution_time_ms": elapsed_ms,
            "measurement": "Single local execution; not a load test",
        },
        "limitations": [
            "The HR session is a predefined fixture and is not a real interview for candidate C001.",
            "HR manual comparisons use stored dataset judgments, not newly collected independent human evaluations.",
            "Technical scores are sample evaluator-provided ratings.",
            "Machine-test score is a sample calculation; no coding task was executed.",
            "The machine-test rubric is design-only and unvalidated.",
            "ATS score uses the available parsed resume fields; missing projects and certifications are treated as empty lists.",
            "This simulation is not evidence of production readiness or validated hiring accuracy.",
        ],
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    json_path = OUTPUT_DIR / "day56_simulation_results.json"
    save_json(result, json_path)

    report_lines = [
        "# ZECPath Day 56 - End-to-End Simulation Report",
        "",
        f"- Generated: {timestamp}",
        f"- Candidate: {candidate_name} ({candidate_id})",
        "- Target role: Backend Python Developer",
        "",
        "## Stage scores",
        "",
        "| Stage | Score | Input provenance |",
        "|---|---:|---|",
    ]

    for stage in scores:
        provenance = stages[stage]["input_provenance"]
        report_lines.append(
            f"| {stage.replace('_', ' ').title()} | {scores[stage]:.2f} | {provenance} |"
        )

    report_lines.extend([
        "",
        "## Unified scoring",
        "",
        f"- Role configuration: {unified_result['role_type']}",
        f"- Hiring Fit Score: {unified_result['hiring_fit_percentage']:.2f}",
        f"- Evaluation status: {unified_result['status']}",
        "",
        "## Final recommendation",
        "",
        f"- Recommendation: {final_recommendation['recommendation_label']}",
        f"- Human review required: {final_recommendation['requires_human_review']}",
        "",
        "## HR simulation comparison",
        "",
        f"- Sessions: {stages['hr_interview']['all_session_count']}",
        f"- Decision agreement: {stages['hr_interview']['evaluation_metrics']['decision_accuracy']}%",
        f"- Mean absolute score difference: {stages['hr_interview']['evaluation_metrics']['mean_absolute_score_difference']}",
        "",
        "These are comparisons against predefined stored manual judgments, not independent real-world validation.",
        "",
        "## Incomplete evaluation check",
        "",
        f"- Test passed: {incomplete_test['passed']}",
        f"- Missing stages: {', '.join(incomplete_test['unified_result']['missing_stages'])}",
        f"- Recommendation: {incomplete_test['recommendation']['recommendation_label']}",
        "",
        "## Performance",
        "",
        f"- Single-run execution time: {elapsed_ms} ms",
        "- This is a local single-run measurement, not a load or production benchmark.",
        "",
        "## Limitations",
        "",
    ])

    report_lines.extend(f"- {item}" for item in result["limitations"])

    report_lines.extend([
        "",
        "## Improvement recommendations",
        "",
        "- Collect independent human-reviewed examples before reporting hiring accuracy.",
        "- Validate ATS field mapping and scoring against approved job-specific criteria.",
        "- Validate screening rules against diverse, reviewed answer samples.",
        "- Obtain subject-matter approval for technical questions and scoring rubrics.",
        "- Implement and validate machine-test execution before treating it as a live stage.",
        "- Connect each candidate's actual interview records to the unified pipeline.",
        "- Run repeated and load tests before drawing performance conclusions.",
        "",
        "## Decision safeguard",
        "",
        "The final recommendation is decision support only. Human review remains necessary; this report does not establish autonomous employment decision capability.",
    ])

    markdown_path = REPORT_DIR / "day56_end_to_end_test_report.md"
    markdown_path.write_text(
        "\n".join(report_lines) + "\n",
        encoding="utf-8",
    )

    print("\n" + "=" * 65)
    print("SIMULATION COMPLETED")
    print("=" * 65)
    print(f"Hiring Fit Score: {unified_result['hiring_fit_percentage']}")
    print(f"Recommendation: {final_recommendation['recommendation_label']}")
    print(f"Incomplete evaluation safeguard: {'PASS' if incomplete_test['passed'] else 'FAIL'}")
    print(f"Execution time: {elapsed_ms} ms")
    print(f"\nJSON result: {json_path}")
    print(f"Markdown report: {markdown_path}")

    if not incomplete_test["passed"]:
        raise AssertionError("Incomplete evaluation safeguard failed.")


if __name__ == "__main__":
    main()

