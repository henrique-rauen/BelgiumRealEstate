#! /usr/bin/python3

#Created by Henrique Rauen (rickgithub@hsj.email)
import numpy as np

def correlation_ratio(categories, values):
    """Calculates the correlation ratio between a numeric variable and a
    category. Receives 2 pd.Series containing the categories and the values"""
    categories = np.array(categories)
    values = np.array(values)

    ss_category = 0
    ss_outside = 0
    if len(set(categories)) == 1:
        return np.NaN
    for category in set(categories): #Iterate only through distinct categories
        subgroup = values[np.where(categories == category)[0]]
        ss_category += sum((subgroup-np.nanmean(subgroup))**2)
        ss_outside += len(subgroup)*(np.nanmean(subgroup)-np.nanmean(values))**2
    return (ss_outside / (ss_outside + ss_category))**.5

def mean_abs_error(model, X,theta,y):
    """Loss function Mean Absolute Error
    For a given model returns the MAE"""
    return 1/len(X) * np.sum(abs(model(X,theta) - y))

def linear_regression(X, theta):
    """Linear regression function. Matrice multiplication"""
    return X.dot(theta)

def gradient_mae(model,X, y, theta):
    """Gradient function for the MAE error loss func"""
    m = len(y)
    y_predict = model(X, theta)
    sign = np.sign(y_predict - y)
    div = np.sum(X * sign, axis=0)
    return -1/m * div

def grad_descent(grad,model,X,y,theta,learning_rate, n):
    """Applies a learning rate to a greadient function grad() using the model
    model for n interation with learning rate learning_rate"""
    for i in range(n):
        tmp = grad(model,X,y,theta)
        theta = theta - learning_rate * tmp
    return theta

def coef_determination(y, pred):
    u = ((y - pred)**2).sum()
    v = ((y - y.mean())**2).sum()
    return 1 - u/v
