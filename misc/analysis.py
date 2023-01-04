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

def calculate_task_adaptation(client, c, tid):
    dic = client[c]['scores']['test_acc']
    acc = []
    val = dic[str(tid)][:client[c]['options']['num_rounds']]
    for i, j in enumerate(val):
        acc.append(j)
        # if i%client[c]['options']['num_tasks']==0:
        #     acc.append(j)
    return np.array(acc)

def plot_task_adaptation(task_data):
    import matplotlib.pyplot as plt
    x = np.arange(len(task_data))
    plt.plot(x, task_data)
    plt.xticks(x, x)
    plt.ylabel('Accuracy %')
    plt.show()

def plot_all_task_adaptation(task_data):
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(2, 5, figsize=(25, 15))

    for i in range(2):
        for j in range(5):
            axs[i, j].plot(np.arange(20), task_data[5*i+j])
            axs[i, j].set_title("Task {}".format(str(5*i+j)))

    for ax in axs.flat:
        ax.set(xlabel='Rounds', ylabel='Accuracy %')

    for ax in axs.flat:
        ax.label_outer()

    plt.show()


for j in list(algo.keys())[2:3]:
    print("-----", j, "-----")
    client = dir(algo[j])
    for i in range(0,1):
        task_data = calculate_task_adaptation(client, i, 0)
        for tid in range(1,10):
            x = calculate_task_adaptation(client, i, tid)
            task_data = np.vstack((task_data, x))
        plot_all_task_adaptation(task_data)
        openArrayInExcel(np.around(task_data, decimals=2))
        # print("client {} accuracy for task {} : {}".format(i, tid, np.array(tid_data)))
        # plot_task_adaptation(np.array(tid_data)*100)
        # print("per-client-avg-accuracy of client {} = {}".format(i, avg_accuracy_client(client, i)[1]))
        # print("per-client-avg-last-accuracy of client {} = {}".format(i, avg_last_round_accuracy_client(client, i)[1]))
    # print("total-accuracy of all clients = ", avg_accuracy_all_clients(client))
    # print("total-accuracy of all clients = ", avg_last_accuracy_all_clients(client))