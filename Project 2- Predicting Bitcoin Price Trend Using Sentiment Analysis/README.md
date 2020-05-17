### Honors Thesis- Predicting Bitcoin Price Trend Using Sentiment Analysis

This project was my honors thesis project at Arizona State. The project was to create the most accurate jodel possible that could predict the price trend of Bitcoin. The solution was not only to use a LSTM neural network to analyze price data but to analyze Bitcoin Twitter data using sentiment analysis as well. I was able to achieve a moddel that predicted 75% of the price trends accurately. Sentiment analysis improved model performance by 22%!

FILES:

- CollectingVWAPBitcoinData.py- This is how I collected the Bitcoin price data. I used Chainrider Finance's API to accomplish this.

- FINALLSTMDatasetBitcoin.xlsx- This is the dataset I fed into my LSTM Neural Network. It includes data on Volume-Average Weighted Price and sentiment analysis data on headlines and user reactions.

- Honors Thesis Presentation- Sam Steinberg.pdf- This is my powerpoint presentation I displayed during my thesis defense. I recommend viewing it to understand the project better.

- LSTMForecastingModelEvaluation.py- This is my final model. This file displays how I loaded in and preprocessed my dataset, building the LSTM Neural Network, and evaluating model performance. 




