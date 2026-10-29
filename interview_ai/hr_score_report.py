import json
class HRScoreReport:
    def to_dict(self,r):
        return {"candidate":{"candidate_id":r["candidate_id"],"job_id":r["job_id"],"session_id":r["session_id"],"job_title":r["job_title"]},
                "interview_summary":{"responses_evaluated":r["response_count"],"normalization_method":r["normalization"]["method"]},
                "score":{"final":r["final_hr_interview_score"],"band":r["band"]},
                "component_scores":r["component_scores"],"explainable_breakdown":r["scoring_breakdown"]}
    def to_json(self,r): return json.dumps(self.to_dict(r),indent=2)
