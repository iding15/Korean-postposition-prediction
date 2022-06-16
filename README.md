# Korean postposition prediction

명사 뒤에 올 조사 예측 프로그램

해당 프로젝트는 "파이썬 머신러닝 완벽 가이드" 88p~146p를 참조하여 진행하였습니다.

# 개요

국어 문법에는 규칙이 있다. 그리고 아주 많다. 외국인들도 한국 문법이 어렵다고들 한다. 컴퓨터는 어떨까? 문법에는 규칙이 존재한다. 이러한 규칙을 직접 알고리즘을 짜두면 문법을 판별하는데에 큰 지장은 없을 것이다. 하지만 여기서 아주 작은 의문이 생겼다. 과연 컴퓨터가 문법을 사람이 짜둔 알고리즘 없이 학습할 수 있을까?
  
아주 간단한 실습 예제를 통해서 이를 검증해보고 싶었다.

## 명사와 조사

우리는 아주 당연하게도 명사뒤에 올 조사를 구분할 수 있다.
'다람쥐'은/**는**, 이/**가**, 을/**를**
'정육점'**은**/는, **이**/가, **을**/를
와 같이 명사 뒤에 끝 음절이 모음이냐 자음이냐에 따라서 조사를 결정할 수 있다.

컴퓨터도 조사를 결정할 수 있다. 아주 간단한 코드 작업을 통해서 명확하게 구분할 수 있다. 하지만 가설을 검증할만한 변수만 알고있다고 가정하고 컴퓨터에 지도학습을 통해 학습을 시키기로 하였다. 때문에, 명사의 끝 음절에 올 음운이 자음이냐 모음이냐에 따라서 구분되도록 하는 것이 아닌, 우리의 **목표**는 한글의 자음과 모음, 그리고 받침에 대해 각각 부여된 weight를 조절하였을 때, 어느 위치에서 최적화가 될지를 확인해보는 것으로 잡았다.

# 데이터 수집

데이터 수집의 대상은 모든 한국어로 된 명사이다. 명사로 된 데이터를 모두 수집하기 위해서 국립국어원의 API를 활용했다.

API는 key만 발급받으면 어렵지 않게 사용 가능하다.

![](https://velog.velcdn.com/images/mivv/post/5b787d74-ddac-4529-84c1-895767fe209a/image.png)

API를 활용해서 700개의 데이터를 수집하여 data.json 파일로 저장했다.

## 1. Code

```python
import re
from typing import List

def _set_noun_data(eumjul: List[str], start: int, step: int, num=100, max_=2000) -> None:
    """
    start: 시작 페이지
    step: 다음 페이지로 넘어가는 간격
    num: 최대 조회 데이터 수 (1~100)
    max_: 마지막 조회 데이터 번호
    """
    data = []
    for q in eumjul:
        print('listen start from '+q+'...')
        cnt = start
        while cnt*num<=max_:
            r = requests.get(API_URL, params=_get_params(
                q, cnt, num
            ))
            if r.status_code==200:
                response = r.json()
                try:
                    form = response['channel']
                    total = form['total']
                    item_data = form['item']
                    
                    for item in item_data:
                        word = item['word']
                        word = re.sub('[ㄱ-ㅎ\-]', '', word)
                        print(word)
                        data.append(word)
                    if total < cnt*num:
                        break
                except:
                    pass
                cnt += step
            else:
                raise Exception('api 요청 실패')
    
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump({
            'start': start,
            'step': step,
            'num': num,
            'max': max_,
            'eumjul': eumjul,
            'data': data
        }, f, ensure_ascii=False, indent=4)
```

## 2. Json data

```shell
vim data.json
```
![](https://velog.velcdn.com/images/mivv/post/ef4928d2-9ee5-4a85-a454-9aa673604ce1/image.png)

# 데이터 전처리

## 1. 동음이의어 제거하기

위의 json data에서 보다시피 중복되는 명사 데이터가 발견된다. 중복되는 명사를 제거한다.

** 동음이의어 제거해서 데이터 가져오기
```python
def get_noun_data():
    try:
        with open('data.json', 'r') as f:
            json_data = json.load(f)
            # remove duplicated data
            data: list = json_data['data']
            json_data['data'] = list(set(data))
            return json_data
    except FileNotFoundError:
        raise FileNotFoundError('data.json파일이 없습니다. noun_data.py 파일을 실행시켜주세요')
```

## 2. 데이터 수치화하기

데이터를 어떻게 수치화 할것이냐에 따라 모델의 정확도가 달라진다.
모델의 정확도를 결정할 독립변수를 자음, 모음, 받침으로 정했다.

명사의 각 음절마다 자음과 모음 및 받침을 추출하여, 자음 w1, 모음 w2, 받침 w3로 가중치를 두고, 모든 값을 더하고 명사의 길이를 나눈 값을 수치화된 데이터로 정했다.

예를 들어, w1, w2, w3 = 1, 0, 10으로 둔다면, '강아지'의 경우
ㄱ+ㅏ+ㅇ+ㅇ+ㅏ+ㅈ+ㅣ=
(1+0+10+1+0+1+0)/3 = 4.333가 된다.

[>> code 보기](https://github.com/iding15/Korean-postposition-prediction/blob/master/preprocessing.py)

# Decision Tree 알고리즘 적용하기

## Decision Tree란?
결정 트리(Decision Tree)는 ML 알고리즘으로, 데이터에 있는 규칙을 학습을 통해 자동으로 찾아내 트리(Tree) 기반의 분류 규칙을 만드는 것이다. if/else 기반으로 룰 기반의 프로그램에 적용되는 if/else를 자동으로 찾아내 예측을 위한 규칙을 만드는 알고리즘이다. 따라서 데이터의 어떤 기준을 바탕으로 규칙을 만들어야 가장 효율적인 분류가 될 것인가가 알고리즘의 성능을 크게 좌우한다.

Decision Tree를 활용하여 예측을 하기 위해 sklearn 라이브러리를 활용하였다.

다음을 import 한다.
```python
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

import pandas as pd
import numpy as np
```

## 1. DecisionTreeClassifier

결정 트리 알고리즘을 사이킷런에서 구현한 DecisionTreeClassifier는 기본으로 지니 계수를 이용해 데이터 세트를 분할한다. 결정트리의 일반적인 알고리즘은 데이터 세트를 분할하는 데 가장 좋은 조건, 즉 정보 이득이 높거나 지니 계수가 낮은 조건을 찾아서 자식 트리 노드에 걸쳐 반복적으로 분할한 뒤, 데이터가 모두 특정 분류에 속하게 되면 분할을 맘추고 분류를 결정한다.

** 지니계수: 경제학에서 불평등 지수를 나타낼 때 사용하는 계수. 0이 가장 평등하고, 1로 갈수록 불평등하다. 머신러닝에 적용될 때는 지니 계수가 낮을수록 데이터 균일도가 높은 것으로 해석해 지니 계수가 낮은 속성을 기준으로 분할한다.

## 2. train_test_split

데이터 세트를 학습용과 테스트용으로 분리하는데 사용하는 함수이다. 만일 테스트 데이터 세트를 이용하지 않고 학습 데이터 세트로만 학습하고 예측하면, 이미 학습한 학습 데이터 세트를 기반으로 예측하기 때문에, 정확도가 100%로 나온다. 따라서 예측을 수행하는 데이터 세트는 학습을 수행한 학습용 데이터 세트가 아닌 전용의 테스트 데이터 세트여야 한다.

## 3. accuracy_score

정확도는 실제 데이터에서 예측 데이터가 얼마나 같은지를 판단하는 지표이디.

# 예측하기

``` python
# pred.py

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

import pandas as pd
import numpy as np

from config import TEST_DATA_SIZE, RANDOM_STATE


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

```

pred.py 파일에 위의 코드를 작성하고 main.py 에서 호출하였다.

``` python
# main.py

from pred import predict_with_decision_tree
from preprocessing import Target, NounData
from noun_data import get_noun_data

noun_data = get_noun_data()['data']

noun = NounData(noun_data).parse()

en = Target(noun_data, 'en').parse()
ig = Target(noun_data, 'ig').parse()
er = Target(noun_data, 'er').parse()

# print(en)
# print(ig)
# print(er)

print(predict_with_decision_tree(noun, en))
```

# 결과

자음, 모음, 받침에 대한 weight을 각각 [0, 1, 10]으로 잡고 예측 모델을 학습시켰을 때,
![](https://velog.velcdn.com/images/mivv/post/622e6afa-523d-47e4-8a4e-4240df84e7df/image.png)
다음과 같은 결과를 얻었다. 76.5%의 정확도로 예측한 겻을 확인할 수 있었다.

이번에는 자음, 모음, 받침에 대한 weight을 다르게 주고 각각의 상황에서 예측을 accuracy_score 대신 average_precision_score를 활용하여 정확도의 **평균**을 산출해보았다.

![](https://velog.velcdn.com/images/mivv/post/bfc6d4f7-d01d-48f0-9955-cb37edd87539/image.png)

처음에는 weight을 다르게 주고 예측을 해보면 결과가 유의미하게 다르게 나타날 것이라 예상했지만, 예상과는 다르게, weight의 변화에 따른 예측 정확도는 큰 차이를 나타내지 못했다.

그렇다면 모든 명사의 음절에서 가중치를 더한 전처리 모델 대신, 명사의 끝 음절에 따라 결정하도록 전처리를 하면 어떤 결과가 나올까?

![](https://velog.velcdn.com/images/mivv/post/61f95f47-c562-4d9d-b6e6-273ad2a6563e/image.png)

위와 같이 받침에 가중치가 충분히 높다면 정확도가 100%까지 나오는 것을 확인할 수 있었다.

가장 가중치가 높은 경우의 weight도 역시 측정해 보았다. weight의 범위를 0~10으로 잡고, 모든 경우의 수 중 가장 weight이 높은 경우를 확인해 보았다.

```shell

get accuracy scores now ...
10.015980958938599s: 371th prediction is processed.
20.037614822387695s: 743th prediction is processed.
30.044543981552124s: 1108th prediction is processed.
get optimized score info success!!
('[3, 2, 2]', 0.7654999338400363)

get accuracy scores now ...
10.000808238983154s: 367th prediction is processed.
20.018985986709595s: 738th prediction is processed.
30.039680004119873s: 1115th prediction is processed.
get optimized score info success!!
('[6, 5, 3]', 0.782057100866671)

get accuracy scores now ...
10.017060041427612s: 377th prediction is processed.
20.028151035308838s: 754th prediction is processed.
30.035942792892456s: 1131th prediction is processed.
get optimized score info success!!
('[2, 10, 2]', 0.7577900788062858)
```

받침에 많은 weight을 주는 경우보다 오히려 자음에 높은 비중을 가져간 경우나 모음에 높은 비중을 주었을 때, 예측점수가 더 높은 것으로 확인되었다.

# 결론

지금까지 분류 알고리즘 중 가장 기초적인 결정 트리를 통해 명사 뒤에 올 조사를 예측하는 간단한 예시를 바탕으로 결과까지 도출해보았다.

결정 트리는 데이터의 스케일링이나 정규화 등의 사전 가공의 영향이 매우 적고, 쉽고 유연하게 적용될 수 있는 알고리즘이다. 하지만 예측 성능을 향상시키기 위해 복잡한 규칙 구조를 가져야 하며, 이로 인한 과적합(overfitting)이 발생해 반대로 예측 성능이 저하될 수도 있다.

때문에, 분류 알고리즘 중에서는 앙상블 기법을 자주 사용하는 편이다. 앙상블 기법은 서로 다른(또는 같은) 머신러닝 알고리즘을 결합한 기법이다. 위에서 언급한 결정 트리의 예측 성능 저하 문제가 앙상블 기법에서는 오히려 장점으로 작용한다. 앙상블은 매우 많은 여러개의 약한 학습기(즉, 예측 성능이 상대적으로 떨어지는 학습 알고리즘)을 결합히 확률적 보완과 오류가 발생한 부분에 대한 가중치를 계속 업데이트하면서 예측 성능을 향상시키는데, 결정 트리가 좋은 약한 학습기가 되기 때문이다.

이미지, 영상, 음성 NLP 영역에서 신경망에 기반한 딥러닝이 머신러닝계를 선도하고 있지만, 이를 제외한 정형 데이터의 예측 분석 영역에서는 앙상블의 예측 성능이 매우 높게 나타난다고 한다.

다음에는 결정 트리모델 이외의 다른 분류 알고리즘을 적용하여 각각의 정확도를 비교해가면서 최종적으로 앙상블 기법을 적용해보도록 해야겠다.
