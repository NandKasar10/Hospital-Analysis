import io
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image

plt.switch_backend("Agg")

REQUIRED_COLUMNS = ["department", "patient_id", "visit_date"]

def load_data(file_obj) -> pd.DataFrame:
    df = pd.read_csv(file_obj)
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    df["department"] = df["department"].astype(str).str.strip()
    df["patient_id"] = df["patient_id"].astype(str).str.strip()
    df["visit_date"] = pd.to_datetime(df["visit_date"], errors="coerce")
    df = df.dropna(subset=["department", "patient_id", "visit_date"])
    return df

def department_counts(df: pd.DataFrame) -> pd.DataFrame:
    counts = df.groupby("department")["patient_id"].nunique().reset_index(name="patient_count")
    return counts.sort_values("patient_count", ascending=False)

def percentage_split(counts_df: pd.DataFrame) -> pd.DataFrame:
    total = counts_df["patient_count"].sum()
    counts_df["percentage"] = (counts_df["patient_count"] / total * 100).round(2)
    return counts_df

def bar_chart(counts_df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(8, 5), dpi=120)
    sns.barplot(data=counts_df, x="department", y="patient_count", ax=ax,
                palette="Blues", hue=None, legend=False)
    ax.set_title("Patient count per department")
    ax.set_xlabel("Department")
    ax.set_ylabel("Patients")
    ax.tick_params(axis="x", rotation=30)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf)

def stats_report(df: pd.DataFrame, counts_df: pd.DataFrame) -> str:
    total_patients = df["patient_id"].nunique()
    total_visits = len(df)
    unique_departments = df["department"].nunique()
    top = counts_df.iloc[0] if not counts_df.empty else None
    lines = [
        f"Total patients: {total_patients}",
        f"Total visits: {total_visits}",
        f"Unique departments: {unique_departments}"
    ]
    if top is not None:
        lines.append(f"Top department: {top['department']} ({top['patient_count']} patients)")
    if "length_of_stay_days" in df.columns:
        avg_los = df["length_of_stay_days"].dropna().astype(float).mean()
        lines.append(f"Average length of stay (days): {avg_los:.2f}")
    return "\n".join(lines)

def end_to_end(file_obj):
    df = load_data(file_obj)
    counts = department_counts(df)
    counts = percentage_split(counts)
    chart_img = bar_chart(counts)
    stats = stats_report(df, counts)
    return counts, chart_img, stats