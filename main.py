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
