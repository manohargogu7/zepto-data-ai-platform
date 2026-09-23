# Module 2 — Titanic Analytics & Machine Learning

## Overview

This module performs exploratory data analysis (EDA), data cleaning, preprocessing, classification, class-imbalance analysis, hyperparameter tuning, regression, model comparison, and deployment-pipeline validation using the Titanic dataset.

### Module Files

```text
analytics/
├── 01_eda.ipynb
├── 02_modeling.ipynb
├── README.md
├── titanic.csv
└── outputs/
    └── best_titanic_pipeline.joblib
```

The module is divided into two notebooks:

- `01_eda.ipynb` — Exploratory Data Analysis and EDA validation
- `02_modeling.ipynb` — Train/test split, preprocessing, classification, imbalance analysis, hyperparameter tuning, regression, final comparison, and pipeline saving/reloading

---

# Part A — Exploratory Data Analysis

# 1. Dataset Loading

The Titanic dataset was loaded using Seaborn:

```python
sns.load_dataset("titanic")
```

The raw dataset was loaded from the network/cache exactly once in the EDA notebook.

Immediately after loading, the dataset was saved as:

```text
analytics/titanic.csv
```

The modeling notebook does not load the Titanic dataset again through Seaborn. It reads the committed CSV file instead:

```python
df = pd.read_csv("titanic.csv")
```

This ensures that both notebooks use the same dataset and avoids repeated external dataset loading.

## Dataset Shape

The original Titanic dataset contained:

- Rows: 891
- Columns: 15

The EDA cleaning step produced a cleaned analysis dataset containing:

- Rows: 889
- Columns: 14

The modeling notebook reads the committed `titanic.csv` file and performs leakage-safe preprocessing on the training data.

---

# 2. Dataset Profiling

The following dataset profiling operations were performed:

```python
df.info()
df.describe()
df.shape
```

The analysis examined:

- Data types
- Numerical summary statistics
- Dataset dimensions
- Missing values
- Categorical variables
- Numerical variables

---

# 3. Missing-Value Analysis and Handling

The missing-value percentages were calculated for every column containing missing values.

## Missing Values in the Original Dataset

| Column | Missing Values | Missing Percentage |
|---|---:|---:|
| age | 177 | 19.87% |
| embarked | 2 | 0.22% |
| deck | 688 | 77.22% |
| embark_town | 2 | 0.22% |

The following threshold-based strategy was used.

## Missing-Value Strategy

- Missingness below 5% → drop affected rows.
- Missingness between 5% and 30% → impute the missing values.
- Missingness above 30% → drop the column when the missingness was too high.

## Applied Decisions

### `age`

`age` had approximately 19.87% missing values.

Because this is between 5% and 30%, missing age values were handled using median imputation.

### `embarked`

`embarked` had approximately 0.22% missing values.

Because the missing percentage was below 5%, the affected rows were removed.

### `embark_town`

`embark_town` had approximately 0.22% missing values.

Because `embark_town` was redundant with `embarked` and was not required for the final modeling feature list, it was excluded from the final modeling features.

### `deck`

`deck` had approximately 77.22% missing values.

Because more than 30% of the observations were missing, the column was dropped rather than attempting to impute such a large proportion of missing values.

After EDA cleaning, the cleaned analysis dataset contained 889 observations and 14 columns.

---

# 4. Univariate Analysis

Histograms and boxplots were created for:

- `age`
- `fare`

The analysis also used the Interquartile Range (IQR) method to identify potential outliers.

The IQR rule used was:

```text
IQR = Q3 - Q1

Lower Bound = Q1 - 1.5 × IQR
Upper Bound = Q3 + 1.5 × IQR
```

## Age Outlier Analysis

For `age`:

- Q1 = 22.0
- Q3 = 35.0
- IQR = 13.0
- Lower bound = 2.5
- Upper bound = 54.5
- IQR outlier count = 65

The observations outside the IQR limits were identified as potential outliers.

## Fare Outlier Analysis

For `fare`:

- Q1 = 7.8958
- Q3 = 31.0
- IQR = 23.1042
- Lower bound = -26.7605
- Upper bound = 65.6563
- IQR outlier count = 114

The fare distribution contained several high-value observations.

The identified outliers were retained because they represent actual observations in the dataset and are useful for understanding the distribution.

---

# 5. Fare Mean, Median, Mode and Skewness

The following statistics were calculated for `fare`:

| Statistic | Value |
|---|---:|
| Mean | 32.0967 |
| Median | 14.4542 |
| Mode | 8.0500 |
| Skewness | 4.8014 |

The mean fare of 32.0967 is substantially higher than the median of 14.4542 and the mode of 8.0500.

The skewness value of 4.8014 indicates strong positive/right skewness.

The difference between the mean, median, and mode shows that a relatively small number of high-fare observations pull the mean upward.

Therefore, the median and mode provide a better representation of a typical fare than the mean because the mean is strongly influenced by extreme high-fare observations.

---

# 6. Bivariate Survival Analysis

Survival rates were calculated by:

- Sex
- Passenger class
- Sex and passenger class

## Survival Rate by Sex

| Sex | Survival Rate (%) |
|---|---:|
| Female | 74.04 |
| Male | 18.89 |

Female passengers had a substantially higher observed survival rate than male passengers.

## Survival Rate by Passenger Class

| Passenger Class | Survival Rate (%) |
|---|---:|
| 1 | 62.62 |
| 2 | 47.28 |
| 3 | 24.24 |

Observed survival rates decreased from first class to third class.

## Survival Rate by Sex and Passenger Class

| Sex | Passenger Class | Survival Rate (%) |
|---|---:|---:|
| Female | 1 | 96.74 |
| Female | 2 | 92.11 |
| Female | 3 | 50.00 |
| Male | 1 | 36.89 |
| Male | 2 | 15.74 |
| Male | 3 | 13.54 |

### Interpretation

Survival rates differed substantially by sex and passenger class.

Female passengers had a survival rate of 74.04%, compared with 18.89% for male passengers.

Survival also varied by passenger class, with rates of 62.62% for first class, 47.28% for second class, and 24.24% for third class.

The combined analysis showed that female first-class passengers had the highest observed survival rate at 96.74%, followed by female second-class passengers at 92.11%.

Female third-class passengers had a survival rate of 50.00%, while male passengers had lower survival rates across all three classes, ranging from 36.89% in first class to 13.54% in third class.

These results show strong associations between sex, passenger class, and survival in this dataset. These are observational relationships and do not by themselves establish causation.

---

# 7. Correlation Analysis

A correlation matrix and heatmap were created using exactly the following six numerical variables:

```text
survived
pclass
age
sibsp
parch
fare
```

The variables `adult_male` and `alone` were explicitly excluded from the correlation analysis.

## Correlation Matrix

| | survived | pclass | age | sibsp | parch | fare |
|---|---:|---:|---:|---:|---:|---:|
| survived | 1.0000 | -0.3355 | -0.0698 | -0.0340 | 0.0832 | 0.2553 |
| pclass | -0.3355 | 1.0000 | -0.3365 | 0.0817 | 0.0168 | -0.5482 |
| age | -0.0698 | -0.3365 | 1.0000 | -0.2325 | -0.1715 | 0.0937 |
| sibsp | -0.0340 | 0.0817 | -0.2325 | 1.0000 | 0.4145 | 0.1609 |
| parch | 0.0832 | 0.0168 | -0.1715 | 0.4145 | 1.0000 | 0.2175 |
| fare | 0.2553 | -0.5482 | 0.0937 | 0.1609 | 0.2175 | 1.0000 |

## Two Strongest Absolute Off-Diagonal Correlations

The two strongest absolute off-diagonal correlations were:

1. `pclass` and `fare`: r = -0.5482
2. `sibsp` and `parch`: r = 0.4145

### Interpretation

The correlation between `pclass` and `fare` is moderately negative.

Higher numerical passenger-class values are generally associated with lower fares. This is consistent with the Titanic coding where first class is represented by 1 and third class by 3, meaning higher-class passengers generally paid higher fares.

The correlation between `sibsp` and `parch` is moderately positive.

Passengers travelling with more siblings/spouses also tended to travel with more parents/children.

These correlations describe associations between variables and do not establish causation.

---

# 8. Multivariate Analysis

At least four multivariate visualizations were created.

## Chart 1 — Survival Rate by Sex and Passenger Class

Female passengers had substantially higher observed survival rates than male passengers across all passenger classes.

Female first- and second-class passengers had survival rates above 90%, while female third-class passengers had a survival rate of 50.00%.

Male survival rates were considerably lower, particularly in second and third class.

## Chart 2 — Age Distribution by Survival Status and Sex

The age distributions show differences between survivors and non-survivors across sex groups.

The distributions also show substantial overlap between survival groups, indicating that age alone does not completely separate survival outcomes.

The presence of outliers in several groups also demonstrates the broad age range of passengers.

## Chart 3 — Fare Distribution by Passenger Class and Survival

Fare values varied strongly across passenger classes.

First-class passengers generally had higher fares, while third-class passengers generally had lower fares.

Surviving passengers also showed higher fare distributions in several passenger classes, although substantial overlap remained between survivors and non-survivors.

## Chart 4 — Age vs Fare by Survival Status and Passenger Class

The scatter plot shows that many observations are concentrated at relatively low fare values, while a smaller number of observations have substantially higher fares.

The observations are distributed across different ages and survival outcomes.

Passenger class adds another dimension to the relationship between age, fare, and survival, showing that these variables interact rather than acting independently.

---

# 9. Age and Fare Standardization

Z-score standardization was applied to `age` and `fare` using the full cleaned dataset as an EDA sanity check.

## Before Standardization

| Variable | Mean |
|---|---:|
| Age | 29.3152 |
| Fare | 32.0967 |

## After Standardization

| Variable | Mean | Standard Deviation |
|---|---:|---:|
| Age | 2.71e-16 | 1.000563 |
| Fare | 1.40e-16 | 1.000563 |

Both means were effectively zero and both standard deviations were approximately one.

This confirms that the z-score standardization was successfully applied.

The standardized variables were used only for EDA validation.

They were not used as the modeling preprocessing pipeline.

The modeling pipeline independently fits preprocessing transformations using the training data only.

---

# Part B — Machine Learning Modeling

# 10. Stratified Train/Test Split

The target variable `survived` contained:

| Class | Count | Percentage |
|---|---:|---:|
| Not Survived (0) | 549 | 61.62% |
| Survived (1) | 342 | 38.38% |

Because the target classes were not evenly distributed, a stratified train/test split was used.

The dataset was divided using:

```python
train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)
```

This produced:

- Training observations: 712
- Test observations: 179

## Training Class Balance

| Class | Percentage |
|---|---:|
| Not Survived (0) | 61.66% |
| Survived (1) | 38.34% |

## Test Class Balance

| Class | Percentage |
|---|---:|
| Not Survived (0) | 61.45% |
| Survived (1) | 38.55% |

The similar proportions confirm that stratification preserved the observed target-class distribution in both subsets.

---

# 11. Preprocessing Pipeline

Preprocessing was fitted only on the training data to avoid data leakage.

The numerical features were:

```text
age
sibsp
parch
fare
```

The categorical features were:

```text
sex
embarked
class
who
adult_male
alone
```

## Numerical Preprocessing

Numerical variables were processed using:

1. Median imputation
2. StandardScaler

## Categorical Preprocessing

Categorical variables were processed using:

1. Most-frequent imputation
2. OneHotEncoder with unknown-category handling

A `ColumnTransformer` was used to combine the numerical and categorical transformations.

The preprocessing object was fitted only on:

```text
X_train
```

It was then used to transform both:

```text
X_train
X_test
```

The processed datasets contained:

- Training shape: `(712, 19)`
- Test shape: `(179, 19)`

The same number of processed features was confirmed for both datasets.

This design prevents information from the test set from influencing preprocessing.

---

# 12. Classification Models

Three classification algorithms were trained using the same stratified train/test split and identical preprocessing:

1. Logistic Regression
2. Decision Tree
3. Random Forest

## Logistic Regression

Logistic Regression was trained with:

```python
LogisticRegression(
    max_iter=1000,
    random_state=42
)
```

## Decision Tree

A Decision Tree classifier was trained and visualized using `plot_tree`.

The tree was rendered with:

- Feature names
- Class names
- Node information
- Gini impurity
- Sample counts

## Random Forest

A Random Forest classifier was trained using the same processed training data.

---

# 13. Classification Evaluation

Each model was evaluated using:

- Confusion matrix
- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC

## Confusion Matrices

### Logistic Regression

```text
[[98 12]
 [17 52]]
```

### Decision Tree

```text
[[92 18]
 [18 51]]
```

### Random Forest

```text
[[97 13]
 [21 48]]
```

## Classification Comparison

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.8380 | 0.8125 | 0.7536 | 0.7820 | 0.8685 |
| Decision Tree | 0.7989 | 0.7391 | 0.7391 | 0.7391 | 0.7769 |
| Random Forest | 0.8101 | 0.7869 | 0.6957 | 0.7385 | 0.8372 |

The three models produced different performance across all evaluation metrics.

---

# 14. Class Imbalance Analysis

The training data contained:

- 439 non-survivors
- 273 survivors

This indicates moderate class imbalance.

Three Logistic Regression approaches were compared:

1. Baseline
2. `class_weight="balanced"`
3. SMOTE applied only to the training data

## Class Imbalance Comparison

| Method | Precision | Recall | F1 |
|---|---:|---:|---:|
| Baseline | 0.8125 | 0.7536 | 0.7820 |
| class_weight='balanced' | 0.7671 | 0.8116 | 0.7887 |
| SMOTE | 0.7632 | 0.8406 | 0.8000 |

SMOTE produced the highest recall at 0.8406 and the highest F1-score at 0.8000.

The baseline produced the highest precision at 0.8125.

The class-weighted model increased recall to 0.8116 compared with the baseline, while precision decreased to 0.7671.

SMOTE increased recall and F1-score while reducing precision.

Therefore, the imbalance analysis demonstrates the trade-off between precision and recall when different imbalance-handling strategies are applied.

---

# 15. Random Forest GridSearchCV and OOB Score

GridSearchCV was applied to the Random Forest classifier.

The hyperparameters searched were:

- `n_estimators`
- `max_depth`
- `max_features`

The best parameters obtained were:

```text
max_depth = 5
max_features = 'sqrt'
n_estimators = 100
```

The best cross-validation F1-score was:

```text
0.7494
```

The best Random Forest model used out-of-bag evaluation with:

```text
oob_score=True
```

The resulting OOB score was:

```text
0.8272
```

---

# 16. Multivariate Linear Regression

A multivariate Linear Regression model was used to predict `fare` from the other available features.

The model was evaluated using:

- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)
- R²
- Adjusted R²

## Regression Results

| Metric | Linear Regression |
|---|---:|
| MAE | 16.4640 |
| RMSE | 41.8471 |
| R² | 0.4353 |
| Adjusted R² | 0.3718 |

The R² value of 0.4353 indicates that the model explains a moderate proportion of the variation in fare.

The adjusted R² of 0.3718 accounts for the number of predictors included in the model.

---

# 17. Residual Analysis and Heteroscedasticity

A residual plot was created using predicted fare values on the x-axis and residuals on the y-axis.

The residual spread was not constant across the range of predicted fare values.

At lower predicted fares, the residuals were relatively concentrated around zero.

At higher predicted fares, the residuals showed substantially greater dispersion and several large positive values.

This widening spread indicates evidence of heteroscedasticity, meaning that the variance of the regression errors changes with the predicted fare.

Therefore, the constant-variance assumption of ordinary linear regression is not fully satisfied for this model.

The presence of several extreme residuals also suggests that high-fare observations have a strong influence on prediction errors.

---

# 18. Final Model Comparison

## Classification Metrics

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.8380 | 0.8125 | 0.7536 | 0.7820 | 0.8685 |
| Decision Tree | 0.7989 | 0.7391 | 0.7391 | 0.7391 | 0.7769 |
| Random Forest | 0.8101 | 0.7869 | 0.6957 | 0.7385 | 0.8372 |

## Regression Metrics

| Model | MAE | RMSE | R² | Adjusted R² |
|---|---:|---:|---:|---:|
| Linear Regression | 16.4640 | 41.8471 | 0.4353 | 0.3718 |

Classification and regression metrics are reported separately because they measure different prediction tasks and are not directly comparable on a single scale.

---

# 19. Final Model Recommendation

The three classification models produced different test-set results.

Logistic Regression achieved an accuracy of 0.8380, precision of 0.8125, recall of 0.7536, F1-score of 0.7820, and ROC-AUC of 0.8685.

Decision Tree achieved an accuracy of 0.7989, precision of 0.7391, recall of 0.7391, F1-score of 0.7391, and ROC-AUC of 0.7769.

Random Forest achieved an accuracy of 0.8101, precision of 0.7869, recall of 0.6957, F1-score of 0.7385, and ROC-AUC of 0.8372.

For this experiment, Logistic Regression was selected as the final classification estimator because it produced the highest observed accuracy and ROC-AUC among the three baseline classifiers.

The class-imbalance experiment showed that SMOTE increased recall to 0.8406 and F1-score to 0.8000, while reducing precision to 0.7632.

For the regression task, Linear Regression produced MAE of 16.4640, RMSE of 41.8471, R² of 0.4353, and adjusted R² of 0.3718, with residual analysis showing evidence of heteroscedasticity.

---

# 20. Complete Saved Pipeline

The final classification pipeline combines:

1. Numerical preprocessing
2. Categorical preprocessing
3. Feature transformation
4. Logistic Regression estimator

The complete pipeline was saved as one object using:

```python
joblib.dump(full_pipeline, "outputs/best_titanic_pipeline.joblib")
```

The saved pipeline contains both preprocessing and the final estimator.

The saved file is:

```text
analytics/outputs/best_titanic_pipeline.joblib
```

The pipeline was subsequently reloaded using:

```python
joblib.load(...)
```

The reload was successful.

A prediction was also generated using a new raw passenger record.

Example output:

```text
Pipeline reloaded successfully.
Prediction for new raw passenger: 0
Predicted outcome: Not Survived
```

This confirms that the complete pipeline can be reloaded and used directly on raw input data.

---

# Reproducibility

The analysis uses fixed random states where required.

The train/test split uses:

```text
random_state = 42
```

The same committed `titanic.csv` file is used by the modeling notebook.

The modeling preprocessing is fitted only on the training data.

SMOTE is applied only to the training data.

The complete preprocessing and final estimator are saved together as a Joblib pipeline.

No paid services are required for this module.