
# Évaluer la ligne suivante en premier
from calisson import test_solver, doSolve
from html_calisson import make_enigma_from_url
import re



with open('./enigmathix/enigmathix.txt') as f:
    lines = f.readlines()

truelines = []
for l in lines:
    if l != "\n":
        truelines.append(l.split(" ")[-1][:-1])

tablines = ["=" + l.split("=")[-1] for l in truelines]


with open('./enigmathix/diagnostics.txt', 'w') as diagFile:
    dictErr = {}
    idx = 0
    for i, tl in enumerate(tablines):
        dim, enigme = make_enigma_from_url(tl)
        lsol = doSolve(enigme,dim)
        if len(lsol) == 1 and not (-1 in lsol[0]):
            pass#print(f"grille correcte : {tl}")
        else:
            idx += 1
            matchNumEnig = re.search('[0-9]+$', tl)
            if matchNumEnig == None:
                numEnigme = 'sans numéro'
            else:
                numEnigme = tl[matchNumEnig.start():]
            diag = ""
            if len(lsol) ==0 : diag += "pas de solution"
            if len(lsol) > 1 : diag += "plusieurs solutions"
            indet = False
            for sol in lsol: indet = indet or (-1 in sol)
            if indet :
                if diag == "":
                    diag = "une solution avec un/plusieurs cube(s) indéterminé(s)"
                else:
                    diag += ", avec des cubes indéterminés"

            msg = f"erreur {idx} -> énigme {numEnigme}  (ligne {i+1}) : {diag}"
            print(msg)
            diagFile.write(msg)
            diagFile.write('\n')
            dictErr[i+1] = (enigme, dim)
            figFile = f'./enigmathix/{str(i+1)}.pdf'
            test_solver(enigme, dim, False, figFile)

