from parsers.information_extractor import InformationExtractor


extractor = InformationExtractor()


resume = """
Software Engineer

Python
SQL
Django
Machine Learning

Education:
MCA
"""


success = 0
failed = 0


total_runs = 20


for i in range(total_runs):

    try:

        result = extractor.extract(resume)

        if result:
            success += 1

    except Exception as error:

        failed += 1

        print(
            f"Run {i + 1} Error:",
            error
        )


success_rate = (
    success / total_runs
) * 100


print("\nSTABILITY TEST")
print("=" * 40)

print(
    "Total Runs:",
    total_runs
)

print(
    "Successful Runs:",
    success
)

print(
    "Failed Runs:",
    failed
)

print(
    "Success Rate:",
    round(success_rate, 2),
    "%"
)