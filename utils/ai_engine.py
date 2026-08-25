import os
import pandas as pd
import numpy as np

def generate_ai_file_insights(df_files, duplicates_df=None, api_key=None):
    """
    Generates intelligent AI Insights and Storage Advisory for uploaded files.
    Works built-in or connects to API key if provided.
    """
    if df_files is None or df_files.empty:
        return {
            "health_score": 100,
            "status": "No Files Uploaded",
            "summary": "Please upload files to enable AI Smart Insights.",
            "recommendations": []
        }

    total_files = len(df_files)
    total_size_mb = df_files["Size (MB)"].sum()
    duplicate_count = len(duplicates_df) if duplicates_df is not None and not duplicates_df.empty else 0
    duplicate_size_mb = duplicates_df["File Size (MB)"].sum() if duplicate_count > 0 else 0.0

    # Calculate Storage Health Index (100 base, penalty for duplicates and huge files)
    dup_penalty = min(duplicate_count * 10, 40)
    size_penalty = 10 if total_size_mb > 500 else 0
    health_score = max(100 - dup_penalty - size_penalty, 20)

    # Category breakdown
    type_counts = df_files["Type"].value_counts().to_dict()
    top_category = max(type_counts, key=type_counts.get) if type_counts else "Unknown"

    # Risk detection (e.g., executables, scripts, huge uncompressed files)
    large_files = df_files[df_files["Size (MB)"] > 50]
    exec_files = df_files[df_files["Extension"].isin([".exe", ".bat", ".vbs", ".sh", ".cmd"])]

    recommendations = []

    if duplicate_count > 0:
        recommendations.append(f"⚠️ **Eliminate Duplicates**: You have {duplicate_count} set(s) of identical files wasting approximately {duplicate_size_mb:.2f} MB of space.")
    else:
        recommendations.append("✅ **Clean Storage**: No duplicate files detected across your uploads.")

    if not large_files.empty:
        recommendations.append(f"📦 **Large Files Advisory**: {len(large_files)} file(s) exceed 50 MB. Consider compressing or archiving them.")

    if not exec_files.empty:
        recommendations.append(f"🛡️ **Security Alert**: Detected {len(exec_files)} executable script file(s). Ensure source credibility before running.")

    recommendations.append(f"📊 **Dominant Category**: Primary storage usage is driven by **{top_category}** files ({type_counts.get(top_category, 0)} files).")

    summary_text = (
        f"Smart AI analysis evaluated **{total_files} file(s)** totaling **{total_size_mb:.2f} MB**. "
        f"The primary storage component consists of **{top_category}** files. "
        f"Storage Efficiency Rating: **{health_score}/100**."
    )

    return {
        "health_score": health_score,
        "status": "Healthy" if health_score >= 80 else ("Needs Attention" if health_score >= 50 else "Critical"),
        "summary": summary_text,
        "recommendations": recommendations,
        "total_files": total_files,
        "total_size_mb": total_size_mb,
        "top_category": top_category
    }
