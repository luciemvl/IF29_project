
from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans
from sklearn import metrics
import matplotlib.pyplot as plt
import time
import numpy as np

#connect from Mongo DB and import it on pandas
from pymongo import MongoClient
import pandas as pd
client = MongoClient("localhost", 27017)
db = client["IF29"]
collec = db.user_db_pca #whole database
data = pd.DataFrame(list(collec.find()))
id_list = data.pop("_id")
n_split = 10
k = 3
"""
rng = np.random.default_rng(42)
data["partition"] = rng.integers(0,n_split,len(data))
for i in range(n_split):
    X = data.loc[:,"pca0":"pca8"][data.partition == i]
    kmeans = KMeans(n_clusters=k, random_state=42,verbose=0)
    kmeans.fit(X)
    labels = kmeans.labels_"""
X = data.loc[:,"pca0":"pca8"]
kmeans = MiniBatchKMeans(n_clusters=k,verbose=1,random_state=42,max_no_improvement=100)
kmeans.set_output(transform="pandas")
Projection = kmeans.fit_transform(X)
data["partition"] = kmeans.labels_
Centroids = pd.DataFrame(kmeans.cluster_centers_)

#Plot kmeans results
plt.scatter(X["pca0"],X["pca1"],c = data.partition,s=0.5)
plt.scatter(Centroids.loc[:,0],Centroids.loc[:,1],c="red",label="centroids")
plt.title("Clusters centroids and repartition")
plt.xlabel('Première composante principale')
plt.ylabel('Deuxième composante principale')
plt.xlim(-5,50)
plt.ylim(-20,20)
plt.legend()
plt.savefig("./images/4_1.minikmeans_representation.png")
plt.show()

