import gradio as gr
from query import ask


def handle_query(question):
    result = ask(question)

    answer = result["answer"]
    sources = "\n".join(f"- {source}" for source in result["sources"])

    return answer, sources


with gr.Blocks() as demo:
    gr.Markdown("# CSU East Bay Professor Reviews RAG System")
    gr.Markdown(
        "Ask a question about the collected CSU East Bay professor and course review documents."
    )

    question = gr.Textbox(
        label="Your question",
        placeholder="Example: What do students say about Professor Christopher Smith’s workload?"
    )

    submit = gr.Button("Ask")

    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved Sources", lines=5)

    submit.click(handle_query, inputs=question, outputs=[answer, sources])
    question.submit(handle_query, inputs=question, outputs=[answer, sources])


demo.launch()