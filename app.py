import os
import streamlit as st
import pandas as pd
import plotly.express as px

# Set Page Config FIRST
st.set_page_config(
    page_title="Smart File Analyzer",
    page_icon="📁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import Utilities
from utils.theme_css import apply_theme
from utils.auth_db import (
    register_user, verify_user, log_file_analysis, get_user_history
)
from utils.file_analyzer import (
    analyze_uploaded_files, detect_duplicates, get_largest_files, convert_size
)
from utils.system_info import get_complete_system_info
from utils.ai_engine import generate_ai_file_insights
from utils.ml_engine import run_ml_anomaly_detection, run_ml_storage_clustering

# Initialize Session State
if "auth_user" not in st.session_state:
    st.session_state["auth_user"] = None
if "nav_page" not in st.session_state:
    st.session_state["nav_page"] = "🏠 Home"
if "theme_mode" not in st.session_state:
    st.session_state["theme_mode"] = "Dark"

# Apply Custom Theme CSS
apply_theme(st.session_state["theme_mode"])

# Main Page Header & Top-Right Theme Selector
head_col1, head_col2 = st.columns([3, 1])

with head_col1:
    st.markdown("""
    <div class="app-header">
        <div class="app-title">📁 Smart File Analyzer</div>
        <div class="app-subtitle">Multi-File Processing • SHA-256 Hashing • AI Insights • Complex ML • System Telemetry</div>
    </div>
    """, unsafe_allow_html=True)

with head_col2:
    st.markdown("<div style='padding-top: 5px;'></div>", unsafe_allow_html=True)
    theme_choice = st.selectbox(
        "🎨 Appearance Theme:",
        ["Dark", "Light", "System"],
        index=["Dark", "Light", "System"].index(st.session_state["theme_mode"])
    )
    if theme_choice != st.session_state["theme_mode"]:
        st.session_state["theme_mode"] = theme_choice
        st.rerun()

# Sidebar Title
st.sidebar.title("📁 Navigation")

# ==============================================================================
# MANDATORY AUTHENTICATION GATEKEEPER
# ==============================================================================
if st.session_state["auth_user"] is None:
    st.sidebar.warning("🔒 Authentication Required")
    st.sidebar.info("Please log in or register on the main panel to unlock the application.")

    st.title("🔐 Authentication Required")
    st.markdown("### You must log in or create an account to access Smart File Analyzer.")
    
    auth_tab1, auth_tab2 = st.tabs(["🔑 Log In", "📝 Register New Account"])

    with auth_tab1:
        st.subheader("Sign In to Your Account")
        l_user = st.text_input("Username:", key="login_username")
        l_pass = st.text_input("Password:", type="password", key="login_password")
        
        if st.button("🔑 Log In", type="primary", use_container_width=True):
            if l_user and l_pass:
                success, res = verify_user(l_user, l_pass)
                if success:
                    st.session_state["auth_user"] = res
                    st.success(f"Welcome back, {res['username']}! Unlocking application...")
                    st.session_state["nav_page"] = "🏠 Home"
                    st.rerun()
                else:
                    st.error(res)
            else:
                st.warning("Please enter both username and password.")

    with auth_tab2:
        st.subheader("Create a New Account")
        r_user = st.text_input("Choose Username:", key="reg_username")
        r_email = st.text_input("Email Address:", key="reg_email")
        r_pass = st.text_input("Choose Password:", type="password", key="reg_password")
        
        if st.button("📝 Register Account", type="primary", use_container_width=True):
            if r_user and r_email and r_pass:
                success, msg = register_user(r_user, r_email, r_pass)
                if success:
                    st.success(msg + " You can now log in.")
                else:
                    st.error(msg)
            else:
                st.warning("Please fill in all registration fields.")

    # Stop execution here if not logged in!
    st.stop()

# ==============================================================================
# AUTHENTICATED USER SESSION (APPLICATION UNLOCKED)
# ==============================================================================
user_name_str = st.session_state["auth_user"]["username"]
st.sidebar.markdown(f'<div class="user-badge">👤 Logged in: {user_name_str}</div>', unsafe_allow_html=True)
if st.sidebar.button("🚪 Logout", use_container_width=True):
    st.session_state["auth_user"] = None
    st.session_state["nav_page"] = "🏠 Home"
    st.rerun()

st.sidebar.markdown("---")

# Sidebar Page Navigation (UNLOCKED AFTER LOGIN)
nav_options = [
    "🏠 Home",
    "📂 File Analyzer",
    "🤖 AI & ML Intelligence Engine",
    "💻 System Information",
    "📜 Database History Log",
    "ℹ️ About"
]

page_selection = st.sidebar.radio(
    "Select Page:",
    nav_options,
    index=nav_options.index(st.session_state["nav_page"]) if st.session_state["nav_page"] in nav_options else 0
)

st.session_state["nav_page"] = page_selection

# ==============================================================================
# PAGE: HOME
# ==============================================================================
if st.session_state["nav_page"] == "🏠 Home":
    st.markdown(f"### Welcome back, **{user_name_str}**! 👋")
    st.markdown("Explore intelligent storage analytics, cryptographic hashing, machine learning clustering, and machine health.")
    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""
        <div class="feature-card">
            <div class="card-icon">📂</div>
            <div class="card-title">File Analyzer</div>
            <div class="card-desc">Process multiple file formats, extract metadata, and run cryptographic SHA-256 duplicate detection.</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="feature-card">
            <div class="card-icon">🤖</div>
            <div class="card-title">AI & ML Engine</div>
            <div class="card-desc">Machine Learning IsolationForest anomaly detection, K-Means clustering, and AI storage recommendations.</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="feature-card">
            <div class="card-icon">💻</div>
            <div class="card-title">System Info</div>
            <div class="card-desc">Inspect real-time CPU, Memory (RAM), Disk partitions, and OS telemetry from the host machine.</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown("""
        <div class="feature-card">
            <div class="card-icon">🗄️</div>
            <div class="card-title">SQL Audit Logs</div>
            <div class="card-desc">Persistent user login authentication and SQLite database file analysis history.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("🚀 Start Analyzing Files Now", type="primary", use_container_width=True):
        st.session_state["nav_page"] = "📂 File Analyzer"
        st.rerun()

# ==============================================================================
# PAGE: FILE ANALYZER
# ==============================================================================
elif st.session_state["nav_page"] == "📂 File Analyzer":
    st.title("📂 Multi-File Analyzer & Hashing Engine")

    c_left, c_right = st.columns([3, 1])
    with c_left:
        uploaded_files = st.file_uploader(
            "Upload files (CSV, Excel, PDF, Images, Code, ZIP, etc.):",
            accept_multiple_files=True,
            key="file_uploader"
        )
    with c_right:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️ Clear Analysis", use_container_width=True):
            st.session_state.pop("file_uploader", None)
            st.session_state.pop("df_analysis", None)
            st.rerun()

    if uploaded_files:
        with st.spinner("Calculating file sizes, categories, and SHA-256 hashes..."):
            df_files = analyze_uploaded_files(uploaded_files)
            st.session_state["df_analysis"] = df_files

            # Automatically log to Database for authenticated user
            log_file_analysis(st.session_state["auth_user"]["username"], df_files)

        if not df_files.empty:
            # Filters
            with st.expander("🔍 Filter Results", expanded=False):
                f1, f2, f3 = st.columns(3)
                with f1:
                    available_types = ["All"] + sorted(df_files["Type"].unique().tolist())
                    selected_type = st.selectbox("Category:", available_types)
                max_size_val = float(df_files["Size (KB)"].max())
                with f2:
                    min_kb = st.number_input("Min Size (KB):", min_value=0.0, max_value=max_size_val, value=0.0)
                with f3:
                    max_kb = st.number_input("Max Size (KB):", min_value=min_kb, max_value=max_size_val if max_size_val > 0 else 1000.0, value=max_size_val if max_size_val > 0 else 1000.0)

            filtered_df = df_files.copy()
            if selected_type != "All":
                filtered_df = filtered_df[filtered_df["Type"] == selected_type]
            filtered_df = filtered_df[(filtered_df["Size (KB)"] >= min_kb) & (filtered_df["Size (KB)"] <= max_kb)]

            # Summary Metrics
            duplicates_df = detect_duplicates(filtered_df)
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Total Files", len(filtered_df))
            m2.metric("Total Storage", convert_size(filtered_df["Size (Bytes)"].sum()))
            m3.metric("File Types", filtered_df["Type"].nunique())
            m4.metric("Duplicate Files", len(duplicates_df) if not duplicates_df.empty else 0)

            st.markdown("---")
            st.subheader("📋 File Metadata Dataframe")
            display_cols = ["File Name", "Extension", "Type", "Size (KB)", "Size (MB)", "SHA-256"]
            st.dataframe(filtered_df[display_cols], use_container_width=True, hide_index=True)

            st.markdown("---")
            st.subheader("🔁 Duplicate Files Detection (SHA-256 Hashing)")
            if not duplicates_df.empty:
                st.warning(f"Identified {len(duplicates_df)} duplicate cluster(s)!")
                st.dataframe(duplicates_df, use_container_width=True, hide_index=True)
            else:
                st.success("No duplicate files found.")

            st.markdown("---")
            st.subheader("📦 Top 10 Largest Files")
            st.dataframe(get_largest_files(filtered_df, top_n=10), use_container_width=True, hide_index=True)

            st.markdown("---")
            st.subheader("📈 Storage Visualizations")
            ch1, ch2 = st.columns(2)
            with ch1:
                tc = filtered_df["Type"].value_counts().reset_index()
                tc.columns = ["File Type", "Count"]
                fig1 = px.bar(tc, x="File Type", y="Count", color="File Type", text_auto=True, title="File Type Distribution", template="plotly_dark")
                st.plotly_chart(fig1, use_container_width=True)
            with ch2:
                stg = filtered_df.groupby("Type")["Size (MB)"].sum().reset_index()
                stg.columns = ["File Type", "Storage (MB)"]
                fig2 = px.bar(stg, x="File Type", y="Storage (MB)", color="File Type", text_auto=".2f", title="Storage by File Type (MB)", template="plotly_dark")
                st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Upload files above to run file metadata analysis.")

# ==============================================================================
# PAGE: AI & ML INTELLIGENCE ENGINE
# ==============================================================================
elif st.session_state["nav_page"] == "🤖 AI & ML Intelligence Engine":
    st.title("🤖 AI Insights & Complex Machine Learning Engine")

    df_current = st.session_state.get("df_analysis", None)
    
    if df_current is not None and not df_current.empty:
        duplicates_df = detect_duplicates(df_current)

        tab_ai, tab_ml_anomaly, tab_ml_cluster = st.tabs([
            "🧠 AI Storage Advisory",
            "🛡️ ML Anomaly Detection (IsolationForest)",
            "📊 ML Storage Clustering (K-Means)"
        ])

        with tab_ai:
            st.subheader("🧠 AI-Powered Smart Insights")
            
            with st.expander("🔑 Optional AI API Settings", expanded=False):
                api_key = st.text_input("Enter OpenAI / Gemini API Key (Optional):", type="password")
                st.caption("If no API key is entered, the app uses built-in AI NLP heuristics.")

            ai_results = generate_ai_file_insights(df_current, duplicates_df, api_key=api_key)

            a1, a2 = st.columns([1, 3])
            with a1:
                st.metric("Storage Health Index", f"{ai_results['health_score']}/100")
                st.caption(f"Status: **{ai_results['status']}**")
            with a2:
                st.markdown(f"""
                <div class="ai-box">
                    <h4>🤖 AI Summary</h4>
                    <p>{ai_results['summary']}</p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("#### 💡 AI Smart Recommendations:")
            for rec in ai_results["recommendations"]:
                st.markdown(f"- {rec}")

        with tab_ml_anomaly:
            st.subheader("🛡️ Machine Learning Anomaly Detection")
            st.markdown("Uses **IsolationForest** unsupervised ML algorithm to flag abnormal file sizes and extension patterns.")
            
            contam = st.slider("Anomaly Sensitivity Threshold:", 0.05, 0.30, 0.10, 0.05)
            df_anomaly, fig_anom = run_ml_anomaly_detection(df_current, contamination=contam)
            
            if fig_anom:
                st.plotly_chart(fig_anom, use_container_width=True)
                st.dataframe(df_anomaly[["File Name", "Type", "Size (MB)", "Is_Anomaly"]], use_container_width=True, hide_index=True)

        with tab_ml_cluster:
            st.subheader("📊 Machine Learning Storage Clustering")
            st.markdown("Uses **K-Means Clustering** algorithm to automatically group uploaded files into smart clusters.")
            
            k_val = st.slider("Number of Clusters (k):", 2, 5, 3)
            df_clustered, fig_cluster = run_ml_storage_clustering(df_current, n_clusters=k_val)
            
            if fig_cluster:
                st.plotly_chart(fig_cluster, use_container_width=True)
                st.dataframe(df_clustered[["File Name", "Type", "Size (MB)", "Cluster_Label"]], use_container_width=True, hide_index=True)
    else:
        st.warning("Please upload files in the '📂 File Analyzer' page first to run AI & ML engines.")

# ==============================================================================
# PAGE: SYSTEM INFORMATION
# ==============================================================================
elif st.session_state["nav_page"] == "💻 System Information":
    st.title("💻 System Information Telemetry")
    if st.button("🔄 Refresh System Information"):
        st.rerun()

    sys_info = get_complete_system_info()
    os_i, cpu_i, mem_i, disk_i = sys_info["os"], sys_info["cpu"], sys_info["memory"], sys_info["disk"]

    p1, p2, p3 = st.columns(3)
    with p1:
        st.write(f"**CPU Usage:** {cpu_i['CPU Usage (%)']}%")
        st.progress(min(cpu_i['CPU Usage (%)'] / 100.0, 1.0))
    with p2:
        st.write(f"**RAM Usage:** {mem_i['RAM Usage (%)']}%")
        st.progress(min(mem_i['RAM Usage (%)'] / 100.0, 1.0))
    with p3:
        st.write(f"**Disk Usage:** {disk_i['Disk Usage (%)']}%")
        st.progress(min(disk_i['Disk Usage (%)'] / 100.0, 1.0))

    st.markdown("---")
    col_os, col_cpu = st.columns(2)
    with col_os:
        st.subheader("🖥️ Operating System")
        st.write(f"**OS:** {os_i['Operating System']} ({os_i['OS Release']})")
        st.write(f"**Architecture:** {os_i['Architecture']}")
        st.write(f"**Processor:** {os_i['Processor']}")
        st.write(f"**Python Version:** {os_i['Python Version']}")
    with col_cpu:
        st.subheader("⚡ CPU Specs")
        st.write(f"**Physical Cores:** {cpu_i['Physical Cores']}")
        st.write(f"**Logical Cores:** {cpu_i['Logical Cores']}")
        st.write(f"**CPU Usage:** {cpu_i['CPU Usage (%)']}%")
        st.write(f"**Frequency:** {cpu_i['CPU Frequency']}")

    st.markdown("---")
    col_mem, col_disk = st.columns(2)
    with col_mem:
        st.subheader("🧠 RAM Memory")
        st.write(f"**Total RAM:** {mem_i['Total RAM (GB)']} GB")
        st.write(f"**Used RAM:** {mem_i['Used RAM (GB)']} GB")
        st.write(f"**Available RAM:** {mem_i['Available RAM (GB)']} GB")
    with col_disk:
        st.subheader("💾 Disk Partition")
        st.write(f"**Mount:** {disk_i['Mountpoint']}")
        st.write(f"**Total Disk:** {disk_i['Total Disk Space (GB)']} GB")
        st.write(f"**Free Disk:** {disk_i['Free Disk Space (GB)']} GB")

# ==============================================================================
# PAGE: DATABASE HISTORY LOG
# ==============================================================================
elif st.session_state["nav_page"] == "📜 Database History Log":
    st.title("📜 SQLite Database File Audit Logs")
    st.markdown(f"Displaying persistent database records for user: **{user_name_str}**")
    
    hist_df = get_user_history(user_name_str)
    if not hist_df.empty:
        st.dataframe(hist_df, use_container_width=True, hide_index=True)
    else:
        st.info("No past file analysis history found in database.")

# ==============================================================================
# PAGE: ABOUT
# ==============================================================================
elif st.session_state["nav_page"] == "ℹ️ About":
    st.title("ℹ️ About Smart File Analyzer")
    st.markdown("""
    ### **Smart File Analyzer (Enterprise Edition)**
    A functional, feature-packed Streamlit application integrating mandatory authentication, file metadata analysis, cryptographic SHA-256 duplicate detection, AI storage insights, complex Machine Learning anomaly detection, user session management, SQLite database logging, and cloud deployment readiness.

    ### **Technologies Included:**
    - **Authentication Gatekeeping**: Mandatory Login / Registration before content access
    - **UI & Themes**: Streamlit, Custom Glassmorphism CSS (Light, Dark, System Modes)
    - **Data & Charts**: Pandas, NumPy, Plotly Express
    - **Database & Auth**: SQLite3, SHA-256 Password Hashing & Audit Logs
    - **AI & ML**: Scikit-Learn (IsolationForest, KMeans), Built-in AI Advisory Engine
    - **System Telemetry**: psutil, platform
    - **Cloud Deployment**: Procfile, .streamlit/config.toml ready for Heroku / Render / Streamlit Cloud
    """)
