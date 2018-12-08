#!/usr/bin/env python3
import h5py
import numpy as np
from matplotlib import pyplot as plt

# read h5 file and extract the flow_order
filename = 'dataset.h5'
f = h5py.File(filename, 'r')

a_group_key = list(f.keys())[0]

# Get the data
data = list(f[a_group_key])

flow_order_data = [data[i].decode('UTF-8') for i in range(len(data))]
meta = ''
sequence = ''

# read the sequence.fasta file and extract the sequence to compare
with open('sequence.fasta', 'r') as fh:
    line = fh.readline()
    while line:
        line = line.rstrip('\n')
        if '>' in line:
            meta = line
        else:
            sequence = sequence + line
        line = fh.readline()

# Compare the flow order data with sequence
if len(flow_order_data) > 0 and len(sequence.strip()) > 0:
    count_flow_order = len(flow_order_data)
    result_seq_list = [0 for k in range(count_flow_order)]

    i = 0
    j = 0
    count = count_flow_order

    while count > 0:
        item_found = False
        if sequence[i].strip() == flow_order_data[j].strip():
            item_found = True
            repeat_count = 1
            if sequence[i].strip() == sequence[i+1].strip():
                repeat_count = repeat_count + 1
                for m in range(i+1,len(sequence)):
                    if sequence[m] != sequence[m+1]:
                        break
                    else:
                        repeat_count = repeat_count + 1
            result_seq_list[j] = repeat_count
            i = i + repeat_count
            j = j + 1
        else:
            j = j + 1
        count = count - 1

    # Plot the graph to show the number of incorporations for each flow
    x_axis = np.array(flow_order_data)
    y_axis = np.array(result_seq_list)

    x=range(len(x_axis))

    fig, ax = plt.subplots(1, 1)
    ax.set_xticks(x) # set tick positions
    ax.set_xticklabels([v for v in x_axis])
    ax.plot(x, y_axis,'bo', x, y_axis)
    #ax.plot(x, y_axis)
    fig.canvas.draw() # actually draw figure
    print('Creating a plot to show the incorporation information')
    plt.show() # enter GUI loop (for non-interactive interpreters)

else:
    print('There is no data to plot')
