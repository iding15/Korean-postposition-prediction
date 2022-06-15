import re
from typing import List, ClassVar, Dict
import numpy as np  # np.array type으로 변환해야 sklearn 활용 가능

from noun_data import bneum, ja, mo, bat
from config import DEFAULT_VARIABLE_WEIGHT


class SerialProcess:
    def __init__(self, raw):
        self.data = raw
        self.func: List[function] = []
    
    def parse(self):
        for f in self.func: self.data = f()
        return self.data


class NounData(SerialProcess):
    weight: ClassVar[List[float]] = DEFAULT_VARIABLE_WEIGHT

    @staticmethod
    def eumun_to_float(buneum_list: List[str], type_: str) -> Dict[str, float]:
        weight = NounData.weight

        types = ['ja', 'mo', 'bat']

        if type_ not in types:
            raise ValueError("올바르지 않은 타입 값입니다: types = ['ja', 'mo', 'bat']")
        div_value: float
        if type_ == 'ja': div_value = weight[0]
        elif type_ == 'mo': div_value = weight[1]
        else: div_value = weight[2]

        result = dict(zip(
            buneum_list,
            list(map(
                lambda num: div_value+float(num/100),
                range(1, len(buneum_list)+1)
            ))
        ))
        return result
    
    @staticmethod
    def noun_to_num(noun: str) -> float:
        if not isinstance(noun, str):
            raise TypeError(f'NounData expected str not {noun.__class__.__name__}')
        
        _to_float: function = NounData.eumun_to_float

        mo_val = _to_float(mo, 'mo')
        ja_val = _to_float(ja, 'ja')
        bat_val = _to_float(bat, 'bat')

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
            return float(num/len(noun))
        except KeyError as k:
            raise KeyError("특수문자나 숫자, '.'을 제거해주세요. 오류: {}".format(k))
        except TypeError as t:
            raise TypeError('문자열로 입력해주세요. 오류: {}'.format(t))

    def __init__(self, raw: List[str]):
        super().__init__(raw)

        if not isinstance(raw, list):
            raise TypeError(f'{self.__name__} expected list not {raw.__class__.__name__}')

        self.func= [
            self.preprocess_noun_data
        ]

    def preprocess_noun_data(self) -> np.array:
        _noun_to_num = NounData.noun_to_num

        return np.array(list(map(
            lambda noun: _noun_to_num(noun), self.data
        ))).reshape(len(self.data), 1)


class Target(SerialProcess):
    josa_type: ClassVar[str] = ""
    @staticmethod
    def divnoun(noun: str) -> str:
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
    
    @staticmethod
    def decide_josa(noun: str, josa_type: str) -> int:
        _divnoun = Target.divnoun

        types = ['en', 'ig', 'er']
        if josa_type not in types:
            raise ValueError("올바르지 않은 조사 유형입니다. -> 기대 인자값: en, ig, er")
        has_bat = False if list(_divnoun(noun))[-1] in mo else True

        return 0 if has_bat else 1
    
    def __init__(self, raw: List[str], josa_type):
        super().__init__(raw)
        self.josa_type = josa_type

        self.func = [self.set_noun_data_to_target]
    
    def set_noun_data_to_target(self):
        _decide_josa = Target.decide_josa

        try:
            target_list = list(map(lambda noun: _decide_josa(noun, self.josa_type), self.data))
            return np.array(target_list).reshape(len(target_list), )
        except ValueError as e:
            raise e
