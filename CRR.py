import math
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as sc
from scipy.stats import norm

Vol = np.zeros(6)    #This is an emty list dedined to append implied volatilites
Strike = [90, 95, 97.5, 100, 105, 110]
BMS = [1.3675, 1.7984, 0.5*(1.7984+2.3828), 2.3828, 5.7711, 10.2249]
Price = 100
Time = 1/12
r = 0.05

for i in range (6):    #This loop iterates over the Strike and BMS lists above to calculate the implied volatility and append it to Vol list

  def sigma (v):      # This function calculates implied volatility for each Strike price and corresponding put value
    y = 0
    p = BMS[i]
    K = Strike[i]
    S = Price
    T = Time
    d1=(np.log(S/K)+(r-y+0.5*(v[0]**2))*T)/(v[0]*math.sqrt(T))
    d2=d1-v[0]*math.sqrt(T)
    vol=(p-K*(np.exp(-r*T))*norm.cdf(-d2)+S*(np.exp(-y*T))*norm.cdf(-d1))
    return vol

  Vol[i]=(sc.fsolve(sigma, 0.1))

CRRMatrix=[]     # Each row of this matrix contains CRR Price of a strike price. Each row contains CRR Price from 10 to 500 time steps.

for m in range(6):     # This is the general iterator which iterates over different put options.
  CRR =[]
  steps = []
  for N in range(10,501):   #This is the first inside loop, which iterates from 10 to 500 for time steps.
    steps.append(N)
    T = 1/12
    sigma = Vol[m]  #implied volatility
    K = Strike[m]
    u = np.exp(sigma * math.sqrt(T/N))    #up factor
    d = 1/u
    q = (math.exp(r*T/N)-d)/(u-d)   # up factor probability
    end = []   #last time step stock prices list
    for i in range(N+1):    #This loop calculates price for each node of last time step
      end.append(max(K - Price * u ** i * d ** (N-i), 0))
    put = end
    final = []
    for i in range (N):   # This loop iterates for time steps, from the last one to the initial point
      x=[]
      for j in range (len(put)-1):    # This loop calculates the nodes' prices of step n based on corresponding nodes in step n+1
        x.append((put[j]*(1-q)+put[j+1]*(q))*math.exp(-0.05*T/N))
      put = x
      final.append(x)
    CRR.append(final[-1])   # this line appends the Put value for each number of time steps to CRR
  CRRMatrix.append(CRR)     # this line append all put values for each strike price for steps from 10 to 500 to CRRMatrix

fig, axs = plt.subplots(3,2)
axs[0, 0].plot(steps, CRRMatrix[0])
axs[0, 0].set_title('Strike = 90')
axs[0, 0].set_xlabel('Time Steps')
axs[0, 0].set_ylabel('Option Price')
axs[0, 1].plot(steps, CRRMatrix[1])
axs[0, 1].set_title('Strike = 95')
axs[0, 1].set_xlabel('Time Steps')
axs[0, 1].set_ylabel('Option Price')
axs[1, 0].plot(steps, CRRMatrix[2])
axs[1, 0].set_title('Strike = 97.5')
axs[1, 0].set_xlabel('Time Steps')
axs[1, 0].set_ylabel('Option Price')
axs[1, 1].plot(steps, CRRMatrix[3])
axs[1, 1].set_title('Strike = 100')
axs[1, 1].set_xlabel('Time Steps')
axs[1, 1].set_ylabel('Option Price')
axs[2, 0].plot(steps, CRRMatrix[4])
axs[2, 0].set_title('Strike = 105')
axs[2, 0].set_xlabel('Time Steps')
axs[2, 0].set_ylabel('Option Price')
axs[2, 1].plot(steps, CRRMatrix[5])
axs[2, 1].set_title('Strike = 110')
axs[2, 1].set_xlabel('Time Steps')
axs[2, 1].set_ylabel('Option Price')
plt.legend()
fig.suptitle('European put price')
plt.show()

#Part b

CRRerror = []
for i in range(6):    #This loop calculates error of CRRMatrix in part a and append it to Matrix CRRerror
  CRRerror.append(100*(np.array(CRRMatrix[i])-np.array(BMS[i]))/np.array(BMS[i]))

dash1 = []
dash2 = []
dash3 = []
for j in range(len(steps)):
  dash1.append(0)
  dash2.append(-0.1)
  dash3.append(0.1)


fig, axs = plt.subplots(3,2)
axs[0, 0].plot(steps, CRRerror[0], steps, dash1, 'r--' , steps, dash2, 'g:', steps, dash3, 'g:')
axs[0, 0].set_title('Strike = 90')
axs[0, 0].set_xlabel('Time Steps')
axs[0, 0].set_ylabel('error')
axs[0, 1].plot(steps, CRRerror[1], steps, dash1, 'r--' , steps, dash2, 'g:', steps, dash3, 'g:')
axs[0, 1].set_title('Strike = 95')
axs[0, 1].set_xlabel('Time Steps')
axs[0, 1].set_ylabel('error')
axs[1, 0].plot(steps, CRRerror[2], steps, dash1, 'r--' , steps, dash2, 'g:', steps, dash3, 'g:')
axs[1, 0].set_title('Strike = 97.5')
axs[1, 0].set_xlabel('Time Steps')
axs[1, 0].set_ylabel('error')
axs[1, 1].plot(steps, CRRerror[3], steps, dash1, 'r--' , steps, dash2, 'g:', steps, dash3, 'g:')
axs[1, 1].set_title('Strike = 100')
axs[1, 1].set_xlabel('Time Steps')
axs[1, 1].set_ylabel('error')
axs[2, 0].plot(steps, CRRerror[4], steps, dash1, 'r--' , steps, dash2, 'g:', steps, dash3, 'g:')
axs[2, 0].set_title('Strike = 105')
axs[2, 0].set_xlabel('Time Steps')
axs[2, 0].set_ylabel('error')
axs[2, 1].plot(steps, CRRerror[5], steps, dash1, 'r--' , steps, dash2, 'g:', steps, dash3, 'g:')
axs[2, 1].set_title('Strike = 110')
axs[2, 1].set_xlabel('Time Steps')
axs[2, 1].set_ylabel('error')
plt.legend()
fig.suptitle('European put price Relative error against Black-Merton-Scholes')
plt.show()
