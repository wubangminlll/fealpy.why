
import numpy as np

class SinCosExpData:
    def __init__(self):
        self.diffusionCoefficient = 1/16

    def init_value(self, p):
        return self.solution(p, 0.0)

    def diffusion_coefficient(self):
        return self.diffusionCoefficient 

    def solution(self, p, t):
        """ The exact solution 
        """
        x = p[:, 0]
        y = p[:, 1]
        pi = np.pi
        u = np.sin(pi*x)*np.cos(pi*y)*np.exp(-pi**2/8*t)
        return u

    def source(self, p, t):
        """ The right hand side of Possion equation
        INPUT:
            p: array object, N*2 
        """
        return 0.0

    def dirichlet(self, p, t):
        """ Dilichlet boundary condition
        """
        return 0.0 

    def neuman(self, p, t):
        """ Neuman boundary condition
        """
        return 0.0

    def is_dirichlet_boundary(self, p):
        eps = 1e-14 
        return (p[:, 0] < eps) | (p[:, 0] > 1.0 - eps) 

    def is_neuman_boundary(self, p):
        eps = 1e-14
        return (p[:, 1] < eps) | (p[:, 1] > 1.0 - eps)

