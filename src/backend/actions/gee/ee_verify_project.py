import ee
from typing import TypedDict
from backend.contracts.action import Action
from backend.shared.result import Result

class VerifyProjectPayload(TypedDict):
    project_id: str

class EEVerifyProject(Action[VerifyProjectPayload ,None]):

    def invoke(self, payload: VerifyProjectPayload) -> Result[None]:
        project_id = (payload.get("project_id") or "").strip()

        if not project_id:
            return Result.fail("Missing project_id")

        try:
            ee.Initialize(project=project_id)
            ee.String("Connection successful").getInfo()
            return Result.success()
        except Exception as e:
            return Result.fail(str(e))
