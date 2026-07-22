---
name: python-datascience
description: >
  Expert guidance for learning and applying Data Science and Machine Learning with Python.
  Use this skill whenever the user asks about NumPy, Pandas, Matplotlib, Seaborn,
  Scikit-learn, TensorFlow, PyTorch, Jupyter Notebooks, Google Colab, data cleaning,
  EDA, feature engineering, model training, evaluation, hyperparameter tuning, SHAP
  explainability, NLP, time series, or any DS/ML workflow in Python.
  Always trigger this skill when the user mentions "dataset", "dataframe", "model",
  "train", "predict", "plot", "accuracy", "loss", "pipeline", "classification",
  "regression", "clustering", or any ML/DS concept — even if phrased as a beginner
  question. Provides beginner-friendly explanations, working code snippets,
  visualizations, and best-practice reminders tailored to a learner progressing from
  Python basics into full ML pipelines.
  Do NOT use for pure SQL queries, spreadsheet tasks, or document generation unrelated
  to data science.
license: MIT
---

# Python Data Science & Machine Learning Skill

> Level: **Python basics → DS/ML learner**
> Stack: **NumPy, Pandas, Matplotlib, Seaborn, Scikit-learn, XGBoost/LightGBM, TensorFlow/PyTorch, HuggingFace**
> Environments: **VS Code (.py files), Jupyter Notebooks, Google Colab** *(all supported)*

---

## Learning Roadmap

```
Python Basics (done ✅)
    ↓
1. NumPy & Pandas            — data manipulation
2. Matplotlib & Seaborn      — visualization
3. Scikit-learn              — classical ML
4. XGBoost / LightGBM        — gradient boosting
5. TensorFlow / PyTorch      — deep learning
6. HuggingFace Transformers  — NLP / GenAI
```

---

## Environment Setup

### Install All Libraries
```bash
# Core stack
pip install numpy pandas scikit-learn matplotlib seaborn scipy statsmodels --break-system-packages

# Gradient boosting
pip install xgboost lightgbm catboost --break-system-packages

# Deep learning
pip install torch torchvision --break-system-packages
pip install tensorflow --break-system-packages

# NLP / GenAI
pip install transformers datasets --break-system-packages

# Explainability
pip install shap lime --break-system-packages

# Experiment tracking & HPO
pip install mlflow optuna --break-system-packages

# Interactive plots
pip install plotly --break-system-packages
```

### Quick Environment Check
```python
import sys, numpy, pandas, sklearn
print(f"Python {sys.version}")
print(f"NumPy {numpy.__version__}, Pandas {pandas.__version__}, Sklearn {sklearn.__version__}")
```

### Your Local Environment (MacBook Air)
- **venv:** `ml-env` at `"/Users/sanjayachaudhary/Desktop/Python Project/Learn_Python"`
- **Activate:** `source ml-env/bin/activate`
- **Formatter:** Black (`formatOnSave` enabled), Ruff for linting
- **Folder structure:** `basics/`, `numerical/`, `pandas/`, `projects/`, `scratch/`
- **Use `# %%` cell markers** in `.py` files to run code in blocks (like notebooks) inside VS Code

---

## 1. NumPy — Numerical Computing

```python
import numpy as np

# Arrays
a = np.array([1, 2, 3, 4, 5])
b = np.zeros((3, 3))          # 3x3 zeros
c = np.random.rand(4, 4)      # random floats 0–1
d = np.arange(0, 10, 2)       # [0, 2, 4, 6, 8]

# Shapes & reshaping
print(a.shape)                 # (5,)
a_2d = a.reshape(1, 5)        # [[1, 2, 3, 4, 5]]

# Math operations (vectorized — no loops needed!)
print(a * 2)                   # [2, 4, 6, 8, 10]
print(np.mean(a))              # 3.0
print(np.std(a))               # std deviation
print(np.dot(c, c))            # matrix multiplication

# Indexing & slicing
print(c[0, :])                 # first row
print(c[:, 1])                 # second column
print(c[c > 0.5])              # boolean mask
```

**💡 Key concept:** NumPy avoids Python loops — always prefer vectorized operations for speed.

---

## 2. Data Ingestion

```python
import pandas as pd

# CSV / TSV
df = pd.read_csv("data.csv")
df = pd.read_csv("data.tsv", sep="\t")

# Excel
df = pd.read_excel("data.xlsx", sheet_name="Sheet1")

# JSON / Parquet / Feather
df = pd.read_json("data.json")
df = pd.read_parquet("data.parquet")
df = pd.read_feather("data.feather")

# SQL
import sqlite3
conn = sqlite3.connect("database.db")
df = pd.read_sql("SELECT * FROM table_name", conn)

# From URL
df = pd.read_csv("https://example.com/data.csv")

# From Claude container uploads
import os
upload_dir = "/mnt/user-data/uploads"
files = os.listdir(upload_dir)
df = pd.read_csv(f"{upload_dir}/{files[0]}")
```

---

## 3. Pandas — Data Manipulation

```python
import pandas as pd

# Creating DataFrames
df = pd.DataFrame({'name': ['Alice', 'Bob'], 'age': [25, 30], 'score': [88, 92]})

# Exploring data (always do this first!)
df.head()                        # first 5 rows
df.shape                         # (rows, columns)
df.info()                        # column types + nulls
df.describe()                    # stats: mean, std, min, max
df.describe(include="all")       # include categoricals
df.isnull().sum()                # count missing values per column
df.isnull().mean().sort_values(ascending=False)  # % missing
df.nunique()                     # unique values per column
df["col"].value_counts()         # frequency count

# Selecting data
df['age']                        # single column → Series
df[['name', 'score']]            # multiple columns → DataFrame
df[df['score'] > 90]             # filter rows
df.loc[0, 'name']                # by label
df.iloc[0, 1]                    # by position

# Cleaning
df.dropna(inplace=True)
df.dropna(axis=1, thresh=int(0.8 * len(df)), inplace=True)  # drop cols >20% missing
df.fillna(0, inplace=True)
df['age'] = df['age'].astype(int)
df.drop_duplicates(inplace=True)

# Transforming
df['grade'] = df['score'].apply(lambda x: 'A' if x >= 90 else 'B')
df_sorted = df.sort_values('score', ascending=False)
df_grouped = df.groupby('grade')['score'].mean()

# Merging
merged = pd.merge(df1, df2, on='id', how='left')
```

**💡 EDA checklist:** `.shape` → `.info()` → `.describe()` → `.isnull().sum()` → `.value_counts()`

---

## 4. Matplotlib & Seaborn — Visualization

```python
import matplotlib.pyplot as plt
import seaborn as sns

# --- Matplotlib basics ---
plt.figure(figsize=(8, 5))
plt.plot(df['age'], df['score'], marker='o', color='steelblue', label='Score')
plt.xlabel('Age'); plt.ylabel('Score'); plt.title('Age vs Score')
plt.legend(); plt.tight_layout(); plt.show()

# Common plot types
plt.bar(df['name'], df['score'])          # bar chart
plt.hist(df['score'], bins=10)            # histogram
plt.scatter(df['age'], df['score'])       # scatter plot
plt.boxplot(df['score'])                  # box plot

# --- Seaborn (easier + prettier) ---
sns.set_theme(style='whitegrid')

sns.histplot(df['score'], kde=True)                        # distribution
sns.scatterplot(data=df, x='age', y='score', hue='grade') # colored scatter
sns.boxplot(data=df, x='grade', y='score')                 # grouped boxplot
sns.heatmap(df.corr(numeric_only=True), annot=True, fmt=".2f", cmap='coolwarm')  # correlation
sns.pairplot(df, hue='grade')                              # all-vs-all plots

# Save outputs to container
plt.savefig("/mnt/user-data/outputs/plot.png")
```

**💡 Use Seaborn for exploratory plots, Matplotlib for fine-tuned custom charts.**

---

## 5. Data Preprocessing

### Handle Missing Values
```python
from sklearn.impute import SimpleImputer, KNNImputer

imputer = SimpleImputer(strategy="median")   # or "mean", "most_frequent"
df[numeric_cols] = imputer.fit_transform(df[numeric_cols])

knn_imputer = KNNImputer(n_neighbors=5)
df[numeric_cols] = knn_imputer.fit_transform(df[numeric_cols])
```

### Encode Categorical Variables
```python
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder, OneHotEncoder

# One-hot encoding
df = pd.get_dummies(df, columns=["col1", "col2"], drop_first=True)

# Label encoding (ordinal or tree-based models)
le = LabelEncoder()
df["col"] = le.fit_transform(df["col"])

# Ordinal encoding
oe = OrdinalEncoder(categories=[["low", "medium", "high"]])
df[["col"]] = oe.fit_transform(df[["col"]])
```

### Scale Features
```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

scaler = StandardScaler()       # zero mean, unit variance (most common)
# scaler = MinMaxScaler()       # [0, 1] range
# scaler = RobustScaler()       # robust to outliers

X_train = scaler.fit_transform(X_train)   # fit + transform on train
X_test  = scaler.transform(X_test)        # NEVER fit on test set
```

### Train/Test Split
```python
from sklearn.model_selection import train_test_split

X = df.drop("target", axis=1)
y = df["target"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y  # stratify for classification
)
```

### Feature Engineering
```python
from sklearn.preprocessing import PolynomialFeatures
import numpy as np

# Polynomial features
poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X)

# Log transform (skewed features)
df["col_log"] = np.log1p(df["col"])

# Interaction terms
df["feat1_x_feat2"] = df["feat1"] * df["feat2"]

# Date features
df["date"] = pd.to_datetime(df["date"])
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["dayofweek"] = df["date"].dt.dayofweek
```

---

## 6. Scikit-learn — Classical ML

### Full ML Pipeline (Quick Start)
```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Prepare → Split → Scale → Train → Evaluate
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test  = scaler.transform(X_test)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))
```

### Common Models Cheat Sheet
| Task | Model | Import |
|------|-------|--------|
| Classification | Logistic Regression | `sklearn.linear_model` |
| Classification | Random Forest | `sklearn.ensemble` |
| Classification | SVM | `sklearn.svm` |
| Classification | XGBoost | `xgboost` |
| Classification | LightGBM | `lightgbm` |
| Regression | Linear / Ridge / Lasso | `sklearn.linear_model` |
| Regression | XGBRegressor | `xgboost` |
| Clustering | K-Means | `sklearn.cluster` |
| Clustering | DBSCAN | `sklearn.cluster` |
| Dimensionality | PCA | `sklearn.decomposition` |
| Dimensionality | t-SNE / UMAP | `sklearn.manifold` / `umap` |

### XGBoost / LightGBM
```python
from xgboost import XGBClassifier
model = XGBClassifier(n_estimators=200, learning_rate=0.1, max_depth=6,
                      eval_metric="logloss", random_state=42)
model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)

from lightgbm import LGBMClassifier
model = LGBMClassifier(n_estimators=200, learning_rate=0.05, num_leaves=31)
model.fit(X_train, y_train)
```

### Clustering
```python
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score

# Elbow method to find optimal k
inertias = []
for k in range(2, 11):
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X_scaled)
    inertias.append(km.inertia_)

km = KMeans(n_clusters=4, random_state=42, n_init=10)
labels = km.fit_predict(X_scaled)
print("Silhouette Score:", silhouette_score(X_scaled, labels))

# DBSCAN (no need to specify k)
db = DBSCAN(eps=0.5, min_samples=5)
labels = db.fit_predict(X_scaled)
```

### Dimensionality Reduction
```python
from sklearn.decomposition import PCA
pca = PCA(n_components=0.95)  # retain 95% variance
X_pca = pca.fit_transform(X_scaled)
print(f"Components kept: {pca.n_components_}")

from sklearn.manifold import TSNE
tsne = TSNE(n_components=2, perplexity=30, random_state=42)
X_embedded = tsne.fit_transform(X_scaled)
```

---

## 7. Model Evaluation

### Classification Metrics
```python
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, classification_report, ConfusionMatrixDisplay
)

y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]  # binary

print(f"Accuracy:  {accuracy_score(y_test, y_pred):.4f}")
print(f"Precision: {precision_score(y_test, y_pred, average='weighted'):.4f}")
print(f"Recall:    {recall_score(y_test, y_pred, average='weighted'):.4f}")
print(f"F1 Score:  {f1_score(y_test, y_pred, average='weighted'):.4f}")
print(f"ROC-AUC:   {roc_auc_score(y_test, y_prob):.4f}")
print(classification_report(y_test, y_pred))

ConfusionMatrixDisplay.from_estimator(model, X_test, y_test)
plt.savefig("/mnt/user-data/outputs/confusion_matrix.png")

from sklearn.metrics import RocCurveDisplay
RocCurveDisplay.from_estimator(model, X_test, y_test)
plt.savefig("/mnt/user-data/outputs/roc_curve.png")
```

### Regression Metrics
```python
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

y_pred = model.predict(X_test)
print(f"MAE:  {mean_absolute_error(y_test, y_pred):.4f}")
print(f"RMSE: {np.sqrt(mean_squared_error(y_test, y_pred)):.4f}")
print(f"R²:   {r2_score(y_test, y_pred):.4f}")
```

### Cross-Validation
```python
from sklearn.model_selection import cross_val_score, StratifiedKFold

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X, y, cv=cv, scoring="f1_weighted")
print(f"CV F1: {scores.mean():.4f} ± {scores.std():.4f}")
```

---

## 8. Hyperparameter Optimization

### GridSearchCV
```python
from sklearn.model_selection import GridSearchCV

param_grid = {"max_depth": [3, 5, 7], "n_estimators": [100, 200], "learning_rate": [0.05, 0.1]}
grid = GridSearchCV(model, param_grid, cv=5, scoring="f1_weighted", n_jobs=-1)
grid.fit(X_train, y_train)
print("Best params:", grid.best_params_)
```

### Optuna (Bayesian Optimization)
```python
import optuna

def objective(trial):
    params = {
        "n_estimators": trial.suggest_int("n_estimators", 100, 500),
        "max_depth": trial.suggest_int("max_depth", 3, 10),
        "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3, log=True),
    }
    model = XGBClassifier(**params, random_state=42)
    scores = cross_val_score(model, X_train, y_train, cv=3, scoring="roc_auc")
    return scores.mean()

study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=50)
print("Best params:", study.best_params)
```

---

## 9. Sklearn Pipelines

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier

numeric_features = ["age", "income"]
categorical_features = ["gender", "city"]

numeric_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

categorical_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer([
    ("num", numeric_transformer, numeric_features),
    ("cat", categorical_transformer, categorical_features)
])

full_pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(n_estimators=100))
])

full_pipeline.fit(X_train, y_train)
y_pred = full_pipeline.predict(X_test)
```

---

## 10. Feature Importance & Explainability (SHAP)

```python
import pandas as pd
import matplotlib.pyplot as plt

# Tree-based feature importance
importances = pd.Series(model.feature_importances_, index=X.columns)
importances.sort_values(ascending=False).head(20).plot(kind="barh", figsize=(8, 6))
plt.title("Feature Importances")
plt.tight_layout()
plt.savefig("/mnt/user-data/outputs/feature_importance.png")

# SHAP values
import shap
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

shap.summary_plot(shap_values, X_test, show=False)
plt.savefig("/mnt/user-data/outputs/shap_summary.png")
```

---

## 11. Deep Learning

### TensorFlow / Keras (beginner-friendly)
```python
import tensorflow as tf
from tensorflow import keras

model = keras.Sequential([
    keras.layers.Dense(128, activation='relu', input_shape=(X_train.shape[1],)),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid')   # binary classification
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

history = model.fit(X_train, y_train,
                    epochs=20, batch_size=32,
                    validation_split=0.2, verbose=1)
model.evaluate(X_test, y_test)

# Plot training history
plt.plot(history.history['accuracy'], label='train')
plt.plot(history.history['val_accuracy'], label='val')
plt.legend(); plt.title('Accuracy'); plt.show()
```

### PyTorch (more control)
```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

X_tensor = torch.FloatTensor(X_train.values)
y_tensor = torch.FloatTensor(y_train.values)
loader = DataLoader(TensorDataset(X_tensor, y_tensor), batch_size=32, shuffle=True)

class MLP(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 128), nn.ReLU(), nn.Dropout(0.3),
            nn.Linear(128, 64),        nn.ReLU(), nn.Dropout(0.3),
            nn.Linear(64, 1),          nn.Sigmoid()
        )
    def forward(self, x): return self.net(x)

model = MLP(X_train.shape[1])
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
criterion = nn.BCELoss()

for epoch in range(50):
    for X_batch, y_batch in loader:
        optimizer.zero_grad()
        pred = model(X_batch).squeeze()
        loss = criterion(pred, y_batch)
        loss.backward()
        optimizer.step()
    if epoch % 10 == 0:
        print(f"Epoch {epoch}, Loss: {loss.item():.4f}")
```

**💡 Start with TensorFlow/Keras — more beginner-friendly. Move to PyTorch when you need more control.**

---

## 12. NLP Basics

### TF-IDF (Classical)
```python
import re
from sklearn.feature_extraction.text import TfidfVectorizer

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    return text.strip()

texts = [clean_text(t) for t in df["text_column"]]
vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2), stop_words="english")
X_tfidf = vectorizer.fit_transform(texts)
```

### HuggingFace Transformers
```python
from transformers import pipeline

# Sentiment analysis
classifier = pipeline("sentiment-analysis")
result = classifier("This product is absolutely amazing!")

# Text generation
generator = pipeline("text-generation", model="gpt2")
output = generator("Once upon a time", max_length=50)

# Named entity recognition
ner = pipeline("ner", grouped_entities=True)
entities = ner("Elon Musk founded SpaceX in Hawthorne, California.")
```

---

## 13. Time Series

```python
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima.model import ARIMA

df["date"] = pd.to_datetime(df["date"])
df.set_index("date", inplace=True)
ts = df["value"].resample("M").mean()

# Decompose trend/seasonality/residual
result = seasonal_decompose(ts, model="additive", period=12)
result.plot()
plt.savefig("/mnt/user-data/outputs/ts_decomposition.png")

# ARIMA forecast
model = ARIMA(ts, order=(1, 1, 1))
fitted = model.fit()
forecast = fitted.forecast(steps=12)
print(forecast)
```

---

## 14. Model Persistence

```python
import joblib

# Save
joblib.dump(model,  "/mnt/user-data/outputs/model.joblib")
joblib.dump(scaler, "/mnt/user-data/outputs/scaler.joblib")

# Load
model  = joblib.load("model.joblib")
scaler = joblib.load("scaler.joblib")
```

---

## 15. MLflow Experiment Tracking

```python
import mlflow
import mlflow.sklearn

mlflow.set_experiment("my_experiment")

with mlflow.start_run():
    mlflow.log_param("model_type", "RandomForest")
    mlflow.log_param("n_estimators", 100)
    model.fit(X_train, y_train)
    acc = accuracy_score(y_test, model.predict(X_test))
    mlflow.log_metric("accuracy", acc)
    mlflow.sklearn.log_model(model, "model")
    print(f"Run logged with accuracy: {acc:.4f}")
```

---

## 16. Output Files Convention

Save all charts and models to `/mnt/user-data/outputs/`:

| File | Description |
|------|-------------|
| `histograms.png` | Feature distributions |
| `correlation.png` | Correlation heatmap |
| `confusion_matrix.png` | Classification confusion matrix |
| `roc_curve.png` | ROC curve |
| `feature_importance.png` | Feature importances |
| `shap_summary.png` | SHAP summary plot |
| `model.joblib` | Trained model |
| `scaler.joblib` | Fitted scaler |
| `predictions.csv` | Model predictions |

---

## Quick Debug Checklist

| Problem | Fix |
|---------|-----|
| `KeyError` on column | Check `df.columns` — watch for spaces/typos |
| Shape mismatch | Print `X.shape`, `y.shape` before fitting |
| Poor accuracy | Check for data leakage, scale features, try more epochs |
| `NaN` in training | Run `df.isnull().sum()` and fill/drop nulls |
| Overfitting | Add Dropout, reduce model size, cross-validate |
| Data leakage | Always `fit` on train set only; `transform` test |
| Class imbalance | Use `class_weight="balanced"`, SMOTE, threshold tuning |
| Feature scaling | Required for: LR, SVM, KNN, Neural Nets — NOT for trees |
| Reproducibility | Set `random_state=42` everywhere |
| Memory issues | Use `dtype` downcasting, chunked reading, sparse matrices |

---

## Algorithm Selection Guide

| Task | Small Data | Large Data |
|------|-----------|------------|
| Binary Classification | Logistic Regression, SVM | XGBoost, LightGBM, Neural Net |
| Multi-class | Random Forest | LightGBM, Softmax NN |
| Regression | Ridge / Lasso | XGBoost, Neural Net |
| Clustering | K-Means, DBSCAN | Mini-batch K-Means |
| Dimensionality Reduction | PCA | UMAP |
| NLP | TF-IDF + LR | Transformers (BERT) |
| Time Series | ARIMA, Exponential Smoothing | Prophet, LSTM |
