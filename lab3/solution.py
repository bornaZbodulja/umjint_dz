from math import log2
import sys


def manageLine(line):
    line = line.replace('\n', '')
    line = line.split(",")
    return line


def readData(path):
    data = []
    a = open(path, mode='r')
    for line in a.readlines():
        line = manageLine(line)
        data.append(line)
    a.close()
    return data


def countEntropy(list):
    entropy = 0.
    for p in list:
        if p != 0:
            entropy += float(-p * log2(p))
    return entropy


class Dataset():
    def __init__(self, path):
        self.data = readData(path)

    def getFeatures(self):
        first = True
        features = []
        label = Label()
        for element in self.data:
            if first:
                j = 0
                # print(len(element))
                for feature in element:
                    if j < (len(element) - 1):
                        newFeature = Feature(feature)
                        features.append(newFeature)
                    j += 1
                first = False
            else:
                i = 0
                for featureValue in element:
                    if i < (len(element) - 1):
                        if features[i].checkIfInValues(featureValue):
                            features[i].increaseValueOfFeature(featureValue)
                        else:
                            newFeatureValue = FeatureValues(featureValue)
                            features[i].values.append(newFeatureValue)
                    else:
                        label.insertValue(featureValue)
                    i += 1
        for it in features:
            it.values = sorted(it.values, key=lambda value: value.name)
        features = sorted(features, key=lambda feature: feature.name)

        return features, label

    def removeFirstLine(self):
        return self.data[1: (len(self.data))]

    def getLabelTest(self):
        first = True
        test_results = []
        for line in self.data:
            if first:
                first = False
            else:
                test_results.append(line[len(line) - 1])

        return test_results


class Label():
    def __init__(self):
        self.names = []
        self.occurancy = []

    def insertValue(self, value):
        i = 0
        for element in self.names:
            if element == value:
                self.occurancy[i] += 1
                return
            i += 1

        self.names.append(value)
        self.occurancy.append(1)
        return

    def getOverallIG(self):
        oc = sum(self.occurancy)
        p = [(n / oc) for n in self.occurancy]
        return countEntropy(p)

    def getFullIG(self, data):
        first = True
        occurancy = [0] * (len(self.names))
        for line in data:
            if not first:
                if line[len(line) - 1] in self.names:
                    index = self.names.index(line[len(line) - 1])
                    occurancy[index] += 1
            else:
                first = False
        oc = sum(occurancy)
        # print(oc)
        if oc != 0:
            return countEntropy([(n / oc) for n in occurancy])
        else:
            return 0


class Feature():
    def __init__(self, name):
        self.name = name
        self.values = []

    def checkIfInValues(self, value):
        for element in self.values:
            if element.name == value:
                return True
        return False

    def increaseValueOfFeature(self, value):
        for element in self.values:
            if element.name == value: element.occurency = element.occurency + 1

    def getIG(self, data, label):
        entropy = label.getFullIG(data)
        label.names.sort()
        for element in self.values:
            count = len(data) - 1
            matches = [0] * len(label.names)
            first = True
            idx = 0
            for line in data:
                if first:
                    first = False
                    idx = line.index(self.name)
                elif element.name == line[idx]:
                    index = label.names.index(line[len(line) - 1])
                    matches[index] += 1
            oc = sum(matches)
            # print(oc)
            # for el in matches: print(el)
            if oc != 0:
                entropy = entropy - (oc / count) * countEntropy([(n / oc) for n in matches])
        return entropy

    def __str__(self):
        return self.name


class FeatureValues():
    def __init__(self, name):
        self.name = name
        self.occurency = 1


class Branch():
    def __init__(self, depth, childFeature, parentFeatureValue, parentFeature, parentNode, valuesList):
        self.depth = depth
        self.childFeature = childFeature
        self.parentFeatureValue = parentFeatureValue
        self.parentFeature = parentFeature
        self.parentNode = parentNode
        self.valuesList = valuesList


def removeAllExceptFeatureValue(featureValue, data, feature):
    newerData = []
    first = True
    index = 0
    for line in data:
        if not first:
            if featureValue.name == line[index]: newerData.append(line)
        else:
            newerData.append(line)
            first = False
            index = line.index(feature.name)
    return list.copy(newerData)


def checkForDecision(data):
    first = True
    firstLine = True
    label = ""
    for line in data:
        if not firstLine:
            if first:
                label = line[len(line) - 1]
                first = False
            elif label != line[len(line) - 1]:
                return False
        else:
            firstLine = False
    return label


def returnMostCommon(data, labels):
    labels.names.sort()
    occurancy = [0] * len(labels.names)
    first = True
    for line in data:
        if first:
            first = False
        else:
            index = labels.names.index(line[len(line) - 1])
            occurancy[index] += 1
    idx_max = occurancy.index(max(occurancy))
    return labels.names[idx_max]


def giveMeTree(currentData, parentData, features, depth, featureValueGeneratedBy, featureGeneratedBy, label, id3Tree, parentNode, valuesList):
    if (len(currentData) == 1):
        finalMostCommonLabel = returnMostCommon(parentData, label)
        id3Tree.append(Branch(depth, finalMostCommonLabel, featureValueGeneratedBy, featureGeneratedBy, parentNode, valuesList))
        return

    mostCommonLabel = returnMostCommon(currentData, label)

    if (len(features) == 0 or (checkForDecision(currentData) != False)):
        id3Tree.append(Branch(depth, mostCommonLabel, featureValueGeneratedBy, featureGeneratedBy, parentNode, valuesList))
        return

    entropy = []
    features = sorted(features, key=lambda feature: feature.name)
    for feature in features:
        entropy.append(feature.getIG(currentData, label))
    index = entropy.index(max(entropy))
    fea = features[index]
    branch = Branch(depth, fea, featureValueGeneratedBy, featureGeneratedBy, parentNode, valuesList)
    id3Tree.append(branch)

    currentFeature = features[index]
    newFeaturesList = list.copy(features)
    newFeaturesList.remove(currentFeature)
    newFeaturesList = sorted(newFeaturesList, key=lambda feature: feature.name)
    depth += 1

    for featureValue in currentFeature.values:
        val = list.copy(valuesList)
        val.append(featureValue.name)
        #print(val)
        newData = removeAllExceptFeatureValue(featureValue, currentData, currentFeature)
        giveMeTree(list.copy(newData), list.copy(currentData), newFeaturesList, depth, featureValue, currentFeature, label, id3Tree, branch, list.copy(val))
        val.remove(featureValue.name)


def giveMeDepthLimitTree(currentData, parentData, features, depth, featureValueGeneratedBy, featureGeneratedBy, label, id3Tree, parentNode, depthLimit, valuesList):
    if (len(currentData) == 1):
        finalMostCommonLabel = returnMostCommon(parentData, label)
        id3Tree.append(Branch(depth, finalMostCommonLabel, featureValueGeneratedBy, featureGeneratedBy, parentNode, valuesList))
        return

    mostCommonLabel = returnMostCommon(currentData, label)

    if (len(features) == 0 or checkForDecision(currentData) != False or depth == depthLimit):
        id3Tree.append(Branch(depth, mostCommonLabel, featureValueGeneratedBy, featureGeneratedBy, parentNode, valuesList))
        return

    entropy = []
    for feature in features:
        entropy.append(feature.getIG(currentData, label))
    index = entropy.index(max(entropy))
    fea = features[index]
    branch = Branch(depth, fea, featureValueGeneratedBy, featureGeneratedBy, parentNode, valuesList)
    id3Tree.append(branch)

    currentFeature = features[index]
    newFeaturesList = list.copy(features)
    newFeaturesList.remove(currentFeature)
    depth += 1

    for featureValue in currentFeature.values:
        val = list.copy(valuesList)
        val.append(featureValue.name)
        newData = removeAllExceptFeatureValue(featureValue, currentData, currentFeature)
        giveMeDepthLimitTree(newData, list.copy(currentData), newFeaturesList, depth, featureValue, currentFeature, label, id3Tree, branch, depthLimit, val)
        val.remove(featureValue.name)

def checkDecision(data, featureValue, root, labels):
    labels.names.sort()
    occurancy = [0] * len(labels)
    index = 0
    first = True
    for line in data:
        if first:
            index = line.index(root.name)
            first = False
        else:
            if featureValue.name == line[index]:
                idx = labels.names.index(line[len(line) - 1])
                occurancy[idx] += 1

    i = occurancy.index(max(occurancy))
    return labels.names[i]


def fit(dataset, depthLimit):
    features, label = dataset.getFeatures()
    featureValues = []
    for feature in features:
        for value in feature.values:
            featureValues.append(value.name)
    entropy = []
    i = 0
    for feature in features:
        entropy.append(feature.getIG(dataset.data, label))
        # print("IG(" + feature.name + ")=" + str(entropy[i]))
        i += 1
    index = entropy.index(max(entropy))
    root = features[index]
    # print(str(0) + ":" + root.name, end="")
    id3Tree = []
    if depthLimit != -1: giveMeDepthLimitTree(dataset.data, dataset.data, features, 0, None, None, label, id3Tree, None, depthLimit, [])
    # else: buildLimitDepthTree(dataset.data, root, features, label, 1, id3Tree, depthLimit)
    else: giveMeTree(dataset.data, dataset.data, features, 0, None, None, label, id3Tree, None, [])
    '''for node in id3Tree:
        if node.child not in label.names:
            print(node.parent.name+ "->" + node.value.name + ": " + str(node.child))
        else:
            print(node.parent.name+ "->" + node.value.name + ": " + node.child)'''

    return id3Tree


def returnChild(tree, featureValue):
    for node in tree:
        if node.value.name == featureValue:
            return node.child
    return False


def predictForNewFeatureValue(allValues, data, labels):
    outcomes = [0] * len(labels.names)
    labels.names.sort()
    first = True
    for line in data:
        if first:
            first = False
        else:
            if all(item in line for item in allValues):
                index = labels.names.index(line[len(line) - 1])
                outcomes[index] += 1
    index = outcomes.index(max(outcomes))
    return labels.names[index]


def prediction(test_dataset, train_dataset, tree, labels):
    root = None
    root_index = 0
    for branch in tree:
        if branch.parentFeature == None:
            root = branch.childFeature
            break
    res = []
    first = True
    features_test = []
    val = []
    for line in test_dataset:
        if first:
            first = False
            features_test = list.copy(line)
            root_index = line.index(root.name)
        else:
            val.clear()
            root_featureValue = line[root_index]
            val.append(root_featureValue)
            depth = 1
            value = checkForValueInTree(tree, root_featureValue, root.name, 1)
            checked_values = list.copy(features_test)
            checked_values.remove(root.name)
            checked_featureValues = list.copy(line)
            checked_featureValues.pop(len(checked_featureValues)-1)

            if value != False:
                if value not in labels.names:
                    previous_value = root_featureValue
                    previous_feature = root.name
                    newThing = value
                    while (newThing not in labels.names):
                        depth += 1
                        #print(val)
                        new_index = features_test.index(newThing.name)
                        ##checked_values.remove(features_test[new_index])
                        saver_f = features_test[new_index]
                        saver_v = line[new_index]
                        val.append(saver_v)
                        newThing = goThroughtTree(tree, line[new_index], features_test[new_index], depth, previous_feature, previous_value, val)
                        if newThing == False:
                            it = features_test.index(previous_feature)
                            res.append(getDecision(line[it], train_dataset, previous_feature, labels))
                            # print(value)
                            break
                        elif newThing in labels.names:
                            res.append(newThing)

                        previous_feature = saver_f
                        previous_value = saver_v

                else:
                    res.append(value)
            else:
                res.append(getMostOccuredInTrain(labels, train_dataset))

    return res


def getMostOccuredInTrain(labels, train_dataset):
    first = True
    labels.names.sort()
    occ = [0] * len(labels.names)
    for line in train_dataset:
        if first:
            first = False
        else:
            idx = labels.names.index(line[len(line) - 1])
            occ[idx] += 1

    idx_max = occ.index(max(occ))
    return labels.names[idx_max]



def checkForValueInTree(tree, featureVlaue, parent, depth):
    for branch in tree:
        if branch.parentFeature != None and branch.parentFeatureValue != None:
            if branch.parentFeature.name == parent and branch.parentFeatureValue.name == featureVlaue and branch.depth == depth:
                return branch.childFeature
    return False

def goThroughtTree(tree, featureValue, parent, depth, parentFeature, parentFeatureValue, checkedValues):
    for node in tree:
        if node.parentNode != None and node.parentFeature != None and node.parentNode.parentFeature != None:
            if node.parentNode.parentFeature.name == parentFeature and node.parentNode.parentFeatureValue.name == parentFeatureValue and node.parentFeature.name == parent and node.parentFeatureValue.name == featureValue and node.depth == depth and node.parentNode.childFeature.name == parent and node.parentNode.depth == (depth-1) and (sublist(checkedValues, node.valuesList)):
                return node.childFeature
    return False


def getDecision(featureValue, dataset, feature, labels):
    first = True
    labels.names.sort()
    index = 0
    occ = [0] * len(labels.names)
    for line in dataset:
        if first:
            first = False
            index = line.index(feature)
        else:
            if line[index] == featureValue:
                idx = labels.names.index(line[len(line) - 1])
                occ[idx] += 1

    idx_max = occ.index(max(occ))
    return labels.names[idx_max]


def countAccuracy(results, testResults):
    matching = 0
    for i in range(len(results)):
        if results[i] == testResults[i]: matching += 1

    return float(matching / len(results))

def readCfg(path):
    max_depth = -1
    a = open(path, mode='r')
    for line in a.readlines():
        line = line.replace('\n', '')
        line = line.split("=")
        if "max_depth" in line:
            max_depth = int(line[1])

    a.close()
    return max_depth

def printMatrix(predictions, realResults, labels, data):
    _, lab = data.getFeatures()
    lab.names.sort()
    for label in lab.names:
        occurancy = [0] * len(lab.names)
        for i in range(len(predictions)):
            if realResults[i] == label:
                index = lab.names.index(predictions[i])
                occurancy[index] += 1

        for element in occurancy:
            print(str(element) + " ", end="")
        print()


def sublist(sublist, lst):
    if not isinstance(sublist, list):
        raise ValueError("sublist must be a list")
    if not isinstance(lst, list):
        raise ValueError("lst must be a list")

    sublist_len = len(sublist)
    k=0
    s=None

    if (sublist_len > len(lst)):
        return False
    elif (sublist_len == 0):
        return True

    for x in lst:
        if x == sublist[k]:
            if (k == 0): s = x
            elif (x != s): s = None
            k += 1
            if k == sublist_len:
                return True
        elif k > 0 and sublist[k-1] != s:
            k = 0

    return False


if __name__ == "__main__":
    inp = sys.argv
    train_path = inp[1]
    test_path = inp[2]
    cfg_path = inp[3]
    dataset = Dataset(train_path)
    features, label = dataset.getFeatures()
    test_dataset = Dataset(test_path)
    max_depth = readCfg(cfg_path)
    test_results = test_dataset.getLabelTest()
    tree = fit(dataset, max_depth)
    first = True
    for branch in tree:
        if first:
            if branch.childFeature not in label.names:
                print(str(branch.depth) + ":" + branch.childFeature.name, end="")
            first = False
        else:
            if branch.childFeature not in label.names:
                print(", " + str(branch.depth) + ":" + branch.childFeature.name, end="")

    res = prediction(test_dataset.data, dataset.data, tree, label)
    first_res = True
    for value in res:
        if first_res:
            print("\n" + value, end=" ")
            first_res = False
        else:
            print(value, end=" ")

    print("\n" + "%.5f" %(countAccuracy(res, test_results)))
    printMatrix(res, test_results, label, dataset)
