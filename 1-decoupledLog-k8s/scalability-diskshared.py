# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
import matplotlib.pyplot as plt
import numpy as np
import sys

upperRangeLimit = 60

warmUpOffset = 5
tailOffset = 5

def CalculateAveThroughput(svrThroughputFilename):
    """
        Extract thoughput for each client execution on rep0.txt (leader)
    """
    fd = open(svrThroughputFilename)
    text = fd.readlines()
    fd.close()

    dataThroughput = []
    sequence = []

    countZeros = 0
    for i in range(len(text)):

        if int(text[i]) == 0:
            countZeros += 1
		
        elif countZeros > 4:
            for j in range(i+warmUpOffset, len(text)):
                if int(text[j]) != 0:
                    sequence.append(int(text[j]))
                else:
                    break

            dataThroughput.append(sequence[:-tailOffset])
            sequence = []
            i = j
            countZeros = 0
        #if

    #print("Sequence numbers for:", svrThroughputFilename)
    #print(dataThroughput)

    # Calculate the average thoughput for each client experiment
    AveThroughput = []
    for i in dataThroughput:
        arr = np.array(i)
        AveThroughput.append(np.mean(arr))

    return AveThroughput[0]


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
    	if i - blankSpace >= upperRangeLimit:
    		break
        dataThroughput.append(int(text[i]))

    return dataThroughput


def CalculateLoggerThroughput(lgrTroughputFilename, numDiffApps):
    fd = open(lgrTroughputFilename)
    text = fd.readlines()
    fd.close()

    dataThroughput = []
    blankSpace = 0

    for i in range(0, len(text), numDiffApps):
        logThr = 0
        for j in range(0, numDiffApps):
            logThr += int(text[i+j])

        if logThr == 0:
            blankSpace += 1
            continue
        if i - (numDiffApps*blankSpace) >= (numDiffApps*upperRangeLimit):
            break

        dataThroughput.append(logThr)

    return dataThroughput


def SummOfFuncs(args):

    acumulative = []
    numFucs = len(args)

    i = 0
    for value in args[0]:
        summ = value
        for j in range(1, numFucs):
            summ += args[j]
        acumulative.append(summ)
        i += 1

    return acumulative


def SummOfValues(args):

    summ = 0
    for value in args:
        summ += value
    return summ

def main():



    notLog1kvA = CalculateAveThroughput('1app/notlog/monit/node16-throughput.out')
    coupLog1kvA = CalculateAveThroughput('1app/applog/monit/node15-throughput.out')
    decoupLog1kvA = CalculateAveThroughput('1app/decouplog/app1/node16-throughput.out')
    #logger1kv = np.mean(CalculateLoggerThroughput('1app/decouplog/node2-throughput.out', 1))
    #logger1kv = CalculateLoggerThroughput('1app/decouplog/logger/node2-throughput.out')


    notLog3kvA = CalculateAveThroughput('3app/notlog/app1/node11-throughput.out')
    notLog3kvB = CalculateAveThroughput('3app/notlog/app2/node12-throughput.out')
    notLog3kvC = CalculateAveThroughput('3app/notlog/app3/node13-throughput.out')
    acuNotLog3kv = SummOfValues([notLog3kvA, notLog3kvB, notLog3kvC])


    coupLog3kvA = CalculateAveThroughput('3app/applog/app1/node14-throughput.out')
    coupLog3kvB = CalculateAveThroughput('3app/applog/app2/node16-throughput.out')
    coupLog3kvC = CalculateAveThroughput('3app/applog/app3/node14-throughput.out')
    acuCoupLog3kv = SummOfValues([coupLog3kvA, coupLog3kvB, coupLog3kvC])


    decoupLog3kvA = CalculateAveThroughput('3app/decouplog/app1/node14-throughput.out')
    decoupLog3kvB = CalculateAveThroughput('3app/decouplog/app2/node13-throughput.out')
    decoupLog3kvC = CalculateAveThroughput('3app/decouplog/app3/node15-throughput.out')
    acuDecoupLog3kv = SummOfValues([decoupLog3kvA, decoupLog3kvB, decoupLog3kvC])




    #logger3kv = np.mean(CalculateLoggerThroughput('DADS-60msec-3kv/AppLog-Decoup/1/dell3kv-Loggerthr.txt', 3))



    notLog6kvA = CalculateAveThroughput('6app/notlog/app1/node10-throughput.out')
    notLog6kvB = CalculateAveThroughput('6app/notlog/app2/node6-throughput.out')
    notLog6kvC = CalculateAveThroughput('6app/notlog/app3/node5-throughput.out')
    notLog6kvD = CalculateAveThroughput('6app/notlog/app4/node11-throughput.out')
    notLog6kvE = CalculateAveThroughput('6app/notlog/app5/node10-throughput.out')
    notLog6kvF = CalculateAveThroughput('6app/notlog/app6/node8-throughput.out')

    acuNotLog6kv = SummOfValues([notLog6kvA, notLog6kvB, notLog6kvC, notLog6kvD, notLog6kvE, notLog6kvF])


    coupLog6kvA = CalculateAveThroughput('6app/applog/app1/node14-throughput.out')
    coupLog6kvB = CalculateAveThroughput('6app/applog/app2/node14-throughput.out')
    coupLog6kvC = CalculateAveThroughput('6app/applog/app3/node14-throughput.out')
    coupLog6kvD = CalculateAveThroughput('6app/applog/app4/node15-throughput.out')
    coupLog6kvE = CalculateAveThroughput('6app/applog/app5/node14-throughput.out')
    coupLog6kvF = CalculateAveThroughput('6app/applog/app6/node15-throughput.out')

    acuCoupLog6kv = SummOfValues([coupLog6kvA, coupLog6kvB, coupLog6kvC, coupLog6kvD, coupLog6kvE, coupLog6kvF])



    decoupLog6kvA = CalculateAveThroughput('6app/decouplog/app1/node6-throughput.out')
    decoupLog6kvB = CalculateAveThroughput('6app/decouplog/app2/node8-throughput.out')
    decoupLog6kvC = CalculateAveThroughput('6app/decouplog/app3/node11-throughput.out')
    decoupLog6kvD = CalculateAveThroughput('6app/decouplog/app4/node7-throughput.out')
    decoupLog6kvE = CalculateAveThroughput('6app/decouplog/app5/node9-throughput.out')
    decoupLog6kvF = CalculateAveThroughput('6app/decouplog/app6/node11-throughput.out')

    acuDecoupLog6kv = SummOfValues([decoupLog6kvA, decoupLog6kvB, decoupLog6kvC, decoupLog6kvD, decoupLog6kvE, decoupLog6kvF])

    #logger4kv = np.mean(CalculateLoggerThroughput('DADS-60msec-4kv/AppLog-Decoup/1/dell4kv-Loggerthr.txt', 4))


    scalaNotLog = [notLog1kvA, acuNotLog3kv, acuNotLog6kv]    
    print(scalaNotLog)

    scalaCoupLog = [coupLog1kvA, acuCoupLog3kv, acuCoupLog6kv]
    print(scalaCoupLog)

    scalaDecoupLog = [decoupLog1kvA, acuDecoupLog3kv, acuDecoupLog6kv]
    print(scalaDecoupLog)

    #scalaLogThr = [logger1kv, logger2kv, logger3kv, logger4kv]
    numInstances=[1, 3, 6]


    # ======================================
    # ========= Plot Graph =================
    # ======================================

    # plt.xlabel('Number of hosted applications')
    # plt.ylabel('Throughput (cmds/s)')

    plt.xlabel(u'Número de aplicações hospedadas')
    plt.ylabel(u'Vazão (cmds/s)')

    ax = plt.axes()
    ax.yaxis.grid(linestyle='--')

    # Plot axis
    # plt.plot(numInstances, scalaNotLog, "h-b", label="diskstorage")
    # plt.plot(numInstances, scalaCoupLog, "v:y", label="diskstorage-level logging")
    # plt.plot(numInstances, scalaDecoupLog, "o--g", label="diskstorage with decoupled logging")
    #plt.plot(numInstances, scalaLogThr, "o--c", label="decoupled logger thr")


    plt.plot(numInstances, scalaNotLog, "h-b", label="sem log")
    plt.plot(numInstances, scalaCoupLog, "v:y", label=u"log em nível de aplicação")
    plt.plot(numInstances, scalaDecoupLog, "o--g", label=u"log desacoplado")
    plt.title('diskstorage')

    # Layout
    plt.legend(loc='best')

    plt.savefig('disk-scalability-PT.png')

if __name__ == "__main__":
    main()
