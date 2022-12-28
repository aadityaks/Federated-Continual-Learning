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



algo = {}
for i,j in enumerate(dir_list):
    if 'fedavg' in j:
        algo['fedavg'] = i
    if 'fedprox' in j:
        algo['fedprox'] = i
    if 'fedweit' in j:
        algo['fedweit'] = i


# algo = {
# 'fedavg':0,
# 'fedprox':1,
# 'fedweit':2
# }

def dir(idx, fpath=None):
    client = []
    for i in range(5):
        fpath = path + '/' + dir_list[idx] + '/' + "client-" + str(i) +".txt"
        with open(fpath) as f:
            client.append(json.load(f))
    return client

def avg_last_round_accuracy_client(client, c):
    client_data = client[c]['scores']['test_acc']
    acc = []
    for task in client_data.keys():
        val = client_data[task]
        acc.append(val[-1])
        for j in val:
            acc.append(j)
    return acc, sum(acc)/len(acc)

def avg_accuracy_client(client, c):
    dic = client[c]['scores']['test_acc']
    acc = []
    for key in dic.keys():
        val = dic[key]
        print(len(val))
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

def avg_last_accuracy_all_clients(client):
    avg_clients_acc = []
    for c in range(5):
        per_client_avg_accuracy = avg_last_round_accuracy_client(client, c)[0]
        for j in per_client_avg_accuracy:
            avg_clients_acc.append(j)
    return sum(avg_clients_acc)/len(avg_clients_acc)

for j in algo.keys():
    print("-----", j, "-----")
    client = dir(algo[j])
    for i in range(5):
        print("per-client-avg-accuracy of client {} = {}".format(i, avg_accuracy_client(client, i)[1]))
        # print("per-client-avg-last-accuracy of client {} = {}".format(i, avg_last_round_accuracy_client(client, i)[1]))
    # print("total-accuracy of all clients = ", avg_accuracy_all_clients(client))
    # print("total-accuracy of all clients = ", avg_last_accuracy_all_clients(client))

fpath_1 = "/Users/aaditya/Downloads/20221227-1259-fedavg-non_iid_50"
client = []
for i in range(5):
    fpath = fpath_1 + '/' + "client-" + str(i) +".txt"
    with open(fpath) as f:
        client.append(json.load(f))

for i in range(5):
    print("per-client-avg-accuracy of client {} = {}".format(i, avg_accuracy_client(client, i)[1]))
print("total-accuracy of all clients = ", avg_accuracy_all_clients(client))