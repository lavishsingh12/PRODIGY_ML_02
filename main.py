import pandas as pd
import matplotlib.pyplot as plt  # For plotting graphs
import seaborn as sns  # For better-looking graphs
from sklearn.cluster import KMeans  # For clustering
from sklearn.preprocessing import StandardScaler  # For scaling values

# Loading the customer detail fil
df = pd.read_csv("Mall_Customers.csv")
print("Details of first 5 customers:")
print(df.head(5))

# We are renaming column names for easir access for our model
df.rename(
    columns={
        "Annual Income (k$)": "Annual_Income",
        "Spending Score (1-100)": "Spending_Score",
    },
    inplace=True,
)

# Selecting features we want to use for clustering
X = df[["Annual_Income", "Spending_Score"]]

# Scale the data to make both features equally important
scaler = StandardScaler()  # Create the scaler
X_scaled = scaler.fit_transform(X)  # Fit and transform the data

# Use Elbow Method to find the best number of clusters
wcss = []  # WCSS = Within-Cluster Sum of Squares (total distance from center)
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, random_state=42)
    kmeans.fit(X_scaled)
    wcss.append(kmeans.inertia_)

# Plotting the elbow graph
plt.figure(figsize=(8, 5))
plt.plot(range(1, 11), wcss, marker="o")
plt.title("Elbow Method - Optimal Number of Clusters")
plt.xlabel("Number of Clusters")
plt.ylabel("WCSS")
plt.grid(True)
plt.show()

# Apply K-Means with the chosen number of clusters (from elbow plot, usually 5)
kmeans = KMeans(n_clusters=5, random_state=42)
df["Cluster"] = kmeans.fit_predict(X_scaled)  # Predict cluster for each customer

# Visualize the clusters
plt.figure(figsize=(8, 5))
sns.scatterplot(
    x="Annual_Income", y="Spending_Score", hue="Cluster", data=df, palette="Set1"
)
plt.title("Customer Segments")
plt.xlabel("Annual Income (k$)")
plt.ylabel("Spending Score (1-100)")
plt.legend(title="Cluster")
plt.grid(True)
plt.show()

# Show the average income and score for each cluster
print("Average income and spending score for each cluster:")
print(df.groupby("Cluster")[["Annual_Income", "Spending_Score"]].mean().round(3))
