import numpy
import scipy
import math

class ProbabilityModel:

    # Returns a single sample (independent of values returned on previous calls).
    # The returned value is an element of the model's sample space.
    def sample(self):
        pass


# The sample space of this probability model is the set of real numbers, and
# the probability measure is defined by the density function 
# p(x) = 1/(sigma * (2*pi)^(1/2)) * exp(-(x-mu)^2/2*sigma^2)
class UnivariateNormal(ProbabilityModel):
    
    # Initializes a univariate normal probability model object
    # parameterized by mu and (a positive) sigma
    def __init__(self,mu,sigma):
        self.mu = mu
        self.sigma = sigma
    def sample(self):
        p = numpy.random.uniform()
        return scipy.special.erfinv(p*2 - 1)
    
# The sample space of this probability model is the set of D dimensional real
# column vectors (modeled as numpy.array of size D x 1), and the probability 
# measure is defined by the density function 
# p(x) = 1/(det(Sigma)^(1/2) * (2*pi)^(D/2)) * exp( -(1/2) * (x-mu)^T * Sigma^-1 * (x-mu) )
class MultiVariateNormal(ProbabilityModel):
    
    # Initializes a multivariate normal probability model object 
    # parameterized by Mu (numpy.array of size D x 1) expectation vector 
    # and symmetric positive definite covariance Sigma (numpy.array of size D x D)
    def __init__(self,Mu,Sigma):
        self.D = len(Mu)
        self.Mu = Mu
        self.Sigma = Sigma
        self.univariate = UnivariateNormal(0, 1) 
    
    def sample(self):
        A = self.cholesky(self.Sigma)
        Z = [self.univariate.sample() for i in xrange(self.D)]
        return self.Mu + numpy.dot(A, Z)

    def cholesky(self, A):
        L = numpy.zeros((self.D, self.D))
        for i in xrange(self.D):
            for j in xrange(self.D):
                if i == j:
                    L[j][j] = math.sqrt(A[j][j] - sum([elem^2 \
                            for elem in L[j][:self.D-1]]))
                else:
                    L[i][j] = (A[i][j] - sum([L[i][k]*L[j][k] \
                            for k in xrange(1, j-1)])) / L[j][j]
        return L
        
# The sample space of this probability model is the finite discrete set {0..k-1}, and 
# the probability measure is defined by the atomic probabilities 
# P(i) = ap[i]
class Categorical(ProbabilityModel):
    
    # Initializes a categorical (a.k.a. multinom, multinoulli, finite discrete) 
    # probability model object with distribution parameterized by the atomic probabilities vector
    # ap (numpy.array of size k).
    def __init__(self,ap):
        self.ap = ap
    
    def sample(self):
        sum = 0
        index = -1
        rand = numpy.random.uniform()
        while rand > sum:
            index += 1
            sum += self.ap[index]
        return index


# The sample space of this probability model is the union of the sample spaces of 
# the underlying probability models, and the probability measure is defined by 
# the atomic probability vector and the densities of the supplied probability models
# p(x) = sum ad[i] p_i(x)
class MixtureModel(ProbabilityModel):
    
    # Initializes a mixture-model object parameterized by the
    # atomic probabilities vector ap (numpy.array of size k) and by the tuple of 
    # probability models pm
    def __init__(self,ap,pm):
        self.pm = pm
        self.categorical = Categorical(ap)

    def sample(self):
        i = self.categorical.sample()
        return self.pm[i].sample()