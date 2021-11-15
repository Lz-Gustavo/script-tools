# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
import matplotlib.pyplot as plt
import numpy as np
import sys

upperRangeLimit = 5400
exaustTime = 200

warmUpOffset = 5000

def CalculateThroughput(svrThroughputFilename):
    """
    	Extract thoughput for each client execution on rep0.txt (leader)
    """
    fd = open(svrThroughputFilename)
    text = fd.readlines()
    fd.close()

    dataThroughput = []
    blankSpace = 0

    for i in range(len(text)):
        if int(text[i]) == 0:
            blankSpace += 1
            continue
    	if i - blankSpace >= upperRangeLimit + exaustTime:
    		break
        dataThroughput.append(int(text[i]))

    return dataThroughput


def CalculateLoggerThroughput(lgrTroughputFilename):
    fd = open(lgrTroughputFilename)
    text = fd.readlines()
    fd.close()

    dataThroughput = []
    blankSpace = 0

    for i in range(0, len(text)-1, 2):
        logThr = int(text[i])+int(text[i+1])
        if logThr == 0:
            blankSpace += 1
            continue
    	if i - (2*blankSpace) >= (2*upperRangeLimit):
    		break
        dataThroughput.append(logThr)

    return dataThroughput


def SummOfFuncs(logA, logB):

    acumulative = []

    i = 0
    for value in logA:
        summ = value + logB[i]
        acumulative.append(summ)
        i += 1

    return acumulative

def main():

    appLogTransfer = CalculateThroughput("9belly/0/540/thr-540s.txt")
    repsLogTransfer = CalculateThroughput("9belly-Decoup/0/540/thr-deco-540s.txt")

    loggerTransfer = CalculateThroughput("9belly-Decoup/0/540/log540-belly.txt")

    pointsInTime = range(warmUpOffset, upperRangeLimit + exaustTime - 7)

    # ======================================
    # ========= Plot Graph =================
    # ======================================
    plt.xlabel('Time (s)')
    plt.ylabel('Throughput (cmds/s)')

    # Plot axis
    plt.plot(pointsInTime, appLogTransfer[warmUpOffset:], "r--", label="kvstore level Log")
    plt.plot(pointsInTime, repsLogTransfer[warmUpOffset:], "b--", label="kvstore with logger")
    plt.plot(pointsInTime, loggerTransfer[warmUpOffset:], "y--", label="decoupled logger")

    # Layout
    # plt.title("Raft Protocol Limit Analises")
    
    plt.legend(loc='best')
    
    # art = []
    # lgd = plt.legend(loc=9, bbox_to_anchor=(0.5, -0.1), ncol=2)
    # art.append(lgd)

    # plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

    plt.savefig('logTransferImpact.png')
    #plt.savefig('name.png',additional_artists=art,bbox_inches="tight")

if __name__ == "__main__":
    main()
