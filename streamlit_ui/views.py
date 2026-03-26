import json

import requests
import streamlit as st

from streamlit_ui.api import SentimentApiClient
from streamlit_ui.config import AppConfig
from streamlit_ui.models import ApiResult
from streamlit_ui.state import AppState


class ResultView:
    def __init__(self, state: AppState, config: AppConfig) -> None:
        self.state = state
        self.config = config

    def render_last_result(self, source: str) -> None:
        result = self.state.last_result
        if not result or result.source != source:
            return

        st.write("Статус:", result.status)
        if result.is_json:
            st.json(result.data)
        else:
            st.text(result.data)

    def render_history(self) -> None:
        st.write(self.config.history_title)
        if not self.state.history:
            st.caption(self.config.empty_history_text)
            return

        for index, item in enumerate(reversed(self.state.history), start=1):
            with st.expander(f"Запрос {index}", expanded=index == 1):
                st.json(item, expanded=True)


class BaseTab:
    def __init__(
        self,
        api_client: SentimentApiClient,
        state: AppState,
        result_view: ResultView,
    ) -> None:
        self.api_client = api_client
        self.state = state
        self.result_view = result_view

    def _save_result_and_rerun(self, result: ApiResult) -> None:
        self.state.save_result(result)
        st.rerun()


class HealthCheckTab(BaseTab):
    def render(self) -> None:
        st.subheader("Health Check")
        if st.button("Хелс-чек API", key="health_check"):
            try:
                result = self.api_client.get_health()
                self._save_result_and_rerun(result)
            except requests.RequestException as error:
                st.error(f"Ошибка запроса: {error}")

        self.result_view.render_last_result("root")
        self.result_view.render_history()


class GetAnalysisTab(BaseTab):
    def __init__(
        self,
        api_client: SentimentApiClient,
        state: AppState,
        result_view: ResultView,
        config: AppConfig,
    ) -> None:
        super().__init__(api_client=api_client, state=state, result_view=result_view)
        self.config = config

    def render(self) -> None:
        st.subheader("Анализ через GET")
        text = st.text_input(
            "Текст для семантического анализа",
            self.config.default_get_text,
        )

        if st.button("Отправить GET", key="submit_get"):
            if not text.strip():
                st.warning("Нужен текст")
            else:
                try:
                    result = self.api_client.analyze_get(text)
                    self._save_result_and_rerun(result)
                except requests.RequestException as error:
                    st.error(f"Ошибка GET: {error}")

        self.result_view.render_last_result("get")


class PostAnalysisTab(BaseTab):
    def __init__(
        self,
        api_client: SentimentApiClient,
        state: AppState,
        result_view: ResultView,
        config: AppConfig,
    ) -> None:
        super().__init__(api_client=api_client, state=state, result_view=result_view)
        self.config = config

    def render(self) -> None:
        st.subheader("Анализ через POST")
        text = st.text_area(
            "Текст для семантического анализа",
            self.config.default_post_text,
        )
        body = {"text": text}
        st.code(json.dumps(body, ensure_ascii=False, indent=2), language="json")

        if st.button("Отправить POST", key="submit_post"):
            if not text.strip():
                st.warning("Нужен текст")
            else:
                try:
                    result, _ = self.api_client.analyze_post(text)
                    self._save_result_and_rerun(result)
                except requests.RequestException as error:
                    st.error(f"Ошибка POST: {error}")

        self.result_view.render_last_result("post")


class FooterSection:
    def __init__(self, state: AppState, config: AppConfig) -> None:
        self.state = state
        self.config = config

    def render(self) -> None:
        st.divider()
        st.write(self.config.footer_title)
        if st.button("Очистить историю", key="clear_history"):
            self.state.clear()
            st.rerun()
