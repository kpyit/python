# скачал отсюда
# https://www.kaggle.com/code/slobo777/tic-tac-toe-agent-using-q-learning/data

 

import numpy as np
import csv
import random
from itertools import groupby
import tensorflow as tf
from keras.layers import Dense  # полносвязные нейронные слои - Dense

class TicTacToeGame():
    def __init__(self):
        
        self.state = '         ' # 9 возможных состояний
        self.player = 'X'
        self.winner = None

        # вознаграждния по умолчанию при ходе
        self.rewards = [
          0.1, 0.1, 0.1,
          0.1, 0.1, 0.1,
          0.1, 0.1, 0.1
        ]
        training =  {
                'X' : { 'inputs': [], 'labels': [] },
                'O' : { 'inputs': [], 'labels': [] },
            }
        agents = { 'X': [], 'O': [] }

        self.modelX: tf.sequential()
        self.modelO: tf.sequential()
 

        # 10  = клетки + вес
        self.modelX.add(Dense(128, input_dim=10, activation='sigmoid'))
        #1 дополнительный слой
        self.modelX.add(Dense(9, activation='sigmoid'))

        self.modelO.add(Dense(128, input_dim=10, activation='sigmoid'))
        #1 дополнительный слой
        self.modelO.add(Dense(9, activation='sigmoid'))


        self.modelX.compile(
            optimizer= 'adam',
            loss= 'meanSquaredError'
        )

        self.modelO.compile(
            optimizer= 'adam',
            loss= 'meanSquaredError'
        )


    # список доступных ходов
    def allowed_moves(self):
        states = []
        for i in range(len(self.state)):
            if self.state[i] == ' ':
                # фактически строка с новым заполненным полем которое было пустым и все остальное состояние копируется
                states.append(self.state[:i] + self.player + self.state[i+1:])
        return states

    # совершить ход
    def make_move(self, next_state):
        if self.winner:
            raise(Exception("Game already completed, cannot make another move!"))
        if not self.__valid_move(next_state):
            raise(Exception("Cannot make move {} to {} for player {}".format(
                    self.state, next_state, self.player)))


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

    # можно ли туда шагнуть
    def __valid_move(self, next_state):
        allowed_moves = self.allowed_moves()
        if any(state == next_state for state in allowed_moves):
            return True
        return False

    # печать доски с текущим состоянием
    def print_board(self):
        s = self.state
        print('     {} | {} | {} '.format(s[0],s[1],s[2]))
        print('    -----------')
        print('     {} | {} | {} '.format(s[3],s[4],s[5]))
        print('    -----------')
        print('     {} | {} | {} '.format(s[6],s[7],s[8]))






class Agent():
    # класс отвечающий за игру передается внутрь
    #игрок X по умолчанию
    def __init__(self, game_class, epsilon=0.1, alpha=0.5, value_player='X'):
        self.V = dict() # словарь
        #Передать можно лююую игру
        self.NewGame = game_class
        self.epsilon = epsilon
        self.alpha = alpha
        self.value_player = value_player


    def state_value(self, game_state):
        return self.V.get(game_state, 0.0)

# обучение на количестве игр
    def learn_game(self, num_episodes=1000):
        # по количеству эпизодов переданных обучаем на каждом
        for episode in range(num_episodes):
            self.learn_from_episode()

    def learn_from_episode(self):

        game = self.NewGame()
        #выбираем первое действие из доступных
        _, move = self.learn_select_move(game)
        # пока есть
        while move:
            move = self.learn_from_move(game, move)


    ########################################################################################################################
    # САМАЯ ВАЖНАЯ ФУНКЦИЯ
    ########################################################################################################################
    # 
    def learn_from_move(self, game, move):
        #Делаем следующий ход с проверкой на выйгравшего 
        game.make_move(move)
        #смотрим вознаграждение
        #если текущий игрок выйграл +1 проиграл -1 не изменился 0
        #еще сюда надо бы перекрытие окончания конкуренту 0.5
        r = self.__reward(game)
        # вознаграждение за текущий шаг
        td_target = r 
        #
        next_state_value = 0.0
        #
        selected_next_move = None

        # ЕСЛИ НЕТ ВЫЙГРАВШЕГО И ЕСТЬ ПУСТЫЕ КЛЕТКИ НА ПОЛЕ
        #
        if game.playable():
            # получаем лучшее на текущий момент решение и рандомное/лучшее
            best_next_move, selected_next_move = self.learn_select_move(game)
            # берем вес лучшего решения при этом он может быть и 0
            next_state_value = self.state_value(best_next_move)

        #Смотрим в базе вес текущего шага
        current_state_value = self.state_value(move)
        #увеличиваем вес текущего шага если можем шагать дальше по лучшему из доступных
        td_target = r + next_state_value

        #заносим в базу|словарь шаг с потенциалом следующего лучшего решения если оно есть

        # оценка идет по лучшему но возвращаем шаг случайный!!
        self.V[move] = current_state_value + self.alpha * (td_target - current_state_value)

        return selected_next_move

    def learn_select_move(self, game):
        # берем доступные действия у игры
        # переводим в словарь с весами качества
        allowed_state_values = self.__state_values( game.allowed_moves())
        # если обучаемый игрок например X текущий обучаемый
        if game.player == self.value_player:
            # берем лучший вариант из словаря для обучения нейросети
            best_move = self.__argmax_V(allowed_state_values)
        else:
            # для 2 игрока худший вариант почему-то
            best_move = self.__argmin_V(allowed_state_values)

        # выбранный ход лучний ход?
        selected_move = best_move

        # элемент случайности rand < 0.1
        if random.random() < self.epsilon:
            # случаййное действие из списка доступных
            selected_move = self.__random_V(allowed_state_values)

        # возврат и лучшего на текущий момент и выбранного возможно случайного возможно лучшего
        return (best_move, selected_move)


    def play_select_move(self, game):
        # СЛОВАРЬ С ДОСТУПНЫМИ ШАГАМИ НА ИТЕРАЦИИ
        allowed_state_values = self.__state_values( game.allowed_moves())
        # ЕСЛИ ШАГ ВЫБРАННОГО ИГРОКА
        if game.player == self.value_player:
            # БЕРЕМ ШАГ С ЛУЧШИМ ВЕСОМ
            return self.__argmax_V(allowed_state_values)
        else:
            # У 2 С МИНИМАЛЬНЫМ
            return self.__argmin_V(allowed_state_values)

# verbose подробный
    def demo_game(self, verbose=False):
        game = self.NewGame()
        t = 0
        # пока не заняты все клетки или ктото не выйграл
        while game.playable():
            if verbose:
                print(" \nTurn {}\n".format(t))
                # печать текущей доски
                game.print_board()
            #выбирает шаг с лучшим весом
            move = self.play_select_move(game)
            #делаем шаг  с тестом на выйгравшего
            game.make_move(move)
            t += 1

        # в конце матча когда выйграл или все заполнено
        if verbose:
            print(" \nTurn {}\n".format(t))
            game.print_board()
            # если есть выйгравший
        if game.winner:
            if verbose:
                print("\n{} is the winner!".format(game.winner))
            return game.winner
        else:
            if verbose:
                print("\nIt's a draw!")
            return '-'


    def interactive_game(self, agent_player='X'):
        game = self.NewGame()
        t = 0
        while game.playable():
            print(" \nTurn {}\n".format(t))
            game.print_board()
            if game.player == agent_player:
                move = self.play_select_move(game)
                game.make_move(move)
            else:
                move = self.__request_human_move(game)
                game.make_move(move)
            t += 1

        print(" \nTurn {}\n".format(t))
        game.print_board()

        if game.winner:
            print("\n{} is the winner!".format(game.winner))
            return game.winner
        print("\nIt's a draw!")
        return '-'




    def round_V(self):
        # After training, this makes action selection random from equally-good choices
        for k in self.V.keys():
            #  
            self.V[k] = round(self.V[k],1) 

    def save_v_table(self):
        with open('state_values.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['State', 'Value'])
            all_states = list(self.V.keys())
            all_states.sort()
            for state in all_states:
                writer.writerow([state, self.V[state]])

            print('end write')

    def __state_values(self, game_states):
        # строки текущего состояния с запоненной след возможным шагом
        # переводим в словарь и в значение заносим уровень вознаграждения за совершеное действие хранимое в словаре - v
        return dict((state, self.state_value(state)) for state in game_states)

    # выбор шага с макс вознаграждением
    def __argmax_V(self, state_values):
        max_V = max(state_values.values())
        chosen_state = random.choice([state for state, v in state_values.items() if v == max_V])
        return chosen_state

    # выбор шага с минимальным вознаграждением
    def __argmin_V(self, state_values):
        min_V = min(state_values.values())
        chosen_state = random.choice([state for state, v in state_values.items() if v == min_V])
        return chosen_state

    def __random_V(self, state_values):
        return random.choice(list(state_values.keys()))


    # вознаграждение за шаг
    def __reward(self, game):
        if game.winner == self.value_player:
            return 1.0
        elif game.winner:
            return -1.0
        else:
            return 0.0

    def __request_human_move(self, game):
        allowed_moves = [i+1 for i in range(9) if game.state[i] == ' ']
        human_move = None
        while not human_move:
            idx = int(input('Choose move for {}, from {} : '.format(game.player, allowed_moves)))
            if any([i==idx for i in allowed_moves]):
                human_move = game.state[:idx-1] + game.player + game.state[idx:]
        return human_move

    def print_V(self):
        print(self.V)

 
# запуск кучи игр с просмотром и заполнение словаря действий
def demo_game_stats(agent):
    # results = [agent.demo_game() for i in range(10000)]
    # results = [agent.demo_game(True) for i in range(1000)]
    results = [agent.demo_game(True) for i in range(2)]
    agent.print_V()

    game_stats = {k: results.count(k)/100 for k in ['X', 'O', '-']}
    print("    percentage results: {}".format(game_stats))

if __name__ == '__main__':

    agent = Agent(TicTacToeGame, epsilon = 0.1, alpha = 1.0)
    # не о чем просто идет случайные партии без обучения словарь не наполняется
    print("состояние перед обучением:")
    demo_game_stats(agent)

    # где то после 6 тысяч мы всегда приходим в ничью
    #скорее всего заполняется словать с правильными ходами но не ясно как случайные переходы формируются
    agent.learn_game(1000)
    print("After 10 learning games:")
    demo_game_stats(agent)

    # agent.learn_game(4000)
    # print("After 5000 learning games:")
    # demo_game_stats(agent)

    # agent.learn_game(5000)
    # print("After 10000 learning games:")
    # demo_game_stats(agent)

    # agent.learn_game(10000)
    # print("After 20000 learning games:")
    # demo_game_stats(agent)

    # agent.learn_game(10000)
    # print("After 30000 learning games:")
    # demo_game_stats(agent)


    agent.round_V()
    agent.save_v_table()
    