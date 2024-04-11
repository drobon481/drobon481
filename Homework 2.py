#!/usr/bin/env python
# coding: utf-8

# In[69]:


def github() -> str:
    """
    Returns a link to solutions on GitHub.
    """
    return "https://github.com/drobon481/drobon481/tree/main"

print(github())


# In[74]:


import numpy as np

def simulate_data(seed: int = 481) -> tuple:
    """
    Simulates data using a specific data generating process. returns an output based on eequaiton.
    """
    n = 1000
    xi1 = np.random.normal(0, 2, n)
    xi2 = np.random.normal(0, 2, n)
    xi3 = np.random.normal(0, 2, n)
    ei = np.random.normal(0, 1, n)

    
    #print(np.mean(xi1))
          
    X = np.column_stack((xi1, xi2, xi3))
    y = 5 + 3 * xi1 + 2 * xi2 + 6 * xi3 + ei

    return y, X

y, X = simulate_data(seed=123)
print(y.shape, X.shape)


# In[75]:


import numpy as np
import scipy as sp

def neg_ll(beta, y, X):
    """
    Negative log likelihood function for the linear regression model.
    """
    beta0, beta1, beta2, beta3 = beta
    y_hat = beta0 + beta1 * X[:, 0] + beta2 * X[:, 1] + beta3 * X[:, 2]
    var = 1 
    MLE = np.sum(0.5 * np.log(2 * np.pi * var) + ((y - y_hat) ** 2) / (2 * var))
    return MLE

def estimate_mle(y: np.array, X: np.array) -> np.array:
    """
    Returns:
    - np.array: Estimated coefficients (beta0, beta1, beta2, beta3).
    """
    result = sp.optimize.minimize(
        fun=neg_ll,  # the objective function
        x0=np.array([0, 0, 0, 0]),  # starting guess
        args=(y, X),  # additional parameters passed to neg_ll
        method='Nelder-Mead'  # optionally pick an algorithm
    )
    return result.x

coefficients = estimate_mle(y, X)
print(coefficients)



# In[76]:


import numpy as np
import scipy as sp

def loss_function(beta, y, X):
    """
    Loss function for OLS estimation.
    """
    y_pred = np.dot(X, beta)
    return np.sum((y - y_pred) ** 2)

def estimate_ols(y: np.array, X: np.array) -> np.array:
    """
    Estimates the OLS coefficients for the linear regression model with an intercept.
    """
    # intercept term
    X_intercept = np.c_[np.ones(X.shape[0]).reshape(-1,1), X]
    
    # beta = 0 vector 
    beta_hat = np.zeros(X_intercept.shape[1])

    # Minimize the loss function
    result = sp.optimize.minimize(loss_function, beta_hat, args=(y, X_intercept))

    return result.x

coefficients = estimate_ols(y, X)
print(coefficients)


# In[ ]:




