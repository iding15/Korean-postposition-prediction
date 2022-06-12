from pred import make_target, mkdata, predjo
from cfJosa import samples

noun = mkdata(samples)
en = make_target(samples, 'en')
ig = make_target(samples, 'ig')
er = make_target(samples, 'er')

# print(en)
# print(ig)
# print(er)

print(predjo(noun, en))
