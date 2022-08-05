from abc import ABC, abstractmethod
import pymc3 as pm


class Likelihood(ABC):
    """Subclasses should implement the observed method which defines an observed random variable"""

    @abstractmethod
    def observed(self, mu, y_scaled):
        pass


class Gaussian(Likelihood):
    """Gaussian likelihood with constant variance"""

    def __init__(self, sigma=0.5):
        self.sigma = sigma

    def observed(self, mu, y_scaled):
        sigma = pm.HalfCauchy("sigma", self.sigma)
        pm.Normal("obs", mu=mu, sd=sigma, observed=y_scaled)


class StudentT(Likelihood):
    """StudentT likelihood with constant variance, robust to outliers"""

    def __init__(self, alpha=1.0, beta=1.0, sigma=0.5):
        self.alpha = alpha
        self.beta = beta
        self.sigma = sigma

    def observed(self, mu, y_scaled):
        nu = pm.InverseGamma("nu", alpha=self.alpha, beta=self.beta)
        sigma = pm.HalfCauchy("sigma", self.sigma)
        pm.StudentT("obs", mu=mu, sd=sigma, nu=nu, observed=y_scaled)
