import kTreePlotter
import KTree
import matplotlib.pyplot as plt
with open('lenses.txt') as f:
	lenses = [inst.strip().split('\t') for inst in f.readlines()]
	lensesLabels  = ['age','prescript', 'astigmatic', 'tearRate']
	lensesTree = KTree.creatTree(lenses, lensesLabels)
	print(lensesTree)
	kTreePlotter.createPlot(lensesTree)
	