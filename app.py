import gradio as gr
from analysis import end_to_end

def analyze_csv(file):
    if file is None:
        return None, None, "Please upload a CSV file or use the sample dataset."
    try:
        counts_df, chart_img, stats_text = end_to_end(file)
        counts_html = counts_df.to_html(index=False)
        return counts_html, chart_img, stats_text
    except Exception as e:
        return None, None, f"Error: {str(e)}"

def analyze_sample():
    # Always available sample dataset
    with open("sample_data.csv", "r") as f:
        counts_df, chart_img, stats_text = end_to_end(f)
        counts_html = counts_df.to_html(index=False)
        return counts_html, chart_img, stats_text

with gr.Blocks(title="Hospital Department Load Analysis") as demo:
    gr.Markdown("# 🏥 Hospital Department Load Analysis")
    gr.Markdown("Upload a CSV or click **Use Sample Data** to try the app instantly.")

    with gr.Row():
        file_input = gr.File(label="Upload CSV", file_types=[".csv"])
        sample_btn = gr.Button("Use Sample Data")

    with gr.Row():
        table_out = gr.HTML(label="Counts table")
        image_out = gr.Image(label="Bar chart", type="pil")
        stats_out = gr.Textbox(label="Stats report", lines=8)

    analyze_btn = gr.Button("Analyze Uploaded File")
    analyze_btn.click(analyze_csv, inputs=[file_input], outputs=[table_out, image_out, stats_out])
    sample_btn.click(analyze_sample, outputs=[table_out, image_out, stats_out])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)