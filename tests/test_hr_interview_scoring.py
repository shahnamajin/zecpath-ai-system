from interview_ai.hr_interview_scoring_engine import HRInterviewScoringEngine
from interview_ai.hr_score_report import HRScoreReport

def responses():
    return [{"answer_relevance":90,"communication":80,"confidence":85,"consistency":95},
            {"answer_relevance":80,"communication":90,"confidence":75,"consistency":85},
            {"answer_relevance":100,"communication":70,"confidence":90,"consistency":80}]

def test_weights_sum_to_one():
    assert abs(sum(HRInterviewScoringEngine().weights.values())-1)<.0001
def test_normalized_scores_are_averages():
    s=HRInterviewScoringEngine().normalize_responses(responses())
    assert s=={"answer_relevance":90.0,"communication":80.0,"confidence":83.33,"consistency":86.67}
def test_final_score_range():
    r=HRInterviewScoringEngine().score_interview("C","J","S","Python Developer",responses())
    assert 0<=r["final_hr_interview_score"]<=100
def test_breakdown_is_explainable():
    r=HRInterviewScoringEngine().score_interview("C","J","S","Python Developer",responses())
    assert all(set(("score","weight","weighted_score"))<=set(r["scoring_breakdown"][c]) for c in HRInterviewScoringEngine.COMPONENTS)
def test_length_normalization():
    e=HRInterviewScoringEngine(); a=responses(); b=a+a
    r1=e.score_interview("C","J","S1","Python Developer",a); r2=e.score_interview("C","J","S2","Python Developer",b)
    assert r1["final_hr_interview_score"]==r2["final_hr_interview_score"]
def test_bands():
    e=HRInterviewScoringEngine()
    assert e.get_band(90)=="strong"; assert e.get_band(70)=="moderate"; assert e.get_band(50)=="developing"; assert e.get_band(20)=="needs_improvement"
def test_invalid_score_rejected():
    e=HRInterviewScoringEngine(); bad=responses()[0].copy(); bad["confidence"]=120
    try:e.normalize_responses([bad]); assert False
    except ValueError: assert True
def test_empty_rejected():
    try:HRInterviewScoringEngine().normalize_responses([]); assert False
    except ValueError: assert True
def test_report_format():
    r=HRInterviewScoringEngine().score_interview("CAND_001","JOB_001","S","Python Developer",responses())
    x=HRScoreReport().to_dict(r)
    assert x["candidate"]["candidate_id"]=="CAND_001" and "final" in x["score"] and "explainable_breakdown" in x
def test_explanation():
    r=HRInterviewScoringEngine().score_interview("C","J","S","Python Developer",responses())
    assert "Final HR Interview Score" in HRInterviewScoringEngine().explain(r)
