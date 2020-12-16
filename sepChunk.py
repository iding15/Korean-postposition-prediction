from mkEumjul import ja, mo, bat
import re
from mkEumjul import bneum

# mkfloatdata
class mkFloat:
    count = 1
    dm = {}
    def __init__(self):
        self.count = float(self.count)
        self.dm = {}
    def float_mo(self):
        for m in mo:
            num = 0.00+self.count/100
            self.dm[m] = float(num)
            self.count+=1
        return self.dm
    def float_ja(self):
        for j in ja:
            num = 1.00+self.count/100
            self.dm[j] = float(num)
            self.count+=1
        return self.dm
    def float_bat(self):
        for b in bat:
            num = 10.00+self.count/100
            self.dm[b] = float(num)
            self.count+=1
        return self.dm

def divsen(sen):
    try:
        sen = re.sub('\s+','',sen)
        l_sen = re.sub('',',',sen).split(',')
        s = ''
        for ls in l_sen:
            if ls !='':
                s = s + bneum(ls)
        # print(s)
        return s
    except KeyError as k:
        print("특수문자나 숫자, '.'을 제거해주세요. 오류: {}".format(k))
    except TypeError as t:
        print('문자열로 입력해주세요. 오류: {}'.format(t))

def numsen(sen):
    fmo = mkFloat().float_mo()
    fja = mkFloat().float_ja()
    fbt = mkFloat().float_bat()
    try:
        sen = re.sub('\s+','',sen)
        l_sen = re.sub('',',',sen).split(',')
        l = []
        for ls in l_sen:
            if ls !='':
                bls = bneum(ls)
                bls = re.sub('',',',bls).split(',')
                if len(bls) == 5:
                    count = 0
                    for b in bls:
                        count+=1
                        if count==2:
                            l.append(fmo[b])
                        elif count==3:
                            l.append(fja[b])
                        elif count==4:
                            l.append(fbt[b])
                elif len(bls)==4:
                    count = 0
                    for b in bls:
                        count+=1
                        if count==2:
                            l.append(fmo[b])
                        elif count==3:
                            l.append(fja[b])
                        elif count==4:
                            l.append(0.0)
        n = 0
        for i in l:
            n = n+i
        return n
    except KeyError as k:
        print("특수문자나 숫자, '.'을 제거해주세요. 오류: {}".format(k))
    except TypeError as t:
        print('문자열로 입력해주세요. 오류: {}'.format(t))

def md(l_chunk):
    l = []
    for lc in l_chunk:
        l.append(numsen(lc))
    return l

fmo = mkFloat().float_mo()
fja = mkFloat().float_ja()
fbt = mkFloat().float_bat()
