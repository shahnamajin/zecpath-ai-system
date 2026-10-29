class CandidateLifecycle:

    STAGES = [

        "Resume Uploaded",

        "Resume Parsed",

        "ATS Completed",

        "Screening",

        "Technical Interview",

        "HR Interview",

        "Final Decision",

        "Offer Sent"

    ]

    def get_stages(self):
        return self.STAGES