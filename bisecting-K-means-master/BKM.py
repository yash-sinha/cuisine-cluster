import csv
import math
import random
import copy

numClusters = 2
BIG_NUMBER = math.pow(10, 10)

def loadCsv(filename):
    lines = csv.reader(open(filename, 'r'))
    samples = list(lines)
    for i in range(len(samples)):
        for j in [0,1]:
            samples[i][j] = float(samples[i][j])
    return samples

class Cluster:
    def __init__(self, datapoints, centroid= None, sse=None):
        self.centroid = centroid
        self.sse = sse
        self.datapoints = datapoints

    def set_initcentroid(self, p):
        self.centroid = p

    def add_datapoint(self, x):
        self.datapoints.append(x)

    def calculate_centroid(self):
        totalX = 0
        totalY = 0
        if(len(self.datapoints)!=0):    #to handle null cluster
            for k in range(len(self.datapoints)):
                totalX += self.datapoints[k][0]
                totalY += self.datapoints[k][1]

            self.centroid = [totalX / len(self.datapoints), totalY / len(self.datapoints)]
        else:
            self.centroid = None

    def calculate_sse(self):
        sumsqr = 0
        if(len(self.datapoints)!=0):    #to handle null cluster
            for j in range(len(self.datapoints)):
                sumsqr+=(math.pow((self.centroid[0] - self.datapoints[j][0]), 2) + math.pow((self.centroid[1] - self.datapoints[j][1]), 2))
            self.sse = sumsqr
        else:
            self.sse = 0

    def get_datapoints(self):
        return self.datapoints

    def get_centroid(self):
        return self.centroid

    def get_sse(self):
        return self.sse

    def clear(self):
        self.datapoints = []

    def display(self):
        print("Data points")
        for i in range(len(self.datapoints)):
            print(self.datapoints[i])
        print("Size of cluster = ", len(self.datapoints))

def get_distance(dataPoint, centroid):
    return math.sqrt(math.pow((centroid[1] - dataPoint[1]), 2) + math.pow((centroid[0] - dataPoint[0]), 2))

def kmeans(selected):
    centroid1 = random.randrange(0,len(selected.datapoints))
    centroid2 = random.randrange(0,len(selected.datapoints))
    cluster1 = Cluster([])
    cluster2 = Cluster([])
    cluster1.set_initcentroid(selected.datapoints[centroid1])
    cluster2.set_initcentroid(selected.datapoints[centroid2])

    isStillMoving = 1
    while(isStillMoving):
        clus1prev = cluster1.get_centroid()
        clus2prev = cluster2.get_centroid()
        for i in range(len(selected.datapoints)):
            bestMinimum = BIG_NUMBER
            currentCluster = 0
            for j in [cluster1, cluster2]:
                if(j.get_centroid() is not None):   #ta handle null cluster
                    distance = get_distance(selected.datapoints[i], j.get_centroid())
                else:
                    distance = bestMinimum
                if(distance <= bestMinimum):
                    bestMinimum = distance
                    currentCluster += 1
            if(currentCluster == 1):
                cluster1.add_datapoint(selected.datapoints[i])
            else:
                cluster2.add_datapoint(selected.datapoints[i])
        cluster1.calculate_centroid()
        cluster2.calculate_centroid()
        if(clus1prev == cluster1.get_centroid() and clus2prev == cluster2.get_centroid()):
            isStillMoving = 0
            cluster1.calculate_sse()
            cluster2.calculate_sse()
        else:
            cluster1.clear()
            cluster2.clear()
    return cluster1, cluster2

def main():
    filename = "dataset1.csv"
    samples = loadCsv(filename)
    c1 = Cluster([])
    for i in range(len(samples)):
        c1.add_datapoint(samples[i])
    c1.calculate_centroid()
    c1.calculate_sse()

    list_of_clusters = [c1]
    while(1):
        selected = list_of_clusters[0]
        for i in range(len(list_of_clusters)):
            if(list_of_clusters[i].get_sse() > selected.get_sse()):
                selected = list_of_clusters[i]
        bcluster1 = Cluster([])
        bcluster2 = Cluster([])
        for itr in range(10):
            [cluster1, cluster2] = kmeans(selected)
            if(itr==0):
                bcluster1=copy.deepcopy(cluster1)
                bcluster2=copy.deepcopy(cluster2)
            else:
                if((cluster1.get_sse()+cluster2.get_sse())<(bcluster1.get_sse()+bcluster2.get_sse())):
                    bcluster1=copy.deepcopy(cluster1)
                    bcluster2=copy.deepcopy(cluster2)

        if(selected.get_sse()-bcluster1.get_sse()-bcluster2.get_sse()<5000 or len(list_of_clusters)>9):
            break
        else:
            list_of_clusters.remove(selected)
            list_of_clusters.append(bcluster1)
            list_of_clusters.append(bcluster2)
    cnt = 1
    for cl in list_of_clusters:
        print("Cluster ",cnt)
        cl.display()
        cnt+=1


main()