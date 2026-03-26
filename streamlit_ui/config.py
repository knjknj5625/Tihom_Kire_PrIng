from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AppConfig:
    api_url: str = "http://127.0.0.1:8000"
    request_timeout: int = 30
    page_title: str = "FastAPI UI"
    page_layout: str = "wide"
    title: str = "Приложение FastAPI + Streamlit для анализа тональности"
    caption: str = "Интерфейс для ручной проверки API."
    language_warning: str = "В API поддерживается только английский текст."
    tabs: tuple[str, str, str] = ("Главная", "GET /{text}", "POST /predict/")
    history_title: str = "История запросов"
    empty_history_text: str = "История пуста"
    footer_title: str = "Сервисные действия"
    default_get_text: str = "DOWNLOAD ALL FILES"
    default_post_text: str = "SKACHYAT INTERNET"
