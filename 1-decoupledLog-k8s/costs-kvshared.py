# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
import matplotlib.pyplot as plt
import numpy as np
import sys

upperRangeLimit = 300


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
        #if text[i] != '\n':
        dataThroughput.append(int(text[i]))

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

def main():

    # 0: bytes receiv, 1: bytes sent, 2: io read, 3: io write

    # choosenData = 0
    # yaxis = 'Data Received (KB)'
    # filename = 'kv-costs-netreceiv.png'

    choosenData = 1
    yaxis = 'Data Sent (KB)'
    filename = 'kv-costs-netsent.png'

    # choosenData = 2
    # yaxis = 'IO Read (KB)'
    # filename = 'kv-costs-ioread.png'

    # choosenData = 3
    # yaxis = 'IO Write (KB)'
    # filename = 'kv-costs-iowrite.png'




    notLog6kvA = ExtractFunc('6app/notlog/app1/io.out', choosenData)
    notLog6kvB = ExtractFunc('6app/notlog/app2/io.out', choosenData)
    notLog6kvC = ExtractFunc('6app/notlog/app3/io.out', choosenData)
    notLog6kvD = ExtractFunc('6app/notlog/app4/io.out', choosenData)
    notLog6kvE = ExtractFunc('6app/notlog/app5/io.out', choosenData)
    notLog6kvF = ExtractFunc('6app/notlog/app6/io.out', choosenData)

    #acuNotLog6kv = SummOfFuncs([notLog6kvA, notLog6kvB, notLog6kvC, notLog6kvD, notLog6kvE, notLog6kvF])
    acuNotLog6kv = np.sum(np.array([notLog6kvA, notLog6kvB, notLog6kvC, notLog6kvD, notLog6kvE, notLog6kvF]), 0)



    coupLog6kvA = ExtractFunc('6app/applog/app1/io.out', choosenData)
    coupLog6kvB = ExtractFunc('6app/applog/app2/io.out', choosenData)
    coupLog6kvC = ExtractFunc('6app/applog/app3/io.out', choosenData)
    coupLog6kvD = ExtractFunc('6app/applog/app4/io.out', choosenData)
    coupLog6kvE = ExtractFunc('6app/applog/app5/io.out', choosenData)
    coupLog6kvF = ExtractFunc('6app/applog/app6/io.out', choosenData)

    #acuCoupLog6kv = SummOfFuncs([coupLog6kvA, coupLog6kvB, coupLog6kvC, coupLog6kvD, coupLog6kvE, coupLog6kvF])
    acuCoupLog6kv = np.sum(np.array([coupLog6kvA, coupLog6kvB, coupLog6kvC, coupLog6kvD, coupLog6kvE, coupLog6kvF]), 0)


    decoupLog6kvA = ExtractFunc('6app/decouplog/app1/io.out', choosenData)
    decoupLog6kvB = ExtractFunc('6app/decouplog/app2/io.out', choosenData)
    decoupLog6kvC = ExtractFunc('6app/decouplog/app3/io.out', choosenData)
    decoupLog6kvD = ExtractFunc('6app/decouplog/app4/io.out', choosenData)
    decoupLog6kvE = ExtractFunc('6app/decouplog/app5/io.out', choosenData)
    decoupLog6kvF = ExtractFunc('6app/decouplog/app6/io.out', choosenData)

    #acuDecoupLog6kv = SummOfFuncs([decoupLog6kvA, decoupLog6kvB, decoupLog6kvC, decoupLog6kvD, decoupLog6kvE, decoupLog6kvF])
    acuDecoupLog6kv = np.sum(np.array([decoupLog6kvA, decoupLog6kvB, decoupLog6kvC, decoupLog6kvD, decoupLog6kvE, decoupLog6kvF]), 0)


    #logger4kv = np.mean(CalculateLoggerThroughput('DADS-60msec-4kv/AppLog-Decoup/1/dell4kv-Loggerthr.txt', 4))


    #scalaLogThr = [logger1kv, logger2kv, logger3kv, logger4kv]
    numInstances = range(upperRangeLimit)


    # ======================================
    # ========= Plot Graph =================
    # ======================================


    # Bytes -> MegaBytes
    acuNotLog6kv = np.divide(acuNotLog6kv, 1000)
    acuCoupLog6kv = np.divide(acuCoupLog6kv, 1000)
    acuDecoupLog6kv = np.divide(acuDecoupLog6kv, 1000)


    plt.xlabel('Time (sec)')
    plt.ylabel(yaxis)

    #plt.xlabel(u'Número de aplicações hospedadas')
    #plt.ylabel(u'Vazão (cmds/s)')

    ax = plt.axes()
    ax.yaxis.grid(linestyle='--')

    # Plot axis
    plt.plot(numInstances, acuNotLog6kv, "--b", label="kvstore")
    plt.plot(numInstances, acuCoupLog6kv, "v:y", label="kvstore-level logging")
    plt.plot(numInstances, acuDecoupLog6kv, "o--g", label="kvstore with decoupled logging")
    #plt.plot(numInstances, scalaLogThr, "o--c", label="decoupled logger thr")


    # Layout
    plt.legend(loc='best')

    plt.savefig(filename)

if __name__ == "__main__":
    main()
