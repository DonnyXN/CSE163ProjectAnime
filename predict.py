import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


def get_test_data(df):
    df = df[['type', 'source', 'producers', 'rating',
             'score', 'studio', 'genre', 'popularity', 'episodes']]
    df = df.dropna()
    features = df.loc[:, df.columns != 'score']
    features = pd.get_dummies(features)
    labels = df['score']
    features_train, features_test, labels_train, labels_test = \
        train_test_split(features, labels, test_size=0.2)
    return features_train, features_test, labels_train, labels_test


def predict_rating(features_train, features_test, labels_train, labels_test):
    model = DecisionTreeRegressor()
    model.fit(features_train, labels_train)
    # labels_train_pred = model.predict(features_train)
    labels_test_pred = model.predict(features_test)

    # print(mean_squared_error(labels_train, labels_train_pred))
    print(mean_squared_error(labels_test, labels_test_pred))


def actual_vs_prediction(features_train, features_test, labels_train,
                         labels_test):
    model = DecisionTreeRegressor()
    model.fit(features_train, labels_train)
    # labels_train_pred = model.predict(features_train)
    labels_test_pred = model.predict(features_test)
    features_test = np.arange(0, len(features_test), 1)
    plt.plot(features_test, labels_test, color='red', label='actual')
    plt.scatter(features_test, labels_test_pred, color='green',
                label='predicted')
    plt.title('Actual vs Predicted')
    plt.xlabel('Animes')
    plt.ylabel('Rating')
    plt.legend()
    plt.savefig('/home/PredictedvsActual.png', bbox_inches='tight')


def main():
    anime1 = pd.read_csv('/home/anime1_sample.csv')
    anime1.columns = anime1.columns.str.replace(' ', '')
    features_train, features_test, labels_train, \
        labels_test = get_test_data(anime1)

    predict_rating(features_train, features_test, labels_train, labels_test)
    actual_vs_prediction(features_train, features_test,
                         labels_train, labels_test)


if __name__ == "__main__":
    main()
