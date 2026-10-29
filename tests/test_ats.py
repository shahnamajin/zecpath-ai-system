from pipeline.pipeline_manager import PipelineManager
from ats_engine.ats_scorer import ATSScorer
from storage.json_storage import JSONStorage

pipeline = PipelineManager()
ats = ATSScorer()
storage = JSONStorage()

candidate = pipeline.process_resume(
    "data/resumes/Shahna_Majin_Resume .pdf"
)

report = ats.score(
    candidate,
    "data/job_descriptions/backend_developer.json"
)

storage.save(
    report,
    "data/ats_scores",
    f"{candidate['candidate_id']}.json"
)

print(report)