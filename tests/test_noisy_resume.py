from utils.resume_cleaner import ResumeCleaner


noisy_resume = """
Python   Python   Python!!!

SQL ### SQL

Pandas / NumPy / Python

Machine-Learning!!!

Email: test@example.com
"""


cleaner = ResumeCleaner()

cleaned = cleaner.clean(
    noisy_resume
)


print("\nOriginal Resume:")
print(noisy_resume)

print("\nCleaned Resume:")
print(cleaned)