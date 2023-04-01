"""
Process Class

arrival_time - Arrival time of process
svc_time - Service time of process
io_time - IO time of process
io_act_time - IO activation time of process since service time
processID - Process ID

"""


class Process:
    def __init__(self, arrTime, svcTime, ioTime, ioact, processID) -> None:
        self.arrival_time: float = arrTime
        self.svc_time: float = svcTime
        self.io_time: float = ioTime
        self.io_act_time = ioact
        self.processID: int = processID

        self.svc_complete: float = 0
        self.act_index: int = 0

        self.finTime: float = 0
        self.resTime: float = -1
        self.tat: float = 0
        
        self.resRatio: float = 0
        self.waitTime: float = 0
        

    def __str__(self):
        return f"Process ID: {self.processID}\t Arrival Time: {self.arrival_time}\t Service Time: {self.svc_time}\t IO Time: {self.io_time}\t IO Activation Time: {self.io_act_time}\n"

    def printStats(self):
        return f"Process ID: {self.processID}\t Finish Time: {self.finTime}\t Response Time: {self.resTime}\t Turnaround Time: {self.tat}\n"
