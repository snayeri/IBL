"""
This model utilizes Idzorek et al (2004)'s approach to incorporate user specific confidence levels on views expressed about assets' absolute or relative performance.
The steps are laid out in Thomas Idzorek's 2004 paper: 
"A step-by-step guide to the Black-Litterman model: Incorporating user-specified confidence levels":
https://www.sciencedirect.com/science/article/pii/B9780750683210500030 
"""

# importing the necessary packages
import pandas as pd
import numpy as np
from pandas_datareader import data as wb
import scipy.optimize as opt

# create a portfolio class
class portfolio:
    """
    uses historal daily prices to compute monthly returns and covariances
    """
    def __init__(self, assets_prices):
        #don't forget you are removing last month
        self.returns = assets_prices.apply(lambda x: np.log(x/x.shift(1))).resample('m').sum()
    def covariance(self):
        return self.returns.cov()

# create the Idzorek approach to Black Litterman model
class IBL_model(portfolio):
    """
    utilizes Thomas Idzorek's 2004 approach in "step by step guide to the black litterman model:"
    https://www.sciencedirect.com/science/article/pii/B9780750683210500030 
    """
    def __init__(self, assets_prices, market_caps, market_prices,monthly_risk_free,tau):
        portfolio.__init__(self,assets_prices) 
        self.tickers = assets_prices.columns.values
        self.mkt_w = market_caps.astype(float)/market_caps.sum()
        self.mkt_r = market_prices.apply(lambda x: np.log(x/x.shift(1))).resample('m').sum()
        self.rf = monthly_risk_free.iloc[:,0]
        self.tau = tau
        self.sigma = self.excess_r().cov()
        self.mkt_var = self.mkt_w.transpose().dot(self.sigma).dot(self.mkt_w)
        self.lamda = (self.mkt_r.mean()[0]-self.rf.mean())/self.mkt_var
        self.pi = self.lamda*self.sigma.dot(self.mkt_w)
    
    def excess_r(self):
        excess_mr = pd.DataFrame()
        for i in self.returns:
            excess_mr[i] = self.returns[i]-self.rf
        return excess_mr
    
    def Im_expc_r(self):
        """ implied equilibrium expected returns vector """
        Implied_equil_expected_returns = pd.DataFrame(wb.get_quote_yahoo(self.tickers)['longName'])
        Implied_equil_expected_returns['e(r)'] = self.pi
        return Implied_equil_expected_returns
    
    def Kview_omega(self,que,rho_v,confidence):
        """
        finds expected returns with one view
        que - floating number. the relative outperformance of two assets (or one assets relative to risk-free) over next month
        rho_v - the rho vector that id's the assets involved in the view. 0 for other assets
        confidence - from 0 to 100 is the confidence interval in the view
        """
        #Step1 compute expected return with 100% confidence
        a = self.tau*self.sigma.dot(rho_v)
        b = a/(rho_v.dot(a))
        c = que - rho_v.transpose().dot(self.pi)
        e_100 = self.pi+b*c
        #Step2 compute weight for 100% confidence
        w_100 = np.linalg.pinv(self.lamda*self.sigma).dot(e_100)
        #Step3 compute departure of weights from market weight
        D_100 = w_100-self.mkt_w
        #Step4 compute tilt caused by less than 100% confidence
        tilt = np.multiply(D_100,confidence)
        #Step5 get target weight based on addition of tilt to market weight
        w_c = self.mkt_w + tilt
        #Step6 find the implied uncertainty 
        def fun(omega_hat):
            a0 = np.linalg.pinv(self.lamda*self.sigma)
            a1 = np.linalg.pinv(self.tau*self.sigma) 
            a2 = np.linalg.pinv(a1 + rho_v.dot((1/omega_hat)*rho_v))
            a3 = a1.dot(self.pi)
            a4 = a3 + rho_v*(que/omega_hat)
            w_k = a0.dot(a2).dot(a4)
            return ((w_c-w_k)**2).sum()
        return opt.fmin(fun,0.01,disp=0)[0]
    
    def views_expected_r(self,Q,P,C):
        """
        finds Black Litterman expected return based on some views about the assets performance.
        Note: all parameters should be inserted as array([])
        Q is (Nx1) array of expected (viewed) outperformance (among assets or relative to risk-free rate). 
        P (rho) is the id matrix with each row identifying assets involved with each view
        C is the confidence matrix with each row showing confidence levels involved with each view
        this is the 7th step of the Idzorek approach.
        """
        Omega = np.identity(len(Q))
        for eachview in range(0,len(Q)):
            Omega[eachview][eachview]=self.Kview_omega(Q[eachview],P[eachview],C[eachview])
        #Step 7 plug in all the parameters to get the expected returns
        P_T = P.transpose()
        Omega_inv = np.linalg.pinv(Omega)
        risk_inv = np.linalg.pinv(self.tau*self.sigma)
        part_one = risk_inv + P_T.dot(Omega_inv).dot(P)
        part_two = risk_inv.dot(self.pi) +P_T.dot(Omega_inv).dot(Q)
        expected_return = np.linalg.pinv(part_one).dot(part_two)
        return expected_return
