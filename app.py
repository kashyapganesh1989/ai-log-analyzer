import os
import streamlit as st
from dotenv import load_dotenv
from utils.log_reader import read_logs
from utils.ai_helper import analyze_with_ai, parse_ai_report
import pandas as pd
import json

# --------------------- Load environment ---------------------
load_dotenv()

# --------------------- Page setup ---------------------
st.set_page_config(
    page_title="AI Log Analyzer",
    page_icon="🧠",
    layout="wide"
)

# --------------------- Custom CSS ---------------------
st.markdown("""
<style>
body {
    background-color: #f8fafc;
    font-family: 'Segoe UI', Roboto, sans-serif;
}
h1 {
    text-align: center;
    font-size: 2.2rem;
    color: #1e3a8a;
    font-weight: 700;
    margin-bottom: 1rem;
}
.issue-card {
    background-color: #f1f5f9;
    padding: 1rem 1.2rem;
    border-radius: 12px;
    margin-bottom: 1rem;
    border-left: 6px solid #3b82f6;
}
.scrollable-container {
    max-height: 70vh;
    overflow-y: auto;
    padding-right: 10px;
}
footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --------------------- Header ---------------------
st.title("🧠 AI Log Analyzer")
st.markdown("Upload logs or provide a folder path. Each issue shows **Log Snippet**, **Cause**, and **Suggested Resolution**.")

# --------------------- Sidebar ---------------------
st.sidebar.title("Configuration")
input_type = st.sidebar.radio("Input Type:", ["Upload File", "Folder Path"])
keyword_filter = st.sidebar.text_input("🔎 Filter by keyword")

log_text = ""
file_name = "log_report"

# --------------------- Load Logs ---------------------
if input_type == "Upload File":
    uploaded_file = st.sidebar.file_uploader("Upload a log file", type=["log", "txt"])
    if uploaded_file:
        log_text = uploaded_file.read().decode("utf-8")
        file_name = os.path.splitext(uploaded_file.name)[0]
elif input_type == "Folder Path":
    folder_path = st.sidebar.text_input("Enter folder path")
    if folder_path and os.path.isdir(folder_path):
        log_text = read_logs(folder_path)

# --------------------- Analyze Logs ---------------------
analyze_clicked = st.sidebar.button("Analyze Logs", key="analyze_logs_btn")

if analyze_clicked:
    if not log_text:
        st.warning("⚠️ Please upload a file or enter a valid folder path before analyzing.")
    else:
        with st.spinner("🔍 Analyzing logs using AI..."):
            ai_report = analyze_with_ai(log_text)
            issues = parse_ai_report(ai_report)

        # --- Sort by severity ---
        severity_order = {"Critical": 0, "High": 1, "Error": 2, "Warning": 3, "Medium": 4, "Low": 5, "Info": 6}
        issues.sort(key=lambda x: severity_order.get(x.get("Severity", "Info"), 99))

        # --- Keyword filter ---
        if keyword_filter:
            issues = [i for i in issues if keyword_filter.lower() in str(i).lower()]

        # --- Display Issues ---
        if not issues:
            st.warning("No issues detected in logs.")
        else:
            st.subheader("📋 Detected Issues")
            st.markdown("<div class='scrollable-container'>", unsafe_allow_html=True)

            for idx, issue in enumerate(issues, 1):
                severity = issue.get("Severity", "Info")#.capitalize()
                color = {
                    "Critical": "#dc2626",
                    "Error": "#ef4444",
                    "Warning": "#f59e0b",
                    "Info": "#3b82f6"
                }.get(severity, "#3b82f6")

                with st.expander(f"{idx}. {severity} - {issue.get('Issue','')}"):
                    st.markdown(f"""
                    <div class="issue-card" style="border-left-color:{color}">
                        <p><strong>Log Snippet:</strong> {issue.get('Issue','Not available')}</p>
                        <p><strong>Cause:</strong> {issue.get('Cause','Not available')}</p>
                        <p><strong>Suggested Resolution:</strong> {issue.get('Resolution','Not available')}</p>
                        <p><strong>Severity:</strong> {severity}</p>

                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

            # --- Export Options ---
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    "📥 Export as CSV",
                    pd.DataFrame(issues).to_csv(index=False).encode('utf-8'),
                    file_name=f"{file_name}_ai_report.csv",
                    mime="text/csv",
                    key="export_csv"
                )
            with col2:
                st.download_button(
                    "📥 Export as JSON",
                    json.dumps(issues, indent=2).encode('utf-8'),
                    file_name=f"{file_name}_ai_report.json",
                    mime="application/json",
                    key="export_json"
                )
