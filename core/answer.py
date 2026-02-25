# core/answer.py
from rag.retriever import retrieve
from llm.text_to_sql import generate_sql_with_claude
from db.run_sql import run_sql

def format_context(items):
    return "\n\n".join(
        f"[{it['table']} | score={it['score']:.4f}]\n{it['text']}"
        for it in items
    )

def answer_question(question: str, top_k: int = 5):
    hits = retrieve(question, top_k=top_k)
    context = format_context(hits)

    sql = generate_sql_with_claude(question, context)
    rows, columns = run_sql(sql)

    return {
        "question": question,
        "sql": sql,
        "columns": columns,
        "rows": rows,
        "retrieved": hits,
    }