

class GlobalReferenceObject:
    """
    A singleton global reference object.
    """
    def __new__(cls): # https://www.geeksforgeeks.org/singleton-pattern-in-python-a-complete-guide/#
        if not hasattr(cls, 'instance'):
            cls.instance = super(GlobalReferenceObject, cls).__new__(cls)
        return cls.instance
    
    BOARD: object   # Current chess board
    # SURFACE: object # Current pygame window # TODO: Remove?
    
    UI: object      # Current ChessUI object
    
    IH: object      # Current InputHandler object
    
    AL: object      # AssetLoader instance

    GM: object      # Current GameManager object
    

OBJREF = GlobalReferenceObject()

class GlobalAccessObject:
    """
    Generic superclass for objects which need access to global references.
    """
    OBJREF: GlobalReferenceObject = OBJREF
    
    @property
    def board(self):
        return self.OBJREF.BOARD
    @property
    def ui(self):
        return self.OBJREF.UI
    @property
    def ih(self):
        return self.OBJREF.IH
    @property
    def al(self):
        return self.OBJREF.AL
    @property
    def gm(self):
        return self.OBJREF.GM

