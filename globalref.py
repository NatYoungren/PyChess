

# TODO: Use properties or getters?
#       I want the cleanest reference 'calls' possible.
#       i.e. board
#            NOT board()
#                OBJREF.board
#                OBJREF.board()

class GlobalReferenceManager:
    """
    A singleton global reference object.
    """
    def __new__(cls): # https://www.geeksforgeeks.org/singleton-pattern-in-python-a-complete-guide/#
        if not hasattr(cls, 'instance'):
            cls.instance = super(GlobalReferenceManager, cls).__new__(cls)
        return cls.instance

    BOARD: object   # Current chess board
    SURFACE: object # Current pygame window
    UI: object      # Current ChessUI object
    
    # @property
    # def board(self):
    #     return self.BOARD
    # @property
    # def surface(self):
    #     return self.SURFACE
    

OBJREF = GlobalReferenceManager()



def board():
    """ Get the current board. """
    return OBJREF.BOARD

def surface():
    """ Get the current surface. """
    return OBJREF.SURFACE

def ui():
    """ Get the current UI. """
    return OBJREF.UI