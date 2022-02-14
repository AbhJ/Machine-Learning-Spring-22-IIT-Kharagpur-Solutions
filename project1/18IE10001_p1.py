import math, pandas, json


def total_entropy(dataSet):
	# This returns the total Entropy of the 'target' attribute of the data.
	dictionary = dataSet['target'].value_counts()
	totalEntropy = 0
	sizeOfDataset = len(dataSet)
	for count in dictionary:
		probability = count / sizeOfDataset
		# We calculate the Shanon's Entropy contributed by the attribute.
		if probability == 0 or probability == 1:
			continue
		totalEntropy -= probability * math.log2(probability)
	return totalEntropy


def entropy_sum(dictionary, sizeOfDataset):
	entropySum = 0
	for key in dictionary:
		temp = 0
		totalCount = sum(dictionary[key])
		for count in dictionary[key]:
			probability = count / totalCount
			# We calculate the Shanon's Entropy contributed by the attribute.
			if probability == 0 or probability == 1:
				continue
			temp -= probability * math.log2(probability)
		entropySum += (sum(dictionary[key]) / sizeOfDataset) * temp
	return entropySum


def target_attribute_hash(dataSet):
	# This returns a hashmap of classes in the attribute 'target'
	targetAttributeHash = {}
	index = 0
	for row in dataSet['target']:
		if row not in targetAttributeHash:
			targetAttributeHash[row] = index
			index += 1
	return targetAttributeHash


def attribute_for_optimal_splitting_at_node(dataSet):
	# This returns the attribute which will be responsible at the split in the current node.
	# This is found using the information gain of the attributes. The one having the maximum
	# Information gain is the attribute that shall be returned.
	targetAttributeHash = target_attribute_hash(dataSet)
	totalNumberOfClasses = len(targetAttributeHash)
	maxInformationGain = 0
	attribute = 'None'
	entropy = total_entropy(dataSet)
	sizeOfDataset = len(dataSet)
	for i in range(len(dataSet.columns) - 1):
		hashMapOfClassesInAttribute = {}
		for row in dataSet[dataSet.columns[i]]:
			if row not in hashMapOfClassesInAttribute:
				hashMapOfClassesInAttribute[row] = [0] * totalNumberOfClasses
		index = 0
		for row in dataSet[dataSet.columns[i]]:
			hashMapOfClassesInAttribute[row][
				targetAttributeHash[dataSet['target'][index]]
			] += 1
			index += 1
		informationGain = entropy - entropy_sum(
			hashMapOfClassesInAttribute, sizeOfDataset
		)
		if informationGain >= maxInformationGain:
			maxInformationGain = informationGain
			attribute = dataSet.columns[i]
	return attribute


def majority_finding_terminating_case(dataSet):
	dictionary = {}
	# We arrive at this case only if there are are more attributes left and hence
	# Majority class is used to decide the value in the node.
	for row in dataSet['target']:
		if row not in dictionary:
			dictionary[row] = 0
		dictionary[row] += 1
	attribute = 'None'
	majorityClass = 0
	for key in dictionary:
		if dictionary[key] > majorityClass:
			majorityClass = dictionary[key]
			attribute = key
	return attribute


def single_class_terminating_case(dataSet):
	classValue = dataSet['target'][0]
	# If all values of an attribute belong to 1 class, we arrive at this base case.
	# Here we create the leaf node with a value of that class.
	for x in dataSet['target']:
		if x != classValue:
			return 0
	return classValue


def tree_generator_from_training_set(dataSet):
	hashMapOfClassesInAttribute = []
	dataSetSize = len(dataSet.columns) - 1
	if dataSetSize == 0:
		return majority_finding_terminating_case(dataSet)
	if single_class_terminating_case(dataSet):
		return single_class_terminating_case(dataSet)
	optimalAttributeForSplitting = attribute_for_optimal_splitting_at_node(dataSet)
	for x in dataSet[optimalAttributeForSplitting]:
		if x not in hashMapOfClassesInAttribute:
			hashMapOfClassesInAttribute.append(x)
	subTree = {}
	for x in hashMapOfClassesInAttribute:
		# We create a dataset where the value that the attribute optimalAttributeForSplitting takes is only x.
		newDataSet = dataSet[dataSet[optimalAttributeForSplitting] == x]
		# Now, since all the data in this new dataset has the attribute optimalAttributeForSplitting with the same value,
		# We don'dataSetSize need to consider this attribute at all in newDataSet.
		question = optimalAttributeForSplitting + '=' + str(x)
		newDataSet = newDataSet.drop(optimalAttributeForSplitting, axis=1)
		newDataSet.index = range(len(newDataSet))
		child = tree_generator_from_training_set(newDataSet)
		subTree[question] = child
	return subTree


def predict_using_test_set(test):
	prediction = []
	count = 0
	totalCount = len(test.index)
	for i in test.index:
		targetAttributeHash = []
		for x in test.columns:
			temp = x + '=' + str(test[x][i])
			targetAttributeHash.append(temp)
		pred = rowwise_predict(targetAttributeHash, tree)
		prediction.append(pred)
		if pred == test_target[i]:
			count += 1
	accuracy = count / totalCount
	return (prediction, accuracy)


def rowwise_predict(arr, tree):
	if type(tree) != dict:
		# We have reached a leaf node. So it contains the prediction to be returned.
		return tree
	for x in arr:
		if x in tree:
			return rowwise_predict(arr, tree[x])


training_set_data = pandas.read_csv(
	r'https://raw.githubusercontent.com/AbhJ/Machine-Learning-Spring-22-IIT-Kharagpur/master/project1%201.data',
	header=None,
)

test_set_data = pandas.read_csv(
	r'https://raw.githubusercontent.com/AbhJ/Machine-Learning-Spring-22-IIT-Kharagpur/master/project1_test.data',
	header=None,
)

# Providing the headers of the dataset
training_set_data.columns = test_set_data.columns = [
	'price',
	'maint',
	'doors',
	'persons',
	'lug_boot',
	'safety',
	'target',
]

#  Since there was no 56 in the training set the decision tree can'dataSetSize make sense of doors as 56 in the test set and can'dataSetSize
#  subsequently make a prediction other than 'None'. Hence we changed number of doors to 56.
test_set_data['doors'] = [6 if x == 56 else x for x in test_set_data['doors']]
test_target = test_set_data['target']
test_set_data = test_set_data.drop('target', axis=1)
tree = tree_generator_from_training_set(training_set_data)
prediction, accuracy = predict_using_test_set(test_set_data)

# JSON dumps in python provides a way to print data in a prettified json format.
print(
	json.dumps(tree, indent='\t', sort_keys=False),
	'\n\n\nAccuracy of our decision tree on the test set is',
	accuracy,
)
