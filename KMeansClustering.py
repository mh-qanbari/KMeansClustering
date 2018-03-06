import re

infinit = float("inf")


class Tweet:
    def __init__(self, json):
        self.json = json

    def getId(self):
        return self.json["id"]

    def getWordSet(self):
        regex = r"\b\w+\b"
        return set(re.findall(regex, self.json["text"]))

    def getDistanceJac(self, other):
        __this_wordset = self.getWordSet()
        __other_wordset = other.getWordSet()
        __intersect = __this_wordset.intersection(__other_wordset)
        __union = __this_wordset.union(__other_wordset)
        return 1. - float(len(__intersect)) / len(__union)


class ClusterCentroid:
    def __init__(self, tweet):
        self.tweet = tweet

    def getDistanceJac(self, tweet):
        return self.tweet.getDistanceJac(tweet)

    def getId(self):
        return self.tweet.getId()


class Cluster:
    def __init__(self, center):
        self.centroid = ClusterCentroid(center)
        self.nodes = [center]
        self.nodesSize = 1
        self.__last_min_dist = float("inf")

    def getDistanceJac(self, tweet):
        return self.centroid.getDistanceJac(tweet)

    def add(self, tweet):
        self.nodes.append(tweet)
        self.nodesSize += 1

    def refresh(self):
        __min_dist = 2. * self.nodesSize
        __min_index = -1
        for i in range(self.nodesSize):
            __sum_dist = 0.
            for j in range(self.nodesSize):
                if i == j:
                    continue
                __node = self.nodes[j]
                if isinstance(__node, ClusterCentroid):
                    __sum_dist += self.nodes[i].getDistanceJac(__node.tweet)
                else:
                    __sum_dist += self.nodes[i].getDistanceJac(__node)
            if __min_dist > __sum_dist:
                __min_dist = __sum_dist
                __min_index = i
        del self.centroid
        self.centroid = ClusterCentroid(self.nodes[__min_index])
        del self.nodes
        self.nodes = [self.centroid.tweet]
        self.nodesSize = 1
        __diff = abs(self.__last_min_dist - __min_dist)
        self.__last_min_dist = __min_dist
        if __diff == infinit:
            return __min_dist
        else:
            return __diff


class K_Means:
    def __init__(self, centroids):
        self.clusters = []
        for __centroid in centroids:
            self.clusters.append(Cluster(__centroid))
        self.clusterSize = len(centroids)
        self.__last_min_diffs = [float("inf")] * len(centroids)
        self.Threshold = 0.5

    def add(self, tweet_json):
        tweet = Tweet(tweet_json)
        # Compute minimum distance
        __min_dist = self.clusters[0].getDistanceJac(tweet)
        __min_index = 0
        for i in range(1, self.clusterSize):
            __dist = self.clusters[i].getDistanceJac(tweet)
            if __min_dist > __dist:
                __min_dist = __dist
                __min_index = i
        # Add to the cluster
        self.clusters[__min_index].add(tweet)

    def restart(self):
        __converged = True
        for i in range(self.clusterSize):
            __diff = self.clusters[i].refresh()
            if abs(__diff - self.__last_min_diffs[i]) > self.Threshold:
                __converged = False
            self.__last_min_diffs[i] = __diff
        return __converged
