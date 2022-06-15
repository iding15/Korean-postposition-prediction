from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

import pandas as pd
import numpy as np

from config import TEST_DATA_SIZE, RANDOM_STATE

## ex_iris
# iris = load_iris()
# iris_data = iris.data
# print(iris_data.shape)
# iris_label = iris.target
# print(iris_label.shape)
# print(type(iris_label))
# print(len(noundata))


def predict_with_decision_tree(noun_data_set: np.array, josa_data_set: np.array) -> pd.DataFrame:
    """
    Decision Tree 알고리즘을 적용한 조사 예측 함수
    """
    X_train, X_test, y_train, y_test = train_test_split(noun_data_set, josa_data_set, test_size=TEST_DATA_SIZE, random_state=RANDOM_STATE)
    dt_clf = DecisionTreeClassifier(random_state=RANDOM_STATE)
    dt_clf.fit(X_train, y_train)

    pred = dt_clf.predict(X_test)

    print(accuracy_score(y_test, pred))  # 정확도 score
    xt = pd.DataFrame(X_test, columns=['X_test'])
    yt = pd.DataFrame(y_test, columns=['y_test'])
    pr = pd.DataFrame(pred, columns=['predict'])

    c = 0
    l=[]
    while c<len(X_test):
        if y_test[c] != pred[c]:
            l.append(c)
        c=c+1
    print(l)  # 예측하는데 사용한 데이터 셋
    return pd.concat([xt,yt,pr],axis=1)
