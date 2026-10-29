from engines.testing_metrics import TestingMetrics


results = [

    {
        "candidate_id": "CAND-001",
        "category": "Tech Fresher",
        "ai_decision": "Shortlist",
        "manual_decision": "Shortlist"
    },

    {
        "candidate_id": "CAND-002",
        "category": "Tech Fresher",
        "ai_decision": "Review",
        "manual_decision": "Shortlist"
    },

    {
        "candidate_id": "CAND-003",
        "category": "Tech Senior",
        "ai_decision": "Shortlist",
        "manual_decision": "Shortlist"
    },

    {
        "candidate_id": "CAND-004",
        "category": "Tech Senior",
        "ai_decision": "Shortlist",
        "manual_decision": "Shortlist"
    },

    {
        "candidate_id": "CAND-005",
        "category": "Non-Tech Fresher",
        "ai_decision": "Shortlist",
        "manual_decision": "Shortlist"
    },

    {
        "candidate_id": "CAND-006",
        "category": "Non-Tech Fresher",
        "ai_decision": "Review",
        "manual_decision": "Review"
    },

    {
        "candidate_id": "CAND-007",
        "category": "Non-Tech Senior",
        "ai_decision": "Shortlist",
        "manual_decision": "Shortlist"
    },

    {
        "candidate_id": "CAND-008",
        "category": "Non-Tech Senior",
        "ai_decision": "Reject",
        "manual_decision": "Reject"
    }
]


metrics = TestingMetrics()


print("\nATS SYSTEM TESTING REPORT")
print("=" * 40)

print(
    "Accuracy:",
    metrics.accuracy(results),
    "%"
)

print(
    "Precision:",
    metrics.precision(results),
    "%"
)

print(
    "Recall:",
    metrics.recall(results),
    "%"
)


print("\nCandidate Results")
print("-" * 40)

for result in results:

    match = (
        result["ai_decision"]
        == result["manual_decision"]
    )

    print(
        result["candidate_id"],
        "|",
        result["category"],
        "| AI:",
        result["ai_decision"],
        "| Manual:",
        result["manual_decision"],
        "| Match:",
        match
    )