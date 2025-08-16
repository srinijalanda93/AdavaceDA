import sys, os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Add cli folder to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from cli.score_docs import score_one  # make sure this returns dict with consistent keys


# -------------------
# Visualization Utils
# -------------------
def plot_risk_distribution(results):
    """Histogram of risk scores"""
    scores = [r["risk"] for r in results]

    fig, ax = plt.subplots()
    sns.histplot(scores, bins=10, kde=True, ax=ax)
    ax.set_title("Risk Score Distribution")
    ax.set_xlabel("Risk Score")
    ax.set_ylabel("Count")
    st.pyplot(fig)


# def plot_fake_vs_registry(results):
    """Bar chart comparing Fake vs Registry"""
    df = pd.DataFrame(results)

    if "prob_registry" in df.columns:
        fig, ax = plt.subplots()
        df[["prob_fake", "prob_registry"]].mean().plot.bar(
            ax=ax, color=["red", "green"]
        )
        ax.set_title("Average Probability: Fake vs Registry")
        ax.set_ylabel("Probability")
        st.pyplot(fig)
    else:
        st.warning("⚠️ 'prob_registry' not found in results, skipping chart.")
def plot_fake_vs_registry(results):
    import pandas as pd
    import matplotlib.pyplot as plt

    # Normalize results
    df = pd.DataFrame(results)

    # Add prob_registry column based on registry.exists
    df["prob_registry"] = df["registry"].apply(lambda r: 1 if r.get("exists") else 0)

    fig, ax = plt.subplots()
    df[["prob_fake", "prob_registry"]].mean().plot.bar(
        ax=ax, color=["red", "green"]
    )
    ax.set_title("Average Fake Probability vs Registry Match")
    ax.set_ylabel("Probability")
    st.pyplot(fig)


def plot_anomaly_pie(results):
    """Pie chart for anomaly detection"""
    anomaly_count = sum(1 for r in results if r.get("is_anomaly", False))
    normal_count = len(results) - anomaly_count

    fig, ax = plt.subplots()
    ax.pie([anomaly_count, normal_count],
           labels=["Anomaly", "Normal"],
           autopct="%1.1f%%",
           colors=["orange", "lightblue"])
    ax.set_title("Anomaly Detection Results")
    st.pyplot(fig)


# -------------------
# Streamlit App
# -------------------
st.set_page_config(page_title="Fake Certificate Detector", layout="wide")
st.title("📄 Fake Certificate Detection Dashboard")

mode = st.sidebar.radio("Choose Mode", ["Single Document", "Batch Documents"])

# ---- SINGLE MODE ----
if mode == "Single Document":
    uploaded_file = st.file_uploader("Upload a certificate PDF", type=["pdf"])

    if uploaded_file is not None:
        os.makedirs("uploads", exist_ok=True)
        save_path = os.path.join("uploads", uploaded_file.name)

        with open(save_path, "wb") as f:
            f.write(uploaded_file.read())

        st.info("🔍 Analyzing document... please wait")
        result = score_one(save_path)

        # Wrap into list for consistency
        results = [result]

        # Summary Metrics
        st.subheader("Document Risk Overview")
        col1, col2, col3 = st.columns(3)
        col1.metric("Probability Fake", f"{result['prob_fake']:.2f}")
        col2.metric("Risk Score", f"{result['risk']:.2f}")
        col3.metric("Anomaly Flag", result["anomaly_flag"])

        st.divider()

        # Registry Info
        st.subheader("Registry Validation")
        st.dataframe(pd.DataFrame([result["registry"]]), use_container_width=True)

        # Extracted Fields
        st.subheader("Extracted Document Fields")
        st.dataframe(pd.DataFrame([result["fields"]]), use_container_width=True)

        # Raw JSON + Visualizations
        with st.expander("🔎 Raw JSON Result"):
            st.json(result)

        st.subheader("📊 Risk Visualizations")
        plot_risk_distribution(results)
        plot_fake_vs_registry(results)
        plot_anomaly_pie(results)


# ---- BATCH MODE ----
elif mode == "Batch Documents":
    uploaded_files = st.file_uploader(
        "Upload multiple certificates (PDFs)",
        type=["pdf"], accept_multiple_files=True
    )

    if uploaded_files:
        os.makedirs("uploads", exist_ok=True)
        results = []

        for file in uploaded_files:
            save_path = os.path.join("uploads", file.name)
            with open(save_path, "wb") as f:
                f.write(file.read())

            result = score_document(save_path)
            result["filename"] = file.name
            results.append(result)

        # Show batch dataframe
        st.subheader("Batch Results")
        st.dataframe(pd.DataFrame(results))

        # Visualizations
        st.subheader("📊 Batch Visualizations")
        plot_risk_distribution(results)
        plot_fake_vs_registry(results)
        plot_anomaly_pie(results)
