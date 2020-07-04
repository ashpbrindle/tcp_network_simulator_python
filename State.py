
class State: 
    state = None #abstract class
    CurrentContext = None
    def __init__(self, Context):
        self.CurrentContext.Context = Context

class StateContext:
    stateIndex = 0
    CurrentState = None
    availableStates = []

    def setState(self, newstate):
        self.CurrentState = self.availableStates[newstate]
        self.stateIndex = newstate

    def getStateIndex(self):
        return self.stateIndex