import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder, StandardScaler

def run_ml_anomaly_detection(df_files, contamination=0.1):
    """
    Applies IsolationForest Machine Learning model to detect anomalous / outlier files.
    """
    if df_files is None or len(df_files) < 3:
        return df_files, None

    df_ml = df_files.copy()

    # Feature engineering for ML
    le_type = LabelEncoder()
    df_ml["type_encoded"] = le_type.fit_transform(df_ml["Type"].astype(str))
    df_ml["ext_len"] = df_ml["Extension"].apply(lambda x: len(str(x)))

    features = df_ml[["Size (MB)", "type_encoded", "ext_len"]]

    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    model = IsolationForest(contamination=contamination, random_state=42)
    df_ml["Anomaly_Score"] = model.fit_predict(scaled_features)
    df_ml["Is_Anomaly"] = df_ml["Anomaly_Score"].apply(lambda x: "Yes (Anomaly)" if x == -1 else "Normal")

    # Plotly Scatter
    fig = px.scatter(
        df_ml,
        x="Size (MB)",
        y="Type",
        color="Is_Anomaly",
        hover_data=["File Name", "Extension", "Formatted Size"],
        title="ML Anomaly Detection (Isolation Forest)",
        template="plotly_dark",
        color_discrete_map={"Normal": "#38bdf8", "Yes (Anomaly)": "#ef4444"}
    )
    fig.update_layout(margin=dict(l=10, r=10, t=40, b=10))

    return df_ml, fig

def run_ml_storage_clustering(df_files, n_clusters=3):
    """
    Applies K-Means Clustering Machine Learning model to group files into smart storage clusters.
    """
    if df_files is None or len(df_files) < n_clusters:
        return df_files, None

    df_cluster = df_files.copy()
    le_type = LabelEncoder()
    df_cluster["type_encoded"] = le_type.fit_transform(df_cluster["Type"].astype(str))

    X = df_cluster[["Size (MB)", "type_encoded"]]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    k = min(n_clusters, len(df_files))
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    df_cluster["Cluster"] = kmeans.fit_predict(X_scaled)
    df_cluster["Cluster_Label"] = df_cluster["Cluster"].apply(lambda c: f"Cluster {c+1}")

    fig = px.scatter(
        df_cluster,
        x="Size (MB)",
        y="type_encoded",
        color="Cluster_Label",
        hover_data=["File Name", "Type", "Formatted Size"],
        title=f"ML Storage Clustering (K-Means k={k})",
        template="plotly_dark",
        labels={"type_encoded": "File Type Category"}
    )
    fig.update_layout(margin=dict(l=10, r=10, t=40, b=10))

    return df_cluster, fig
