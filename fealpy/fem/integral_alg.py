import numpy as np

class IntegralAlg():
    def __init__(self, integrator, mesh, measure=None):
        self.mesh = mesh
        self.integrator = integrator
        if measure is None:
            self.measure = mesh.entity_measure()
        else:
            self.measure = measure 

    def integral(self, u, celltype=False):
        qf = self.integrator  
        bcs, ws = qf.quadpts, qf.weights
        val = u(bcs)
        e = np.einsum('i, ij..., j->j...', ws, val, self.measure)
        if celltype is True:
            return e
        else:
            return e.sum() 

    def L1_error(self, u, uh, celltype=False):
        def f(x):
            xx = self.mesh.bc_to_point(x)
            return np.abs(u(xx) - uh(x))
        e = self.integral(f, celltype=celltype)
        if elemtype is False:
            return e.sum()
        else:
            return e
        return 

    def L2_error(self, u, uh, celltype=False):
        def f(x):
            xx = self.mesh.bc_to_point(x)
            return (u(xx) - uh(x))**2
        e = self.integral(f, celltype=celltype)
        if celltype is False:
            return np.sqrt(e.sum())
        else:
            return np.sqrt(e)
        return 

    def Lp_error(self, u, uh, p, celltype=False):
        def f(x):
            xx = self.mesh.bc_to_point(x)
            return np.abs(u(xx) - uh(x))**p
        e = self.integral(f, celltype=celltype)
        if celltype is False:
            return e.sum()**(1/p)
        else:
            return e**(1/p)
        return 
