import os
import hashlib
import pandas as pd

# Extension category mapping dictionary
CATEGORY_MAP = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".tiff", ".ico"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".ppt", ".pptx"},
    "Videos": {".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"},
    "Audio": {".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"},
    "Data": {".csv", ".xlsx", ".xls", ".json", ".xml", ".parquet", ".tsv", ".sql", ".db"},
    "Code": {".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".sh", ".php", ".ts", ".rb", ".go", ".rs", ".h", ".ipynb"}
}

def convert_size(size_bytes):
    """Converts bytes to human-readable size string (Bytes, KB, MB, GB)."""
    if size_bytes is None or size_bytes < 0:
        return "0 Bytes"
    if size_bytes < 1024:
        return f"{size_bytes} Bytes"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.2f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"

def get_file_extension(filename):
    """Extracts file extension in lowercase, e.g. '.pdf'."""
    if not filename or '.' not in filename:
        return "None"
    _, ext = os.path.splitext(filename)
    return ext.lower() if ext else "None"

def get_file_category(extension):
    """Classifies file extension into a general category."""
    if not extension or extension == "None":
        return "Other"
    
    ext_lower = extension.lower()
    for category, ext_set in CATEGORY_MAP.items():
        if ext_lower in ext_set:
            return category
    return "Other"

def calculate_sha256(file_bytes):
    """Calculates SHA-256 hash of file byte content."""
    sha256_hash = hashlib.sha256()
    sha256_hash.update(file_bytes)
    return sha256_hash.hexdigest()

def analyze_uploaded_files(uploaded_files):
    """
    Processes a list of Streamlit UploadedFile objects.
    Calculates size, category, extension, and SHA-256 hash.
    Returns a pandas DataFrame.
    """
    file_records = []

    for uploaded_file in uploaded_files:
        try:
            filename = uploaded_file.name
            size_bytes = uploaded_file.size
            file_bytes = uploaded_file.getvalue()
            uploaded_file.seek(0) # Reset pointer

            ext = get_file_extension(filename)
            category = get_file_category(ext)
            size_kb = round(size_bytes / 1024, 2)
            size_mb = round(size_bytes / (1024 * 1024), 4)
            file_hash = calculate_sha256(file_bytes)

            file_records.append({
                "File Name": filename,
                "Extension": ext,
                "Type": category,
                "Size (Bytes)": size_bytes,
                "Size (KB)": size_kb,
                "Size (MB)": size_mb,
                "Formatted Size": convert_size(size_bytes),
                "SHA-256": file_hash
            })
        except Exception as e:
            # Handle potential file read errors safely
            continue

    if not file_records:
        return pd.DataFrame(columns=[
            "File Name", "Extension", "Type", "Size (Bytes)",
            "Size (KB)", "Size (MB)", "Formatted Size", "SHA-256"
        ])

    return pd.DataFrame(file_records)

def detect_duplicates(df):
    """
    Identifies duplicate files based on SHA-256 hash.
    Returns a DataFrame containing SHA-256, duplicate file names, and copy counts.
    """
    if df.empty or "SHA-256" not in df.columns:
        return pd.DataFrame()

    dup_hashes = df[df.duplicated(subset=["SHA-256"], keep=False)]
    if dup_hashes.empty:
        return pd.DataFrame()

    grouped = dup_hashes.groupby("SHA-256").agg(
        File_Names=("File Name", lambda names: ", ".join(list(names))),
        Copies_Count=("File Name", "count"),
        Total_Size_MB=("Size (MB)", "first")
    ).reset_index()

    grouped.rename(columns={
        "SHA-256": "SHA-256 Hash",
        "File_Names": "Duplicate File Names",
        "Copies_Count": "Number of Copies",
        "Total_Size_MB": "File Size (MB)"
    }, inplace=True)

    return grouped

def get_largest_files(df, top_n=10):
    """Returns top N largest uploaded files sorted descending by size."""
    if df.empty:
        return pd.DataFrame()

    sorted_df = df.sort_values(by="Size (Bytes)", ascending=False).head(top_n).copy()
    sorted_df.reset_index(drop=True, inplace=True)
    sorted_df["Rank"] = sorted_df.index + 1

    display_df = sorted_df[["Rank", "File Name", "Type", "Formatted Size", "Size (MB)", "Size (KB)"]]
    return display_df
