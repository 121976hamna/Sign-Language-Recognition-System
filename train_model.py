import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA

# Load the collected data
df = pd.read_csv('urdu_gesture_data.csv')

# Handle null values
df.dropna(inplace=True)

# Features and labels
X = df[['f1', 'f2', 'f3', 'f4', 'f5']]
y = df['label']

# Count samples per label
print("🔢 Sample count per label:")
print(df['label'].value_counts())

# Plot class distribution
label_counts = df['label'].value_counts().reset_index()
label_counts.columns = ['Category', 'Count']
plt.figure(figsize=(14, 4), dpi=200)
sns.barplot(data=label_counts, x='Category', y='Count', palette='icefire', width=0.4)
plt.title('Class Distribution in Dataset', fontsize=15)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Check for data leakage: overlapping samples
overlap = pd.merge(X_train, X_test, how='inner')
print(f"⚠️ Overlapping samples between train and test: {len(overlap)}")
# Train Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save test data
test_df = X_test.copy()
test_df['label'] = y_test.values
test_df.to_csv('urdu_gesture_test_data.csv', index=False)
print("📁 Test dataset saved as 'urdu_gesture_test_data.csv'")



# Predict and evaluate
y_pred = model.predict(X_test)
print("📊 Classification Report:")
print(classification_report(y_test, y_pred))
print(f"✅ Accuracy on test set: {model.score(X_test, y_test):.2f}")


# Confusion Matrix
conf_mat = confusion_matrix(y_test, y_pred, labels=model.classes_)
plt.figure(figsize=(10, 8), dpi=200)
sns.heatmap(conf_mat, annot=True, fmt='d', cmap='Blues',
            xticklabels=model.classes_, yticklabels=model.classes_)
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.title('Confusion Matrix')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Manual inspection of predictions
print("🔍 Predicted vs Actual:")
print(pd.DataFrame({'Actual': y_test.values, 'Predicted': y_pred}))

# Cross-validation accuracy
cv_scores = cross_val_score(model, X, y, cv=5)
print("📈 Cross-validation scores:", cv_scores)
print("📊 Mean CV accuracy:", cv_scores.mean())



# Save trained model
joblib.dump(model, 'urdu_sign_model.pkl')
print("✅ Model saved as 'urdu_sign_model.pkl'")