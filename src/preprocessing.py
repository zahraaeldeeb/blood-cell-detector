import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def clean_and_preprocess_data(df):
    
    drop_cols = [
        'cell_id', 'dataset_source', 'staining_protocol', 'labeller_confidence_score',
        'disease_category', 'cell_type', 'cytodiffusion_anomaly_score', 
        'cytodiffusion_classification_confidence', 'microscope_model'
    ]
    df_cleaned = df.drop(columns=[c for c in drop_cols if c in df.columns])
    
  
    if 'patient_sex' in df_cleaned.columns:
        df_cleaned['patient_sex'] = df_cleaned['patient_sex'].map({'M': 0, 'F': 1})
    if 'patient_age_group' in df_cleaned.columns:
        age_map = {'Pediatric': 0, 'Adult': 1, 'Elderly': 2}
        df_cleaned['patient_age_group'] = df_cleaned['patient_age_group'].map(age_map)
        
    return df_cleaned

def prepare_splits(df, target_col='anomaly_label'):
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    return X_train, X_test, X_train_scaled, X_test_scaled, y_train, y_test
