class Sequence:
    """Creates a Sequence from id, and seq"""
    def __init__(self, seq, id="<unknown id>"):
        if id is not None and not isinstance(id, str):
            raise TypeError("id argument must be a string")
        self._seq=seq
        self.id=id
    
    def sequence(self):
        return self._seq

