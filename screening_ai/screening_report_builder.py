from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


class ScreeningReportBuilder:
    """Build recruiter-friendly reports from structured AI screening outputs."""

    def _extract_score(self, screening: Dict[str, Any]) -> Optional[float]:
        for key in (
            "final_screening_score",
            "average_score",
            "total_score",
            "score",
        ):
            value = screening.get(key)

            if isinstance(value, (int, float)):
                return round(float(value), 2)

        return None

    def _extract_entities(self, item: Dict[str, Any]) -> Dict[str, Any]:
        entities = item.get("entities", {})

        return {
            "skills": entities.get("skills", []) or [],
            "experience": entities.get("experience"),
            "availability": entities.get("availability"),
            "salary_expectation": entities.get("salary_expectation"),
        }

    def _answer_text(self, item: Dict[str, Any]) -> str:
        answer = item.get("answer", {})

        if isinstance(answer, dict):
            return str(
                answer.get("raw_text")
                or answer.get("text")
                or ""
            ).strip()

        return str(
            item.get("raw_text")
            or item.get("text")
            or ""
        ).strip()

    def _intent(self, item: Dict[str, Any]) -> str:
        answer = item.get("answer", {})

        if isinstance(answer, dict):
            return str(answer.get("intent", "unknown"))

        return "unknown"

    def _question_id(self, item: Dict[str, Any]) -> str:
        return str(
            item.get("question_id")
            or item.get("id")
            or "unknown"
        )

    def _quality_flags(self, item: Dict[str, Any]) -> Dict[str, bool]:
        quality = item.get("quality", {})

        return {
            "missing": bool(quality.get("is_missing")),
            "vague": bool(quality.get("is_vague")),
            "off_topic": bool(quality.get("is_off_topic")),
        }

    def build(
        self,
        candidate: Dict[str, Any],
        answers: List[Dict[str, Any]],
        screening: Dict[str, Any],
        behavioral: Optional[Dict[str, Any]] = None,
        report_id: Optional[str] = None,
    ) -> Dict[str, Any]:

        behavioral = behavioral or {}

        key_answers = []

        skills = set()
        strengths = []
        risks = []
        missing = []

        salary = None
        availability = None

        for item in answers:

            text = self._answer_text(item)
            intent = self._intent(item)

            entities = self._extract_entities(item)
            flags = self._quality_flags(item)

            # Key answer
            key_answers.append(
                {
                    "question_id": self._question_id(item),
                    "intent": intent,
                    "answer": text,
                }
            )

            # Skills
            for skill in entities["skills"]:
                skills.add(str(skill))

            # Salary
            if entities["salary_expectation"] and not salary:
                salary = entities["salary_expectation"]

            # Availability
            if entities["availability"] and not availability:
                availability = entities["availability"]

            # Missing / risks
            if flags["missing"] or not text:

                missing.append(
                    {
                        "question_id": self._question_id(item),
                        "reason": "Missing answer",
                    }
                )

            elif flags["off_topic"]:

                risks.append(
                    {
                        "question_id": self._question_id(item),
                        "reason": "Off-topic response",
                    }
                )

            elif flags["vague"]:

                risks.append(
                    {
                        "question_id": self._question_id(item),
                        "reason": "Vague response",
                    }
                )

            else:

                if intent in {
                    "skills",
                    "experience",
                    "education",
                    "availability",
                    "salary_expectation",
                }:
                    strengths.append(
                        "Provided a relevant "
                        + intent.replace("_", " ")
                        + " response"
                    )

        # Behavioral signals
        communication = behavioral.get(
            "communication_signals",
            {},
        )

        sentiment = behavioral.get(
            "sentiment",
            {},
        )

        contradiction = behavioral.get(
            "contradiction",
            {},
        )

        # Communication strength
        communication_strength = communication.get(
            "communication_strength"
        )

        if communication_strength is not None:

            if communication_strength >= 70:

                strengths.append(
                    f"Communication signal score: "
                    f"{communication_strength}/100"
                )

            elif communication_strength < 50:

                risks.append(
                    f"Communication signal score is "
                    f"{communication_strength}/100"
                )

        # Sentiment
        if sentiment.get("sentiment") == "positive":

            strengths.append(
                "Positive sentiment indicators were detected"
            )

        elif sentiment.get("sentiment") == "negative":

            risks.append(
                "Negative sentiment indicators were detected"
            )

        # Contradictions
        if contradiction.get("detected"):

            for detail in contradiction.get("details", []):

                risks.append(
                    {
                        "reason": "Potential contradiction",
                        "details": detail,
                    }
                )

        # Missing highlighted fields
        if not salary:

            missing.append(
                {
                    "field": "salary_expectation",
                    "reason": "Not provided",
                }
            )

        if not availability:

            missing.append(
                {
                    "field": "availability",
                    "reason": "Not provided",
                }
            )

        if not skills:

            missing.append(
                {
                    "field": "skills",
                    "reason": "No skills confirmed",
                }
            )

        return {
            "report_id": report_id
            or f"RPT_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}",

            "report_version": "1.0",

            "generated_at":
                datetime.now(timezone.utc).isoformat(),

            "candidate": {
                "candidate_id": candidate.get("candidate_id"),
                "name": candidate.get("name"),
                "job_id": candidate.get("job_id"),
                "role": candidate.get("role"),
            },

            "screening_summary": {
                "final_score":
                    self._extract_score(screening),

                "total_questions":
                    screening.get(
                        "total_questions",
                        len(answers),
                    ),

                "answered_questions":
                    sum(
                        1
                        for answer in key_answers
                        if answer["answer"]
                    ),
            },

            "key_answers": key_answers,

            "highlighted_information": {
                "confirmed_skills":
                    sorted(skills),

                "salary_expectation":
                    salary,

                "availability":
                    availability,
            },

            "strengths": strengths,

            "risks": risks,

            "missing_data": missing,

            "behavioral_signals": behavioral,

            "recruiter_summary":
                self._build_summary(
                    skills,
                    salary,
                    availability,
                    strengths,
                    risks,
                    missing,
                ),
        }

    def _build_summary(
        self,
        skills,
        salary,
        availability,
        strengths,
        risks,
        missing,
    ):

        parts = []

        if skills:

            parts.append(
                f"Confirmed skills: "
                f"{', '.join(sorted(skills))}."
            )

        else:

            parts.append(
                "No skills were confirmed."
            )

        if salary:

            parts.append(
                f"Salary expectation: {salary}."
            )

        else:

            parts.append(
                "Salary expectation was not provided."
            )

        if availability:

            parts.append(
                f"Availability: {availability}."
            )

        else:

            parts.append(
                "Availability was not provided."
            )

        parts.append(
            f"{len(strengths)} strength indicator(s) "
            f"and {len(risks)} risk indicator(s) "
            f"were identified."
        )

        if missing:

            parts.append(
                f"{len(missing)} missing-data item(s) "
                f"require recruiter follow-up."
            )

        return " ".join(parts)