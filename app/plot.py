import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

target = None
print 'Please chose a file to plot'
for dirname, dirnames, filenames in os.walk('data'):
    for idx in range(len(filenames)):
        print '(%d) %s' % (idx, filenames[idx])
    print ''
    
    file_idx = int(raw_input('Type file number: '))
    target = '%s/%s' % (dirname, filenames[file_idx])

print 'Target:\t%s' % target

df = pd.read_csv(target)

# print 'Decribeion'
# print df.describe()
# print '---first 3'
# print df.head(3)
# print '---column'
# print df.columns
# print '---index'
# print df.index
# print '---info'
# print df.info

# in 4 model, compare back propagation, inference, and training
def save_flag_compare_gpu(data_f, algo):
    resnet_gpu = data_f[data_f.loc[:, 'process-unit'] == 'gpu']
    resnet_flags = []
    resnet_flags.append( resnet_gpu[resnet_gpu.loc[:, 'flag'] == 'training'])
    resnet_flags.append( resnet_gpu[resnet_gpu.loc[:, 'flag'] == 'inference'])
    resnet_flags.append( resnet_gpu[resnet_gpu.loc[:, 'flag'] == 'back'])

    plt.title('Rate (images/sec) with Batch size')
    plt.xlabel('batch size')
    plt.ylabel('images / sec')
    labels = ['training', 'inference', 'back propagation']
    colors = ['r', 'b', 'g']
    styles = ['o', 's', '^']

    for idx in range(len(resnet_flags)):
        resnet_flags[idx] = resnet_flags[idx].sort_values(by = 'batch')
        # print resnet_flags[idx].flag
        # print resnet_flags[idx].train_rate
        # print labels[idx]
        # print '------------------------------------------------------------------------'
        plt.plot(resnet_flags[idx].batch, resnet_flags[idx].train_rate, label = labels[idx], color = colors[idx], marker = styles[idx])

    plt.legend(loc = 'best')
    plt.savefig('report/%s-flag-rate.png' % algo, format='png')
    plt.close()
    return

def save_compare_process_unit(data, algo):
    # use inference data to draw
    data = data[data.loc[:, 'flag'] == 'training']
    data_cpu = data[data.loc[:, 'process-unit'] == 'cpu']
    data_gpu = data[data.loc[:, 'process-unit'] == 'gpu']
    data_gpu = data_gpu.sort_values(by = 'batch')
    data_cpu = data_cpu.sort_values(by = 'batch')

    plt.title('Rate: Gpu compare CPU')
    plt.xlabel('batch size')
    plt.ylabel('images / sec')
    plt.plot(data_gpu.batch, data_gpu.train_rate, label = 'GPU', color = 'r', marker = 'o')
    plt.plot(data_cpu.batch, data_cpu.train_rate, label = 'CPU', color = 'b', marker = '^')
    plt.legend(loc = 'best')
    plt.savefig('report/%s-process-unit-compare.png' % algo, format = 'png')
    plt.close()
    return

def save_loss_in_models(data, algos):
    plt.title('Loss in models')
    plt.xlabel('batch size')
    plt.ylabel('loss rate')

    colors = ['r', 'b', 'g', 'y']
    styles = ['o', 's', '^', 'd']
    data_algo = []
    for algo in algos:
        tmp = data[data.loc[:, 'algo'] == algo]
        tmp = tmp[tmp.loc[:, 'process-unit'] == 'gpu']
        tmp = tmp[tmp.loc[:, 'flag'] == 'training']
        tmp = tmp.sort_values(by = 'batch')
        plt.plot(tmp.batch, tmp.step_10, label = algo, color = colors.pop() , marker = styles.pop())
        data_algo.append(tmp)

    plt.legend(loc = 'best')
    plt.savefig('report/loss.png', format = 'png')
    plt.close()    
    return

algos = ['resnet50', 'inception3', 'vgg16', 'alexnet']
for algo in algos:
    data_f = df[df.loc[:, 'algo'] == algo]
    save_flag_compare_gpu(data_f, algo)
    save_compare_process_unit(data_f, algo)
save_loss_in_models(df, algos)
