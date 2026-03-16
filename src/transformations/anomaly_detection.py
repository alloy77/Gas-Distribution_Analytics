from sklearn.neighbors import NearestNeighbors

def detect_anomalies(df):

    features = df[["Flow_std", "Pressure"]].fillna(0)

    model = NearestNeighbors(n_neighbors=5)

    model.fit(features)

    distances, _ = model.kneighbors(features)

    df["Anomaly_Score"] = distances.mean(axis=1)

    return df