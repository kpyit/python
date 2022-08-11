
class tic_tac_toe():
    def __init__(self):
        
        self.state = '         ' # 9 возможных состояний
        self.player = 'X'
        self.winner = None

    # список доступных ходов
    def allowed_moves(self):
        states = []
        
        for i in range(len(self.state)):
            if self.state[i] == ' ':
                # фактически строка с новым заполненным полем которое было пустым и все остальное состояние копируется
                states.append(self.state[:i] + self.player + self.state[i+1:])
        # [states.append(self.state[:i] + self.player + self.state[i+1:]) for i in range(len(self.state)) if self.state[i] == ' ']            
        return states

        
        
        return states



    # совершить ход
    def make_move(self, next_state):
        self.state = next_state
        # проверка на выйгрыш собрался ли ряд Х или O
        self.winner = self.predict_winner(self.state)
        # или если есть выйгравший дальнейший игрок не определен его нет  а выйгравшего можно посмотреть в self.winner
        if self.winner:
            self.player = None
        elif self.player == 'X':
            self.player = 'O'
        else:
            self.player = 'X'
 
    # еще играем или закончили
    def playable(self):
        return ( (not self.winner) and any(self.allowed_moves()) )

    #выйграл ли кто либо
    def predict_winner(self, state):
        lines = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        winner = None
        for line in lines:
            line_state = state[line[0]] + state[line[1]] + state[line[2]]
            if line_state == 'XXX':
                winner = 'X'
            elif line_state == 'OOO':
                winner = 'O'
        return winner
 

    # печать доски с текущим состоянием
    def print_board(self):
        s = self.state
        print('     {} | {} | {} '.format(s[0],s[1],s[2]))
        print('    -----------')
        print('     {} | {} | {} '.format(s[3],s[4],s[5]))
        print('    -----------')
        print('     {} | {} | {} '.format(s[6],s[7],s[8]))
 

    def game(self): 
        t = 0 # тактирование игры
        while self.playable():
            if(t%2==0):
                move = self.request_move('X')                
                self.make_move(move)
            else:
                move = self.request_move('O')
                self.make_move(move) 
            t += 1

            print(f" Шаг {t}")
            self.print_board()



        if self.winner:
            print(f" {self.winner} поздравляем победил !")
        else:
            print(r'Никто не выйграл')
        #     # выходим
        #     return self.winner
        # return ''

    def request_move(self, char = 'X'):
        allowed_moves = [i+1 for i in range(9) if self.state[i] == ' ']
        human_move = None
        while not human_move:
            idx = int(input(f"Выберите для {char}, из {allowed_moves} "))
            if any([i==idx for i in allowed_moves]):
                human_move = self.state[:idx-1] + char + self.state[idx:] #заносим в строку позицию
        return human_move


toe = tic_tac_toe()
toe.game()

