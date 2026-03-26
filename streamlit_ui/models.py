from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class ApiResult:
    source: str
    status: int
    data: Any
    is_json: bool
    text: str | None = None

    def to_history_item(self) -> dict[str, Any]:
        item: dict[str, Any] = {
            "type": self.source,
            "status": self.status,
            "data": self.data,
        }
        if self.text is not None:
            item["text"] = self.text
        return item
