import streamlit as st

from streamlit_ui.api import SentimentApiClient
from streamlit_ui.config import AppConfig
from streamlit_ui.state import AppState
from streamlit_ui.views import (
    FooterSection,
    GetAnalysisTab,
    HealthCheckTab,
    PostAnalysisTab,
    ResultView,
)


class StreamlitSentimentApp:
    def __init__(self, config: AppConfig | None = None) -> None:
        self.config = config or AppConfig()

    def run(self) -> None:
        st.set_page_config(
            page_title=self.config.page_title,
            layout=self.config.page_layout,
        )

        state = AppState(st.session_state)
        api_client = SentimentApiClient(
            base_url=self.config.api_url,
            timeout=self.config.request_timeout,
        )
        result_view = ResultView(state=state, config=self.config)

        self._render_header()
        tab_main, tab_get, tab_post = st.tabs(list(self.config.tabs))

        with tab_main:
            HealthCheckTab(
                api_client=api_client,
                state=state,
                result_view=result_view,
            ).render()

        with tab_get:
            GetAnalysisTab(
                api_client=api_client,
                state=state,
                result_view=result_view,
                config=self.config,
            ).render()

        with tab_post:
            PostAnalysisTab(
                api_client=api_client,
                state=state,
                result_view=result_view,
                config=self.config,
            ).render()

        FooterSection(state=state, config=self.config).render()

    def _render_header(self) -> None:
        st.title(self.config.title)
        st.caption(self.config.caption)
        st.text(self.config.language_warning)
