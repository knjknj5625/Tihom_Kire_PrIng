import json
import requests
import streamlit as st


st.set_page_config(page_title="FastAPI UI", layout="wide")

API_URL = "http://127.0.0.1:8000"

if "history" not in st.session_state:
    st.session_state.history = []

st.title("Приложение FastAPI + Streamlit для анализа тональности")
st.caption("СКАЧАТЬ ВЕСЬ ИНТЕРНЕТ.")
st.text("Внимание! Для API поддерживается только английский язык!!")

tab1, tab2, tab3 = st.tabs(["Главная", "GET /{text}", "POST /predict/"])

with tab1:
    st.subheader("Health Check")
    if st.button("Хелс-чек API"):
        try:
            r = requests.get(API_URL + "/", timeout=30)
            st.write("Статус:", r.status_code)
            try:
                data = r.json()
                st.json(data)
                st.session_state.history.append(
                    {"type": "root", "status": r.status_code, "data": data}
                )
            except Exception:
                st.text(r.text)
                st.session_state.history.append(
                    {"type": "root", "status": r.status_code, "data": r.text}
                )
        except Exception as e:
            st.error("Ошибка запроса: " + str(e))

    st.write("История запросов")
    for x in st.session_state.history[::-1]:
        st.write(x)

with tab2:
    st.subheader("Анализ через GET")
    text_for_get = st.text_input("Текст для семантического анализа", "DOWNLOAD ALL FILES") # POSITIVE SCORE 0.993 CONFIRMED
    if st.button("Отправить GET"):
        if text_for_get.strip() == "":
            st.warning("Нужен текст")
        else:
            try:
                r = requests.get(API_URL + "/" + text_for_get, timeout=30)
                st.write("Статус:", r.status_code)
                try:
                    data = r.json()
                    st.json(data)
                    st.session_state.history.append(
                        {"type": "get", "text": text_for_get, "status": r.status_code, "data": data}
                    )
                except Exception:
                    st.text(r.text)
                    st.session_state.history.append(
                        {"type": "get", "text": text_for_get, "status": r.status_code, "data": r.text}
                    )
            except Exception as e:
                st.error("Ошибка GET: " + str(e))

with tab3:
    st.subheader("Анализ через POST")
    text_for_post = st.text_area("Текст для семантического анализа", "SKACHYAT INTERNET")
    if st.button("Отправить POST"):
        if text_for_post.strip() == "":
            st.warning("Нужен текст")
        else:
            body = {"text": text_for_post}
            st.code(json.dumps(body, ensure_ascii=False, indent=2), language="json")
            try:
                r = requests.post(API_URL + "/predict/", json=body, timeout=30)
                st.write("Статус:", r.status_code)
                try:
                    data = r.json()
                    st.json(data)
                    st.session_state.history.append(
                        {"type": "post", "text": text_for_post, "status": r.status_code, "data": data}
                    )
                except Exception:
                    st.text(r.text)
                    st.session_state.history.append(
                        {"type": "post", "text": text_for_post, "status": r.status_code, "data": r.text}
                    )
            except Exception as e:
                st.error("Ошибка POST: " + str(e))

st.divider()
st.write("Футер")
if st.button("Очистить историю"):
    st.session_state.history = []
    st.success("История очищена")
