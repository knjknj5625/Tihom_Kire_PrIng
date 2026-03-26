from typing import Any

from streamlit_ui.models import ApiResult


class AppState:
    HISTORY_KEY = "history"
    LAST_RESULT_KEY = "last_result"

    def __init__(self, session_state: Any) -> None:
        self.session_state = session_state
        self._ensure_defaults()

    def _ensure_defaults(self) -> None:
        self.session_state.setdefault(self.HISTORY_KEY, [])
        self.session_state.setdefault(self.LAST_RESULT_KEY, None)

    @property
    def history(self) -> list[dict[str, Any]]:
        return self.session_state[self.HISTORY_KEY]

    @property
    def last_result(self) -> ApiResult | None:
        return self.session_state[self.LAST_RESULT_KEY]

    def save_result(self, result: ApiResult) -> None:
        self.history.append(result.to_history_item())
        self.session_state[self.LAST_RESULT_KEY] = result

    def clear(self) -> None:
        self.session_state[self.HISTORY_KEY] = []
        self.session_state[self.LAST_RESULT_KEY] = None
