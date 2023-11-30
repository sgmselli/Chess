from pawn import Pawn
from castle import Castle
from queen import Queen
from bishop import Bishop
from king import King
from horse import Horse

class Board():
    def __init__(self, turn):
        self.whiteChecked = False
        self.blackChecked = False

        self.whiteKingPos = [0,3]
        self.blackKingPos = [7,4]

        self.turn = turn

        self.board = self.initialBoard()
        self.piecesList = self.createPieces()

        self.checkMate = False

        self.updateBoard()
        
    #An array of all the initial pieces with their corresponding initial positions
    def createPieces(self):
        pieces = []

        #Append pawn pieces with their starting positions
        for i in range(8):
            pieces.append(Pawn([1,i], 'W', self.deletePiece))
            pieces.append(Pawn([6,i], 'B', self.deletePiece)) 
       
        #Append castle pieces with their starting positions
        pieces.append(Castle([0,0], 'W', self.deletePiece))
        pieces.append(Castle([0,7], 'W', self.deletePiece))
        pieces.append(Castle([7,0], 'B', self.deletePiece))
        pieces.append(Castle([7,7], 'B', self.deletePiece))

        #Append queen pieces with their starting positions
        pieces.append(Queen([0,4], 'W', self.deletePiece))
        pieces.append(Queen([7,3], 'B', self.deletePiece))

        #Append king pieces with their starting positions
        pieces.append(King(self.getBlackKingPos(), 'B', self.deletePiece))
        pieces.append(King(self.getWhiteKingPos(), 'W', self.deletePiece))

        #Append horse pieces with their starting positions
        pieces.append(Horse([0,1], 'W', self.deletePiece))
        pieces.append(Horse([0,6], 'W', self.deletePiece))
        pieces.append(Horse([7,1], 'B', self.deletePiece))
        pieces.append(Horse([7,6], 'B', self.deletePiece))
    
        #Append bishop pieces with their starting positions
        pieces.append(Bishop([0,2], 'W', self.deletePiece))
        pieces.append(Bishop([0,5], 'W', self.deletePiece))
        pieces.append(Bishop([7,2], 'B', self.deletePiece))
        pieces.append(Bishop([7,5], 'B', self.deletePiece))

        return pieces
    
    #Initial empty board 8x8 grid 
    def initialBoard(self):
        return [[' ' for _ in range(8)] for _ in range(8)]
            
    #Updates all the positions on the board
    def updateBoard(self):
        pieces = self.getPieces()
        board = self.initialBoard()

        for i in range(len(pieces)):
            
            x_piece, y_piece = pieces[i].position[0], pieces[i].position[1] #Get each pieces positions and asign to board
            board[x_piece][y_piece] = pieces[i]
    
        self.board = board

        self.printBoard()

        self.validate_checkmate('B')
        print()
        self.validate_checkmate('W')

    #Displays the board in terms of letters instead of the Object ID
    def printBoard(self):
        uiBoard = [row[:] for row in self.board] #Copy array
        for i in range(8):
            for j in range(8):
                if type(uiBoard[i][j]) != str:
                    uiBoard[i][j] = uiBoard[i][j].getName()
        
        print()
        print(f"                    {self.getTurn()}'s turn")
        print()
        print('      0    1    2    3    4    5    6    7')
        print()
        for i in range(8):
            print(f'{i}   {uiBoard[i]}')
            print()
        print()

    def getPieces(self):
        return self.piecesList
    
    def getBoard(self):
        return self.board
    
    def getTurn(self):
        return self.turn
    
    def getBlackKingPos(self):
        return self.blackKingPos
    
    def getWhiteKingPos(self):
        return self.whiteKingPos
    
    def getWhiteChecked(self):
        return self.whiteChecked
    
    def getBlackChecked(self):
        return self.blackChecked
    
    def getWhiteKing(self):
        return [king for king in self.getPieces() if king.getName() == 'K' and king.getColor() == 'W'][0]
    
    def getBlackKing(self):
        return [king for king in self.getPieces() if king.getName() == 'K' and king.getColor() == 'B'][0]
    
    def getCheckMate(self):
        return self.checkMate
    
    def switchTurn(self):
        if self.getTurn() == 'W':
            self.turn = 'B'
        else:
            self.turn = 'W'

    def deletePiece(self, position):
        self.piecesList = [x for x in self.piecesList if x.getPosition() != position]
    
    def potentialMoves(self, position):
        xPos, yPos = position[0], position[1]
        pieceAtPos = [piece for piece in self.piecesList if piece.getPosition() == [xPos, yPos]][0]
        moveArguments = []

        #Must select a piece and the color must be equal to the current players turn
        if type(pieceAtPos) != str and pieceAtPos.getColor() == self.getTurn():

            #Potential moves for a pawn piece
            if pieceAtPos.getName() == 'P' :
                moveArguments+=(self.find_pawn_positions(pieceAtPos))
                
            #Potential moves for a castle piece
            if pieceAtPos.getName() == 'C':
                moveArguments+=(self.find_hoz_positions(pieceAtPos))
                moveArguments+=(self.find_vert_positions(pieceAtPos))

            #Potential moves for a queen piece
            if pieceAtPos.getName() == 'Q':
                moveArguments+=(self.find_hoz_positions(pieceAtPos))
                moveArguments+=(self.find_vert_positions(pieceAtPos))
                moveArguments+=(self.find_diag_positions(pieceAtPos))
            
            #Potential moves for a bishop piece
            if pieceAtPos.getName() == 'B':
                moveArguments+=(self.find_diag_positions(pieceAtPos))

            #Potential moves for a horse piece
            if pieceAtPos.getName() == 'H':
                moveArguments+=(self.find_horse_positions(pieceAtPos))

            #Potential moves for a king piece
            if pieceAtPos.getName() == 'K':
                moveArguments+=(self.find_king_positions(pieceAtPos))

            #Offers potential moves to user and makes move based on input
            if pieceAtPos.getName() == 'K' and pieceAtPos.getColor() == 'B':
                self.blackKingPos = pieceAtPos.move(moveArguments)
            elif pieceAtPos.getName() == 'K' and pieceAtPos.getColor() == 'W':
                self.whiteKingPos = pieceAtPos.move(moveArguments)
            else:
                pieceAtPos.move(moveArguments)

            self.switchTurn()
            self.updateBoard()

            self.whiteChecked = self.validateCheck(self.getWhiteKing(), self.getWhiteKingPos())
            self.blackChecked = self.validateCheck(self.getBlackKing(), self.getBlackKingPos())

            print(f'White king checked: {self.whiteChecked}')
            print(f'Black king checked: {self.blackChecked}')
            
        else:
            print('Select your own color piece')
            self.printBoard()

    #Given the chosen pawn piece's position, an array of possible pawn positions to move to is outputted
    def find_pawn_positions(self, piece):

        availablePositions = []
        xPos, yPos = piece.getPosition()[0], piece.getPosition()[1]
        pawnColor = piece.getColor()

        #White pawn pieces move up the board
        if pawnColor == 'W':
            #Move up one if there is no piece in the way 
            if xPos+1 < 8 and type(self.board[xPos+1][yPos]) == str:
                self.validate_and_append_position(availablePositions, [xPos+1, yPos], piece)

            #Move up two if there is no piece in the way and before the middle of board
            if xPos < 2 and type(self.board[xPos+1][yPos]) == str and type(self.board[xPos+2][yPos]) == str:
                self.validate_and_append_position(availablePositions, [xPos+2, yPos], piece)

            #Take piece top right of pawn if there exists an opposing piece
            if xPos+1 < 8 and yPos+1 < 8 and type(self.board[xPos+1][yPos+1]) != str and self.board[xPos+1][yPos+1].getColor() != pawnColor:
                self.validate_and_append_position(availablePositions, [xPos+1, yPos+1], piece)

            #Take piece top left of pawn if there exists an opposing piece
            if xPos+1 < 8 and yPos-1 >= 0 and type(self.board[xPos+1][yPos-1]) != str and self.board[xPos+1][yPos-1].getColor() != pawnColor:
                self.validate_and_append_position(availablePositions, [xPos+1, yPos-1], piece)
                
        #Black pawn pieces move down the board
        else: 
            #Move up one if there is no piece in the way 
            if type(self.board[xPos-1][yPos]) == str:
                self.validate_and_append_position(availablePositions, [xPos-1, yPos], piece)
 
            #Move up two if there is no piece in the way and before the middle of board
            if xPos > 5 and type(self.board[xPos-1][yPos]) == str and type(self.board[xPos-2][yPos]) == str:
                self.validate_and_append_position(availablePositions, [xPos-2, yPos], piece)

            #Take piece top right of pawn if there exists an opposing piece
            if xPos-1 >= 0 and yPos-1 >= 0 and type(self.board[xPos-1][yPos-1]) != str and self.board[xPos-1][yPos-1].getColor() != pawnColor:
                self.validate_and_append_position(availablePositions, [xPos-1, yPos-1], piece)
 
            #Take piece top left of pawn if there exists an opposing piece
            if xPos-1 >= 0 and yPos+1 < 8 and type(self.board[xPos-1][yPos+1]) != str and self.board[xPos-1][yPos+1].getColor() != pawnColor:
                self.validate_and_append_position(availablePositions, [xPos-1, yPos+1], piece)
       
        
        return availablePositions

    #Given the chosen piece's position, an array of possible horizontal positions to move to is outputted
    def find_hoz_positions(self, piece):
        horizontalPieces = []
        horizontalPositions = []
        xPos, yPos = piece.getPosition()[0], piece.getPosition()[1]
        pieceColor = piece.getColor()

        for i in range(8):
            if type(self.board[xPos][i]) == str:
                horizontalPieces.append(' ')
            else:
                horizontalPieces.append(self.board[xPos][i].getName())

        i, j = yPos-1, yPos+1
        while i>0 and horizontalPieces[i] == ' ':
            i-=1
        while j<len(horizontalPieces)-1 and horizontalPieces[j] == ' ':
            j+=1
        if i<0 or (horizontalPieces[i] != ' ' and self.board[xPos][i].getColor() == pieceColor):
            i+=1
   
        if j>len(horizontalPieces)-1 or (horizontalPieces[j] != ' ' and self.board[xPos][j].getColor() == pieceColor):
            j-=1

        for x in range(i,yPos):
            self.validate_and_append_position(horizontalPieces, [x, xPos], piece)

        for x in range(yPos+1, j+1):
            self.validate_and_append_position(horizontalPieces, [x, xPos], piece)

        return horizontalPositions

    #Given the chosen piece's position, an array of possible vertical positions to move to is outputted
    def find_vert_positions(self, piece):
        verticalPieces = []
        verticalPositions = []
        xPos, yPos = piece.getPosition()[0], piece.getPosition()[1]
        pieceColor = piece.getColor()

        for i in range(8):
            if type(self.board[i][yPos]) == str:
                verticalPieces.append(' ')
            else:
                verticalPieces.append(self.board[i][yPos].getName())

        i, j = xPos-1, xPos+1
        while i>0 and verticalPieces[i] == ' ':
            i-=1
        while j<len(verticalPieces)-1 and verticalPieces[j] == ' ':
            j+=1
        if i<0 or (verticalPieces[i] != ' ' and self.board[i][yPos].getColor() == pieceColor):
            i+=1
        if j>len(verticalPieces)-1 or (verticalPieces[j] != ' ' and self.board[j][yPos].getColor() == pieceColor):
            j-=1

        for y in range(i,xPos):
            self.validate_and_append_position(verticalPositions, [y, yPos], piece)
            
        for y in range(xPos+1, j+1):
            self.validate_and_append_position(verticalPositions, [y, yPos], piece)

        return verticalPositions

    #Given the chosen piece's position, an array of possible diagonal positions to move to is outputted
    def find_diag_positions(self, piece):
        diagonalPosition = []
        xPos, yPos = piece.getPosition()[0], piece.getPosition()[1]
        pieceColor = piece.getColor()

        a = xPos+1
        b = yPos-1
        c = xPos-1
        d = yPos+1

        #Appends the possible bottom left diagonal of piece positions to array
        while a < 8 and b >= 0 and type(self.board[a][b]) == str:
            self.validate_and_append_position(diagonalPosition, [a,b], piece)
            a+=1
            b-=1
        if a < 8 and b >= 0 and type(self.board[a][b]) != str and self.board[a][b].getColor() != pieceColor:
            self.validate_and_append_position(diagonalPosition, [a,b], piece)
        
        #Appends the possible top right diagonal of piece positions to array
        while c >= 0 and d < 8 and type(self.board[c][d]) == str:
            self.validate_and_append_position(diagonalPosition, [c,d], piece)
            c-=1
            d+=1
        if c >= 0 and d < 8 and type(self.board[c][d]) != str and self.board[c][d].getColor() != pieceColor:
            self.validate_and_append_position(diagonalPosition, [c,d], piece)

        e = xPos+1
        f = yPos+1
        g = xPos-1
        h = yPos-1

        #Appends the possible bottom right diagonal of piece positions to array
        while e < 8 and f < 8 and type(self.board[e][f]) == str:
            self.validate_and_append_position(diagonalPosition, [e,f], piece)
            e+=1
            f+=1
        if e < 8 and f < 8 and type(self.board[e][f]) != str and self.board[e][f].getColor() != pieceColor:
            self.validate_and_append_position(diagonalPosition, [e,f], piece)

        #Appends the possible top left diagonal of piece positions to array
        while g >= 0 and h >= 0 and type(self.board[g][h]) == str:
            self.validate_and_append_position(diagonalPosition, [g,h], piece)
            g-=1
            h-=1
        
        if g >= 0 and h >= 0 and type(self.board[g][h]) != str and self.board[g][h].getColor() != pieceColor:
            self.validate_and_append_position(diagonalPosition, [g,h], piece)

        return diagonalPosition
    
    #Given the chosen horse piece position, an array of possible horse positions to move to is outputted
    def find_horse_positions(self, piece):
        availablePositions = []

        xPos, yPos = piece.getPosition()[0], piece.getPosition()[1]
        pieceColor = piece.getColor()

        # checks position 2 north 1 east 
        if xPos+2 < 8 and yPos+1 < 8 and (type(self.board[xPos+2][yPos+1]) == str or self.board[xPos+2][yPos+1].getColor() != pieceColor):
            self.validate_and_append_position(availablePositions, [xPos+2, yPos+1], piece)

        # checks position 2 north 1 west
        if xPos+2 < 8 and yPos-1 >= 0 and (type(self.board[xPos+2][yPos-1]) == str or self.board[xPos+2][yPos-1].getColor() != pieceColor):
            self.validate_and_append_position(availablePositions, [xPos+2, yPos-1], piece)

        # checks position 2 west 1 north
        if xPos+1 < 8 and yPos-2 >= 0 and (type(self.board[xPos+1][yPos-2]) == str or self.board[xPos+1][yPos-2].getColor() != pieceColor):
            self.validate_and_append_position(availablePositions, [xPos+1, yPos-2], piece)
          
        # checks position 2 west 1 south
        if xPos-1 >= 0 and yPos-2 >= 8 and (type(self.board[xPos-1][yPos-2]) == str or self.board[xPos-1][yPos-2].getColor() != pieceColor):
            self.validate_and_append_position(availablePositions, [xPos-1, yPos-2], piece)

        # checks position 2 south 1 west
        if xPos-2 >= 0 and yPos-1 >= 0 and (type(self.board[xPos-2][yPos-1]) == str or self.board[xPos-2][yPos-1].getColor() != pieceColor):
            self.validate_and_append_position(availablePositions, [xPos-2, yPos-1], piece)

        # checks position 2 south 1 east
        if xPos-2 >= 0 and yPos+1 < 8 and (type(self.board[xPos-2][yPos+1]) == str or self.board[xPos-2][yPos+1].getColor() != pieceColor):
            self.validate_and_append_position(availablePositions, [xPos-2, yPos+1], piece)

        # checks position 2 east 1 south
        if xPos-1 >= 0 and yPos+2 < 8 and (type(self.board[xPos-1][yPos+2]) == str or self.board[xPos-1][yPos+2].getColor() != pieceColor):
            self.validate_and_append_position(availablePositions, [xPos-1, yPos+2], piece)

        # checks position 2 east 1 north
        if xPos+1 < 8 and yPos+2 < 8 and (type(self.board[xPos+1][yPos+2]) == str or self.board[xPos+1][yPos+2].getColor() != pieceColor):
            self.validate_and_append_position(availablePositions, [xPos-1, yPos+2], piece)
    
        return availablePositions
    
    #Given the chosen king piece position, an array of possible king positions to move to is outputted
    def find_king_positions(self, piece):
        availablePositions = []
        xPos, yPos = piece.getPosition()[0], piece.getPosition()[1]

        #moves up
        if xPos+1 < 8 and (type(self.board[xPos+1][yPos]) == str or self.board[xPos+1][yPos].getColor() != piece.getColor()) and not self.validateKingCheck(piece, [xPos+1, yPos]):
            availablePositions.append([xPos+1, yPos])

        #moves down
        if xPos-1 >= 0 and (type(self.board[xPos-1][yPos]) == str or self.board[xPos-1][yPos].getColor() != piece.getColor()) and not self.validateKingCheck(piece, [xPos-1, yPos]):
            self.validate_and_append_position(availablePositions, [xPos-1, yPos], piece)

        #moves left
        if yPos-1 >= 0 and (type(self.board[xPos][yPos-1]) == str or self.board[xPos][yPos-1].getColor() != piece.getColor()) and not self.validateKingCheck(piece, [xPos, yPos-1]):
            availablePositions.append([xPos, yPos-1])

        #moves right
        if yPos+1 < 8 and (type(self.board[xPos][yPos+1]) == str or self.board[xPos][yPos+1].getColor() != piece.getColor()) and not self.validateKingCheck(piece, [xPos, yPos+1]):
            availablePositions.append([xPos, yPos+1])

        #moves top right
        if xPos+1 < 8 and yPos+1 < 8 and (type(self.board[xPos+1][yPos+1]) == str or self.board[xPos+1][yPos+1].getColor() != piece.getColor()) and not self.validateKingCheck(piece, [xPos+1, yPos+1]):
            availablePositions.append([xPos+1, yPos+1])

        #moves top left
        if xPos+1 < 8 and yPos-1 >= 0 and (type(self.board[xPos+1][yPos-1]) == str or self.board[xPos+1][yPos-1].getColor() != piece.getColor()) and not self.validateKingCheck(piece, [xPos+1, yPos-1]):
            availablePositions.append([xPos+1, yPos-1])

        #moves bottom right
        if xPos-1 >= 0 and yPos+1 < 8 and (type(self.board[xPos-1][yPos+1]) == str or self.board[xPos-1][yPos+1].getColor() != piece.getColor()) and not self.validateKingCheck(piece, [xPos-1, yPos+1]):
            availablePositions.append([xPos-1, yPos+1])

        #moves bottom left
        if xPos-1 >= 0 and yPos-1 >= 0 and (type(self.board[xPos-1][yPos-1]) == str or self.board[xPos-1][yPos-1].getColor() != piece.getColor()) and not self.validateKingCheck(piece, [xPos-1, yPos-1]):
            availablePositions.append([xPos-1, yPos-1])

        return availablePositions
    
    #Takes the array you want to append to, the piece and position you're validating to see if moving results in check
    def validate_and_append_position(self, array, position, piece):
        xPos, yPos = position[0], position[1]
        if piece.getName() != 'K':
            if not self.validateCheck(piece, [xPos, yPos]):
                array.append([xPos, yPos])
        else:
                array.append([xPos, yPos])

    def validateKingCheck(self, king, new_position):
        xPos, yPos = king.getPosition()[0], king.getPosition()[1]
        new_position_piece = enemy_piece_color = ' '
        checked = False

        if type(self.board[new_position[0]][new_position[1]]) != str:
            new_position_piece = self.board[new_position[0]][new_position[1]].getName()
    
        if king.getColor() == 'W':
            enemy_piece_color = 'B'
        else:
            enemy_piece_color = 'W'

        self.board[xPos][yPos] = ' '
        self.board[new_position[0]][new_position[1]] = king
        king.setPosition(new_position)

        #Check if king is checked horizontally or vertically
        horizontal_or_vertical = []
        horizontal_or_vertical += (self.find_hoz_positions(king))
        horizontal_or_vertical += (self.find_vert_positions(king))
        #Get all castle and queen positions to see if the king is in their range
        queenAndCastlePositions = [piece.getPosition() for piece in self.getPieces() if piece.getColor() == enemy_piece_color and (piece.getName() == 'Q' or piece.getName() == 'C')]
        #Check is any castles or queens are in view of king horizontally or vertically
        for pos in queenAndCastlePositions:
            if pos in horizontal_or_vertical:
                checked = True

        #Check if king is checked diagonally
        diagonally = self.find_diag_positions(king)
        #Get all castle and queen positions to see if the king is in their range
        queenAndBishopPositions = [piece.getPosition() for piece in self.getPieces() if piece.getColor() == enemy_piece_color and (piece.getName() == 'Q' or piece.getName() == 'B')]
        #Check is any bishops or queens are in view of king diagonally
        for pos in queenAndBishopPositions:
            if pos in diagonally:
                checked = True

        #Check if king is checked by horse
        horse = self.find_horse_positions(king)
        #Get all horse  positions to see if the king is in their range
        horsePositions = [piece.getPosition() for piece in self.getPieces() if piece.getColor() == enemy_piece_color and piece.getName() == 'H']
        #Check is any horses are in view of king
        for pos in horsePositions:
            if pos in horse:
                checked = True
        
        #Check if king is checked by pawn
        pawn = self.find_pawn_positions(king)
        #Get all pawn positions to see if the king is in their range
        pawnPositions = [piece.getPosition() for piece in self.getPieces() if piece.getColor() == enemy_piece_color and piece.getName() == 'P']
        #Check is any horses are in view of king
        for pos in pawnPositions:
            if pos in pawn:
                checked = True

        self.board[xPos][yPos] = king 
        self.board[new_position[0]][new_position[1]] = new_position_piece
        king.setPosition([xPos, yPos])

        return checked
    
    #From the kings position, it checks whether it is in check with any opposing pieces. 
    def validateCheck(self, piece, new_position):

        xPos, yPos = piece.getPosition()[0], piece.getPosition()[1]
        new_position_piece = enemy_piece_color = king = ' '
        checked = False

        if type(self.board[new_position[0]][new_position[1]]) != str:
            new_position_piece = self.board[new_position[0]][new_position[1]].getName()
    
        if piece.getColor() == 'W':
            king = self.getWhiteKing()
            enemy_piece_color = 'B'
        else:
            king = self.getBlackKing()
            enemy_piece_color = 'W'

        self.board[xPos][yPos] = ' '
        self.board[new_position[0]][new_position[1]] = piece

        #Check if king is checked horizontally or vertically
        horizontal_or_vertical = []
        horizontal_or_vertical += (self.find_hoz_positions(king))
        horizontal_or_vertical += (self.find_vert_positions(king))
        #Get all castle and queen positions to see if the king is in their range
        queenAndCastlePositions = [piece.getPosition() for piece in self.getPieces() if piece.getColor() == enemy_piece_color and (piece.getName() == 'Q' or piece.getName() == 'C')]
        #Check is any castles or queens are in view of king horizontally or vertically
        for pos in queenAndCastlePositions:
            if pos in horizontal_or_vertical:
                checked = True

        #Check if king is checked diagonally
        diagonally = self.find_diag_positions(king)
        #Get all castle and queen positions to see if the king is in their range
        queenAndBishopPositions = [piece.getPosition() for piece in self.getPieces() if piece.getColor() == enemy_piece_color and (piece.getName() == 'Q' or piece.getName() == 'B')]
        #Check is any bishops or queens are in view of king diagonally
        for pos in queenAndBishopPositions:
            if pos in diagonally:
                checked = True

        #Check if king is checked by horse
        horse = self.find_horse_positions(king)
        #Get all horse  positions to see if the king is in their range
        horsePositions = [piece.getPosition() for piece in self.getPieces() if piece.getColor() == enemy_piece_color and piece.getName() == 'H']
        #Check is any horses are in view of king
        for pos in horsePositions:
            if pos in horse:
                checked = True
        
        #Check if king is checked by pawn
        pawn = self.find_pawn_positions(king)
        #Get all pawn positions to see if the king is in their range
        pawnPositions = [piece.getPosition() for piece in self.getPieces() if piece.getColor() == enemy_piece_color and piece.getName() == 'P']
        #Check is any horses are in view of king
        for pos in pawnPositions:
            if pos in pawn:
                checked = True

        self.board[xPos][yPos] = piece
        self.board[new_position[0]][new_position[1]] = new_position_piece

        return checked
    
    def validate_checkmate(self, color):
        horseMoves = [self.find_horse_positions(piece) for piece in self.getPieces() if piece.getColor() == color and piece.getName() == 'H']
        queenMoves = [self.find_hoz_positions(piece)+self.find_vert_positions(piece) for piece in self.getPieces() if piece.getColor() == color and piece.getName() == 'Q']
        bishopMoves = [self.find_diag_positions(piece) for piece in self.getPieces( ) if piece.getColor() == color and piece.getName() == 'B']
        pawnMoves = [self.find_pawn_positions(piece) for piece in self.getPieces( ) if piece.getColor() == color and piece.getName() == 'P']
        castleMoves = [self.find_hoz_positions(piece) for piece in self.getPieces( ) if piece.getColor() == color and piece.getName() == 'C']
        kingMoves = [self.find_king_positions(piece) for piece in self.getPieces( ) if piece.getColor() == color and piece.getName() == 'K']

        allMoves = horseMoves+queenMoves+bishopMoves+pawnMoves+castleMoves+kingMoves
        for move in allMoves:
            if len(move)>0:
                return False
        self.checkMate = True
        return True
        



initialTurn = 'W'
board = Board(initialTurn)

while board.getCheckMate() != True:
    positions = input('Enter a x and y position of a piece you want to move: ')
    print()
    board.potentialMoves([int(positions[0]), int(positions[1])])

print('Checkmate!')