class ScoreAggregator:
    """
    Aggregates per-question screening scores
    into an overall screening score.
    """

    def normalize_score(self, score):
        """
        Normalize a score to the range 0-100.
        """

        return round(
            max(0.0, min(100.0, float(score))),
            2
        )

    def aggregate(self, question_scores):
        """
        Calculate the overall screening score.
        """

        if not question_scores:
            return {
                "total_questions": 0,
                "average_score": 0.0,
                "normalized_score": 0.0
            }

        scores = [
            float(
                item.get("total_score", 0)
            )
            for item in question_scores
        ]

        average_score = sum(scores) / len(scores)

        normalized_score = self.normalize_score(
            average_score
        )

        return {
            "total_questions": len(scores),
            "average_score": round(
                average_score,
                2
            ),
            "normalized_score": normalized_score
        }