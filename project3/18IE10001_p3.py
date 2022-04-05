# Roll Number:       18IE10001
# Name:              Abhijay Mitra
# Assignment Number: 3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import math

data = pd.read_csv(
    r"https://raw.githubusercontent.com/AbhJ/Machine-Learning-Spring-22-IIT-Kharagpur/master/Project3.csv"
)
sample = data.copy()
rows = len(data)
cols = len(data.columns)


# Replacing data with the z scores
sample["Age"] = np.divide(
    np.subtract(np.array(sample["Age"]), np.mean(sample["Age"])),
    np.std(sample["Age"]),
)
sample["Income"] = np.divide(
    np.subtract(np.array(sample["Income"]), np.mean(sample["Income"])),
    np.std(sample["Income"]),
)


def dist(A, B):
    # This method returns the distance between two data points
    distance = 0
    for i in range(1, len(A)):
        # Iterating through all the columns in the data point
        if i in [3, 5]:
            # Non categorical data type
            distance += (A[i] - B[i]) ** 2
        else:
            # Categorical data type
            distance += A[i] != B[i]
    return math.sqrt(distance)


# Apply KMeans to find out the centroids and categorize the data points with their custers
def KMeans(iterationsCount, K):
    cluster = {}
    Centroids = initializer(K)
    for it in range(iterationsCount):
        # For every iteration, find out new centroids
        for i in range(K):
            cluster[i + 1] = []
        for i in range(rows):
            trainRow = sample.iloc[i]
            D = []
            for C in Centroids:
                D.append(dist(trainRow, C))
            clusterNo = np.argmin(D) + 1
            cluster[clusterNo].append(trainRow)
        for key in cluster:
            Centroids[key - 1] = clusterMean(cluster[key])
    return cluster


def initializer(K):
    # Randomly initialize K points as cluster centers before the iteration
    Centroids = []
    X = sample.iloc[:].values
    randomPoints = []
    while len(randomPoints) < K:
        rand = random.randint(0, rows - 1)
        if rand not in randomPoints:
            randomPoints.append(rand)
    for i in randomPoints:
        Centroids.append(X[i])
    return Centroids


def clusterMean(arr):
    # arr is a cluster of points whose mean (center) will be returned from this function
    arrLength = len(arr)
    clusterMean = [0 for i in range(8)]
    if arrLength == 0:
        return clusterMean
    for i in range(1, cols):
        if i in [3, 5]:
            # Non categorical data type
            total = 0
            for c in arr:
                total += c[i]
            clusterMean[i] = total / arrLength
        else:
            # Categorical data type
            # The mean of categorical or nominal data types is the mode
            v = []
            for c in arr:
                v.append(c[i])
            clusterMean[i] = np.bincount(v).argmax()
    return clusterMean


def printingHelper(cluster):
    data = {}
    for key in cluster:
        for dataPoint in cluster[key]:
            data[dataPoint.ID] = key
    printList = []
    print("The file 18IE10001_P3.out is being generated.")
    for i in range(len(sample)):
        print(data[sample.iloc[i].ID], end=" ")
        printList.append(str(data[sample.iloc[i].ID]))
    with open("18IE10001_P3.out", mode="wt", encoding="utf-8") as myfile:
        myfile.write(" ".join(printList))
    print("\nThe file 18IE10001_P3.out has been generated.")


# Calculating the Mean Squared Error per cluster
def ClusterMSE(cluster):
    distance = 0
    for k in cluster:
        centroid = clusterMean(cluster[k])
        for data in cluster[k]:
            distance += dist(centroid, data) ** 2
    return distance


while 1:
    input_char = input(
        "Print for only optimal k? (Press 'Y' for Yes and 'N' for No and hit Return/Enter): "
    )
    if input_char.upper() == "N":
        print(
            "The optimal value of k is 16.\nIt has been found out by plotting the graph of MSE with k.\nNow, let us see the output for other values too.\nIterating over k from 1 to 299"
        )
        MSEList = []
        for i in range(1, 45):
            print("Now at k = ", i)
            MSEList.append(ClusterMSE(KMeans(50, i)))
        k = [i for i in range(1, 45)]
        plt.plot(k, MSEList)
    elif input_char.upper() == "Y":
        printingHelper(KMeans(50, 16))
    else:
        continue
    break
