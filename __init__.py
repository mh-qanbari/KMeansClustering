from test import K_Means, Tweet, ClusterCentroid, Cluster
import copy

null = None


if __name__ == '__main__':
    tweets = []
    with open("Tweets.json", 'r') as tweets_file:
        for tweet in tweets_file:
            tweet = tweet.replace('\n', ' ').strip()
            tweets.append(eval(tweet))
    print tweets[0]

    init_seeds = []
    with open("InitialSeeds.txt", 'r') as seeds_file:
        for seed in seeds_file:
            init_seeds.append(long(seed.replace(',', '')))
    print init_seeds

    tweet_jsons = []
    centroids = []
    for tweet_json in tweets:
        tweet_obj = Tweet(tweet_json)
        if tweet_obj.getId() in init_seeds:
            centroids.append(ClusterCentroid(tweet_obj))
        else:
            tweet_jsons.append(tweet_json)

    kmeans = K_Means(centroids)
    for tweet_json in tweet_jsons:
        kmeans.add(tweet_json)

    converged_clusters = [copy.deepcopy(cluster) for cluster in kmeans.clusters]
    converged = kmeans.restart()
    while True:
        if converged:
            break
        for tweet_json in tweet_jsons:
            kmeans.add(tweet_json)
        converged_clusters = [copy.deepcopy(cluster) for cluster in kmeans.clusters]
        converged = kmeans.restart()

    for cluster in converged_clusters:
        print "Centroid :", cluster.centroid.tweet.getId()
        print "Tweets:"
        for tweet_obj in cluster.nodes:
            print "\t", tweet_obj.getId()
        print "-------------------------------------------"
