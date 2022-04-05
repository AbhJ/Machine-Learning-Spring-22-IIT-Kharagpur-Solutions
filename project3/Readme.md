# Readme for Project 3

### Submitted by Abhijay Mitra (18IE10001)

## Instructions to run the file

 - The code is submitted as a single python3 file **`18IE10001_p3.py`** which can be run on any machine with the libraries installed with the command:
	 **`python3 18IE10001_p3.py`**.
 - The libraries used in the program are math, numpy, matplotlib, random and pandas and have been solely used for the purpose of import and extraction of data, and printing data in an orderly fashion. All necessary functions and methods for the purpose of the project have been self generated.
 - In case of difficulty to run the code with the github links for extracting the training and test data (line 11) due to internet or server issues, feel free to use any offline copy of the same.
 - In the functions **`dist`** and **`clusterMean`** non categorical data types and categorical data types have been handled separately as the distances for non categorical data types cannot be calculated as such and requires special handling.

 ## Detailed explanations to the major functions/methods in the code

 - **`initializer`**: This method randomly initializes K points as cluster centers before the iteration. We make use of the random library in python for the same.
 - **`clusterMean`**: This method takes as input a cluster of points and returns the mean (centroid) of the cluster.
 - **`KMeans`**: This method applies KMeans to find out the centroids and categorize the data points with their custers. For every iteration it finds out new centroids of the k clusters.
 - **`print_helper`**: This method is a helper function to print the cluster label of eea of the test data.

## Contact

In case of any further queries feel free to contact

 - Abhijay Mitra
