from mkEumjul import ja, mo, bat, bneum
import re
from typing import List


def to_float(buneum_list: List[str], type_: str) -> dict:
    """
    to_float 함수는 모음 리스트를 받아서 각 모음에 해당하는 float 값을 dictionary에 담아서 전달하는 함수이다.
    """
    data = {}
    types = ['ja', 'mo', 'bat']

    if type_ not in types:
        raise ValueError("올바르지 않은 타입 값입니다: types = ['ja', 'mo', 'bat']")
    div_value: float
    if type_ == 'ja': div_value = 1.00
    elif type_ == 'mo': div_value = 0.00
    else: div_value = 10.00

    count = 1
    for bm in buneum_list:
        num = div_value+float(count/100)
        data[bm] = num
        count += 1
    return data


mo_val = to_float(mo, 'mo')
ja_val = to_float(ja, 'ja')
bat_val = to_float(bat, 'bat')


# mkfloatdata
class mkFloat:
    """
    float_mo 메소드는 모음 리스트를 받아서 각 모음에 해당하는 
    """
    def __init__(self):
        self.count = 1.0
        self.dm = {}
    def float_mo(self):
        dm = {}
        for m in mo:
            num = 0.00+self.count/100
            dm[m] = float(num)
            self.count+=1
        return dm
    def float_ja(self):
        dm = {}
        for j in ja:
            num = 1.00+self.count/100
            dm[j] = float(num)
            self.count+=1
        return dm
    def float_bat(self):
        dm = {}
        for b in bat:
            num = 10.00+self.count/100
            dm[b] = float(num)
            self.count+=1
        return dm


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
        print("특수문자나 숫자, '.'을 제거해주세요. 오류: {}".format(e))
    except TypeError as e:
        print('문자열로 입력해주세요. 오류: {}'.format(e))


def noun_to_num(noun):
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
        print("특수문자나 숫자, '.'을 제거해주세요. 오류: {}".format(k))
    except TypeError as t:
        print('문자열로 입력해주세요. 오류: {}'.format(t))


def chunk_to_num(raw: List[str]) -> List[float]:
    result = []
    for noun in raw:
        result.append(noun_to_num(noun))
    return result
