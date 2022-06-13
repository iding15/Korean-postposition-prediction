from pred import predjo
from preprocessing import make_target, make_data
from noun_data import get_noun_data

noun_data = get_noun_data()['data']

noun = make_data(noun_data)
en = make_target(noun_data, 'en')
ig = make_target(noun_data, 'ig')
er = make_target(noun_data, 'er')

# print(en)
# print(ig)
# print(er)

print(predjo(noun, en))
