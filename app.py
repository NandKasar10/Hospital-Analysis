import gradio as gr
import pandas as pd
from analysis import end_to_end

def analyze_csv(file):
    if file is None:
        return None, None, "Please upload a CSV file."
    try:
        # Pass the file object directly to analysis
        counts_df, chart_png, stats_text = end_to_end(file)
        # Convert DataFrame to HTML for display
        counts_html = counts_df.to_html(index=False)
        return counts_html, chart_png, stats_text
    except Exception as e:
        return None, None, f"Error: {str(e)}"

with gr.Blocks(title="Hospital Department Load Analysis") as demo:
    gr.Markdown("# 🏥 Hospital Department Load Analysis")
    gr.Markdown(
        "Upload a CSV with columns: **department, patient_id, visit_date**. "
        "Optional: gender, age, length_of_stay_days."
    )

    with gr.Row():
        file_input = gr.File(label="Upload CSV", file_types=[".csv"])

    with gr.Row():
        table_out = gr.HTML(label="Counts table")
        image_out = gr.Image(label="Bar chart", type="pil")  # ✅ fixed
        stats_out = gr.Textbox(label="Stats report", lines=8)

    analyze_btn = gr.Button("Analyze")

    analyze_btn.click(
        analyze_csv,
        inputs=[file_input],
        outputs=[table_out, image_out, stats_out]
    )

if __name__ == "__main__":
    demo.launch()