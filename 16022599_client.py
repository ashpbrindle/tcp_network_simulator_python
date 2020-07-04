from State import State, StateContext

CLOSED = 0
SYNSENT = 1
ESTABLISHED = 2
FINWAIT1 = 3
FINWAIT2 = 4
TIMEDWAIT = 5

class Transition:
    def activeOpen(self):
        print "Error cannot active open"
    
    def rst(self):
        print "Error cannot rst"

    def timeout(self):
        print "Error cannot timeout"   

    def synack(self):
        print "Error cannot syn+ack"

    def close(self):
        print "Error cannot close"
        
    def ack(self):
        print "Error cannot ack"

    def syn(self):
        print "Error cannot syn"  

class Closed(State, Transition):
    def __init__(self, context):
        self.CurrentContext = context

    def activeOpen(self):
        '''send syn,
        Transition to SynSent'''

    def trigger(self):
        '''reset'''
        pass

class SynSent(State, Transition):
    def __init__(self, context):
        self.CurrentContext = context

    def rst(self):
        '''do nothing (
        transfer to Closed'''

    def timeout(self):
        '''reset, 
        transfer to CLOSED'''

    def synack(self):
        '''send ack,
        transition to established'''

    def trigger(self):
        pass

class Established(State, Transition):
    def __init__(self, context):
        self.CurrentContext = context

    def close(self):
        '''fin (
        transfer to finwait1'''

    def trigger(self):
        pass

class FinWait1(State, Transition):
    def __init__(self, context):
        self.CurrentContext = context

    def ack(self):
        '''do nothing (
        transfer to finwait2'''

    def trigger(self):
        pass

class FinWait2(State, Transition):
    def __init__(self, context):
        self.CurrentContext = context

    def fin(self):
        '''ack (
        transfer to timed wait'''

    def trigger(self):
        pass

class TimedWait(State, Transition):
    def __init__(self, context):
        self.CurrentContext = context

    def timeout(self):
        '''idk what to do here (
        transfer to closed'''

    def trigger(self):
        pass

class Client(StateContext, Transition):
    def __init__(self):

        self.availableStates[CLOSED] = Closed(self)
        self.availableStates[SYNSENT] = SynSent(self)
        self.availableStates[ESTABLISHED] = Established(self)
        self.availableStates[FINWAIT1] = FinWait1(self)
        self.availableStates[FINWAIT2] = FinWait2(self)
        self.availableStates[TIMEDWAIT] = TimedWait(self)

        self.setState(CLOSED)

    def activeOpen(self):
       self.CurrentState.activeOpen()
    
    def rst(self):
        self.CurrentState.rst()

    def timeout(self):
        self.CurrentState.timeout()    

    def synack(self):
        self.CurrentState.synack()

    def close(self):
        self.CurrentState.close()
        
    def ack(self):
        self.CurrentState.ack()

    def syn(self):
        self.CurrentState.syn()    