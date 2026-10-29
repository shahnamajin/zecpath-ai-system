import uuid


class IDGenerator:

    @staticmethod
    def generate_candidate_id():

        return "CAND-" + str(uuid.uuid4())[:8].upper()