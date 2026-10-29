import json
from pathlib import Path
from statistics import mean

class HRInterviewScoringEngine:
    COMPONENTS=("answer_relevance","communication","confidence","consistency")
    def __init__(self,config_path=None):
        if config_path is None:
            config_path=Path(__file__).resolve().parent.parent/"data/hr_interview_scoring/scoring_weights.json"
        with open(config_path,encoding="utf-8") as f: self.config=json.load(f)
        self.weights=self.config["weights"]
        if abs(sum(self.weights.values())-1.0)>0.0001: raise ValueError("Scoring weights must sum to 1.0")
    @staticmethod
    def _clamp(v): return round(max(0,min(100,float(v))),2)
    def _validate_response(self,r):
        for c in self.COMPONENTS:
            if c not in r: raise ValueError(f"Missing scoring component: {c}")
            if not 0<=float(r[c])<=100: raise ValueError(f"{c} must be between 0 and 100")
    def normalize_responses(self,responses):
        if not responses: raise ValueError("At least one interview response is required")
        for r in responses: self._validate_response(r)
        return {c:self._clamp(mean(float(r[c]) for r in responses)) for c in self.COMPONENTS}
    def calculate_score(self,scores):
        breakdown={}
        for c in self.COMPONENTS:
            s=self._clamp(scores[c]); w=self.weights[c]
            breakdown[c]={"score":s,"weight":w,"weighted_score":round(s*w,2)}
        return self._clamp(sum(x["weighted_score"] for x in breakdown.values())),breakdown
    @staticmethod
    def get_band(score):
        if score>=80:return "strong"
        if score>=60:return "moderate"
        if score>=40:return "developing"
        return "needs_improvement"
    def score_interview(self,candidate_id,job_id,session_id,job_title,responses):
        scores=self.normalize_responses(responses)
        final,breakdown=self.calculate_score(scores)
        return {"candidate_id":candidate_id,"job_id":job_id,"session_id":session_id,"job_title":job_title,
                "response_count":len(responses),"normalization":{"method":"response_average"},
                "component_scores":scores,"scoring_breakdown":breakdown,
                "final_hr_interview_score":final,"band":self.get_band(final)}
    def explain(self,result):
        lines=[f"Candidate: {result['candidate_id']}",f"Job: {result['job_title']}","",
               "SCORING BREAKDOWN"]
        for c,x in result["scoring_breakdown"].items():
            lines.append(f"- {c}: {x['score']:.2f} x {x['weight']*100:.0f}% = {x['weighted_score']:.2f}")
        lines += ["",f"Final HR Interview Score: {result['final_hr_interview_score']:.2f}/100",
                  f"Band: {result['band']}","Normalization: response-average method"]
        return "\n".join(lines)
