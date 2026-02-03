import ee
from backend.contracts.action import Action
from backend.shared.result import Result
from typing import TypedDict

class AuthenticatePayload(TypedDict, total=False):
    force: bool

class EEAuthentication(Action[AuthenticatePayload, None]):

    def invoke(self, payload: AuthenticatePayload) -> Result[None]:
        try:
            force = bool(payload.get("force", False))
            ee.Authenticate(force=force)
            return Result.success()
        except Exception as e:
            return Result.fail(str(e))
