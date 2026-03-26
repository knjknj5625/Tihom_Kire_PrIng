from urllib.parse import quote

import requests

from streamlit_ui.models import ApiResult


class SentimentApiClient:
    def __init__(
        self,
        base_url: str,
        timeout: int = 30,
        session: requests.Session | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = session or requests.Session()

    def get_health(self) -> ApiResult:
        response = self.session.get(f"{self.base_url}/", timeout=self.timeout)
        return self._build_result(source="root", response=response)

    def analyze_get(self, text: str) -> ApiResult:
        encoded_text = quote(text, safe="")
        response = self.session.get(
            f"{self.base_url}/{encoded_text}",
            timeout=self.timeout,
        )
        return self._build_result(source="get", response=response, text=text)

    def analyze_post(self, text: str) -> tuple[ApiResult, dict[str, str]]:
        body = {"text": text}
        response = self.session.post(
            f"{self.base_url}/predict/",
            json=body,
            timeout=self.timeout,
        )
        return self._build_result(source="post", response=response, text=text), body

    @staticmethod
    def _build_result(
        source: str,
        response: requests.Response,
        text: str | None = None,
    ) -> ApiResult:
        try:
            data = response.json()
            is_json = True
        except ValueError:
            data = response.text
            is_json = False

        return ApiResult(
            source=source,
            status=response.status_code,
            data=data,
            is_json=is_json,
            text=text,
        )
