# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
import matplotlib.pyplot as plt
import sys

MAX_APPS = 9
F_FAULTS = 1
K_FAULTS = 1

# 43200: minutes in one month
KV_DISK_APP = 0
#KV_DISK_LOG = 2046208
KV_DISK_LOG = 62046208 * 43200

DISK_DISK_APP = 52150272 * 43200
DISK_DISK_LOG = 10928128 * 43200

ACCOUNTING_BASE = True

# 1 USD per MB
#PHI = 0.000001

# 1 USD per GB
#PHI = 0.000000001

# 0.025 USD per GB in one month
PHI = 0.025 * 0.000000001

# 10 USD per machine
#EPSILON = 10

# 0.0104 USD per hour in one month
EPSILON = 0.0104 * 720

def costApp(f, disk_app, disk_log, n_apps, phi, base):
    return ((((2*f + 1) * (disk_app + disk_log)) * n_apps) * phi) + base
    
    # EQUIVALENT TO:
    #return (((2*f + 1) * n_apps) * (phi * (disk_app + disk_log))) + base

def costLog(f, k, disk_app, disk_log, n_apps, phi, base):
    return (((((2*f + 1) * disk_app) * n_apps) + ((k+1) * disk_log)) * phi) + base

def baseApp(f, epsilon, n_apps):
    return ((2*f+1)*n_apps)*epsilon

def baseLog(f, k, epsilon, n_apps):
    #return (2*f+k+2)*epsilon
    return (((2*f+1)*n_apps)+(k+1))*epsilon

def main():

    pointsInTime = range(1, MAX_APPS+1)
    kvApp = []
    kvLog = []
    dkApp = []
    dkLog = []
    for i in pointsInTime:
        if ACCOUNTING_BASE:
            kvApp.append(costApp(F_FAULTS, KV_DISK_APP, KV_DISK_LOG, i, PHI, baseApp(F_FAULTS, EPSILON, i)))
            kvLog.append(costLog(F_FAULTS, K_FAULTS, KV_DISK_APP, KV_DISK_LOG, i, PHI, baseLog(F_FAULTS, K_FAULTS, EPSILON, i)))

            dkApp.append(costApp(F_FAULTS, DISK_DISK_APP, DISK_DISK_LOG, i, PHI, baseApp(F_FAULTS, EPSILON, i)))
            dkLog.append(costLog(F_FAULTS, K_FAULTS, DISK_DISK_APP, DISK_DISK_LOG, i, PHI, baseLog(F_FAULTS, K_FAULTS, EPSILON, i)))

        else:
            kvApp.append(costApp(F_FAULTS, KV_DISK_APP, KV_DISK_LOG, i, PHI, 0))
            kvLog.append(costLog(F_FAULTS, K_FAULTS, KV_DISK_APP, KV_DISK_LOG, i, PHI, 0))

            dkApp.append(costApp(F_FAULTS, DISK_DISK_APP, DISK_DISK_LOG, i, PHI, 0))
            dkLog.append(costLog(F_FAULTS, K_FAULTS, DISK_DISK_APP, DISK_DISK_LOG, i, PHI, 0))

    plt.xlabel('Number of hosted applications')
    plt.ylabel('Monetary Cost ($)')

    ax = plt.axes()
    ax.yaxis.grid(linestyle='--')

    print(kvApp)
    print(kvLog)
    print(dkApp)
    print(dkLog)

    # Plot axis
    plt.plot(pointsInTime, kvApp, "y-h", label="kvstore-level logging")
    plt.plot(pointsInTime, kvLog, "b-^", label="kvstore with decoupled logging")
    #plt.plot(pointsInTime, dkApp, "r-o", label="disk-level logging")
    #plt.plot(pointsInTime, dkLog, "g-*", label="disk with decoupled logging")
    plt.legend(loc='best')
    plt.savefig('kv-monthly-costs2.png')


if __name__ == "__main__":
    main()
