import math 

class LinearCooling:
    def __init__(self, name, beta, last_tmp):
        self.name = name
        self.beta = beta
        self.last_tmp = last_tmp       
        
    def cooling(self):
        self.last_tmp = self.last_tmp - self.beta
        return self.last_tmp

class GeometricCooling:
    def __init__(self, name, alpha, last_tmp):
        self.name = name
        self.alpha = alpha
        self.last_tmp = last_tmp
        
    def cooling(self):
        self.last_tmp = self.alpha * self.last_tmp
        return self.last_tmp

class LogarithmicCooling:
    def __init__(self, name, iter, last_tmp):
        self.name = name
        self.iter = iter
        self.last_tmp = last_tmp
    
    def cooling(self):
        self.last_tmp = (math.log(self.iter)/math.log(self.iter+1))*self.last_tmp
        return self.last_tmp

class HybridCooling:
    def __init__(self, name, alpha, beta, iter, last_tmp):
        self.name = name
        self.alpha = alpha
        self.beta = beta
        self.iter = iter
        self.last_tmp = last_tmp
    
    def cooling(self):
        if self.iter <= self.beta:
            self.last_tmp = (self.iter/self.iter+1)*self.last_tmp
        else:
            self.last_tmp = self.alpha * self.last_tmp
        return self.last_tmp

class ExponentialCooling:
    def __init__(self, name, beta, last_tmp):
        self.name = name
        self.beta = beta
        self.last_tmp = last_tmp
    
    def cooling(self):
        self.last_tmp = self.last_tmp/(1+(self.beta*self.last_tmp))
        return self.last_tmp