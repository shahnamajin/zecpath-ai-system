
"""ZECPath AI - Recruiter-ready HR Interview Summary Generator."""

from statistics import mean


class InterviewSummaryGenerator:
    def __init__(self):
        self.strength_threshold = 80
        self.weakness_threshold = 65
        self.risk_threshold = 60

    @staticmethod
    def _clamp(value):
        return round(max(0.0, min(100.0, float(value))), 2)

    def extract_inconsistencies(self, responses):
        return [
            {
                "question_id": r.get("question_id"),
                "detail": r.get("inconsistency")
            }
            for r in responses
            if not r.get("consistent", True) and r.get("inconsistency")
        ]

    def generate_strengths(self, data):
        strengths = []
        if data.get("hr_score", 0) >= self.strength_threshold:
            strengths.append("Strong overall HR interview performance")
        if data.get("communication_score", 0) >= self.strength_threshold:
            strengths.append("Clear and structured communication")
        if data.get("confidence_score", 0) >= self.strength_threshold:
            strengths.append("Consistent confidence signals")
        if data.get("consistency_score", 0) >= self.strength_threshold:
            strengths.append("Consistent responses across evaluated answers")
        if data.get("aptitude_logic_score", 0) >= 70:
            strengths.append("Demonstrates observable reasoning and problem-solving structure")
        return strengths

    def generate_weaknesses(self, data):
        weaknesses = []
        if data.get("communication_score", 0) < self.weakness_threshold:
            weaknesses.append("Communication clarity may need improvement")
        if data.get("confidence_score", 0) < self.weakness_threshold:
            weaknesses.append("Confidence signals were comparatively lower")
        if data.get("consistency_score", 0) < self.weakness_threshold:
            weaknesses.append("Response consistency requires further review")
        if data.get("aptitude_logic_score", 0) < self.weakness_threshold:
            weaknesses.append("Reasoning responses may need deeper evaluation")
        return weaknesses

    def generate_cultural_fit_indicators(self, responses):
        text = " ".join(r.get("answer", "").lower() for r in responses)
        indicators = []
        if any(x in text for x in ["team", "teamwork", "coordinate", "collaborate"]):
            indicators.append("Team collaboration is referenced in responses")
        if any(x in text for x in ["communicate", "communication", "discuss"]):
            indicators.append("Communication and coordination are referenced")
        if any(x in text for x in ["responsibility", "ownership", "accountable"]):
            indicators.append("Ownership or responsibility is referenced")
        if not indicators:
            indicators.append("Insufficient response evidence for a cultural-fit indicator")
        return indicators

    def generate_risk_flags(self, data, inconsistencies):
        risks = []
        if data.get("consistency_score", 0) < self.risk_threshold:
            risks.append("Low consistency score")
        if data.get("confidence_score", 0) < self.risk_threshold:
            risks.append("Low confidence signal score")
        if data.get("communication_score", 0) < self.risk_threshold:
            risks.append("Low communication score")
        if inconsistencies:
            risks.append("One or more response inconsistencies require review")
        if not risks:
            risks.append("No major automated risk flag detected in the supplied analysis")
        return risks

    def overall_performance(self, data):
        values = [
            data.get("hr_score", 0),
            data.get("communication_score", 0),
            data.get("confidence_score", 0),
            data.get("consistency_score", 0),
            data.get("aptitude_logic_score", 0)
        ]
        return self._clamp(mean(values))

    def natural_language_summary(self, data, strengths, weaknesses, culture, risks, inconsistencies):
        candidate = data.get("candidate_id", "Candidate")
        job = data.get("job_title", "the role")
        overall = self.overall_performance(data)

        text = (
            f"{candidate} completed the AI-assisted HR interview for {job}. "
            f"The supplied analysis indicates an overall performance score of {overall:.2f}/100. "
        )

        if strengths:
            text += "Key observed strengths include " + "; ".join(strengths[:3]) + ". "
        if weaknesses:
            text += "Areas requiring further review include " + "; ".join(weaknesses[:3]) + ". "
        if culture:
            text += "Cultural-fit indicators observed in the supplied responses include " + "; ".join(culture[:2]) + ". "
        if inconsistencies:
            text += f"{len(inconsistencies)} response inconsistency requires review against the underlying interview evidence. "
        if risks:
            text += "Automated risk review: " + "; ".join(risks[:2]) + "."

        return text

    def generate(self, data):
        responses = data.get("responses", [])
        inconsistencies = self.extract_inconsistencies(responses)
        strengths = self.generate_strengths(data)
        weaknesses = self.generate_weaknesses(data)
        culture = self.generate_cultural_fit_indicators(responses)
        risks = self.generate_risk_flags(data, inconsistencies)
        overall = self.overall_performance(data)

        return {
            "candidate": {
                "candidate_id": data.get("candidate_id"),
                "job_id": data.get("job_id"),
                "session_id": data.get("session_id"),
                "job_title": data.get("job_title")
            },
            "overall_performance": {
                "hr_score": self._clamp(data.get("hr_score", 0)),
                "aptitude_logic_score": self._clamp(data.get("aptitude_logic_score", 0)),
                "communication_score": self._clamp(data.get("communication_score", 0)),
                "confidence_score": self._clamp(data.get("confidence_score", 0)),
                "consistency_score": self._clamp(data.get("consistency_score", 0)),
                "summary_score": overall
            },
            "insights": {
                "strengths": strengths,
                "weaknesses": weaknesses,
                "cultural_fit_indicators": culture,
                "risk_flags": risks,
                "inconsistencies": inconsistencies
            },
            "natural_language_summary": self.natural_language_summary(
                data, strengths, weaknesses, culture, risks, inconsistencies
            ),
            "disclaimer": (
                "Summary reflects the supplied AI analysis and should be reviewed "
                "with the underlying interview evidence."
            )
        }
