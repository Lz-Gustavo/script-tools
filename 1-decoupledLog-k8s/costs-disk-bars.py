# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import sys

upperRangeLimit = 20000000000


def ExtractFunc(filename, firstPos):
    """
    	Extract thoughput for each client execution on rep0.txt (leader)
    """
    fd = open(filename)
    text = fd.readlines()
    #print("TEXTO:", text)
    fd.close()

    dataThroughput = []

    for i in range(firstPos, len(text), 5):
        if i >= upperRangeLimit * 5:
            break

        #dataThroughput.append(int(text[i]))

        # NOTE: modify the line above for single data
        dataThroughput.append(int(text[i]) + int(text[i+1]))

    return dataThroughput


def SummOfFuncs(args):

    acumulative = []
    numFucs = len(args)

    i = 0
    for value in args[0]:
        summ = value
        for j in range(1, numFucs):
            summ += args[j][i]
        acumulative.append(summ)
        i += 1

    return acumulative


def SummOfValues(args):

    summ = 0
    for value in args:
        summ += value
    return summ


def SumOfLists(lists):
    res = list()
    for j in range(0, len(lists[0])):
        tmp = 0
        for i in range(0, len(lists)):
            if j < len(lists[i]):
                tmp = tmp + lists[i][j]
        res.append(tmp)
    return res


def delta(func):
    return max(func) - min(func)

def main():

    # 0: bytes receiv, 1: bytes sent, 2: io read, 3: io write
    # with i + (i+1) -> 0: net traffic, 2: io usage

    choosenData = 0
    yaxis = 'Network Traffic (MB)'
    filename = 'disk-costs-net.png'


    # choosenData = 2
    # yaxis = 'IO Usage (MB)'
    # filename = 'disk-costs-io.png'



    notLog3kvA = ExtractFunc('3app/notlog/app1/io.out', choosenData)
    notLog3kvB = ExtractFunc('3app/notlog/app2/io.out', choosenData)
    notLog3kvC = ExtractFunc('3app/notlog/app3/io.out', choosenData)
    acuNotLog3kv = SumOfLists([notLog3kvA, notLog3kvB, notLog3kvC])



    coupLog3kvA = ExtractFunc('3app/applog/app1/io.out', choosenData)
    coupLog3kvB = ExtractFunc('3app/applog/app2/io.out', choosenData)

    # TODO: investigate later
    coupLog3kvC = ExtractFunc('3app/applog/app2/io.out', choosenData)
    acuCoupLog3kv = SumOfLists([coupLog3kvA, coupLog3kvB, coupLog3kvC])



    # TODO: investigate later
    decoupLog3kvA = ExtractFunc('3app/decouplog/app3/io.out', choosenData)
    decoupLog3kvB = ExtractFunc('3app/decouplog/app3/io.out', choosenData)
    decoupLog3kvC = ExtractFunc('3app/decouplog/app3/io.out', choosenData)

    logger3kvA = ExtractFunc('3app/decouplog/logger1/io.out', choosenData)
    logger3kvB = ExtractFunc('3app/decouplog/logger2/io.out', choosenData)

    acuDecoupLog3kv = SumOfLists([decoupLog3kvA, decoupLog3kvB, decoupLog3kvC])
    acuLoggers3kv = SumOfLists([logger3kvA, logger3kvB])
    #acuDecoupAll3kv = np.sum(np.array([acuDecoupLog3kv, acuLoggers3kv]), 0)



    # 6 apps
    notLog6kvA = ExtractFunc('6app/notlog/app1/io.out', choosenData)
    notLog6kvB = ExtractFunc('6app/notlog/app2/io.out', choosenData)
    notLog6kvC = ExtractFunc('6app/notlog/app3/io.out', choosenData)
    notLog6kvD = ExtractFunc('6app/notlog/app4/io.out', choosenData)
    notLog6kvE = ExtractFunc('6app/notlog/app5/io.out', choosenData)
    notLog6kvF = ExtractFunc('6app/notlog/app6/io.out', choosenData)
    acuNotLog6kv = SumOfLists([notLog6kvA, notLog6kvB, notLog6kvC, notLog6kvD, notLog6kvE, notLog6kvF])



    coupLog6kvA = ExtractFunc('6app/applog/app1/io.out', choosenData)
    coupLog6kvB = ExtractFunc('6app/applog/app2/io.out', choosenData)
    coupLog6kvC = ExtractFunc('6app/applog/app3/io.out', choosenData)
    coupLog6kvD = ExtractFunc('6app/applog/app4/io.out', choosenData)
    coupLog6kvE = ExtractFunc('6app/applog/app5/io.out', choosenData)

    # TODO: investigate later
    coupLog6kvF = ExtractFunc('6app/applog/app5/io.out', choosenData)
    acuCoupLog6kv = SumOfLists([coupLog6kvA, coupLog6kvB, coupLog6kvC, coupLog6kvD, coupLog6kvE, coupLog6kvF])


    decoupLog6kvA = ExtractFunc('6app/decouplog/app1/io.out', choosenData)
    decoupLog6kvB = ExtractFunc('6app/decouplog/app2/io.out', choosenData)
    decoupLog6kvC = ExtractFunc('6app/decouplog/app3/io.out', choosenData)
    decoupLog6kvD = ExtractFunc('6app/decouplog/app4/io.out', choosenData)
    decoupLog6kvE = ExtractFunc('6app/decouplog/app5/io.out', choosenData)
    decoupLog6kvF = ExtractFunc('6app/decouplog/app6/io.out', choosenData)
    acuDecoupLog6kv = SumOfLists([decoupLog6kvA, decoupLog6kvB, decoupLog6kvC, decoupLog6kvD, decoupLog6kvE, decoupLog6kvF])


    logger6kvA = ExtractFunc('6app/decouplog/logger1/io.out', choosenData)
    logger6kvB = ExtractFunc('6app/decouplog/logger2/io.out', choosenData)
    acuLoggers6kv = SumOfLists([logger6kvA, logger6kvB])
    #acuDecoupAll6kv = np.sum(np.array([acuDecoupLog6kv, acuLoggers6kv]), 0)



    #Bytes -> MBytes
    divisor = 1024 * 1024
    acuNotLog3kv = np.divide(acuNotLog3kv, divisor)
    acuCoupLog3kv = np.divide(acuCoupLog3kv, divisor)

    #acuDecoupAll3kv = np.divide(acuDecoupAll3kv, divisor)
    acuDecoupLog3kv = np.divide(acuDecoupLog3kv, divisor)
    acuLoggers3kv = np.divide(acuLoggers3kv, divisor)

    acuNotLog6kv = np.divide(acuNotLog6kv, divisor)
    acuCoupLog6kv = np.divide(acuCoupLog6kv, divisor)

    acuDecoupLog6kv = np.divide(acuDecoupLog6kv, divisor)
    acuLoggers6kv = np.divide(acuLoggers6kv, divisor)



    # costDiffs for stackbars
    cost3kvnotlog = 3 * delta(acuNotLog3kv)
    cost3kvapplog = 3 * delta(acuCoupLog3kv)
    cost3kvdecouplog = 3 * delta(acuDecoupLog3kv) + delta(acuLoggers3kv)


    cost6kvnotlog = 3 * delta(acuNotLog6kv)
    cost6kvapplog = 3* delta(acuCoupLog6kv)

    cost6kvdecouplog = 3 * delta(acuDecoupLog6kv) + delta(acuLoggers6kv)


    labels = ["3 Apps", "6 Apps"]
    #labels = ["3 Apps"]

    xlabels = np.arange(len(labels))
    width = 0.2

    costsNotlog = [cost3kvnotlog, cost6kvnotlog]
    costsApplog = [cost3kvapplog, cost6kvapplog]
    costsDecoup = [cost3kvdecouplog, cost6kvdecouplog]

    #costsNotlog = [cost3kvnotlog]
    #costsApplog = [cost3kvapplog]
    #costsDecoup = [cost3kvdecouplog]

    fig, ax = plt.subplots()
    ax.yaxis.grid(linestyle='--')
    
    ax.bar(xlabels - width, costsNotlog, width, label='diskstorage')
    ax.bar(xlabels, costsApplog, width, label='diskstorage-level logging')
    ax.bar(xlabels + width, costsDecoup, width, label='diskstorage with decoupled logging')

    ax.set_ylabel(yaxis)
    ax.set_xlabel('Number of Applications')

    ax.set_xticks(xlabels)
    ax.set_xticklabels(labels)
    fig.tight_layout()


    plt.legend(loc='best')
    plt.savefig(filename)

if __name__ == "__main__":
    main()
