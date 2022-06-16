import requests
import re
import json
from typing import List

from config import API_KEY, API_URL, NOUN_DATA_SETTING


_default_params = {
    'key': API_KEY,
    'req_type': 'json',
    'advanced': 'y',
    'pos': [1],
    'method': 'start'
}


def _get_params(q, start, num=100):
    _default_params['q'] = q
    _default_params['start'] = start
    _default_params['num'] = num
    return _default_params


# ref: https://smlee729.github.io/python/natural%20language%20processing/2015/12/24/korean-letter-processing-part1.html
JAMO_START_LETTER = 44032
JAMO_END_LETTER = 55203
JAMO_CYCLE = 1

assert chr(JAMO_START_LETTER)=='가', '올바르지 않은 ord값입니다.'
assert ord('힣')==JAMO_END_LETTER, f"정확하지 않은 ord입니다: {ord('힣')} != {JAMO_END_LETTER}"

EUMJUL = []

curr = JAMO_START_LETTER
while(curr <= JAMO_END_LETTER):
    EUMJUL.append(chr(curr))
    curr += JAMO_CYCLE


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


bat = ['', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ',
        'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
ja = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
mo = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
# 음절
bun_eum = []
for cho in mo:
    for jung in ja:
        for jong in bat:
            s_eum = cho+jung+jong
            bun_eum.append(s_eum)

d_hb = {bun_eum[i]: EUMJUL[i] for i in range(len(bun_eum))}  # 분리된 값이 키가 되는 음절데이터
d_bn = {EUMJUL[i]: bun_eum[i] for i in range(len(EUMJUL))}  # 음절이 키가 되는 분리된 값 데이터


def hbeum(bun):
    """
    자음, 모음을 합치는 함수
    """
    try:
        return d_hb[bun]
    except KeyError as k:
        print('특수문자나 .이 있는지 확인해주세요. 오류명: {}'.format(k))
    except TypeError as t:
        print('문자열로 입력해주세요. 오류명: {}'.format(t))


def bneum(hab: str) -> str:
    """
    음절을 자음, 모음으로 분리시키는 함수
    """
    try:
        return d_bn[hab]
    except KeyError as k:
        print('입력 오류입니다. 특수문자나 숫자, .이 있는지 확인해주세요. 오류: {}'.format(k))
    except TypeError as t:
        print('문자열로 입력해주세요. 오류: {}'.format(t))


if __name__=="__main__":
    setting = NOUN_DATA_SETTING
    lookup = [EUMJUL[0], EUMJUL[21], EUMJUL[1176], EUMJUL[1764], EUMJUL[3528]]
    _set_noun_data(lookup, **setting)
