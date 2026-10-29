class RankingEngine:

    # -----------------------------------
    # Rank candidates by score
    # -----------------------------------
    def rank(self, candidates):

        ranked = sorted(
            candidates,
            key=lambda x: x["score"],
            reverse=True
        )

        for index, candidate in enumerate(ranked, start=1):
            candidate["rank"] = index

        return ranked

    # -----------------------------------
    # Return top N candidates
    # -----------------------------------
    def top_candidates(self, candidates, top_n=3):

        ranked = self.rank(candidates)

        return ranked[:top_n]