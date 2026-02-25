# ui_streamlit.py
import streamlit as st
import pandas as pd

from core.answer import answer_question

st.set_page_config(page_title="Text-to-SQL RAG", layout="wide")
st.title("Text-to-SQL (RAG + Bedrock)")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        if m["role"] == "assistant" and "df" in m:
            st.dataframe(m["df"], use_container_width=True)
            st.caption("Generated SQL")
            st.code(m["sql"], language="sql")
        else:
            st.write(m["content"])

q = st.chat_input("질문을 입력하세요")
if q:
    st.session_state.messages.append({"role": "user", "content": q})
    with st.chat_message("user"):
        st.write(q)

    with st.chat_message("assistant"):
        with st.spinner("생성 중..."):
            result = answer_question(q, top_k=5)

            df = pd.DataFrame(result["rows"], columns=result["columns"])
            st.dataframe(df, use_container_width=True)
            st.caption("Generated SQL")
            st.code(result["sql"], language="sql")

    st.session_state.messages.append({
        "role": "assistant",
        "content": "결과를 출력했습니다.",
        "df": df,
        "sql": result["sql"],
    })