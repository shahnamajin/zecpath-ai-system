import json
from pathlib import Path
from interview_ai.hr_interview_scoring_engine import HRInterviewScoringEngine
from interview_ai.hr_score_report import HRScoreReport

def main():
    p=Path(__file__).resolve().parent.parent/"data/hr_interview_scoring/sample_hr_interview.json"
    with open(p,encoding="utf-8") as f: d=json.load(f)
    r=HRInterviewScoringEngine().score_interview(d["candidate_id"],d["job_id"],d["session_id"],d["job_title"],d["responses"])
    print("ZECPath AI - HR INTERVIEW SCORING ENGINE DEMO")
    print("="*58)
    print(f"\nCandidate ID : {r['candidate_id']}\nJob ID       : {r['job_id']}\nSession ID   : {r['session_id']}\nJob Title    : {r['job_title']}\nResponses    : {r['response_count']}")
    print("\nNORMALIZED COMPONENT SCORES")
    for c,s in r["component_scores"].items(): print(f"{c.replace('_',' ').title():22}: {s:.2f}/100")
    print("\nEXPLAINABLE SCORING BREAKDOWN")
    for c,x in r["scoring_breakdown"].items(): print(f"{c.replace('_',' ').title():22}: {x['score']:.2f} x {x['weight']*100:.0f}% = {x['weighted_score']:.2f}")
    print("\nFINAL HR INTERVIEW RESULT")
    print(f"Final HR Score           : {r['final_hr_interview_score']:.2f}/100")
    print(f"Score Band               : {r['band']}")
    print(f"Normalization Method     : {r['normalization']['method']}")
    out=Path(__file__).resolve().parent.parent/"data/hr_interview_scoring/sample_hr_score_report.json"
    out.write_text(HRScoreReport().to_json(r),encoding="utf-8")
    print(f"Report Export            : {out.name}")
    print("\nHR INTERVIEW SCORING ENGINE COMPLETED SUCCESSFULLY")
if __name__=="__main__": main()
