from engines.ranking_engine import RankingEngine
from engines.shortlisting_engine import ShortlistingEngine


def main():

    candidates = [
        {"candidate_id": "DEMO-001", "score": 91},
        {"candidate_id": "DEMO-002", "score": 72},
        {"candidate_id": "DEMO-003", "score": 85},
        {"candidate_id": "DEMO-004", "score": 68},
        {"candidate_id": "DEMO-005", "score": 54},
    ]

    ranking_engine = RankingEngine()
    shortlisting_engine = ShortlistingEngine()

    ranked = ranking_engine.rank(candidates)

    final_result = shortlisting_engine.apply(ranked)

    print("\nFINAL ATS EVALUATION")
    print("=" * 50)

    for candidate in final_result:
        print(
            candidate["candidate_id"],
            "| Rank:", candidate["rank"],
            "| Score:", candidate["score"],
            "| Status:", candidate["status"]
        )


if __name__ == "__main__":
    main()