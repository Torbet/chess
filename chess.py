class Chess():
    def __init__(self):
        self.board = []
        self.pieces = {
            "empty": Empty,
            "r": Rook,
            "n": Knight,
            "p": Pawn,
            "b": Bishop,
            "q": Queen,
            "k": King,
        }
        self.ranks = {
            "a": 0,
            "b": 1,
            "c": 2,
            "d": 3,
            "e": 4,
            "f": 5,
            "g": 6,
            "h": 7
        }

    def placePieces(self, fen):
        #starting FEN: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR
        self.board.append([])
        row = 0
        col = 0
        for i in fen:
            if i == "/":
                self.board.append([])
                row += 1
                col = 0
            elif i.isnumeric():
                for x in range(int(i)):
                    self.board[row].append(Empty(self.board, None, (row, col)))
                    col += 1
            else:
                if i.islower():
                    side = "b"
                elif i.isupper():
                    side = "w"
                self.board[row].append(self.pieces[i.lower()](self.board, side, (row, col)))
                col += 1


    def display(self):
        for row in self.board:
            for i in row:
                i.availableMoves()
                print(i, end="  ")
            print("")
        print('\n\n')
    
    def move(self, start, end):
        piece = self.board[start[0]][start[1]]
        piece.position = end
        piece.movesMade += 1
        self.board[start[0]][start[1]] = Empty(self.board, None, (start[0], start[1]))
        self.board[end[0]][end[1]] = piece
    
    def pgn(self, pgn):
        #example pgn: 1. e4 e6 2. d4 d5 3. Nc3 Nf6 4. Bg5 dxe4 5. Nxe4 Nbd7 6. Bd3 h6 7. Bh4 g5 8. Bg3 Nxe4 9. Bxe4 f5 10. Qh5+ Ke7 11. h4
        moves = pgn.replace("+", "").replace("#", "").split(" ")
        for i in moves:
            if "." in i:
                moves.remove(i)
        for move in moves:
            endpos = (8 - int(move[-1]), self.ranks[move[-2]])
            available = self.board[endpos[0]][endpos[1]].availableTo
            if len(move) == 2:
                print(move)
                for p in available:
                    if self.board[p[0]][p[1]].__class__.__name__ == "Pawn":
                        self.move(p, endpos)
                        self.display()




#piece movement patterns
Cardinals = [(1,0),(0,1),(-1,0),(0,-1)]
Diagonals = [(1,1),(-1,1),(1,-1),(-1,-1)]
KnightMoves = [(1, 2), (2, 1), (-1, -2), (-2, -1), (1, -2), (2, -1), (-1, 2), (-2, 1)]

class Piece():
    def __init__(self, board, color, position):
        self.color = color
        self.position = position
        self.movesMade = 0
        self.stringRep = ""
        self.board = board
        self.availableTo = []
        

    def __str__(self):
        if self.color == "b":
            return self.stringRep.lower()
        else: return self.stringRep
    
    def isInBounds(self,x,y):
        if x >= 0 and x < 8 and y >= 0 and y < 8:
            return True
        return False

    def getMoves(self, x, y, color, directions, single=False):
        moves = []
        for xint, yint in directions:
            xtemp,ytemp = x+xint,y+yint
            while self.isInBounds(xtemp,ytemp):
                
                target = self.board[xtemp][ytemp]

                if target == '·': 
                    moves.append((xtemp,ytemp))

                elif target.color != color: 
                    target.availableTo.append((self.position))
                    moves.append((xtemp,ytemp))
                    break

                else:
                    break

                if single == True: break
                
                xtemp, ytemp = xtemp + xint, ytemp + yint
        return moves

    def availableMoves(self):
        pass

    def showMoves(self):
        for move in self.availableMoves():
            self.board[move[0]][move[1]] = "+"

class Empty(Piece):
    def __init__(self, board, side, position):
        super().__init__(board, side, position)
        self.stringRep = "·"
    def availableMoves(self):
        pass

class Rook(Piece):
    def __init__(self, board, side, position):
        super().__init__(board, side, position)
        self.stringRep = "R"

    def availableMoves(self):
        return self.getMoves(self.position[0], self.position[1], self.color, Cardinals)

class Pawn(Piece):
    def __init__(self, board, side, position):
        super().__init__(board, side, position)
        self.stringRep = "P"
        
    def availableMoves(self):
        #this really needs tidied up, pawns are fucking annoying
        moves = []
        dir = 0
        if self.color == "w": dir = -1
        if self.color == "b": dir = 1
        if (self.movesMade == 0) and (self.board[self.position[0] + 2*dir][self.position[1]].__class__.__name__ == "Empty"):
            moves.append((self.position[0] + 2*dir, self.position[1]))
            self.board[self.position[0] + 2*dir][self.position[1]].availableTo.append((self.position[0], self.position[1]))
        if self.board[self.position[0] + dir][self.position[1]].__class__.__name__ == "Empty":
            moves.append((self.position[0] + dir, self.position[1]))
            self.board[self.position[0] + dir][self.position[1]].availableTo.append((self.position[0], self.position[1]))
        if self.isInBounds(self.position[0] + dir, self.position[1]+1) and self.board[self.position[0] + dir][self.position[1]+1].__class__.__name__ != "Empty" and self.board[self.position[0] + dir][self.position[1]+1].color != all([self.color, None]): moves.append((self.position[0] + dir, self.position[1]+1))
        if self.isInBounds(self.position[0] + dir, self.position[1]-1) and self.board[self.position[0] + dir][self.position[1]-1].__class__.__name__ != "Empty" and  self.board[self.position[0] + dir][self.position[1]-1].color != all([self.color, None]): moves.append((self.position[0] + dir, self.position[1]-1))
        return moves



class Queen(Piece):
    def __init__(self, board, side, position):
        super().__init__(board, side, position)
        self.stringRep = "Q"
    def availableMoves(self):
        return self.getMoves(self.position[0], self.position[1], self.color, Cardinals + Diagonals)

class Bishop(Piece):
    def __init__(self, board, side, position):
        super().__init__(board, side, position)
        self.stringRep = "B"
    def availableMoves(self):
        return self.getMoves(self.position[0], self.position[1], self.color, Diagonals)
        
class King(Piece):
    def __init__(self, board, side, position):
        super().__init__(board, side, position)
        self.stringRep = "K"
    def availableMoves(self):
        return self.getMoves(self.position[0], self.position[1], self.color, Cardinals, single=True)

class Knight(Piece):
    def __init__(self, board, side, position):
        super().__init__(board, side, position)
        self.stringRep = "N"
    def availableMoves(self):
        return self.getMoves(self.position[0], self.position[1], self.color, KnightMoves, single=True)





chess = Chess()
chess.placePieces("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
#chess.board[1][4].showMoves()
chess.display()



chess.pgn("1. e4 e6 2. d4 d5 3. Nc3 Nf6 4. Bg5 dxe4 5. Nxe4 Nbd7 6. Bd3 h6 7. Bh4 g5 8. Bg3 Nxe4 9. Bxe4 f5 10. Qh5+ Ke7 11. h4")
