from pipeline.pipeline_manager import PipelineManager
from storage.json_storage import JSONStorage

pipeline = PipelineManager()

storage = JSONStorage()

candidate = pipeline.process_resume(
    "data/resumes/Shahna_Majin_Resume .pdf"
)

storage.save(
    

    candidate,

    "data/parsed_resumes",

    candidate["candidate_id"] + ".json"

)

print(candidate)