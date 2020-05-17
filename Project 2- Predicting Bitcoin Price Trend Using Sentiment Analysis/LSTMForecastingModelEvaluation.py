#https://machinelearningmastery.com/multivariate-time-series-forecasting-lstms-keras/

#Importing Libraries
from pandas import DataFrame
from pandas import concat
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers import LSTM
import pandas as pd
from matplotlib import pyplot as plt
from numpy import concatenate
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from math import sqrt

# convert series to supervised learning
def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
	n_vars = 1 if type(data) is list else data.shape[1]
	df = DataFrame(data)
	cols, names = list(), list()
    
	# input sequence (t-n, ... t-1)
	for i in range(n_in, 0, -1):
		cols.append(df.shift(i))
		names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
        
	# forecast sequence (t, t+1, ... t+n)
	for i in range(0, n_out):
		cols.append(df.shift(-i))
		if i == 0:
			names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
		else:
			names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
            
	# put it all together
	agg = concat(cols, axis=1)
	agg.columns = names
    
	# drop rows with NaN values
	if dropnan:
		agg.dropna(inplace=True)
	return agg

dataset = pd.read_excel('FINALLSTMDatasetBitcoin.xlsx', nrows = 305) #FINALLSTMDatasetBitcoin.xlsx

values = dataset.iloc[:,4].values #Getting vwap scores [2:5]
values = values.astype('float32')
#values = values.tolist()
#Feature Scaling- converts vwap scores into values ranging from 0 to 1 (normalizing data)
values = values.reshape(-1,1) #Only do this if you have 1 input variable
scaler = MinMaxScaler(feature_range = (0,1)) 
scaled = scaler.fit_transform(values)

#Retrieve data from previous timestep (Supervised Learning)
reframed = series_to_supervised(scaled, 1, 1)

#Drop columns we don't want to predict
#reframed.drop(reframed.columns[[4,5,6]], axis = 1, inplace = True) 
print(reframed.head())

#Splitting data into train and test sets
reframedValues = reframed.values
n_train_days = 265 * 1 #90% data is train, 10% test
train = reframedValues[:n_train_days, :]
test = reframedValues[n_train_days+1:296, :]

#Assigning inputs and output datasets
train_X, train_y = train[:, :-1], train[:, -1]
test_X, test_y = test[:, :-1], test[:, -1]
#Reshaping input to be 3 dimensions (samples, timesteps, features)
train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))
print(train_X.shape, train_y.shape, test_X.shape, test_y.shape)

#Building LSTM Neural Network model
model = Sequential()
model.add(LSTM(50, input_shape=(train_X.shape[1], train_X.shape[2]))) #Recurrent Layer
model.add(Dropout(0.4)) #Dropout Layer
model.add(Dense(15, activation = 'tanh')) #Fully Connected Layer
model.add(Dense(1, activation = 'sigmoid')) #Output Layer
model.compile(loss='mae', optimizer= 'adam', metrics=['acc']) #Compiling the model

#Fitting model
history = model.fit(train_X, train_y, epochs = 200, batch_size=25, validation_data=(test_X, test_y), verbose=2, shuffle=False) #Best so far: 100 neurons, epochs = 400, batch_size = 53

#Plotting training loss vs validation loss
plt.plot(history.history['loss'], label='train')
plt.plot(history.history['val_loss'], label='validation')
plt.legend()
plt.show()

 
#Model making a prediction
yhat = model.predict(test_X)
test_X = test_X.reshape((test_X.shape[0], test_X.shape[2]))

#Inverting data back from feature scaling
inv_yhat = concatenate((test_X[:, :-1], yhat), axis=1)
inv_yhat = scaler.inverse_transform(inv_yhat)
inv_yhat = inv_yhat[:,0] #2

test_y = test_y.reshape((len(test_y), 1))
inv_y = concatenate((test_X[:, :-1], test_y), axis=1)
inv_y = scaler.inverse_transform(inv_y)
inv_y = inv_y[:,0] #2

#Calculating RMSE and MAE
rmse = sqrt(mean_squared_error(inv_y, inv_yhat))
mae = mean_absolute_error(inv_y, inv_yhat)
print('Test MAE: %.3f' % mae)
print('Test RMSE: %.3f' % rmse)


#Visualising Results (Actual vs Predicted)
plt.plot(inv_y, color = 'red', label = 'Actual Bitcoin VWAP')
plt.plot(inv_yhat, color = 'blue', label = 'Predicted Bitcoin VWAP') #[1:38]
plt.title('Bitcoin VWAP Prediction')
plt.xlabel('Time Interval (1 interval = 3.5 hours)')
plt.ylabel('VWAP')
plt.legend()
plt.show()




