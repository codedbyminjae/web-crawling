# ---------------------------------------------
# 12장 군집분석: 소비자 K-평균 클러스터링 전체 코드
# PyCharm 단일 파일 실행용 (.py)
# ---------------------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn.preprocessing import StandardScaler
import matplotlib.cm as cm

# ---------------------------------------------
# 1. 데이터 로드
# ---------------------------------------------
file_path = "Online_Retail.xlsx"   # ★ 너의 경로로 수정 필요

retail_df = pd.read_excel(file_path)
print(retail_df.head())

# ---------------------------------------------
# 2. 데이터 정제
# ---------------------------------------------
# CustomerID 없는 행 제거
retail_df = retail_df[retail_df['CustomerID'].notnull()]

# Quantity, UnitPrice 음수 제거
retail_df = retail_df[(retail_df['Quantity'] > 0) & (retail_df['UnitPrice'] > 0)]

# CustomerID 정수형 변환
retail_df['CustomerID'] = retail_df['CustomerID'].astype(int)

# 중복 제거
retail_df = retail_df.drop_duplicates()

print(retail_df.info())

# ---------------------------------------------
# 3. 분석용 변수 생성
# ---------------------------------------------
# 주문금액 SaleAmount = UnitPrice × Quantity
retail_df["SaleAmount"] = retail_df["UnitPrice"] * retail_df["Quantity"]

# 고객별 집계
customer_df = retail_df.groupby("CustomerID").agg({
    "InvoiceNo": "count",
    "SaleAmount": "sum",
    "InvoiceDate": "max"
}).reset_index()

customer_df.columns = ["CustomerID", "Freq", "SaleAmount", "LastPurchaseDate"]

# 기준 날짜
ref_date = pd.to_datetime("2011-12-10")
customer_df["ElapsedDays"] = (ref_date - customer_df["LastPurchaseDate"]).dt.days

# ---------------------------------------------
# 4. 로그 변환
# ---------------------------------------------
customer_df["Freq_log"] = np.log1p(customer_df["Freq"])
customer_df["SaleAmount_log"] = np.log1p(customer_df["SaleAmount"])
customer_df["ElapsedDays_log"] = np.log1p(customer_df["ElapsedDays"])

# ---------------------------------------------
# 5. 스케일링
# ---------------------------------------------
X_features = customer_df[["Freq_log", "SaleAmount_log", "ElapsedDays_log"]]
scaler = StandardScaler()
X_features_scaled = scaler.fit_transform(X_features)

# ---------------------------------------------
# 6. 엘보 기법으로 k 선택
# ---------------------------------------------
distortions = []
K_range = range(1, 11)

for k in K_range:
    model = KMeans(n_clusters=k, random_state=42)
    model.fit(X_features_scaled)
    distortions.append(model.inertia_)

plt.figure(figsize=(8, 5))
plt.plot(K_range, distortions, marker='o')
plt.xlabel("K (클러스터 개수)")
plt.ylabel("Distortion")
plt.title("Elbow Method")
plt.show()

# ---------------------------------------------
# 7. K=3 예시 모델 학습
# ---------------------------------------------
k = 3
kmeans = KMeans(n_clusters=k, random_state=42)
Y_labels = kmeans.fit_predict(X_features_scaled)

customer_df["ClusterLabel"] = Y_labels
print(customer_df.head())

# ---------------------------------------------
# 8. 시각화 함수 정의
# ---------------------------------------------
def silhouetteViz(n_cluster, X_features_scaled, Y_labels):
    silhouette_vals = silhouette_samples(X_features_scaled, Y_labels)
    y_ax_lower = 10
    yticks = []

    for i in range(n_cluster):
        vals = silhouette_vals[Y_labels == i]
        vals.sort()
        y_ax_upper = y_ax_lower + len(vals)

        color = cm.jet(float(i) / n_cluster)
        plt.barh(range(y_ax_lower, y_ax_upper), vals,
                 height=1.0, edgecolor='none', color=color)

        yticks.append((y_ax_lower + y_ax_upper) / 2)
        y_ax_lower = y_ax_upper + 10

    silhouette_avg = np.mean(silhouette_vals)

    plt.axvline(silhouette_avg, color="red", linestyle='--')
    plt.yticks(yticks, [str(i) for i in range(n_cluster)])
    plt.xlabel("Silhouette coefficient")
    plt.ylabel("Cluster")
    plt.title(f"Silhouette Plot: k={n_cluster}")

    plt.show()


def clusterScatter(n_cluster, X_features_scaled, Y_labels):
    kmeans = KMeans(n_clusters=n_cluster, random_state=42)
    kmeans.fit(X_features_scaled)

    centers = kmeans.cluster_centers_

    plt.figure(figsize=(7, 6))
    plt.scatter(X_features_scaled[:, 0], X_features_scaled[:, 1],
                c=Y_labels, cmap="viridis", s=5)
    plt.scatter(centers[:, 0], centers[:, 1], marker="^", s=200, c="red")

    plt.xlabel("Freq_log (scaled)")
    plt.ylabel("SaleAmount_log (scaled)")
    plt.title(f"Cluster Scatter Plot: k={n_cluster}")
    plt.show()

# ---------------------------------------------
# 9. K=3,4,5,6 비교 (실루엣 + 분포)
# ---------------------------------------------
for k in [3, 4, 5, 6]:
    model = KMeans(n_clusters=k, random_state=42)
    Y = model.fit_predict(X_features_scaled)

    silhouetteViz(k, X_features_scaled, Y)
    clusterScatter(k, X_features_scaled, Y)

# ---------------------------------------------
# 10. 최종 선택된 k=4 적용
# ---------------------------------------------
final_k = 4
final_model = KMeans(n_clusters=final_k, random_state=42)
customer_df["ClusterLabel"] = final_model.fit_predict(X_features_scaled)

# CSV 저장
customer_df.to_csv("customer_cluster_final.csv", index=False)
print("📁 customer_cluster_final.csv 저장 완료!")

# ---------------------------------------------
# 11. 추가 분석
# ---------------------------------------------
customer_cluster_df = customer_df.copy()
customer_cluster_df["SaleAmountAvg"] = (
    customer_cluster_df["SaleAmount"] / customer_cluster_df["Freq"]
)

cluster_summary = customer_cluster_df.drop(
    ["Freq_log", "SaleAmount_log", "ElapsedDays_log"], axis=1
).groupby("ClusterLabel").mean()

print(cluster_summary)
