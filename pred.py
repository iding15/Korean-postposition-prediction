from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

import pandas as pd
import numpy as np

from cfJosa import decide
from sepChunk import chunk_to_num

from typing import List
## ex_iris
# iris = load_iris()
# iris_data = iris.data
# print(iris_data.shape)
# iris_label = iris.target
# print(iris_label.shape)
# print(type(iris_label))
# print(len(noundata))



# make data
def mkdata(raw_data: List[str]) -> np.array:
    """
    예측하기 전 명사 raw 데이터를 array형으로 변환하는 과정
    """
    float_data = chunk_to_num(raw_data)
    return np.array(float_data).reshape(len(float_data), 1)


def make_target(raw_data: List[str], josa_type: str) -> np.array:
    """
    raw 데이터로 부터 정답 1, 오답 0인 target data를 추출하는 과정
    """
    try:
        target_list = list(map(lambda noun: decide(noun, josa_type), raw_data))
        return np.array(target_list).reshape(len(target_list), )
    except ValueError as e:
        raise e


def predjo(noun, josa):
    X_train, X_test, y_train, y_test = train_test_split(noun, josa, test_size=0.2, random_state=11)
    dt_clf = DecisionTreeClassifier(random_state=11)
    dt_clf.fit(X_train, y_train)

    pred = dt_clf.predict(X_test)

    print(accuracy_score(y_test, pred))
    xt = pd.DataFrame(X_test, columns=['X_test'])
    yt = pd.DataFrame(y_test, columns=['y_test'])
    pr = pd.DataFrame(pred, columns=['predict'])

    c = 0
    l=[]
    while c<len(X_test):
        if y_test[c] != pred[c]:
            l.append(c)
        c=c+1
    print(l)
    return pd.concat([xt,yt,pr],axis=1)
