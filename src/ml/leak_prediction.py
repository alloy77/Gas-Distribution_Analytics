import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score


def train_leak_model(data_path='data/processed/CGD_Transformation_Final.csv', model_path='models/leak_prediction_rf.pkl'):
    df = pd.read_csv(data_path, parse_dates=['TS'])

    if 'Leak_Flag' not in df.columns:
        raise ValueError('Leak_Flag column required in input data')

    df = df.dropna(subset=['Pressure','Pressure_Drop','Flow_std','Flow_Change','DMA_Zone','Leak_Flag'])

    X = df[['Pressure','Pressure_Drop','Flow_std','Flow_Change','DMA_Zone']].copy()
    X = pd.get_dummies(X, columns=['DMA_Zone'], dummy_na=False)
    y = df['Leak_Flag'].map(lambda v: 1 if str(v).strip().lower() == 'yes' else 0)

    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    report = classification_report(y_test, y_pred, output_dict=True)
    accuracy = accuracy_score(y_test, y_pred)

    joblib.dump(model, model_path)

    return { 'model_path': model_path, 'accuracy': accuracy, 'report': report }
