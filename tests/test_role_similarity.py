from config.role_similarity import ROLE_SIMILARITY

print("Software Engineer Similar Roles:\n")

for role in ROLE_SIMILARITY["Software Engineer"]:
    print("-", role)