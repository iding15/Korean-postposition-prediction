from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from cfJosa import decideJosa
from sklearn.metrics import accuracy_score
from sepChunk import md

## ex_iris
# iris = load_iris()
# iris_data = iris.data
# print(iris_data.shape)
# iris_label = iris.target
# print(iris_label.shape)
# print(type(iris_label))
# print(len(noundata))

# make data
def mkdata(lnoun):
    # noun = decideJosa.noundata
    n_n = md(lnoun)
    numnoun = []
    for n in n_n:
        numnoun.append([n])
    # print(numnoun)
    n_numN = np.array(numnoun).reshape(len(n_n),1)
    # print(n_numN)
    return n_numN
class mktarget:
    def __init__(self,noun = decideJosa.noundata):
        self.li = []
        self.noun = noun
        self.lenn = len(self.noun)
    def t_en(self):
        en = decideJosa(self.noun).EunNeun()
        for i in en:
            if i=='은':
                self.li.append(0)
            else:
                self.li.append(1)
        n_eunneun = np.array(self.li).reshape(self.lenn,)
        return n_eunneun
    def t_ig(self):
        ig = decideJosa(self.noun).IGa()
        for i in ig:
            if i=='이':
                self.li.append(0)
            else:
                self.li.append(1)
        n_iga = np.array(self.li).reshape(self.lenn,)
        return n_iga
    def t_er(self):
        er = decideJosa(self.noun).EulRul()
        for i in er:
            if i=='을':
                self.li.append(0)
            else:
                self.li.append(1)
        n_iga = np.array(self.li).reshape(self.lenn,)
        return n_iga

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
