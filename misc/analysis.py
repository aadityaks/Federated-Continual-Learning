import os
import json

algo = {
'fedavg':0,
'fedprox':1,
'fedweit':2
}

path = "/Users/aaditya/Downloads/outputs/logs"
dir_list = os.listdir(path)
dir_list.remove(dir_list[1])


def dir(idx, fpath=None):
    client = []
    for i in range(5):
        fpath = path + '/' + dir_list[idx] + '/' + "client-" + str(i) +".txt"
        with open(fpath) as f:
            client.append(json.load(f))
    return client

def avg_accuracy_client(client, c):
    dic = client[c]['scores']['test_acc']
    acc = []
    for key in dic.keys():
        val = dic[key]
        for j in val:
            acc.append(j)
    return acc, sum(acc)/len(acc)

def avg_accuracy_all_clients(client):
    avg_clients_acc = []
    for c in range(5):
        per_client_avg_accuracy = avg_accuracy_client(client, c)[0]
        for j in per_client_avg_accuracy:
            avg_clients_acc.append(j)
    return sum(avg_clients_acc)/len(avg_clients_acc)

for j in algo.keys():
    print("-----", j, "-----")
    client = dir(algo[j])
    for i in range(5):
        print("per-client-avg-accuracy of client {} = {}".format(i, avg_accuracy_client(client, i)[1]))
    print("total-accuracy of all clients = ", avg_accuracy_all_clients(client))


fpath_1 = "/Users/aaditya/Downloads/20221227-1259-fedavg-non_iid_50"
client = []
for i in range(5):
    fpath = fpath_1 + '/' + "client-" + str(i) +".txt"
    with open(fpath) as f:
        client.append(json.load(f))

for i in range(5):
    print("per-client-avg-accuracy of client {} = {}".format(i, avg_accuracy_client(client, i)[1]))
print("total-accuracy of all clients = ", avg_accuracy_all_clients(client))