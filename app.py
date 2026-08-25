import streamlit as st
import pandas as pd
import plotly.express as px
from utils.file_analyzer import (
    analyze_uploaded_files, detect_duplicates, get_largest_files, convert_size
)
from utils.system_info import get_complete_system_info

# Page Configuration
st.set_page_config(
    page_title="Smart File Analyzer",
    page_icon="📁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State for Navigation
if "nav_page" not in st.session_state:
    st.session_state["nav_page"] = "🏠 Home"

# Sidebar Navigation
st.sidebar.title("📁 Navigation")
page_selection = st.sidebar.radio(
    "Select Page:",
    ["🏠 Home", "📂 File Analyzer", "💻 System Information", "ℹ️ About"],
    index=["🏠 Home", "📂 File Analyzer", "💻 System Information", "ℹ️ About"].index(st.session_state["nav_page"])
)

st.session_state["nav_page"] = page_selection

# ==============================================================================
# PAGE 1: HOME
# ==============================================================================
if st.session_state["nav_page"] == "🏠 Home":
    st.title("📁 Smart File Analyzer")
    st.markdown("### *Analyze your files, discover storage insights, and identify duplicate or large files.*")
    st.markdown("---")

    # Three Main Feature Cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background-color: #1e293b; padding: 20px; border-radius: 10px; border: 1px solid #334155;">
            <h4>📊 Analyze Files</h4>
            <p>Upload multiple files to automatically extract sizes, extensions, categories, and visual insights.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div style="background-color: #1e293b; padding: 20px; border-radius: 10px; border: 1px solid #334155;">
            <h4>🔁 Find Duplicates</h4>
            <p>Cryptographically detect exact duplicate files across your uploads using SHA-256 hashing.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div style="background-color: #1e293b; padding: 20px; border-radius: 10px; border: 1px solid #334155;">
            <h4>💻 System Information</h4>
            <p>Inspect real-time CPU, RAM, and Disk metrics of the machine hosting Streamlit.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("⚡ How It Works")
    st.info("📌 **Workflow:** Upload Files ➔ Process Metadata ➔ Analyze Storage & Hashes ➔ Visualize Insights")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 Launch File Analyzer", type="primary", use_container_width=True):
        st.session_state["nav_page"] = "📂 File Analyzer"
        st.rerun()

# ==============================================================================
# PAGE 2: FILE ANALYZER
# ==============================================================================
elif st.session_state["nav_page"] == "📂 File Analyzer":
    st.title("📂 File Analyzer")
    st.markdown("Upload files below to compute metadata, identify duplicate files, and explore storage distributions.")

    # Top Upload & Control Buttons
    c_left, c_right = st.columns([3, 1])
    with c_left:
        uploaded_files = st.file_uploader(
            "Select one or multiple files to analyze:",
            accept_multiple_files=True,
            key="file_uploader"
        )
    with c_right:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️ Clear Analysis", use_container_width=True):
            st.session_state.pop("file_uploader", None)
            st.rerun()

    if uploaded_files:
        # Backend Processing
        with st.spinner("Processing file metadata and calculating SHA-256 hashes..."):
            df_files = analyze_uploaded_files(uploaded_files)

        if not df_files.empty:
            # Filtering Options Section
            with st.expander("🔍 Filter Uploaded Files", expanded=False):
                f_col1, f_col2, f_col3 = st.columns(3)
                
                with f_col1:
                    available_types = ["All"] + sorted(df_files["Type"].unique().tolist())
                    selected_type = st.selectbox("Filter by Category:", available_types)
                
                min_size_val = float(df_files["Size (KB)"].min())
                max_size_val = float(df_files["Size (KB)"].max())
                
                with f_col2:
                    min_kb = st.number_input("Minimum Size (KB):", min_value=0.0, max_value=max_size_val, value=0.0)
                with f_col3:
                    max_kb = st.number_input("Maximum Size (KB):", min_value=min_kb, max_value=max_size_val if max_size_val > 0 else 1000.0, value=max_size_val if max_size_val > 0 else 1000.0)

            # Apply Filters
            filtered_df = df_files.copy()
            if selected_type != "All":
                filtered_df = filtered_df[filtered_df["Type"] == selected_type]
            filtered_df = filtered_df[(filtered_df["Size (KB)"] >= min_kb) & (filtered_df["Size (KB)"] <= max_kb)]

            # Summary Metrics Banners
            total_files = len(filtered_df)
            total_bytes = filtered_df["Size (Bytes)"].sum()
            total_storage_str = convert_size(total_bytes)
            num_types = filtered_df["Type"].nunique()
            
            duplicates_df = detect_duplicates(filtered_df)
            num_duplicates = len(duplicates_df) if not duplicates_df.empty else 0

            st.markdown("### 📊 Summary Metrics")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Total Files", total_files)
            m2.metric("Total Storage", total_storage_str)
            m3.metric("Number of File Types", num_types)
            m4.metric("Duplicate Files", num_duplicates)

            st.markdown("---")
            st.subheader("📑 File Analysis Table")
            display_cols = ["File Name", "Extension", "Type", "Size (KB)", "Size (MB)", "SHA-256"]
            st.dataframe(filtered_df[display_cols], use_container_width=True, hide_index=True)

            st.markdown("---")
            
            # Duplicate Files Section
            st.subheader("🔁 Duplicate Files")
            if not duplicates_df.empty:
                st.warning(f"Found {len(duplicates_df)} sets of duplicate files!")
                st.dataframe(duplicates_df, use_container_width=True, hide_index=True)
            else:
                st.success("No duplicate files found.")

            st.markdown("---")
            
            # Largest Files Section
            st.subheader("📦 Largest Files")
            largest_df = get_largest_files(filtered_df, top_n=10)
            st.dataframe(largest_df, use_container_width=True, hide_index=True)

            st.markdown("---")
            
            # Interactive Charts Section
            st.subheader("📈 Visual Insights & Charts")
            ch1, ch2 = st.columns(2)

            with ch1:
                st.markdown("#### Chart 1: File Type Distribution")
                type_counts = filtered_df["Type"].value_counts().reset_index()
                type_counts.columns = ["File Type", "Number of Files"]
                fig1 = px.bar(
                    type_counts,
                    x="File Type",
                    y="Number of Files",
                    color="File Type",
                    text_auto=True,
                    template="plotly_dark"
                )
                fig1.update_layout(margin=dict(l=10, r=10, t=30, b=10))
                st.plotly_chart(fig1, use_container_width=True)

            with ch2:
                st.markdown("#### Chart 2: Storage by File Type")
                storage_df = filtered_df.groupby("Type")["Size (MB)"].sum().reset_index()
                storage_df.columns = ["File Type", "Total Storage (MB)"]
                fig2 = px.bar(
                    storage_df,
                    x="File Type",
                    y="Total Storage (MB)",
                    color="File Type",
                    text_auto=".2f",
                    template="plotly_dark"
                )
                fig2.update_layout(margin=dict(l=10, r=10, t=30, b=10))
                st.plotly_chart(fig2, use_container_width=True)

            st.markdown("#### Chart 3: Largest Files Overview")
            top_10 = filtered_df.sort_values(by="Size (MB)", ascending=True).tail(10)
            fig3 = px.bar(
                top_10,
                x="Size (MB)",
                y="File Name",
                orientation="h",
                color="Type",
                text_auto=".2f",
                title="Top 10 Largest Files (MB)",
                template="plotly_dark"
            )
            fig3.update_layout(margin=dict(l=10, r=10, t=30, b=10))
            st.plotly_chart(fig3, use_container_width=True)

        else:
            st.info("No files matched the selected filters.")
    else:
        st.info("📁 Please upload one or more files above to begin analysis.")

# ==============================================================================
# PAGE 3: SYSTEM INFORMATION (MANDATORY PAGE)
# ==============================================================================
elif st.session_state["nav_page"] == "💻 System Information":
    st.title("💻 System Information")
    st.markdown("Real-time telemetry and hardware specs of the machine running Streamlit.")

    if st.button("🔄 Refresh System Information"):
        st.rerun()

    sys_info = get_complete_system_info()
    os_info = sys_info["os"]
    cpu_info = sys_info["cpu"]
    mem_info = sys_info["memory"]
    disk_info = sys_info["disk"]

    # Visual Progress Indicators Banner
    st.markdown("### ⚡ Live System Resource Indicators")
    p1, p2, p3 = st.columns(3)
    
    with p1:
        st.write(f"**CPU Usage:** {cpu_info['CPU Usage (%)']}%")
        st.progress(min(cpu_info['CPU Usage (%)'] / 100.0, 1.0))
        
    with p2:
        st.write(f"**RAM Usage:** {mem_info['RAM Usage (%)']}%")
        st.progress(min(mem_info['RAM Usage (%)'] / 100.0, 1.0))
        
    with p3:
        st.write(f"**Disk Usage:** {disk_info['Disk Usage (%)']}%")
        st.progress(min(disk_info['Disk Usage (%)'] / 100.0, 1.0))

    st.markdown("---")

    col_os, col_cpu = st.columns(2)
    with col_os:
        st.subheader("🖥️ Operating System")
        st.write(f"**Operating System:** {os_info['Operating System']}")
        st.write(f"**OS Version:** {os_info['OS Version']}")
        st.write(f"**Machine:** {os_info['Machine']}")
        st.write(f"**Architecture:** {os_info['Architecture']}")
        st.write(f"**Processor:** {os_info['Processor']}")
        st.write(f"**Python Version:** {os_info['Python Version']}")

    with col_cpu:
        st.subheader("⚡ CPU Details")
        st.write(f"**Physical Cores:** {cpu_info['Physical Cores']}")
        st.write(f"**Logical Cores:** {cpu_info['Logical Cores']}")
        st.write(f"**CPU Usage:** {cpu_info['CPU Usage (%)']}%")
        st.write(f"**CPU Frequency:** {cpu_info['CPU Frequency']}")

    st.markdown("---")

    col_mem, col_disk = st.columns(2)
    with col_mem:
        st.subheader("🧠 Memory (RAM)")
        st.write(f"**Total RAM:** {mem_info['Total RAM (GB)']} GB")
        st.write(f"**Used RAM:** {mem_info['Used RAM (GB)']} GB")
        st.write(f"**Available RAM:** {mem_info['Available RAM (GB)']} GB")
        st.write(f"**RAM Usage Percentage:** {mem_info['RAM Usage (%)']}%")

    with col_disk:
        st.subheader("💾 Disk Partition Space")
        st.write(f"**Mountpoint:** {disk_info['Mountpoint']}")
        st.write(f"**Total Disk Space:** {disk_info['Total Disk Space (GB)']} GB")
        st.write(f"**Used Disk Space:** {disk_info['Used Disk Space (GB)']} GB")
        st.write(f"**Free Disk Space:** {disk_info['Free Disk Space (GB)']} GB")
        st.write(f"**Disk Usage Percentage:** {disk_info['Disk Usage (%)']}%")

# ==============================================================================
# PAGE 4: ABOUT
# ==============================================================================
elif st.session_state["nav_page"] == "ℹ️ About":
    st.title("ℹ️ About Smart File Analyzer")
    
    st.markdown("""
    ### **Application**
    **Smart File Analyzer**

    ### **Purpose**
    A Streamlit-based application for analyzing uploaded files and understanding storage usage.

    ### **Features**
    - 📁 Multi-file upload support
    - 📑 File metadata extraction & analysis
    - 🏷️ Automatic file type classification
    - 🔁 SHA-256 cryptographic duplicate detection
    - 📦 Top 10 largest file identification
    - 📈 Dynamic Plotly chart visualizations
    - 💻 Live system-level machine information monitoring

    ### **Technologies**
    - Python 3
    - Streamlit
    - Pandas
    - Plotly
    - psutil

    ---
    
    > *"Developed as a functional Streamlit application demonstrating backend processing and system-level information retrieval."*
    """)
