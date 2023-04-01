from process import Process

import csv
import os
import copy
import random

"""
Contains all scheduling algorithms and the main function

fcfs() - First Come First Serve
rr() - Round Robin
srt() - Shortest Remaining Time
hrrn() - Highest Response Ratio Next
processGenerator - Generates processes for simulation
simTesting() - Simulates scheduling algorithms with process testing and saves results to a csv

main() - Main function - Calls simTesting() and simInput(), with user input for selection of algorithm to run

"""


class ALGO:
    def __init__(self) -> None:
        self.numProc: int = 0
        self.sumFinTime: float = 0
        self.procList: Process = []
        self.lastAdded: int = 0

        self.procListEarly = []

    def __str__(self):
        return f"Number of processes: {self.numProc}\t Sum of finish times: {self.sumFinTime}\n"

    def fcfs(self):
        runQueue = []
        ioQueue = []

        counter: int = 0

        runQueue.append(self.procList[0])

        while 1:
            if len(ioQueue) != 0:
                runQueue.append(ioQueue.pop(0))

            if counter % 2 == 0 and counter != 0:
                self.lastAdded += 1

                if self.lastAdded < len(self.procList):
                    runQueue.append(self.procList[self.lastAdded])

            if (
                self.lastAdded >= len(self.procList)
                and len(runQueue) == 0
                and len(ioQueue) == 0
            ):
                self.sumFinTime = counter
                break

            currProc = runQueue[0]

            if currProc.resTime == -1:
                currProc.resTime = counter - currProc.arrival_time

            currProc.svc_complete += 1

            counter += 1

            if currProc.act_index < len(currProc.io_act_time):
                if currProc.io_act_time[currProc.act_index] == currProc.svc_complete:
                    ioQueue.append(currProc)
                    currProc.act_index += 1
                    runQueue.pop(0)
                    continue

            if currProc.svc_time == currProc.svc_complete:
                currProc.finTime = counter
                currProc.tat = currProc.finTime - currProc.arrival_time
                # currProc.resTime = currProc.tat - currProc.svc_complete
                self.numProc += 1
                runQueue.pop(0)
                continue

        return 0

    def srt(self):
        runQueue = []
        ioQueue = []

        counter: int = 0

        runQueue.append(self.procList[0])

        while 1:
            if (
                self.lastAdded >= len(self.procList)
                and len(runQueue) == 0
                and len(ioQueue) == 0
            ):
                self.sumFinTime = counter
                break

            if counter % 2 == 0 and counter != 0:
                self.lastAdded += 1

                if self.lastAdded < len(self.procList):
                    runQueue.append(self.procList[self.lastAdded])
                    runQueue.sort(
                        key=lambda x: (x.svc_time - x.svc_complete), reverse=False
                    )

            if len(runQueue) != 0:
                currProc = runQueue[0]
                currProc.svc_complete += 1

                if currProc.resTime == -1:
                    currProc.resTime = counter - currProc.arrival_time

            counter += 1

            if len(ioQueue) != 0:
                runQueue.append(ioQueue.pop(0))
                runQueue.sort(
                    key=lambda x: (x.svc_time - x.svc_complete), reverse=False
                )

            if currProc.act_index < len(currProc.io_act_time):
                if currProc.io_act_time[currProc.act_index] == currProc.svc_complete:
                    ioQueue.append(currProc)
                    currProc.act_index += 1
                    runQueue.pop(0)

            if currProc.svc_time == currProc.svc_complete:
                currProc.finTime = counter
                currProc.tat = currProc.finTime - currProc.arrival_time
                self.numProc += 1
                runQueue.pop(0)

        return 0

    def hrrn(self):
        runQueue = []
        ioQueue = []

        counter: int = 0

        runQueue.append(self.procList[0])

        if len(self.procList) == 0:
            return 0

        while 1:
            if (
                self.lastAdded >= len(self.procList)
                and len(runQueue) == 0
                and len(ioQueue) == 0
            ):
                self.sumFinTime = counter
                break

            if (counter) % 2 == 0 and counter != 0:
                self.lastAdded += 1
                if self.lastAdded < len(self.procList):
                    runQueue.append(self.procList[self.lastAdded])

                    for proc in runQueue:
                        proc.resRatio = (
                            counter
                            - proc.svc_complete
                            - proc.arrival_time
                            + proc.svc_time
                        ) / proc.svc_time

            if len(runQueue) != 0:
                currProc = runQueue[0]
                currProc.svc_complete += 1

                if currProc.resTime == -1:
                    currProc.resTime = counter - currProc.arrival_time

            counter += 1

            if len(ioQueue) != 0:
                runQueue.append(ioQueue.pop(0))
                for proc in runQueue:
                    proc.resRatio = (
                        counter - proc.svc_complete - proc.arrival_time + proc.svc_time
                    ) / proc.svc_time

            if (
                currProc.act_index < len(currProc.io_act_time)
                and currProc.io_act_time[currProc.act_index] == currProc.svc_complete
            ):
                ioQueue.append(currProc)
                currProc.act_index += 1
                runQueue.pop(0)

                for proc in runQueue:
                    proc.resRatio = (
                        counter - proc.svc_complete - proc.arrival_time + proc.svc_time
                    ) / proc.svc_time

                runQueue.sort(key=lambda x: x.resRatio, reverse=True)

                continue

            if currProc.svc_time == currProc.svc_complete:
                currProc.finTime = counter
                currProc.tat = currProc.finTime - currProc.arrival_time
                self.numProc += 1
                runQueue.pop(0)

                for proc in runQueue:
                    proc.resRatio = (
                        counter - proc.svc_complete - proc.arrival_time + proc.svc_time
                    ) / proc.svc_time

                runQueue.sort(key=lambda x: x.resRatio, reverse=True)

                continue

        return 0

    def rr(self):
        runQueue = []
        ioQueue = []

        counter: int = 0

        runQueue.append(self.procList[0])

        while 1:
            if (
                self.lastAdded >= len(self.procList)
                and len(runQueue) == 0
                and len(ioQueue) == 0
            ):
                self.sumFinTime = counter
                break

            tempIOProc: Process = None
            tempNewProc: Process = None

            if ioQueue != []:
                tempIOProc = ioQueue.pop(0)

            if (counter + 1) % 2 == 0 and counter != 0:
                self.lastAdded += 1

                if self.lastAdded < len(self.procList):
                    tempNewProc = self.procList[self.lastAdded]

            if runQueue != []:
                currProc = runQueue[0]
                currProc.svc_complete += 1

                if currProc.resTime == -1:
                    currProc.resTime = counter + 1 - currProc.arrival_time

            if currProc.act_index < len(currProc.io_act_time):
                if currProc.io_act_time[currProc.act_index] == currProc.svc_complete:
                    ioQueue.append(currProc)
                    currProc.act_index += 1
                    runQueue.pop(0)
                    counter += 1

                    if tempIOProc != None:
                        runQueue.append(tempIOProc)

                    if tempNewProc != None:
                        runQueue.append(tempNewProc)

                    continue

            if currProc.svc_time == currProc.svc_complete:
                currProc.finTime = counter + 1
                currProc.tat = currProc.finTime - currProc.arrival_time
                self.numProc += 1
                runQueue.pop(0)
                counter += 1

                if tempIOProc != None:
                    runQueue.append(tempIOProc)

                if tempNewProc != None:
                    runQueue.append(tempNewProc)

                continue

            if len(runQueue) != 0:
                runQueue.append(runQueue.pop(0))

            if tempIOProc != None:
                runQueue.append(tempIOProc)

            if tempNewProc != None:
                runQueue.append(tempNewProc)

            counter += 1

        return 0

    def cfs(self):
        
        return 0


    def processGenerator(self):
        lastArrivalTime: int = 0
        svcSum: int = 0

        for i in range(0, random.randint(30, 60)):

            svc = random.randint(5, 40)
            ioTime: int = random.randint(0, 2)

            if ioTime == 0:
                DiskIO = []
            elif ioTime == 1:
                DiskIO = [random.randint(1, svc - 1)]
            else:
                DiskIO = [random.randint(1, svc - 3)]
                DiskIO.append(random.randint(DiskIO[0] + 1, svc - 1))

            svcSum += svc

            newProc = Process(lastArrivalTime, svc, ioTime, DiskIO, i)

            self.procList.append(newProc)

            lastArrivalTime += 2

        self.saveProcList()
        return 0

    def simTesting(self, inputVal: int):
        self.processGenerator()
        self.procListEarly = copy.deepcopy(self.procList)

        match (inputVal):
            case 1:
                self.fcfs()
            case 2:
                self.srt()
            case 3:
                self.hrrn()
            case 4:
                self.rr()
            case 5:
                filename: str = "output.csv"

                if os.path.exists(filename):
                    with open(filename, "w", newline="") as f:
                        writer = csv.writer(f)

                        writer.writerow(["FCFS"])
                        writer.writerow(
                            [
                                "Process ID",
                                "Arrival Time",
                                "Service Time",
                                "Finish Time",
                                "Turnaround Time",
                                "Response Time",
                                "Ratio TAT/SVC",
                            ]
                        )

                else:
                    with open(filename, "x", newline="") as f:
                        writer = csv.writer(f)

                        writer.writerow(["FCFS"])
                        writer.writerow(
                            [
                                "Process ID",
                                "Arrival Time",
                                "Service Time",
                                "Finish Time",
                                "Turnaround Time",
                                "Response Time",
                                "Ratio TAT/SVC",
                            ]
                        )

                self.fcfs()

                with open(filename, "a", newline="") as f:
                    writer = csv.writer(f)

                    for proc in self.procList:
                        writer = csv.writer(f)
                        writer.writerow(
                            [
                                proc.processID,
                                proc.arrival_time,
                                proc.svc_time,
                                proc.finTime,
                                proc.tat,
                                proc.resTime,
                                proc.tat / proc.svc_time,
                            ]
                        )

                    writer.writerow(["Throughput", self.numProc / self.sumFinTime])
                    writer.writerow([])

                self.restart()

                self.srt()

                with open(filename, "a", newline="") as f:
                    writer = csv.writer(f)

                    writer.writerow(["SRT"])
                    for proc in self.procList:
                        writer = csv.writer(f)
                        writer.writerow(
                            [
                                proc.processID,
                                proc.arrival_time,
                                proc.svc_time,
                                proc.finTime,
                                proc.tat,
                                proc.resTime,
                                proc.tat / proc.svc_time,
                            ]
                        )

                    writer.writerow(["Throughput", self.numProc / self.sumFinTime])
                    writer.writerow([])

                self.restart()

                self.hrrn()

                with open(filename, "a", newline="") as f:
                    writer = csv.writer(f)

                    writer.writerow(["HRRN"])
                    for proc in self.procList:
                        writer = csv.writer(f)
                        writer.writerow(
                            [
                                proc.processID,
                                proc.arrival_time,
                                proc.svc_time,
                                proc.finTime,
                                proc.tat,
                                proc.resTime,
                                proc.tat / proc.svc_time,
                            ]
                        )

                    writer.writerow(["Throughput", self.numProc / self.sumFinTime])
                    writer.writerow([])

                self.restart()

                self.rr()

                with open(filename, "a", newline="") as f:
                    writer = csv.writer(f)

                    writer.writerow(["RR"])
                    for proc in self.procList:
                        writer = csv.writer(f)
                        writer.writerow(
                            [
                                proc.processID,
                                proc.arrival_time,
                                proc.svc_time,
                                proc.finTime,
                                proc.tat,
                                proc.resTime,
                                proc.tat / proc.svc_time,
                            ]
                        )

                    writer.writerow(["Throughput", self.numProc / self.sumFinTime])
                    writer.writerow([])

                self.restart()

            case 6:
                print("Exit")
            case _:
                print("Invalid input, please try again")

        return 0

    def printProcList(self):
        for proc in self.procList:
            print(proc.printStats())

        return 0

    def saveProcList(self):
        filename: str = "process_list.csv"

        if os.path.exists(filename):
            with open(filename, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(
                    [
                        "Process ID",
                        "Arrival Time",
                        "Service Time",
                        "IO Time",
                        "Disk IO Activity",
                    ]
                )

        else:
            with open(filename, "x", newline="") as f:
                writer = csv.writer(f)

                writer.writerow(["FCFS"])
                writer.writerow(
                    [
                        "Process ID",
                        "Arrival Time",
                        "Service Time",
                        "IO Time",
                        "Disk IO Activity",
                    ]
                )

        for proc in self.procList:
            with open(filename, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(
                    [
                        proc.processID,
                        proc.arrival_time,
                        proc.svc_time,
                        proc.io_time,
                        proc.io_act_time,
                    ]
                )

    def restart(self):
        self.procList = copy.deepcopy(self.procListEarly)
        self.lastAdded = 0
        self.numProc = 0
        self.sumFinTime = 0

        return 0


def main():
    algoInst: ALGO = ALGO()

    print("Welcome to the CPU Scheduling Simulator \n")
    print("Please select an algorithm to run: \n")
    print("1. First Come First Serve (FCFS)\n")
    print("2. Shortest Remaining Time (SRT)\n")
    print("3. Highest Response Ratio Next (HRRN)\n")
    print("4. Round Robin (RR)\n")
    print("5. Simulate all algorithms and store to csv\n")
    print("6. Exit\n")

    inputVal: int = int(input("Enter a number: "))

    algoInst.simTesting(inputVal)

    return 0


if __name__ == "__main__":
    main()
