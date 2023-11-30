from chessPiece import ChessPiece

class Castle(ChessPiece):

    def __init__(self, position, color, deletePiece):
        super().__init__(position, color, deletePiece)
        self.name = 'C'
