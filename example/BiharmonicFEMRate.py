import matplotlib.pyplot as plt
import numpy as np
import sys

from fealpy.pde.BiharmonicModel2d import SinSinData, BiharmonicData4
from fealpy.fem.BiharmonicFEMModel import BiharmonicRecoveryFEMModel
from fealpy.mesh import MeshZoo
from fealpy.mesh.meshio import load_mat_mesh


from fealpy.tools.show import show_error_table 
from fealpy.tools.show import showmultirate

m = int(sys.argv[1]) 
meshtype = int(sys.argv[2])
rtype = int(sys.argv[3])
d = sys.argv[4]

if rtype == 1:
    rtype='simple'
elif rtype == 2:
    rtype='harmonic'
elif rtype == 3:
    rtype = 'test'

if m == 1:
    pde = SinSinData()
    box = [0, 1, 0, 1]
elif m == 2:
    pde = BiharmonicData4()
    box = [0, 1, 0, 1]

maxit = 4

Ndof = np.zeros((maxit,), dtype=np.int)
errorType = [
         '$\| u - u_h\|$',
         '$\|\\nabla u - \\nabla u_h\|$',
         '$\|\\nabla u_h - G(\\nabla u_h) \|$',
         '$\|\\nabla u - G(\\nabla u_h)\|$',
         '$\|\Delta u - \\nabla\cdot G(\\nabla u_h)\|$',
         '$\|\Delta u -  G(\\nabla\cdot G(\\nabla u_h))\|$',
         '$\|G(\\nabla\cdot G(\\nabla u_h)) - \\nabla\cdot G(\\nabla u_h)\|$'
         ]
errorMatrix = np.zeros((len(errorType), maxit), dtype=np.float)
meshzoo = MeshZoo()
n = 10
dirichlet = False 
for i in range(maxit):
    if meshtype == 1:
        mesh = meshzoo.regular(box, n=n)
    elif meshtype == 2:
        mesh = meshzoo.rice_mesh(box, n=n)
    elif meshtype == 3:
        mesh = meshzoo.cross_mesh(box, n=n)
    elif meshtype == 4:
        mesh = meshzoo.fishbone(box, n=n)
    elif meshtype == 5:
        mesh = load_mat_mesh('../data/square'+str(i+2)+'.mat')

    n *= 2
    fem = BiharmonicRecoveryFEMModel(mesh, pde, 1, 5, rtype=rtype, dirichlet=dirichlet)
    fem.solve()

    Ndof[i] = fem.space.number_of_global_dofs()
    e0, e1, e2, e3, e4 = fem.get_error()
    eta0 = fem.grad_recover_estimate()
    eta1 = fem.laplace_recover_estimate(etype=1)

    e5 = np.sqrt(np.sum(eta0**2))
    e6 = np.sqrt(np.sum(eta1**2))

    errorMatrix[0, i] = e0
    errorMatrix[1, i] = e1
    errorMatrix[2, i] = e5
    errorMatrix[3, i] = e2
    errorMatrix[4, i] = e3
    errorMatrix[5, i] = e4
    errorMatrix[6, i] = e6


show_error_table(Ndof, errorType, errorMatrix, end='\\\\\\hline\n')
showmultirate(plt, 1, Ndof, errorMatrix,  errorType)

n = 10
if meshtype == 1:
    mesh = meshzoo.regular(box, n=n)
elif meshtype == 2:
    mesh = meshzoo.rice_mesh(box, n=n)
elif meshtype == 3:
    mesh = meshzoo.cross_mesh(box, n=n)
elif meshtype == 4:
    mesh = meshzoo.fishbone(box, n=n)
elif meshtype == 5:
    mesh = load_mat_mesh('../data/square'+str(2)+'.mat')

fig = plt.figure()
fig.set_facecolor('white')
axes = fig.gca() 
mesh.add_plot(axes, cellcolor='w')
fig.savefig(d+'/mesh'+str(m-2)+'-'+str(i)+'.pdf')

plt.show()
