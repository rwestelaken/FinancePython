import numpy as np
import pandas as pd

import tensorflow as tf
from sklearn.utils import shuffle
from sklearn.preprocessing import MinMaxScaler

# Load Data
data = pd.read_csv('dj30_10y.csv', sep=',', engine='python')
assets = data.columns.values[1:].tolist()
data = data.iloc[:, 1:]

# Load index
index = pd.read_csv('dj30_index_10y.csv', sep=',', engine='python')
index = index.iloc[-data.values.shape[0]:, 1:]

# Normalize data
scaler = MinMaxScaler([0.1,0.9])
data_X = scaler.fit_transform(data)
scaler_index = MinMaxScaler([0.1,0.9])
index = scaler_index.fit_transform(index)

# Number of components
N_COMPONENTS = 3

## Autoencoder - TensorFlow
# Network hyperparameters
n_inputs = len(assets)
n_core = N_COMPONENTS
n_outputs = n_inputs

# Building the encoder
def encoder(x):
    return tf.nn.sigmoid(tf.add(tf.matmul(x, w1), b1))

# Building the decoder
def decoder(x):
    return tf.nn.sigmoid(tf.add(tf.matmul(x, w2), b2))

# TF Graph input and output
X = tf.placeholder("float", [None, n_inputs])
Y = tf.placeholder("float", [None, n_inputs])

# Construct model
encoder_op = encoder(X)
decoder_op = decoder(encoder_op)
# Prediction
y_pred = decoder_op

# Create weights and biases for each layer
initializer = tf.initializers.glorot_normal()
w1 = tf.Variable(initializer([n_inputs, n_core]))
w2 = tf.transpose(w1)
b1 = tf.Variable(tf.zeros([n_core]))
b2 = tf.Variable(tf.zeros([n_outputs]))

# Targets are the same as input data
y_true = X

# Define loss to minimize the squared error
mse = tf.losses.mean_squared_error(y_true, y_pred)
# Define optimizer
optimizer = tf.train.AdamOptimizer(lr).minimize(mse)

# Training parameters
lr = 0.01
epochs = 40
batch_size = 1

# Start Training
# Start a new TF session
with tf.Session() as sess:
    # Initialize the network
    sess.run(tf.global_variables_initializer())
    # Training
    for i in range(epochs):
        X_train1 = shuffle(X_train)
        for j in range(X_train.shape[0] // batch_size):
            batch_y = X_train1[j * batch_size:j * batch_size + batch_size,
            :]
            batch_x = X_train1[j * batch_size:j * batch_size + batch_size,
            :]
            _, loss_value = sess.run([optimizer, mse], feed_dict={X:
            batch_x, Y: batch_y})
        # Display loss
        print('Epoch: %i -> Loss: %f' % (i, loss_value))
    # Make predictions
    y_pred_AE_tf = sess.run(decoder_op, feed_dict={X: X_train, Y: X_train})
    print('Test Error: %f' % tf.losses.mean_squared_error(X_train,y_pred_AE_tf).eval())