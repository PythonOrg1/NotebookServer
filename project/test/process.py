
arrDsets = []
for d in pjs.dsets:
    if not d in arrDsets:
        arrDsets.append(d)
numDsetsTotal = len(arrDsets)   # size of the datasets that need to be copy


for p in projects:
    numCurPj = projects.index(p) + 1


    for d in dsets:
        numCurDset = dsets.index(d) + 1

        path = pUser + '/system/datasets' + d.Id
        if not os.path.exists(path):
            #start copying
            startProcessThreadForDataset()
            shell.exec(cp)

