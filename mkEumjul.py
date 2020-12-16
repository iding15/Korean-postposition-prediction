from habEum import hab_eum

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
# print(bun_eum)
d_hb = {bun_eum[i]: hab_eum[i] for i in range(len(bun_eum))}
d_bn = {hab_eum[i]: bun_eum[i] for i in range(len(hab_eum))}
# res = {test_keys[i]: test_values[i] for i in range(len(test_keys))}
def hbeum(bun):
    try:
        return d_hb[bun]
    except KeyError as k:
        print('특수문자나 .이 있는지 확인해주세요. 오류명: {}'.format(k))
    except TypeError as t:
        print('문자열로 입력해주세요. 오류명: {}'.format(t))

def bneum(hab):
    try:
        return d_bn[hab]
    except KeyError as k:
        print('입력 오류입니다. 특수문자나 숫자, .이 있는지 확인해주세요. 오류: {}'.format(k))
    except TypeError as t:
        print('문자열로 입력해주세요. 오류: {}'.format(t))

