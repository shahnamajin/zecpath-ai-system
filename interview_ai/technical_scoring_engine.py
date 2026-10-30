"""Explainable technical answer scoring and skill-wise aggregation.

Scores are supplied by a human or a separately validated evaluator on a 0-4 scale.
This module aggregates and explains those ratings; it does not claim to understand
technical correctness from raw text by itself.
"""
import json
from pathlib import Path
from datetime import datetime, timezone


DIMENSIONS = ("accuracy", "depth", "logical_reasoning", "real_world_applicability")


class TechnicalScoringEngine:
    def __init__(self, rubric_path=None):
        default = Path(__file__).resolve().parent.parent / "data" / "technical_interview" / "technical_scoring_rubrics.json"
        self.rubric_path = Path(rubric_path or default)
        with self.rubric_path.open("r", encoding="utf-8") as f:
            self.rubrics = json.load(f)

    def _validate_scores(self, scores):
        if not isinstance(scores, dict):
            raise ValueError("dimension_scores must be a dictionary")
        missing = set(DIMENSIONS) - set(scores)
        if missing:
            raise ValueError(f"Missing scoring dimensions: {sorted(missing)}")
        cleaned = {}
        for key in DIMENSIONS:
            value = scores[key]
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 <= value <= 4:
                raise ValueError(f"{key} must be a number between 0 and 4")
            cleaned[key] = float(value)
        return cleaned

    def score_answer(self, question, dimension_scores, evidence_coverage=None,
                     evidence_notes=None, evaluator_id=None, evaluator_version=None):
        required = ("question_id", "skill_domain", "section", "difficulty", "prompt")
        missing = [key for key in required if key not in question]
        if missing:
            raise ValueError(f"Question is missing fields: {missing}")
        question_type = question.get("question_type", question["section"])
        if question_type not in self.rubrics["question_type_weights"]:
            raise ValueError(f"Unsupported question_type: {question_type}")
        if question["difficulty"] not in self.rubrics["difficulty_expectations"]:
            raise ValueError(f"Unsupported difficulty: {question['difficulty']}")

        scores = self._validate_scores(dimension_scores)
        weights = self.rubrics["question_type_weights"][question_type]
        if evidence_coverage is not None:
            if isinstance(evidence_coverage, bool) or not isinstance(evidence_coverage, (int, float)) or not 0 <= evidence_coverage <= 1:
                raise ValueError("evidence_coverage must be between 0 and 1")
            coverage = float(evidence_coverage)
        else:
            coverage = None

        weighted = {key: round(scores[key] * weights[key], 4) for key in DIMENSIONS}
        raw_score = sum(weighted.values()) / 4 * 100
        normalized = round(max(0.0, min(100.0, raw_score)), 2)

        shallow_policy = self.rubrics["shallow_deep_policy"]
        if scores["depth"] < 2.0 or (coverage is not None and coverage < 0.40):
            answer_depth = "shallow"
        elif (scores["depth"] >= 3.0 and scores["logical_reasoning"] >= 3.0
              and (coverage is None or coverage >= 0.70)):
            answer_depth = "deep"
        else:
            answer_depth = "developing"

        explanations = []
        for dimension in DIMENSIONS:
            rating = scores[dimension]
            if rating >= 3.5:
                label = "strong"
            elif rating >= 2.5:
                label = "good"
            elif rating >= 1.5:
                label = "partial"
            else:
                label = "needs_review"
            explanations.append({
                "dimension": dimension,
                "rating": rating,
                "weight": weights[dimension],
                "weighted_contribution": round(weighted[dimension] / 4 * 100, 2),
                "assessment": label,
                "evidence_note": (evidence_notes or {}).get(dimension, "")
            })

        return {
            "question_id": question["question_id"],
            "skill_domain": question["skill_domain"],
            "section": question["section"],
            "question_type": question_type,
            "difficulty": question["difficulty"],
            "dimension_scores": scores,
            "dimension_breakdown": explanations,
            "evidence_coverage": coverage,
            "answer_depth": answer_depth,
            "raw_score": normalized,
            "normalized_score": normalized,
            "normalization_note": self.rubrics["normalization"]["method"],
            "difficulty_expectation": self.rubrics["difficulty_expectations"][question["difficulty"]],
            "evidence_notes": evidence_notes or {},
            "evaluator": {"id": evaluator_id, "version": evaluator_version},
            "scored_at": datetime.now(timezone.utc).isoformat()
        }

    def build_skill_breakdown(self, scored_answers):
        skills = {}
        for answer in scored_answers:
            skill = answer["skill_domain"]
            skills.setdefault(skill, []).append(answer["normalized_score"])
        result = {}
        for skill, scores in sorted(skills.items()):
            result[skill] = {
                "question_count": len(scores),
                "average_score": round(sum(scores) / len(scores), 2),
                "minimum_score": round(min(scores), 2),
                "maximum_score": round(max(scores), 2)
            }
        return result

    def build_report(self, candidate_id, job_id, session_id, role_id,
                     experience_years, scored_answers, evaluator_summary=None):
        if not scored_answers:
            raise ValueError("At least one scored answer is required")
        skill_breakdown = self.build_skill_breakdown(scored_answers)
        overall = round(sum(a["normalized_score"] for a in scored_answers) / len(scored_answers), 2)
        shallow = sum(a["answer_depth"] == "shallow" for a in scored_answers)
        deep = sum(a["answer_depth"] == "deep" for a in scored_answers)
        return {
            "report_type": "technical_interview_evaluation",
            "report_version": "1.0",
            "candidate_id": candidate_id,
            "job_id": job_id,
            "session_id": session_id,
            "role_id": role_id,
            "experience_years": experience_years,
            "overall_score": overall,
            "question_count": len(scored_answers),
            "skill_wise_breakdown": skill_breakdown,
            "answer_depth_summary": {"shallow": shallow, "developing": len(scored_answers)-shallow-deep, "deep": deep},
            "question_evaluations": scored_answers,
            "evaluator_summary": evaluator_summary or {},
            "decision_status": "human_review_required",
            "limitations": [
                "Scores depend on the validity and consistency of the supplied dimension ratings.",
                "This report is an evaluation aid and does not make an autonomous hiring decision."
            ],
            "generated_at": datetime.now(timezone.utc).isoformat()
        }

    @staticmethod
    def save_report(report, output_path):
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(report, indent=2), encoding="utf-8")
        return str(path)
