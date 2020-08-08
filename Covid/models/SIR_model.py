import pandas as pd
import numpy as np

from datetime import datetime
import pandas as pd 

from scipy import optimize
from scipy import integrate
from functools import reduce

from scipy.integrate import odeint
from scipy.optimize import minimize,curve_fit

df_analyse=pd.read_csv('data/processed/COVID_small_flat_table_conf.csv',sep=';')
df_analyse_=pd.read_csv('data/processed/COVID_small_flat_table_recov.csv',sep=';')

def get_data(country):

    data = pd.DataFrame({"date":df_analyse['date'],"confirmed":df_analyse[country],"recovered":df_analyse_[country]})
    print(data)
    blks = 10
    futr = 30
    t = np.arange(blks)
    N = 1000000

    def SIR(y, t, beta, gamma):    
        S = y[0]
        I = y[1]
        R = y[2]
        return -beta*S*I/N, (beta*S*I)/N-(gamma*I), gamma*I

    def fit_odeint(t,beta, gamma):
        return odeint(SIR,(s_0,i_0,r_0), t, args = (beta,gamma))[:,1]
    
    def loss(point, data, s_0, i_0, r_0):
        # print(data)
        predict = fit_odeint(t, *point)
        l1 = np.sqrt(np.mean((predict - data)**2))
        return l1
    
    predicted_simulations = []

    for i in range(len(data)-blks):
        if i%blks == 0:
            train = list(data['confirmed'][i:i+blks])
            i_0 = train[0]
            r_0 = data ['recovered'].values[i]
            s_0 = 1000000 - i_0 - r_0 
            params, cerr = curve_fit(fit_odeint,t, train)
            optimal = minimize(loss, params, args=(train, s_0, i_0, r_0))
            beta,gamma = optimal.x
            predicted_simulations = predicted_simulations[:-(futr-blks)]
            predict = list(fit_odeint(np.arange(futr),beta,gamma))
            predicted_simulations.extend(predict)
    
    return (predicted_simulations, data)