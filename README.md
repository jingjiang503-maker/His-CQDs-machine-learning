# Machine Learning-Assisted Toxicity Prediction Using His-CQDs Spectroscopic Sensor


## Overview

This repository contains the machine learning algorithm developed for predicting aquatic toxicity based on the spectral response of histidine-functionalized carbon quantum dots (His-CQDs).

The workflow establishes a nonlinear relationship between His-CQDs spectral response patterns and toxicity units (TU) through spectral feature extraction, machine learning regression, and model interpretation.

The complete pipeline includes:

- Spectral data loading and preprocessing
- Signal normalization
- Spectral feature extraction
- Feature standardization
- Random forest regression modeling
- SHAP-based feature interpretation
- Feature selection
- Leave-one-out cross-validation (LOOCV)
- Toxicity unit prediction


---

# Workflow


```
His-CQDs spectral response

            ↓

Spectral normalization

            ↓

Extraction of 24 spectral features

            ↓

Feature standardization

            ↓

Random Forest regression

            ↓

SHAP feature importance analysis

            ↓

Selection of top contributing features

            ↓

LOOCV model evaluation

            ↓

Predicted toxicity unit (TU)
```


---

# Dataset Description


## Input Data

The input file is:

```
raw_data.xlsx
```


The Excel file contains His-CQDs spectral responses collected under different toxicity levels.

The calibration dataset contains toxicity levels from:

```
0.1 TU to 0.9 TU
```


Each toxicity level is stored in an individual worksheet:

```
0.1TU
0.2TU
0.3TU
...
0.9TU
```


Each worksheet contains multiple spectral response curves.

The algorithm automatically extracts spectral signals, assigns corresponding TU labels, and constructs the training dataset.


---

# Spectral Preprocessing


## Signal Normalization


Each spectral response curve is normalized using:


```
Normalized signal = Signal intensity / Maximum signal intensity
```


Normalization reduces the influence of absolute signal intensity variation between samples and emphasizes the intrinsic response pattern of the His-CQDs sensor.


---

# Feature Extraction


A total of **24 physical spectral features** are extracted from normalized response curves.


## 1. Statistical Features


These features describe the overall distribution characteristics of spectral responses:


- Mean
- Standard deviation (Std)
- Skewness (Skew)
- Kurtosis (Kurt)


---

## 2. Derivative Features


Savitzky-Golay filtering is applied to calculate the first-order and second-order derivatives of spectral curves.


Extracted features:


- MaxD1
- MinD1
- MaxD2
- MinD2


These features describe spectral slope variation and curvature information.


---

## 3. Geometric Features


The following parameters are extracted to characterize spectral morphology:


- Center of gravity (Cog)
- Area under curve (AUC)
- Peak count
- Peak distance
- Full width at half maximum (FWHM)
- Maximum intensity (MaxInt)


---

## 4. Wavelet Features


Wavelet transformation is performed using the Daubechies 4 (db4) wavelet.


Five-level decomposition is applied to extract multi-scale spectral energy information.


Extracted wavelet features:


- Wave_1
- Wave_2
- Wave_3
- Wave_4
- Wave_5
- Wave_6


Additional dynamic features:


- Slope mean
- Energy
- Entropy
- Curvature


---

# Machine Learning Model


## Random Forest Regression


A random forest regression model is used to learn the nonlinear relationship between spectral features and toxicity units.


Model parameters:


```
Number of estimators: 500

Maximum depth: 6

Random state: 42
```


The model is trained using standardized spectral features.


---

# Feature Interpretation and Selection


## SHAP Analysis


SHAP (SHapley Additive exPlanations) is applied to interpret the contribution of each spectral feature to the model prediction.


The global importance of each feature is calculated using the mean absolute SHAP value.


The five most important features are selected according to SHAP contribution values and used for final model evaluation.


Output file:


```
SHAP_Importance.png
```


---

# Model Evaluation


## Leave-One-Out Cross Validation (LOOCV)


LOOCV is applied to evaluate model generalization performance under limited sample conditions.


The procedure includes:


1. One sample is selected as the testing sample.
2. The remaining samples are used for model training.
3. The trained model predicts the excluded sample.
4. The process is repeated until all samples are predicted once.


---

# Evaluation Metrics


Model performance is evaluated using:


## R²

Coefficient of determination


## MAE

Mean absolute error


## Prediction accuracy


Defined as:


```
Prediction error < 0.1 TU
```


---

# Output Files


After running the algorithm, the following files will be generated:


## 1. SHAP Feature Importance


```
SHAP_Importance.png
```


This figure illustrates the contribution of extracted spectral features to TU prediction.


---

## 2. Prediction Results


```
Prediction_Results.xlsx
```


The output file contains:


| Parameter | Description |
|---|---|
| True_TU | Experimental toxicity unit |
| Pred_TU | Machine learning predicted toxicity unit |
| Error | Absolute prediction error |


---

## 3. Prediction Visualization


```
prediction results.png
```


This figure shows the correlation between experimental TU values and predicted TU values.


---

# Requirements


Recommended environment:


```
Python >= 3.10
```


Required packages:


```
pandas

numpy

shap

PyWavelets

scipy

scikit-learn

matplotlib

openpyxl
```


Install dependencies:


```bash
pip install -r requirements.txt
```


---

# Running the Code


Place the input dataset:


```
raw_data.xlsx
```


in the same directory as the Python script.


Run:


```bash
python His-CQDs_ML.py
```


The complete workflow will automatically perform:


- Data loading
- Signal normalization
- Feature extraction
- Feature scaling
- Random forest training
- SHAP analysis
- Feature selection
- LOOCV evaluation
- TU prediction

---

# Citation


If you use this machine learning workflow, please cite:


[Bio-inspired quantum dot spectroscopic sensor enables real-time motioning of aquatic eco-toxicity]


---

# Contact


For questions regarding this project:


[yingzheng.fan@nju.edu.cn]
