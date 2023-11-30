class ChessPiece():
    def __init__(self, position, color, deletePiece):
        self.name = ''
        self.position = position    
        self.color = color
        self.deletePiece = deletePiece

    def move(self, *args):
        moveChoices = args[0]

        print('You can:')
        print()
        print('0 for cancel')
        for i in range(len(moveChoices)):
            print(f'{i+1} for {moveChoices[i]}')
        move = int(input('\nChoose a move: '))
       
        while move not in [x for x in range(len(moveChoices)+1)]: #Must choose a move out of the choices provided
            move = int(input('\nChoose a move out of these choices: '))
            
        chosenPosition = moveChoices[move-1]

        if chosenPosition != ' ':
            self.deletePiece(chosenPosition)
        
        self.position = (chosenPosition)
        
        return chosenPosition

    def getName(self):
        return self.name
    
    def getPosition(self):
        return self.position
    
    def getColor(self):
        return self.color
    
    def setPosition(self, position):
        self.position = position