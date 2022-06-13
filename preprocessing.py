from noun_data import ja, mo, bat, bneum
from config import DEFAULT_ESTIMATOR

import re
from typing import List


def to_float(buneum_list: List[str], type_: str, estimator: List[float]) -> dict:
    """
    to_float 함수는 모음 리스트를 받아서 각 모음에 해당하는 float 값을 dictionary에 담아서 전달하는 함수이다.
    """
    data = {}
    types = ['ja', 'mo', 'bat']

    if type_ not in types:
        raise ValueError("올바르지 않은 타입 값입니다: types = ['ja', 'mo', 'bat']")
    div_value: float
    if type_ == 'ja': div_value = estimator[0]
    elif type_ == 'mo': div_value = estimator[1]
    else: div_value = estimator[2]

    count = 1
    for bm in buneum_list:
        num = div_value+float(count/100)
        data[bm] = num
        count += 1
    return data


def divnoun(noun: str) -> str:
    """
    명사를 전달 받으면 명사의 각 음절을 음운 list로 나누어 return한다
    """
    try:
        noun = re.sub('\s+','',noun)  # 공백 제거
        splited = re.sub('',',',noun).split(',')
        s = ''
        for eum in splited:
            if eum !='':
                s = s + bneum(eum)
        return s
    except KeyError as e:
        raise KeyError("특수문자나 숫자, '.'을 제거해주세요. 오류: {}".format(e))
    except TypeError as e:
        raise TypeError('문자열로 입력해주세요. 오류: {}'.format(e))


def noun_to_num(noun: str, estimator: List[float]) -> float:
    """
    명사가 주어지면 자음, 모음, 받침에 적당한 weight을 주어 수치화한다.
    """
    mo_val = to_float(mo, 'mo', estimator=estimator)
    ja_val = to_float(ja, 'ja', estimator=estimator)
    bat_val = to_float(bat, 'bat', estimator=estimator)

    try:
        noun = re.sub('\s+','',noun)
        num = 0
        for eum in list(noun):
            bun_eum: str = bneum(eum)
            # splited_buneum = re.sub('', ',', bun_eum).split(',')
            if len(bun_eum) == 3:
                num += (
                    mo_val[bun_eum[0]] +
                    ja_val[bun_eum[1]] +
                    bat_val[bun_eum[2]]
                )
            elif len(bun_eum)==2:
                num += (
                    mo_val[bun_eum[0]] +
                    ja_val[bun_eum[1]]
                )
            else:
                raise Exception('한글이 아닌 문자열이 포함되었습니다.')
        return num
    except KeyError as k:
        raise KeyError("특수문자나 숫자, '.'을 제거해주세요. 오류: {}".format(k))
    except TypeError as t:
        raise TypeError('문자열로 입력해주세요. 오류: {}'.format(t))


import numpy as np  # np.array type으로 변환해야 sklearn 활용 가능


def make_data(raw_data: List[str], estimator: List[float]=DEFAULT_ESTIMATOR) -> np.array:
    """
    예측하기 전 명사 raw 데이터를 array형으로 변환하는 과정
    estimator에서는 ja, mo, bat 순서로 각각의 계수(weight)를 리스트로 담는다
    """
    float_data = []
    for noun in raw_data:
        float_data.append(noun_to_num(noun, estimator=estimator))
    return np.array(float_data).reshape(len(float_data), 1)


def decide_josa(noun: str, josa_type: str):
    types = ['en', 'ig', 'er']
    if josa_type not in types:
        raise ValueError("올바르지 않은 조사 유형입니다. -> 기대 인자값: en, ig, er")
    has_bat = False if list(divnoun(noun))[-1] in mo else True

    return 0 if has_bat else 1


def make_target(raw_data: List[str], josa_type: str) -> np.array:
    """
    raw 데이터로 부터 정답 1, 오답 0인 target data를 추출하는 과정
    """
    try:
        target_list = list(map(lambda noun: decide_josa(noun, josa_type), raw_data))
        return np.array(target_list).reshape(len(target_list), )
    except ValueError as e:
        raise e
