import time
import tracemalloc

from parsers.information_extractor import InformationExtractor


extractor = InformationExtractor()


sample_resume = """
SHAHNA MAJI

Email: shahna@example.com
Phone: 9876543210

PROFESSIONAL SUMMARY

MCA student with skills in Python, SQL, Data Analytics,
Machine Learning and Software Development.

EDUCATION

Master of Computer Applications
LEAD College of Management
2026

Bachelor of Computer Applications
Malabar College of Advanced Studies
2025

SKILLS

Python
SQL
Pandas
NumPy
Machine Learning
Flutter
JavaScript

EXPERIENCE

Software Developer Intern
Worked on Python applications and data analysis projects.

PROJECTS

MedLens
Healthcare analysis application using Python.

SmartCrop AI
Crop recommendation system using Machine Learning.

CERTIFICATIONS

GenAI Powered Data Analytics
Flutter Development
React JS
"""


total_runs = 10

times = []

tracemalloc.start()

for i in range(total_runs):

    start = time.perf_counter()

    result = extractor.extract(
        sample_resume
    )

    end = time.perf_counter()

    times.append(
        end - start
    )


current_memory, peak_memory = (
    tracemalloc.get_traced_memory()
)

tracemalloc.stop()


average_time = sum(times) / len(times)

minimum_time = min(times)

maximum_time = max(times)


print("\nATS PERFORMANCE TEST")
print("=" * 40)

print(
    "Total Runs:",
    total_runs
)

print(
    "Average Execution Time:",
    round(average_time, 6),
    "seconds"
)

print(
    "Minimum Execution Time:",
    round(minimum_time, 6),
    "seconds"
)

print(
    "Maximum Execution Time:",
    round(maximum_time, 6),
    "seconds"
)

print(
    "Peak Memory:",
    round(
        peak_memory / (1024 * 1024),
        4
    ),
    "MB"
)