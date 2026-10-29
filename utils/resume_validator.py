class ResumeValidator:

    def validate(self, candidate):

        errors = []

        if not candidate["personal_information"]["full_name"]:
            errors.append("Missing Name")

        if not candidate["personal_information"]["email"]:
            errors.append("Missing Email")

        if not candidate["skills"]["programming"]:
            errors.append("No Programming Skills")

        return errors