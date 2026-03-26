import json

import requests
import streamlit as st


st.set_page_config(page_title="FastAPI UI", layout="wide")

API_URL = "http://127.0.0.1:8000"

if "history" not in st.session_state:
    st.session_state.history = []

if "last_result" not in st.session_state:
    st.session_state.last_result = None


def save_result(source, response, text=None):
    try:
        data = response.json()
        is_json = True
    except Exception:
        data = response.text
        is_json = False

    history_item = {
        "type": source,
        "status": response.status_code,
        "data": data,
    }
    if text is not None:
        history_item["text"] = text

    st.session_state.history.append(history_item)
    st.session_state.last_result = {
        "source": source,
        "status": response.status_code,
        "data": data,
        "is_json": is_json,
    }
    st.rerun()


def render_last_result(source):
    result = st.session_state.last_result
    if not result or result["source"] != source:
        return

    st.write("Статус:", result["status"])
    if result["is_json"]:
        st.json(result["data"])
    else:
        st.text(result["data"])


def render_history():
    st.write("История запросов")
    if not st.session_state.history:
        st.caption("История пуста")
        return
    for index, item in enumerate(reversed(st.session_state.history), start=1):
        with st.expander(f"Запрос {index}", expanded=index == 1):
            st.json(item, expanded=True)


st.title("Приложение FastAPI + Streamlit для анализа тональности")
st.caption("СКАЧАТЬ ВЕСЬ ИНТЕРНЕТ.")
st.text("Внимание! Для API поддерживается только английский язык!!")

tab1, tab2, tab3 = st.tabs(["Главная", "GET /{text}", "POST /predict/"])

with tab1:
    st.subheader("Health Check")
    if st.button("Хелс-чек API"):
        try:
            response = requests.get(API_URL + "/", timeout=30)
            save_result("root", response)
        except Exception as error:
            st.error("Ошибка запроса: " + str(error))

    render_last_result("root")
    render_history()

with tab2:
    st.subheader("Анализ через GET")
    text_for_get = st.text_input(
        "Текст для семантического анализа",
        "DOWNLOAD ALL FILES",
    )
    if st.button("Отправить GET"):
        if text_for_get.strip() == "":
            st.warning("Нужен текст")
        else:
            try:
                response = requests.get(API_URL + "/" + text_for_get, timeout=30)
                save_result("get", response, text_for_get)
            except Exception as error:
                st.error("Ошибка GET: " + str(error))

    render_last_result("get")

with tab3:
    st.subheader("Анализ через POST")
    text_for_post = st.text_area(
        "Текст для семантического анализа",
        "SKACHYAT INTERNET",
    )
    if st.button("Отправить POST"):
        if text_for_post.strip() == "":
            st.warning("Нужен текст")
        else:
            body = {"text": text_for_post}
            st.code(json.dumps(body, ensure_ascii=False, indent=2), language="json")
            try:
                response = requests.post(API_URL + "/predict/", json=body, timeout=30)
                save_result("post", response, text_for_post)
            except Exception as error:
                st.error("Ошибка POST: " + str(error))

    render_last_result("post")

st.divider()
st.write("Футер")
if st.button("Очистить историю"):
    st.session_state.history = []
    st.session_state.last_result = None
    st.rerun()
