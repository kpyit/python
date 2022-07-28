from os import system
from time import sleep
from random import choice
import operator 
import tensorflow as tf
 
from keras.models import Sequential
# from keras.models import
from keras.layers import Dense  # полносвязные нейронные слои - Dense
from keras import utils
# from keras import Model
import numpy as np  # дополнительные утилиты
from keras.preprocessing import image


isAutomatic = True
isDuel = True
isDelay = False


#Чем меньше сделано ходов, тем выше награда от 0.1 до 1.0
worstReward = -1.0      #Занятая ячейка имеет награду -1.0
lossReward = -0.4       #Проигрышная ячейка получит награду -0.4
basicReward = 0.1   #Свободная ячейка имеет награду 0.1
stepReward = 0.2    #Ход в свободную ячейку увеличивает её награду до 0.2
interestReward = 0.5    #Выигрышная ячейка соперника имеет награду 0.5
bestReward = 1.0    #Победная ячейка принесёт награду 1.0

mountedIndex = 11


#DATA  
modelX: tf.sequential()
modelO: tf.sequential()
modelX
trainingCount = { 'X': 0, 'O': 0 }
training = {
    'X': { 'inputs': [], 'labels': [] },
    'O': { 'inputs': [], 'labels': [] }
}
agents = { 'X': {}, 'O': {} }
victories = { 'X': 0, 'O': 0 }
victoriesStatus = { 'X': False, 'O': False }

fieldSize = 9
step = 1
trainingGames = 1

timer = 0
timeTraining = 5 * 60

isDuel = False
duel = {
    'step': 1,
    'field': [
    '', '', '',
    '', '', '',
    '', '', '',
]
}

duelGames = 1

AIvsHuman = {
    'isDuel': False,
    'step': 1,
    'victories': { 'X': 0, 'O': 0 },
    'rewards': [
        0.1, 0.1, 0.1,
        0.1, 0.1, 0.1,
        0.1, 0.1, 0.1,
    ],
    'field': [
        '', '', '',
        '', '', '',
        '', '', '',
    ],
},

 
 
# console.log(mountedIndex);
# timer = JSON.parse(localStorage.getItem('syntet_TicTacToe_timer'));
      
# последовательная модель
modelX,modelO = Sequential()

modelX =  tf.loadLayersModel('localstorage://syntet_TicTacToe_model_X')
modelO =  tf.loadLayersModel('localstorage://syntet_TicTacToe_model_O')

modelX.compile(optimizer ='adam', loss = 'meanSquaredError')

modelO.compile(optimizer= 'adam', loss = 'meanSquaredError')

    #   this.modelX = modelX;
    #   this.modelO = modelO;
    # } else {
    #   this.setupModel({ model: this.modelX });
    #   this.setupModel({ model: this.modelO });
    # }

# по идее надо оформлять как методы класса
agentsSetting( sign = 'X' )
agentsSetting( sign = 'O' )
# this.agentsSetting( sign = 'X' )
# this.agentsSetting( sign = 'O' )

# запуск таймера для просчета времени
# this.setTimer();

if(isAutomatic):
   gameLoop()
# this.gameLoop()


# methods:
def restoreFromLocalStorage():
  print('чтение из локального хранилища')
  # this.trainingCount = JSON.parse(localStorage.getItem('syntet_TicTacToe_trainingCount'));
  # this.victories = JSON.parse(localStorage.getItem('syntet_TicTacToe_victories'));
  # this.trainingGames = JSON.parse(localStorage.getItem('syntet_TicTacToe_trainingGames'));
  # this.duelGames = JSON.parse(localStorage.getItem('syntet_TicTacToe_duelGames'));
  # this.AIvsHuman.victories = JSON.parse(localStorage.getItem('syntet_TicTacToe_AIvsHuman_victories'));

def setupModel(model):
  model.add(tf.layers.dense(
        # +1 - Количество ходов.
        inputShape = (fieldSize + 1),
        activation = 'sigmoid',
        units = 128,
      ))

# средний слой
  # model.add(tf.layers.dense(
  #        activation = 'sigmoid',
  #        units = 32,
  #     ));

  model.add(tf.layers.dense(
    activation = 'sigmoid',
    units = fieldSize,
  ))

  model.compile(
    optimizer = 'adam',
    loss = 'meanSquaredError',
  )
  


def agentsSetting( sign ):
  dict_agent = {
    'sign': sign,
    'isAlive' : True,
    'isVictory': False,
    'rewards': [
      0.1, 0.1, 0.1,
      0.1, 0.1, 0.1,
      0.1, 0.1, 0.1,
          ],
          'field': [
            '', '', '',
            '', '', '',
            '', '', '',
          ],       
  }

  agents[sign].update(dict_agent)

  # setTimer():
  #   setTimeout(this.setTimer, 1000);
  #   this.timer += 1;
    

def gameLoop():
  if (AIvsHuman.isDuel):
        agentsSetting( sign = 'X' )
        agentsSetting( sign = 'O' )

        # запуск потока который работает отдельно от основного кода
        # await new Promise((resolve) => setTimeout(resolve, 300));
        # this.gameLoop();
        # return;

  if (isDuel):
        # await this.startDuel(); асинхронный процесс
    startDuel()
    duelGames += 1
  else:
    # не ясно как это должно отрабатывать
    isDuel = (trainingGames % fieldSize) == 0
    startTraining()
    trainingGames += 1

  if (isDelay):
    print('пока нет задержки я не знаю как ее вызывать')
    # Promise асинхронный вызов но вот чего?  resolve не находится в коде
    # new Promise((resolve) => setTimeout(resolve, 300))


  if ((timer != 0) and ((timer % timeTraining) == 0)):
    saveInLocalStorage();
    saveModelsLocal();

        #  Высвобождение ресурсов, чтобы не зависала вкладка.
        # window.location.reload();
  # что то вроде самоперезапуска
  gameLoop();
    



def saveInLocalStorage():  
  print('')
  # запись статистики
  # localStorage.setItem('syntet_TicTacToe_timer', JSON.stringify(this.timer));
  # localStorage.setItem('syntet_TicTacToe_trainingCount', JSON.stringify(this.trainingCount));
  # localStorage.setItem('syntet_TicTacToe_victories', JSON.stringify(this.victories));
  # localStorage.setItem('syntet_TicTacToe_trainingGames', JSON.stringify(this.trainingGames));
  # localStorage.setItem('syntet_TicTacToe_duelGames', JSON.stringify(this.duelGames));
  # localStorage.setItem('syntet_TicTacToe_AIvsHuman_victories', JSON.stringify(this.AIvsHuman.victories));


def saveModelsLocal():
    # print('')
    modelX.save('model_X.h5')
    modelO.save('model_O.h5')
    

def startDuel():
  taskCount = 2

  global agents
      # await new Promise((resolve) => {
        
  agents_duel = [ag for ag in agents if ag['isAlive']==True]
  print(f"agents_duel {agents_duel}")

  # agents = agents.X.filter(({ isAlive }) => isAlive);
  count = agents_duel.__len__()
  print(f"agents_duel count {count}")

  if count > 0:
  
    for ag in agents_duel:      
      modelPredict( model =  modelX, agent = ag )
      count -= 1

    if count == 0:
      print('')
      # типа брейк
      # resolve();
  else:
    taskCount -= 1
    # resolve();
  


def modelPredict( model, agent ):
  global step
  global duel
  global isDuel
  # current_step = isDuel ? duel['step'] : step
  if isDuel:
    current_step = duel['step']
  else:
    current_step = step

  # field = isDuel ? duel['field'] : agent['field'];
  #ВОЗМОЖНО ДЛЯ ОТОБРАЖЕНИЯ ИСПОЛЬЗУЕТСЯ
  if isDuel:
    field = duel['field']
  else:
    field = agent['field']


def increasingInterest(model:tf.sequential, field, agent ):
  global step
  # ЧТО-ТО ВРОДЕ ТЕКУЩЕГО ШАГА ПЕРЕВЕДЕННОГО В 0-1.f
  stepInput = getStepInput(step)
  # 
  print(stepInput)
  # 
  # model= tf.sequential()
  # 
  # predictions = model.predict(tf.tensor2d([agent.rewards.concat([stepInput])])).data();

# https://russianblogs.com/article/3754854107/
# https://js.tensorflow.org/api/latest/
# создает 2 мерный вектор работает только в js
  # revards = tf.tensor2d([agent.rewards.concat([stepInput])])
  current_agent_rewards = agent['rewards'].copy().append(stepInput)
  print(f"current_agent_rewards - {current_agent_rewards}")
  

  # revards = tf.tensor2d(current_agent_rewards)
  # вроде как аналог
  # https://docs.w3cub.com/tensorflow~python/tf/tensor
  const = tf.constant(current_agent_rewards)
  



  print(f'revards - {revards}')

  # https://www.tensorflow.org/api_docs/python/tf/keras/Sequential#predict
  # https://github.com/keras-team/keras/blob/v2.9.0/keras/engine/training.py#L1869-L2064
  # возващает Numpy array(s) of predictions. 
  predictions = model.predict(revards)
  print(f'predictions - {predictions}')


  # подозреваю что не работает!!
  predictions_data = predictions.data()
  print(f'predictions_data - {predictions_data}')


  cellIndex = predictions.indexOf(Math.max(...predictions));

  if field['cellIndex'].length == 0:
    sign  = agent;
    field.splice(cellIndex, 1, sign);

    agent.rewards = recalculateRewards( rewards = agent.rewards, field )
    isWinner = determineWinner(field, sign )

    if (isWinner):
      agent.isAlive = False
      agent.isVictory = True
      agent.rewards[cellIndex] = bestReward;

      saveTraining( type: 'winner', field, agent, stepInput )

      if (isDuel):
        victories[sign] += 1
        victoriesStatus[sign] = True
      
      else:
        agent['rewards'][cellIndex] = basicReward
        saveTraining( type: 'step', field, agent, stepInput )
    
  else:
    agent['isAlive'] = False
    agent.rewards = recalculateRewards( rewards = agent.rewards, field )

    saveTraining( type: 'loss', field, agent, stepInput )



# не ясно но похоже на приведение к 0.0-1.0 формату текущего шага
def getStepInput(step):
  global fieldSize
  print(f'1 - (step / fieldSize) = {1 - (step / fieldSize)}')
  return 1 - (step / fieldSize)



# перерачет вознаграждений в зависимости от свобоности или занятости ячеек
def recalculateRewards( rewards, field ):
  global basicReward
  global worstReward
  reward=0 # внутрення переменная

  if (field[index].length == 0):
          reward = basicReward
  else:
          reward = worstReward

  return [reward for i in range(9)];





      await new Promise((resolve) => {
        const agents = this.agents.O.filter(({ isAlive }) => isAlive);
        let count = agents.length;

        if (count > 0) {
          agents.forEach(async (agent) => {
            await this.modelPredict({ model: this.modelO, agent });
            count -= 1;

            if (count === 0) {
              resolve();
            }
          });
        } else {
          taskCount -= 1;
          resolve();
        }
      });

      if (taskCount === 2) {
        this.duel.step = this.fieldSize;
      }

      if (this.duel.step === this.fieldSize) {
        await Promise.all([
          this.modelFit({ model: this.modelX, sign: 'X' }),
          this.modelFit({ model: this.modelO, sign: 'O' }),
        ]);

        this.isDuel = false;

        this.duel = {
          step: 1,
          field: [
            '', '', '',
            '', '', '',
            '', '', '',
          ],
        };
      } else {
        this.duel.step += 1;
      }
    },

    // Знаки обучаются ходить.
    async startTraining() {
      const tasks = this.agents.X.filter(({ isAlive }) => isAlive)
        .map((agent) => this.modelPredict({ model: this.modelX, agent }))
        .concat(this.agents.O.filter(({ isAlive }) => isAlive)
          .map((agent) => this.modelPredict({ model: this.modelO, agent })));

      if (tasks.length === 0) {
        this.step = this.fieldSize;
      } else {
        await Promise.all(tasks);
      }

      if (this.step === this.fieldSize) {
        await Promise.all([
          this.modelFit({ model: this.modelX, sign: 'X' }),
          this.modelFit({ model: this.modelO, sign: 'O' }),
        ]);

        this.step = 1;
      } else {
        this.step += 1;
      }
    },





    # Повышение интереса для хода к потенциально выигрышной ячейки противника.
    increasingInterest({ field, agent }) {
      const signNextTurn = agent.sign === 'X' ? 'O' : 'X';

      for (let i = 0; i < field.length; i += 1) {
        if (field[i].length === 0) {
          field.splice(i, 1, agent.sign);
          const isWinner = this.determineWinner({ field, sign: agent.sign });
          field.splice(i, 1, '');

          if (isWinner) {
            agent.rewards[i] = bestReward;
            break;
          }

          // ---

          field.splice(i, 1, signNextTurn);
          const isOtherWinner = this.determineWinner({ field, sign: signNextTurn });
          field.splice(i, 1, '');

          if (isOtherWinner) {
            agent.rewards[i] = interestReward;
            break;
          }
        }
      }
    },








    determineWinner({ field, sign }) {
      return hasVictory.horizontalGroup({ field, sign })
        || hasVictory.verticalGroup({ field, sign, start: 0, step: 2 })
        || hasVictory.obliquelyGroup({ field, sign });
    },

    saveTraining({ type, field, agent, stepInput }) {
      const { sign, rewards: label } = agent;
      const input = field.map((cell) => this.trafficLights({ type, sign, cell })).concat([stepInput]);

      this.training[sign].inputs.push(input);
      this.training[sign].labels.push(label);

      this.trainingCount[sign] += 1;
    },

    trafficLights({ type, sign, cell }) {
      let reward = basicReward;

      // Если ячейка свободна, то это нормально, но если занято другим знаком - это плохо.
      if (type === 'winner') {
        if (sign === cell) {
          reward = bestReward;
        } else if (cell.length === 0) {
          reward = basicReward;
        } else {
          reward = worstReward;
        }
      } else if (type === 'step') {
        if (sign === cell) {
          reward = stepReward;
        } else if (cell.length === 0) {
          reward = basicReward;
        } else {
          reward = worstReward;
        }
      } else if (type === 'loss') {
        if (sign === cell) {
          reward = lossReward;
        } else if (cell.length === 0) {
          reward = basicReward;
        } else {
          reward = worstReward;
        }
      }

      return reward;
    },

    async modelFit({ model, sign }) {
      if (this.trainingCount[sign] > 0) {
        // Где то данные не кладутся, но счётчик увеличивается.
        if (this.training[sign].inputs.length === 0 || this.training[sign].labels.length === 0) {
          return;
        }

        this.trainingCount[sign] = 0;
        this.victoriesStatus[sign] = false;

        await model.fit(
          tf.tensor2d(this.training[sign].inputs),
          tf.tensor2d(this.training[sign].labels),
        );

        this.trainingReset(sign);

        this.agentsSetting({ sign: 'X' });
        this.agentsSetting({ sign: 'O' });
      }
    },

    trainingReset(sign) {
      this.training[sign].inputs = [];
      this.training[sign].labels = [];
    },

    async setHumanSign(humanCellIndex) {
      if (!this.AIvsHuman.isDuel) {
        this.AIvsHuman.isDuel = true;

        this.trainingReset('X');
        this.trainingReset('O');
      }

      const { isPass } = await this.humanSignXO({ sign: 'X', cIndex: humanCellIndex });

      if (isPass) {
        await this.humanSignXO({ sign: 'O', cIndex: -1 });
      }
    },

    async humanSignXO({ sign, cIndex }) {
      if (this.AIvsHuman.step > this.fieldSize) {
        this.AIvsHumanReset();
        return { isPass: false };
      }

      this.AIvsHuman.step += 1;
      const stepInput = this.getStepInput(this.AIvsHuman.step);

      const { field } = this.AIvsHuman;
      let cellIndex = cIndex;

      if (sign === 'O') {
        this.increasingInterest({ field, agent: this.AIvsHuman });

        const predictions = await this.modelO.predict(tf.tensor2d([this.AIvsHuman.rewards.concat([stepInput])])).data();
        cellIndex = predictions.indexOf(Math.max(...predictions));
      }

      if (field[cellIndex].length === 0) {
        field.splice(cellIndex, 1, sign);

        this.AIvsHuman.rewards = this.recalculateRewards({ rewards: this.AIvsHuman.rewards, field });
        const isWinnerXO = this.determineWinner({ field, sign });

        if (isWinnerXO) {
          const agent = { sign, rewards: this.AIvsHuman.rewards };
          this.saveTraining({ type: 'winner', field, agent, stepInput });

          this.AIvsHuman.victories[sign] += 1;
          await this.AIvsHumanFit();

          return { isPass: false };
        }

        // Даст выход -> return { isPass: true };
      } else {
        this.AIvsHuman.rewards = this.recalculateRewards({ rewards: this.AIvsHuman.rewards, field });
        const agent = { sign, rewards: this.AIvsHuman.rewards };
        this.saveTraining({ type: 'loss', field, agent, stepInput });

        this.AIvsHuman.victories[sign] -= 1;
        await this.AIvsHumanFit();

        return { isPass: false };
      }

      return { isPass: true };
    },

    async AIvsHumanFit() {
      await Promise.all([
        this.modelFit({ model: this.modelX, sign: 'X' }),
        this.modelFit({ model: this.modelO, sign: 'O' }),
      ]);

      this.AIvsHumanReset();
    },

    AIvsHumanReset() {
      this.AIvsHuman = {
        ...this.AIvsHuman,
        isDuel: false,
        step: 1,
        rewards: [
          0.1, 0.1, 0.1,
          0.1, 0.1, 0.1,
          0.1, 0.1, 0.1,
        ],
        field: [
          '', '', '',
          '', '', '',
          '', '', '',
        ],
      };
    },

    async saveModelsOnPC() {
      try {
        await Promise.all([
          this.modelX.save('downloads://syntet_TicTacToe_model_X'),
          this.modelO.save('downloads://syntet_TicTacToe_model_O'),
        ]);
      } catch (err) {
        console.error('saveModels', err);
      }
    },

    localStorageClear() {
      localStorage.clear();
    },

    async restoreModelsFromGitHub() {
      const uriModelX = './models/syntet_TicTacToe_model_X.json';
      const uriModelO = './models/syntet_TicTacToe_model_O.json';

      const [modelX, modelO] = await Promise.all([
        tf.loadLayersModel(uriModelX),
        tf.loadLayersModel(uriModelO),
      ]);

      modelX.compile({
        optimizer: 'adam',
        loss: 'meanSquaredError',
      });

      modelO.compile({
        optimizer: 'adam',
        loss: 'meanSquaredError',
      });

      this.modelX = modelX;
      this.modelO = modelO;
    },
  },
};