
import sys
import time
import statistics
from pathlib import Path

# Add project root to Python import path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from screening_ai.intent_classifier import IntentClassifier
from screening_ai.threshold_optimizer import ThresholdOptimizer
from screening_ai.false_rejection_analyzer import FalseRejectionAnalyzer
from hiring_ai.unified_scoring_engine import UnifiedScoringEngine


def benchmark(name, function, iterations=1000):

    timings = []

    for _ in range(iterations):
        start = time.perf_counter()
        function()
        end = time.perf_counter()

        timings.append((end - start) * 1000)

    average = statistics.mean(timings)
    minimum = min(timings)
    maximum = max(timings)

    print(f"\n{name}")
    print("-" * 40)
    print(f"Iterations: {iterations}")
    print(f"Average: {average:.6f} ms")
    print(f"Minimum: {minimum:.6f} ms")
    print(f"Maximum: {maximum:.6f} ms")


# Initialize components outside timed functions
classifier = IntentClassifier()
optimizer = ThresholdOptimizer()
analyzer = FalseRejectionAnalyzer()
scoring_engine = UnifiedScoringEngine()

candidate_answer = (
    "I completed MCA and have experience working "
    "with Python, Java, SQL and machine learning projects."
)

evaluation_scores = {
    "ats": 85,
    "screening": 80,
    "hr_interview": 90,
    "technical_interview": 88,
    "machine_test": 92,
}

screening_results = [
    {
        "case_id": f"C{i}",
        "expected_decision": "continue",
        "predicted_decision": "continue",
    }
    for i in range(100)
]


if __name__ == "__main__":

    print("=" * 50)
    print("ZECPath Day 54 Processing Speed Benchmark")
    print("=" * 50)

    print(f"Project root: {PROJECT_ROOT}")

    benchmark(
        "Intent Classification",
        lambda: classifier.classify(
            candidate_answer,
            "education"
        )
    )

    benchmark(
        "Threshold Optimization",
        lambda: optimizer.decide(
            score=85,
            intent="skills"
        )
    )

    benchmark(
        "False Rejection Analysis (100 cases)",
        lambda: analyzer.analyze(screening_results),
        iterations=100
    )

    benchmark(
        "Unified Scoring Engine",
        lambda: scoring_engine.calculate(evaluation_scores)
    )

    print("\nBenchmark completed.")
