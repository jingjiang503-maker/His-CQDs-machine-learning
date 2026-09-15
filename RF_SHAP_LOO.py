import pandas as pd
import numpy as np
import shap
import pywt
from scipy.signal import find_peaks, savgol_filter
from scipy.stats import skew, kurtosis
from sklearn.model_selection import LeaveOneOut
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error
import matplotlib.pyplot as plt

# load data
def ultimate_fused_pipeline_full(file_path='raw_data.xlsx'):
    xl = pd.ExcelFile(file_path, engine='openpyxl')
    X_list, y_list = [], []
    for i in range(1, 10):
        sheet_name = f'{i / 10:.1f}TU'
        if sheet_name in xl.sheet_names:
            df = pd.read_excel(xl, sheet_name=sheet_name, header=None)
            for col in [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31]:
                if col < df.shape[1]:
                    data = df.iloc[:, col].values
                    X_list.append(data[~pd.isna(data)])
                    y_list.append(i / 10)
    X = np.array([x[:min(len(x) for x in X_list)] for x in X_list], dtype=np.float32)
    y = np.array(y_list, dtype=np.float32)
    X_norm = X / (np.max(X, axis=1, keepdims=True) + 1e-8)

    # feature extraction
    feature_names = ['Mean', 'Std', 'Skew', 'Kurt', 'MaxD1', 'MinD1', 'MaxD2', 'MinD2',
                     'Cog', 'AUC', 'PeakCount', 'PeakDist', 'FWHM', 'MaxInt',
                     'Wave_1', 'Wave_2', 'Wave_3', 'Wave_4', 'Wave_5', 'Wave_6',
                     'Slope_Mean', 'Energy', 'Entropy', 'Curvature']

    features = []
    for s in X_norm:
        mean, std, sk, kurt = np.mean(s), np.std(s), skew(s), kurtosis(s)
        d1 = savgol_filter(s, 15, 2, deriv=1)
        d2 = savgol_filter(s, 15, 2, deriv=2)
        peaks, _ = find_peaks(s, height=0.2)
        cog = np.sum(np.arange(len(s)) * s) / (np.sum(s) + 1e-8)

        coeffs = pywt.wavedec(s, 'db4', level=5)
        wave = [np.mean(c ** 2) for c in coeffs[:6]]

        f = [mean, std, sk, kurt, np.max(d1), np.min(d1), np.max(d2), np.min(d2), cog,
             np.trapz(s), len(peaks), (peaks[1] - peaks[0] if len(peaks) > 1 else 0),
             np.sum(s > (np.max(s) * 0.5)), np.max(s)] + wave + [np.mean(d1), np.sum(s ** 2),
                                                                 -np.sum(s * np.log(s + 1e-8)), np.mean(d2)]
        features.append(f)

    X_feats = pd.DataFrame(features, columns=feature_names)
    X_scaled = StandardScaler().fit_transform(X_feats)

    # model development
    model = RandomForestRegressor(n_estimators=500, max_depth=6, random_state=42).fit(X_scaled, y)

    # feature selection
    explainer = shap.TreeExplainer(model)
    shap_values = explainer(X_scaled)
    plt.figure(figsize=(10, 8))
    shap.summary_plot(shap_values, X_scaled, feature_names=feature_names, show=False, max_display=24)
    plt.title("SHAP Feature Importance (All 24 Features)")
    plt.savefig("SHAP_Importance.png", dpi=300, bbox_inches='tight')
    plt.show()

    global_shap = np.abs(shap_values.values).mean(0)
    top_indices = np.argsort(global_shap)[-5:][::-1]

    # model evaluation: Leave one out
    best_features = X_scaled[:, top_indices]
    y_preds = []
    for train_idx, test_idx in LeaveOneOut().split(best_features):
        model.fit(best_features[train_idx], y[train_idx])
        y_preds.append(model.predict(best_features[test_idx])[0])

    acc = np.mean(np.abs(y - np.array(y_preds)) < 0.1)
    print(f"R²: {r2_score(y, y_preds):.4f}")
    print(f"MAE: {mean_absolute_error(y, y_preds):.4f}")
    print(f"accuracy(error < 0.1 TU): {acc:.4f}")

    results = pd.DataFrame({'True_TU': y, 'Pred_TU': y_preds, 'Error': np.abs(y - y_preds)})
    print("\n")
    print(results.to_string())
    results.to_excel("Prediction_Results.xlsx", index=False)

    plt.figure(figsize=(8, 6))
    plt.scatter(y, y_preds, c=np.abs(y - np.array(y_preds)), cmap='RdYlGn_r', alpha=0.7)
    plt.plot([0.1, 0.9], [0.1, 0.9], 'r--')
    plt.xlabel('True TU')
    plt.ylabel('Predicted TU')
    plt.title(f'True vs Predicted (R²={r2_score(y, y_preds):.3f})')
    plt.colorbar(label='Absolute Error')
    plt.savefig("prediction results.png", dpi=300, bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    ultimate_fused_pipeline_full()