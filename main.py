from pred import predjo
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

print(predjo(noun, en))
