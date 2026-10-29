from datetime import datetime


class AILogger:

    def log(self, stage, candidate_id):

        print({

            "candidate_id": candidate_id,

            "stage": stage,

            "timestamp": datetime.now().isoformat()

        })