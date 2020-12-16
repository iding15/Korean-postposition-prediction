import pred as ap
import cfJosa as ac
noun = ap.mkdata(ac.decideJosa.noundata)
en = ap.mktarget().t_en()
ig = ap.mktarget().t_ig()
er = ap.mktarget().t_er()
# print(en)
# print(ig)
# print(er)
print(ap.predjo(noun,en))