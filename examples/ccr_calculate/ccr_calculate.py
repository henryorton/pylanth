from paramagpy import protein, fit, dataparse, metal
import numpy as np

# Load the PDB file and get iron centre
prot = protein.load_pdb('1bzrH.pdb')
ironAtom = prot[0]['A'][("H_HEM",154," ")]['FE']

# Make high and low spin Fe paramagnetic centers
met_cn = metal.Metal(position=ironAtom.position, 
					 B0=18.79, 
					 temperature=303.0,
					 taur=5.7E-9)
met_f = met_cn.copy()
met_cn.iso = 4.4E-32
met_f.iso = 30.1E-32

# Load experimental data
data_cn = prot.parse(dataparse.read_ccr("myo_cn.ccr"))
data_f = prot.parse(dataparse.read_ccr("myo_f.ccr"))

# Calculate the cross-correlated realxation
compare_cn = []
for H, N, value, error in data_cn:
	delta = met_cn.atom_ccr(H, N)
	compare_cn.append((delta, value))

compare_f = []
for H, N, value, error in data_f:
	delta = met_f.atom_ccr(H, N)
	compare_f.append((delta, value))

m0 = metal.Metal(position=ironAtom.position)
m, cal, qfac = fit.nlr_fit_metal_from_ccr(m0, data_f)

print(m.info())










# # Plot theory compared to experimental data
# from matplotlib import pyplot as plt
# fig = plt.figure(figsize=(6,6))
# ax = fig.add_subplot(111)
# ax.scatter(*zip(*compare_cn), label="myo_cn")
# ax.scatter(*zip(*compare_f), label="myo_f")
# ax.legend()
# ax.set_xlabel("Calculated")
# ax.set_ylabel("Experiment")
# plt.show()
