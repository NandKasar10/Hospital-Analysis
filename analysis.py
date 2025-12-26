import io
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image

# Use non-interactive backend (important for Hugging Face Spaces)
plt.switch_backend("Agg")

# Required columns for the dataset
REQUIRED_COLUMNS = ["department", "patient_id", "visit_date"]

def load_data(file_obj) -> pd.DataFrame:
    """
    Load and clean hospital data from CSV.
    Accepts file path or file-like object.
    """
    df = pd.read_csv(file_obj)
    # Check required columns
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    # Basic cleaning
    df["department"] = df["department"].astype(str).str.strip()
    df["patient_id"] = df["patient_id"].astype(str).str.strip()
    df["visit_date"] = pd.to_datetime(df["visit_date"], errors="coerce")
    df = df.dropna(subset=["department", "patient_id", "visit_date"])
    return df

def department_counts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Count unique patients per department.
    """
    counts = df.groupby("department")["patient_id"].nunique().reset_index(name="patient_count")
    counts = counts.sort_values("patient_count", ascending=False)
    return counts

def percentage_split(counts_df: pd.DataFrame) -> pd.DataFrame:
    """
    Add percentage column relative to total patients.
    """
    total = counts_df["patient_count"].sum()
    counts_df["percentage"] = (counts_df["patient_count"] / total * 100).round(2)
    return counts_df

def bar_chart(counts_df: pd.DataFrame):
    """
    Generates a bar chart as a PIL Image.
    """
    fig, ax = plt.subplots(figsize=(8, 5), dpi=120)
    sns.barplot(data=counts_df, x="department", y="patient_count", ax=ax, palette="Blues", legend=False)
    ax.set_title("Patient count per department")
    ax.set_xlabel("Department")
    ax.set_ylabel("Patients")
    ax.tick_params(axis="x", rotation=30)
    fig.tight_layout()

    # Save to buffer
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)

    # Convert bytes to PIL image
    img = Image.open(buf)
    return img

def stats_report(df: pd.DataFrame, counts_df: pd.DataFrame) -> str:
    """
    Generate a human-readable stats summary.
    """
    total_patients = df["patient_id"].nunique()
    total_visits = len(df)
    unique_departments = df["department"].nunique()
    top = counts_df.iloc[0] if not counts_df.empty else None

    lines = []
    lines.append(f"Total patients: {total_patients}")
    lines.append(f"Total visits: {total_visits}")
    lines.append(f"Unique departments: {unique_departments}")
    if top is not None:
        lines.append(f"Top department: {top['department']} ({top['patient_count']} patients)")
    # Optional: average length of stay if column exists
    if "length_of_stay_days" in df.columns:
        avg_los = df["length_of_stay_days"].dropna().astype(float).mean()
        lines.append(f"Average length of stay (days): {avg_los:.2f}")
    return "\n".join(lines)

def end_to_end(file_obj):
    """
    Full pipeline: load, aggregate, chart, stats.
    Returns (counts_df, png_bytes, stats_text).
    """
    df = load_data(file_obj)
    counts = department_counts(df)
    counts = percentage_split(counts)
    chart_png = bar_chart(counts)
    stats = stats_report(df, counts)
    return counts, chart_png, stats