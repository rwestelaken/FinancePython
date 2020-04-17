import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler
from keras.layers import Input, Dense
from keras.models import Model
import seaborn as sns
from tqdm import tqdm

# Load Data
folder = "/home/westy/Source/FinancePython/src/tf/"
data = pd.read_csv(folder + "dj30_10y.csv", sep=',')
assets = data.columns.values[1:].tolist()
data = data.iloc[:, 1:]

# Load index
index = pd.read_csv(folder + "dj30_index_10y.csv", sep=',')
index = index.iloc[-data.values.shape[0]:, 1:]

# Normalize data
scaler = MinMaxScaler([0.1,0.9])
data_X = scaler.fit_transform(data)
scaler_index = MinMaxScaler([0.1,0.9])
index = scaler_index.fit_transform(index)

# Number of components
N_COMPONENTS = 3
## Autoencoder - Keras
# Network hyperparameters
n_inputs = len(assets)
n_core = N_COMPONENTS
n_outputs = n_inputs

# Create model
input = Input(shape=(n_inputs,))
# Encoder
encoded = Dense(n_core, activation='sigmoid')(input)
# Decoder
decoded = Dense(n_outputs, activation='sigmoid')(encoded)

# define model
autoencoder = Model(input, decoded)
autoencoder.compile(optimizer='adam', loss='mse')

# Testing in-sample
X_train = data_X
X_test = data_X

# Training parameters
epochs = 20
# Fit the model
history = autoencoder.fit( \
    X_train,\
    X_train,\
    epochs=epochs,\
    batch_size=1,\
    shuffle=True,\
    verbose=1)

# Make AE predictions
y_pred_AE_keras = autoencoder.predict(X_test)
print('test loss: '+str(autoencoder.evaluate(y_pred_AE_keras, X_test)))

## PCA
pca = PCA()
pca.fit(X_train)
print(pca.explained_variance_ratio_)
cum_exp_var = np.cumsum(pca.explained_variance_ratio_)
plt.plot(np.arange(1, 31), cum_exp_var)
plt.xlabel('Principal components')
plt.ylabel('Cumulative explained variance')
plt.show()

pca = PCA(n_components=N_COMPONENTS)
pca.fit(X_train)
y_latent_PCA = pca.transform(X_train)
y_pred_PCA = pca.inverse_transform(y_latent_PCA)

# Average
ma = np.mean(data_X, axis=1)

# Plot series
count = 30

for stk in tqdm(range(count), desc='Series', leave=True):
    fig=plt.figure()
    plt.plot(X_train[: ,stk], label='X')
    plt.plot(y_pred_PCA[: ,stk], label='PCA reconstruction')
    plt.plot(y_pred_AE_keras[: ,stk], label='AE reconstruction')
    plt.plot(ma, label='MA')
    plt.plot(index, label='DJIA')
    plt.title(assets[stk])
    plt.legend()
    plt.savefig(folder+"series/"+assets[stk]+'.png', bbox_inches='tight')
    plt.close(fig)

## Correlations

def corr(x, y, **kwargs):
    # Calculate the value
    coef = np.corrcoef(x, y)[0][1]
    # Make the label
    label = str(round(coef, 2))
    ax = plt.gca()
    # Add the label to the plot
    font_size = abs(coef) * 40 + 5
    ax.annotate(label, [.5, .5,], xycoords=ax.transAxes,
    ha='center', va='center', fontsize=font_size)

for stk in tqdm(range(29), desc='Correlations', leave=True):
    df = pd.DataFrame({'0-Asset': data_X[:, stk], \
        '2-PCA': y_pred_PCA[:, stk], \
        '1-AE': y_pred_AE_keras[:, stk], \
        '3-Average': ma, \
        '4-DJI index': index.flatten()})
    sns.set(style='white', font_scale=1.6)
    g = sns.PairGrid(df, aspect=1.4, diag_sharey=False)
    g.map_lower(sns.regplot, lowess=True, ci=False, line_kws={'color':'black'})
    g.map_diag(sns.distplot, kde_kws={'color': 'black'})
    g.map_upper(corr)# dot(g.data, kde_kws={'color': 'black'})
    plt.savefig(folder+"correlation/" + assets[stk] + '.png', bbox_inches='tight')
    plt.close("all")