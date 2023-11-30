from chessPiece import ChessPiece

class King(ChessPiece):
    
    def __init__(self, position, color, deletePiece):
        super().__init__(position, color, deletePiece)
        self.name = 'K'

    