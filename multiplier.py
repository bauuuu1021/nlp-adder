from keras.models import Sequential
from keras.layers import Dense
from keras import layers
import numpy as np
import os
import matplotlib.pyplot as plt
from six.moves import range

def mul(DIGITS, EPOCH):
    class colors:
        ok = '\033[92m'
        fail = '\033[91m'
        close = '\033[0m'

    TRAINING_SIZE = 80000
    REVERSE = False
    MAXLEN = DIGITS + 1 + DIGITS
    chars = '0123456789* '
    RNN = layers.LSTM
    HIDDEN_SIZE = 128
    BATCH_SIZE = 128
    LAYERS = 1

    class CharacterTable(object):
        def __init__(self, chars):
            self.chars = sorted(set(chars))
            self.char_indices = dict((c, i) for i, c in enumerate(self.chars))
            self.indices_char = dict((i, c) for i, c in enumerate(self.chars))
        
        def encode(self, C, num_rows):
            x = np.zeros((num_rows, len(self.chars)))
            for i, c in enumerate(C):
                x[i, self.char_indices[c]] = 1
            return x
        
        def decode(self, x, calc_argmax=True):
            if calc_argmax:
                x = x.argmax(axis=-1)
            return "".join(self.indices_char[i] for i in x)

    ctable = CharacterTable(chars)
    ctable.indices_char

    questions = []
    expected = []
    seen = set()
    print('Generating data...')
    while len(questions) < TRAINING_SIZE:
        f = lambda: int(''.join(np.random.choice(list('0123456789')) for i in range(np.random.randint(1, DIGITS + 1))))
        a, b = f(), f()
        key = tuple(sorted((a, b)))
        if key in seen:
            continue
        seen.add(key)
        q = '{}*{}'.format(a, b)
        query = q + ' ' * (MAXLEN - len(q))
        ans = str(a * b)
        ans += ' ' * (DIGITS + 1 - len(ans))
        if REVERSE:
            query = query[::-1]
        questions.append(query)
        expected.append(ans)
    print('Total addition questions:', len(questions))

    print(questions[:5], expected[:5])

    print('Vectorization...')
    x = np.zeros((len(questions), MAXLEN, len(chars)), dtype=np.bool)
    y = np.zeros((len(expected), DIGITS * 2, len(chars)), dtype=np.bool)
    for i, sentence in enumerate(questions):
        x[i] = ctable.encode(sentence, MAXLEN)
    for i, sentence in enumerate(expected):
        y[i] = ctable.encode(sentence, DIGITS * 2)

    indices = np.arange(len(y))
    np.random.shuffle(indices)
    x = x[indices]
    y = y[indices]

    # train_test_split
    train_x = x[:20000]
    train_y = y[:20000]
    test_x = x[20000:]
    test_y = y[20000:]

    split_at = len(train_x) - len(train_x) // 10
    (x_train, x_val) = train_x[:split_at], train_x[split_at:]
    (y_train, y_val) = train_y[:split_at], train_y[split_at:]

    print('Training Data:')
    print(x_train.shape)
    print(y_train.shape)

    print('Validation Data:')
    print(x_val.shape)
    print(y_val.shape)

    print('Testing Data:')
    print(test_x.shape)
    print(test_y.shape)

    print("input: ", x_train[:3], '\n\n', "label: ", y_train[:3])

    print('Build model...')

    model = Sequential()
    model.add(RNN(HIDDEN_SIZE, input_shape=(MAXLEN, len(chars))))   # shape (7,12)
    model.add(layers.RepeatVector(DIGITS * 2))
    model.add(RNN(HIDDEN_SIZE, return_sequences=True))
    model.add(layers.TimeDistributed(layers.Dense(len(chars), activation='softmax')))
    model.compile(loss='categorical_crossentropy',
                optimizer='adam',
                metrics=['accuracy'])

    model.summary()

    while (EPOCH != 0):
        if (EPOCH > 100):
            loop = 100
            EPOCH -= 100
        else:
            loop = EPOCH
            EPOCH = 0

        for iteration in range(loop):
            print()
            print('-' * 50)
            print('Iteration', iteration)
            model.fit(x_train, y_train,
                    batch_size=BATCH_SIZE,
                    epochs=1,
                    validation_data=(x_val, y_val))
            for i in range(10):
                ind = np.random.randint(0, len(x_val))
                rowx, rowy = x_val[np.array([ind])], y_val[np.array([ind])]
                preds = model.predict_classes(rowx, verbose=0)
                q = ctable.decode(rowx[0])
                correct = ctable.decode(rowy[0])
                guess = ctable.decode(preds[0], calc_argmax=False)
                print('Q', q[::-1] if REVERSE else q, end=' ')
                print('T', correct, end=' ')
                if correct == guess:
                    print(colors.ok + '☑' + colors.close, end=' ')
                else:
                    print(colors.fail + '☒' + colors.close, end=' ')
                print(guess)

        print("MSG : Prediction")

        test_size = 1000
        right = 0

        for _ in range (test_size):
            ind = np.random.randint(0, 60000)
            rowx, rowy = test_x[np.array([ind])], test_y[np.array([ind])]
            preds = model.predict_classes(rowx, verbose=0)
            q = ctable.decode(rowx[0])
            correct = ctable.decode(rowy[0])
            guess = ctable.decode(preds[0], calc_argmax=False)
            print('Q', q[::-1] if REVERSE else q, end=' ')
            print('T', correct, end=' ')
            if correct == guess:
                right += 1
                print(colors.ok + '☑' + colors.close, end=' ')
            else:
                print(colors.fail + '☒' + colors.close, end=' ')
            print(guess) 

        correctness = (right/test_size)*100
        print('Correctness: %f %%'%(correctness)) 
        
        fp = open("tmp.txt","a")
        fp.write("%f\n"%(correctness))
        fp.close()     

def origin_mul():
    digit = 3
    epoch = 100
    mul(digit, epoch)

def epoch_mul():
    digit = 3
    mul(digit, 300)
    
    # load correctness
    cor = np.zeros((3), dtype=float)
    fp = open("tmp.txt", "r")
    for i in range(3):
        cor[i] = float(fp.readline())
    fp.close()

    # plot
    label = ['100', '200', '300']
    pos = np.arange(len(label))
    plt.bar(pos, cor, label = 'correctness (%)', align = "center", width = 0.3)
    plt.xticks(pos, label)
    plt.legend(loc=4)    

    for i, v in enumerate(cor):
        plt.text(pos[i] - 0.08, v + 0.1, str(v))

    plt.savefig('img/digit_%d_multi.png'%(digit))
    plt.show()
    os.remove("tmp.txt")

if __name__ == "__main__":
    epoch_mul()