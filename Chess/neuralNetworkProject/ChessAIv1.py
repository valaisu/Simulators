import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from numpy import loadtxt
import math
import matplotlib.pyplot as plt


#ChessData.csv caontains data in a list format, where each element
#discribes a square on a chess board (and the possible piece on that
#square). The last element is an exception, it describes the end result
#of the game.

#This neural network does compile and so on, but after analyzing the
#results, turns out it learns jack shit. This might be, because in high
#level games (out of which the dataset was made) the material tends to be
#equal, even though the evaluation is maybe not. Once the material balance
#is about to tip, the losing side usually resigns. The data was in a format,
#that highlights the material.  

dataset = loadtxt('ChessData.csv', delimiter=',')
features = dataset[:,0:65] #other data
labels = dataset[:,65] #labels
print(features[0])
print(labels[0])
tot = 0
for i in range(len(labels)):
    tot += abs(labels[i])
print(tot/len(labels))


model = Sequential([
  layers.Conv2D(16, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Conv2D(32, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Conv2D(64, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Flatten(),
  layers.Dense(128, activation='relu'),
  layers.Dense(3)
])


model.compile(loss = tf.losses.MeanAbsoluteError(),#???
                    optimizer = tf.optimizers.Adam(),
                    metrics=['accuracy'])

history = model.fit(features, labels, epochs=100, validation_split=0.2)#20% of data goes to validation


#Results vizualization
r = range(100)

loss = history.history['loss']
val_loss = history.history['val_loss']
for i in range(len(loss)):
    loss[i] = math.sqrt(loss[i])
    val_loss[i] = math.sqrt(val_loss[i])

axes = plt.gca()
axes.set_ylim([0, 2])
plt.plot(r, loss, label='Training Loss')
plt.plot(r, val_loss, label='Validation Loss')
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.title("")
plt.legend()
plt.show()
