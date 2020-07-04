from State import State, StateContext
from socket import socket

CLOSED = 0
LISTEN = 1
SYNRECVD = 2
ESTABLISHED = 3
CLOSEWAIT = 4
LASTACK = 5

states = ["CLOSED", "LISTEN", "SYNRECVD", "ESTABLISHED", "CLOSEWAIT", "LASTACK"]

class Transition:
    def passiveOpen(self):
        print "Error cannot passive open"
    
    def syn(self):
        print "Error cannot syn"

    def ack(self):
        print "Error cannot ack"    

    def fin(self):
        print "Error cannot fin"

    def close(self):
        print "Error cannot close"

class Closed(State, Transition):
    def __init__(self, context):
        self.CurrentContext = context

    def passiveOpen(self):
        '''transitions to the Listen state to listen for 
        an incomming connection'''

        self.CurrentContext.setState(LISTEN)

    def trigger(self):
        ''' this will activate whenever transitioned to this state
        and will act as a grounding state and reset the TCP/IP'''

        try:
            print "Current state" + states[self.CurrentContext.stateIndex]
            print "Attempting to close connection"
            self.CurrentContext.socket.close()
            self.CurrentContext.address = 0
            return True
        except:
            return False

class Listen(State, Transition):
    def __init__(self, context):
        self.CurrentContext = context

    def syn(self):
        '''send syn+ack, 
        Transition to SYN RECVD'''
        self.CurrentContext.connection.send("SYNACK")
        print "Sending SYNACK"
        self.CurrentContext.setState(SYNRECVD)
        print "Transitioning to SYNRECVD"
        return True

    def trigger(self):
        print "Current state" + states[self.CurrentContext.stateIndex]
        if self.CurrentContext.listen() is True:
            self.syn()
        else:
            return False

class SynRecvd(State, Transition):
    def __init__(self, context):
        self.CurrentContext = context

    def ack(self):
        message = self.CurrentContext.connection.recv(1024)
        if message == "SYNACK":
            print message + " Received!"
            print "Transitioning to ESTABLISHED"
            self.CurrentContext.setState(ESTABLISHED)

    def trigger(self):
        print "Current state" + states[self.CurrentContext.stateIndex]
        self.ack()

class Established(State, Transition):
    def __init__(self, context):
        self.CurrentContext = context

    def fin(self):
        '''send ack,
        Transition to CloseWait'''
        self.CurrentContext.connection.send("ACK")
        print "Sending ACK"


    def trigger(self):
        self.fin()

class CloseWait(State, Transition):
    def __init__(self, context):
        self.CurrentContext = context

    def close(self):
        '''send fin
        Transition to LastAck'''

    def trigger(self):
        pass

class LastAck(State, Transition):
    def __init__(self, context):
        self.CurrentContext = context

    def ack(self):
        '''send nothing, (basically acknoledge)
        Transition to Closed'''

    def trigger(self):
        pass

class Server(StateContext, Transition):
    def __init__(self):

        self.host = "127.0.0.1"
        self.port = 5000
        self.socket = None
        self.address = 0

        self.availableStates[CLOSED] = Closed(self)
        self.availableStates[LISTEN] = Listen(self)
        self.availableStates[SYNRECVD] = SynRecvd(self)
        self.availableStates[ESTABLISHED] = Established(self)
        self.availableStates[CLOSEWAIT] = CloseWait(self)
        self.availableStates[LASTACK] = LastAck(self)
        self.setState(CLOSED)

    def passiveOpen(self):
       self.CurrentState.passiveOpen()
    
    def syn(self):
        self.CurrentState.syn()

    def ack(self):
        self.CurrentState.ack()    

    def fin(self):
        self.CurrentState.fin()

    def close(self):
        self.CurrentState.close()

    def listen(self):
        self.socket = socket()
        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen(1)
            self.connection, self.address = self.socket.accept()
            print "Address: ", self.address
            return True
        except Exception as e:
            print e
            exit()

    