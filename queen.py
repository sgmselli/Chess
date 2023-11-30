from chessPiece import ChessPiece

class Queen(ChessPiece):
    
    def __init__(self, position, color, deletePiece):
        super().__init__(position, color, deletePiece)
        self.name = 'Q'

    
