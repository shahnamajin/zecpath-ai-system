from pprint import pprint

from engines.ranking_engine import RankingEngine
from engines.shortlisting_engine import ShortlistingEngine


# -----------------------------------
# Sample candidate data
# -----------------------------------

candidates = [

    {"candidate_id": "CAND-001", "score": 91},

    {"candidate_id": "CAND-002", "score": 85},

    {"candidate_id": "CAND-003", "score": 72},

    {"candidate_id": "CAND-004", "score": 54}

]


# -----------------------------------
# Step 1: Rank candidates
# -----------------------------------

ranking_engine = RankingEngine()

ranked = ranking_engine.rank(candidates)


# -----------------------------------
# Step 2: Apply shortlisting
# -----------------------------------

shortlisting_engine = ShortlistingEngine()

final_output = shortlisting_engine.apply(ranked)


# -----------------------------------
# Final ranked list
# -----------------------------------

print("\nFinal Ranked Candidate List:\n")

pprint(final_output)


# -----------------------------------
# Recruiter friendly output
# -----------------------------------

print("\nRecruiter Friendly Output:\n")

for c in final_output:

    print(
        f"Rank: {c['rank']} | "
        f"ID: {c['candidate_id']} | "
        f"Score: {c['score']} | "
        f"Status: {c['status']}"
    )


# -----------------------------------
# Top candidates
# -----------------------------------

top3 = ranking_engine.top_candidates(
    candidates,
    top_n=3
)

print("\nTop 3 Candidates:\n")

pprint(top3)