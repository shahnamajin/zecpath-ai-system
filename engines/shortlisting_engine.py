class ShortlistingEngine:

    # -----------------------------------
    # Decide candidate status
    # -----------------------------------
    def classify(self, score):

        if score >= 80:
            return "Shortlist"

        elif score >= 60:
            return "Review"

        else:
            return "Reject"

    # -----------------------------------
    # Apply classification to all candidates
    # -----------------------------------
    def apply(self, candidates):

        for candidate in candidates:
            candidate["status"] = self.classify(
                candidate["score"]
            )

        return candidates