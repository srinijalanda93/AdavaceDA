# # app.py
# import streamlit as st
# import pandas as pd
# from cli.score_docs import score_document

# st.set_page_config(page_title="Doc Authenticity Checker", layout="wide")

# st.title("📄 Document Authenticity & Risk Analyzer")

# uploaded_files = st.file_uploader("Upload one or more PDFs", type=["pdf"], accept_multiple_files=True)

# if uploaded_files:
#     results = []
#     for uploaded_file in uploaded_files:
#         with open(f"temp_{uploaded_file.name}", "wb") as f:
#             f.write(uploaded_file.getbuffer())
#         res = score_document(f.name)
#         results.append(res)

#     df = pd.DataFrame(results)

#     st.subheader("📊 Scoring Results")
#     st.dataframe(df[["path", "prob_fake", "risk", "date"]])

#     st.subheader("📈 Risk Distribution")
#     st.bar_chart(df["risk"])

#     st.subheader("⚠️ High Risk Docs")
#     st.write(df[df["risk"] > 0.7][["path", "risk"]])
# else:
#     st.info("Please upload PDFs to analyze.")


# import os
# import glob
# import pandas as pd
# import streamlit as st
# import matplotlib.pyplot as plt

# # import your existing scoring lo
# from cli.score_docs import score_one
#   # make sure score_document(path) returns dict

# st.set_page_config(page_title="Document Risk Analyzer", layout="wide")

# st.title("📑 Document Risk Analyzer")
# st.write("Upload PDFs or analyze a folder of documents to detect anomalies and risks.")

# # --- Helper for batch scoring ---
# def score_folder(folder_path):
#     results = []
#     pdf_files = glob.glob(os.path.join(folder_path, "*.pdf"))
#     for pdf in pdf_files:
#         try:
#             result = (pdf)
#             result["filename"] = os.path.basename(pdf)
#             results.append(result)
#         except Exception as e:
#             st.error(f"Failed on {pdf}: {e}")
#     return results

# # --- Sidebar for navigation ---
# mode = st.sidebar.radio("Choose Mode", ["Single Document", "Batch Analysis"])

# # --- SINGLE DOCUMENT MODE ---
# if mode == "Single Document":
#     uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
#     if uploaded_file:
#         # save temp file
#         temp_path = os.path.join("temp_uploaded.pdf")
#         with open(temp_path, "wb") as f:
#             f.write(uploaded_file.read())

#         result = score_document(temp_path)

#         st.subheader("🔎 Document Analysis Result")
#         st.json(result)

#         st.metric("Risk Score", round(result.get("risk", 0), 3))
#         st.metric("Probability Fake", round(result.get("prob_fake", 0), 3))
#         st.metric("Anomaly Flag", result.get("anomaly_flag", 0))

# # --- BATCH MODE ---
# elif mode == "Batch Analysis":
#     folder_path = st.text_input("Enter folder path containing PDFs", "data/ecommerce_custom/")

#     if st.button("Run Batch Analysis"):
#         if not os.path.isdir(folder_path):
#             st.error("Invalid folder path")
#         else:
#             results = score_folder(folder_path)
#             if len(results) == 0:
#                 st.warning("No PDFs found in folder")
#             else:
#                 df = pd.DataFrame(results)
#                 st.success(f"Analyzed {len(df)} documents")

#                 # --- Show Data Table ---
#                 st.subheader("📊 Results Table")
#                 st.dataframe(df)

#                 # --- Summary Stats ---
#                 st.subheader("📈 Summary Analytics")

#                 col1, col2, col3 = st.columns(3)
#                 with col1:
#                     st.metric("Avg Risk", round(df["risk"].mean(), 3))
#                 with col2:
#                     st.metric("Avg Prob Fake", round(df["prob_fake"].mean(), 3))
#                 with col3:
#                     st.metric("Anomalies Detected", df["anomaly_flag"].sum())

#                 # --- Chart 1: Risk Distribution ---
#                 st.subheader("Risk Distribution")
#                 fig, ax = plt.subplots()
#                 ax.hist(df["risk"], bins=10, edgecolor="black")
#                 ax.set_xlabel("Risk Score")
#                 ax.set_ylabel("Count")
#                 st.pyplot(fig)

#                 # --- Chart 2: Anomaly Flags Pie ---
#                 st.subheader("Anomaly Breakdown")
#                 fig2, ax2 = plt.subplots()
#                 anomaly_counts = df["anomaly_flag"].value_counts()
#                 ax2.pie(anomaly_counts, labels=anomaly_counts.index, autopct="%1.1f%%")
#                 st.pyplot(fig2)

#                 # --- Download CSV ---
#                 csv = df.to_csv(index=False).encode("utf-8")
#                 st.download_button(
#                     "Download Results as CSV",
#                     data=csv,
#                     file_name="doc_risk_analysis.csv",
#                     mime="text/csv",
#                 )

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# import os
# import glob
# import pandas as pd
# import streamlit as st
# import matplotlib.pyplot as plt
# import seaborn as sns

# import streamlit as st
# import pandas as pd
# # from cli.score_docs import score_one  # ✅ use correct function from your cli folder
# from cli.score_docs import score_one

# -------------------
# Visualization Utils
# -------------------
# 

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys, os

# # Ensure cli folder is in path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from cli.score_docs import score_one  # ✅ assumes it returns dict


# ------------------------
# Visualization Functions
# ------------------------
def plot_fake_vs_registry(result):
    df = pd.DataFrame([{
        "Probability Fake": result["prob_fake"],
        "Probability Registry": result["prob_registry"],
    }])

    fig, ax = plt.subplots(figsize=(5, 3))
    df.mean().plot.bar(ax=ax, color=["red", "green"], alpha=0.7)
    ax.set_title("Fake vs Registry Probability")
    ax.set_ylabel("Probability")
    st.pyplot(fig)


def plot_risk_distribution(results):
    df = pd.DataFrame(results)
    fig, ax = plt.subplots(figsize=(5, 3))
    sns.histplot(df["risk"], bins=5, kde=True, ax=ax)
    ax.set_title("Risk Score Distribution")
    ax.set_xlabel("Risk Score")
    st.pyplot(fig)


def plot_anomaly_count(results):
    df = pd.DataFrame(results)
    fig, ax = plt.subplots(figsize=(5, 3))
    sns.countplot(x="anomaly_flag", data=df, ax=ax, palette="Set2")
    ax.set_title("Anomaly Flag Counts")
    st.pyplot(fig)


# ------------------------
# Streamlit UI
# ------------------------
st.set_page_config(page_title="Document Risk Analyzer", layout="wide")
st.title("📄 Document Risk Analyzer")

uploaded_file = st.file_uploader("Upload a document (PDF, TXT, etc.)", type=["pdf", "txt", "docx"])

if uploaded_file:
    # Save temporarily
    temp_path = os.path.join("temp", uploaded_file.name)
    os.makedirs("temp", exist_ok=True)
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.read())

    # Run scoring
    result = score_one(temp_path)

    # ------------------------
    # Summary Metrics
    # ------------------------
    st.subheader("🔎 Document Risk Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Probability Fake", f"{result['prob_fake']:.2f}")
    col2.metric("Risk Score", f"{result['risk']:.2f}")
    col3.metric("Anomaly Flag", result["anomaly_flag"])
    st.divider()

    # ------------------------
    # Registry Info
    # ------------------------
    st.subheader("📑 Registry Validation")
    reg_df = pd.DataFrame([result["registry"]])
    st.dataframe(reg_df, use_container_width=True)

    # ------------------------
    # Extracted Fields
    # ------------------------
    st.subheader("📌 Extracted Document Fields")
    fields_df = pd.DataFrame([result["fields"]])
    st.dataframe(fields_df, use_container_width=True)
    st.divider()

    # ------------------------
    # Visualizations
    # ------------------------
    st.subheader("📊 Visual Analytics")

    # Wrap single result as list for consistency
    results = [result]

    col1, col2 = st.columns(2)
    with col1:
        plot_fake_vs_registry(result)
    with col2:
        plot_risk_distribution(results)

    st.divider()
    plot_anomaly_count(results)

    st.success("✅ Analysis complete!")
