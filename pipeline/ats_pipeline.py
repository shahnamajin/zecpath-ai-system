from ats_engine.ats_scorer import ATSScorer
from storage.json_storage import JSONStorage


class ATSPipeline:

    def __init__(self):

        self.ats = ATSScorer()
        self.storage = JSONStorage()

    def process(self, candidate):

        score = self.ats.score(candidate)

        self.storage.save(
            score,
            "data/ats_scores",
            candidate["candidate_id"] + ".json"
        )

        return score