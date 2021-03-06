import numpy as np

from ..mesh.TriangleMesh import TriangleMesh  
from ..mesh.tree_data_structure import Quadtree 

class PolyData:
    def __init__(self, beta=10):
        self.beta = beta


    def init_mesh(self, n=4, meshtype='tri'):
        node = np.array([
            (0, 0),
            (0.5, 0),
            (1, 0),
            (0, 0),
            (0.5, 0.5),
            (1, 0.5),
            (0, 1),
            (0.5, 1),
            (1, 1)], dtype=np.float)
        if meshtype is 'quadtree':
            cell = np.array([
                (0, 3, 4, 1),
                (1, 4, 5, 2),
                (3, 6, 7, 4),
                (4, 7, 8, 5)], dtype=np.int)
            mesh = Quadtree(node, cell)
            mesh.uniform_refine(n)
        elif meshtype is 'tri':
            cell = np.array([
                (1, 0, 4),
                (3, 4, 0),
                (4, 5, 1),
                (2, 1, 5), 
                (4, 3, 7),
                (6, 7, 3),
                (7, 8, 4),
                (5, 4, 8)], dtype=np.int)
            mesh = TriangleMesh(node, cell)
            mesh.uniform_refine(n)
        else:
            raise ValueError("".format)
        return mesh


    def source(self, p):
        beta = self.beta
        x = p[..., 0]
        y = p[..., 1]
        val = np.zeros(p.shape)
        t = 1 + beta*np.sqrt(2*(x**2 + y**2))
        val[..., 0] = t*(x + y) + 3*x**2
        val[..., 1] = t*(x - y) + 3*y**2
        return val

    def velocity(self, p):
        x = p[..., 0]
        y = p[..., 1]
        val = np.zeros(p.shape)
        val[..., 0] = x + y
        val[..., 1] = x - y
        return val

    def pressure(self, p):
        x = p[..., 0]
        y = p[..., 1]
        val = x**3 + y**3 
        return val

    def grad_pressure(self, p):
        x = p[..., 0]
        y = p[..., 1]
        val = np.zeros(p.shape)
        val[..., 0] = 3*x**2
        val[..., 1] = 3*y**2 
        return val

    def grad_velocity(self, p):
        pass

    def neumann(self, p):
        eps = 1e-12
        x = p[..., 0]
        y = p[..., 1]
        val = np.zeros(p.shape[0:-1])
        flag = abs(x+1) < eps
        val[flag] = 1 - y[flag]
        flag = abs(x - 1) < eps
        val[flag] = 1 + y[flag]
        flag = abs(y + 1) < eps
        val[flag] = -x[flag] - 1
        flag = abs(y - 1) < eps
        val[flag] = x[flag] - 1
        return val


