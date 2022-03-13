import pandas as pd
import numpy as np
import math


# Function to calculate VDM with x and y as the values of the attributes.
def vdm(traindb, index, x, y):
    c = data["target"].unique()
    dist = 0
    if x == y:
        return 0
    for cl in c:
        n_axc, n_ayc, n_ax, n_ay = 0, 0, 0, 0
        for i in range(len(traindb[index])):
            if traindb[index][i] == x:
                n_ax += 1
            if traindb[index][i] == y:
                n_ay += 1
            if traindb["target"][i] == cl and traindb[index][i] == x:
                n_axc += 1
            if traindb["target"][i] == cl and traindb[index][i] == y:
                n_ayc += 1
        dist += ((n_axc / n_ax) - (n_ayc / n_ay)) ** 2
    return dist


# Create training row
def training_row(dataPrime, i):
    trainRow = []
    for x in dataPrime.columns:
        if x != "target":
            trainRow.append(dataPrime[x][i])
    return trainRow


# Creating a list of lists of distance
def get_distance_list(dataPrime, test):
    distanceList = []
    dist = 0
    for i in dataPrime.index:
        # Creating a list of distance for every test case in the dataset
        trainRow = training_row(dataPrime, i)
        dist = 0
        qnt = [0, 3, 4, 7, 9]
        for j in range(len(trainRow)):
            if j in qnt:
                dist += (trainRow[j] - test[j]) ** 2
                continue
            l = [trainRow[j], test[j]]
            l.sort()
            tup = (*l,)
            if (j, tup) not in VDM:
                VDM[j, tup] = vdm(dataPrime, dataPrime.columns[j], trainRow[j], test[j])
                dist += VDM[j, tup] ** 2
            else:
                dist += VDM[j, tup] ** 2
        dist = math.sqrt(dist)
        distanceList.append((i, dist))
    distanceList.sort(key=lambda tup: tup[1])
    return distanceList


def list_of_neighbors(dist_list, cntNeighbors):
    neighbors = []
    for i in range(cntNeighbors):
        neighbors.append(dist_list[i][0])
    return neighbors


# Returns boolean value to indicate majority voting
def is_the_majority_voting(data, lst):
    p, N = 0, len(lst)
    for i in lst:
        if data["target"][i]:
            p += 1
    if p <= N - p:
        return 0
    return 1


data = pd.read_csv(
    r"https://raw.githubusercontent.com/AbhJ/Machine-Learning-Spring-22-IIT-Kharagpur/master/project2.csv"
)
test = pd.read_csv(
    r"https://raw.githubusercontent.com/AbhJ/Machine-Learning-Spring-22-IIT-Kharagpur/master/project2_test.csv"
)
db = {}
VDM = {}
qnt = [0, 3, 4, 7, 9]
for i in qnt:
    db[i] = (np.mean(data[data.columns[i]]), np.std(data[data.columns[i]]))
dataPrime = data.copy()
for i in ["chol", "trestbps", "age", "thalach", "oldpeak"]:
    # Replacing data with the z scores
    dataPrime[i] = np.divide(
        np.subtract(np.array(dataPrime[i]), np.mean(dataPrime[i])), np.std(dataPrime[i])
    )
for i in qnt:
    test[test.columns[i]] = np.divide(
        np.subtract(np.array(test[test.columns[i]]), db[i][0]), db[i][1]
    )
for k in range(1, 300):
    print("{0:03}".format(k), ": ", end="")
    for i in test.index:
        testRow = []
        for x in test.columns:
            testRow.append(test[x][i])
        print(
            is_the_majority_voting(
                dataPrime, list_of_neighbors(get_distance_list(dataPrime, testRow), k)
            ),
            end=" ",
        )
    print()
