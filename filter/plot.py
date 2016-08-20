import numpy as np
import matplotlib.pyplot as plt	

f11 = lambda x: 0.4*(-2*(x**3)+9*(x**2)-12*x+5)
f12 = lambda x: 0.4*(0.75*(x**3)-2.25*(x**2)+6*x-4)

f21 = lambda x: 0.5*np.sin(np.pi*(x-1.5)) + 0.5
f22 = lambda x: 0.5*np.sin(0.5*np.pi*(x-1)) + 0.5

x1 = np.linspace(1, 2, num = 1e6)
x2 = np.linspace(2, 4, num = 2*1e6)

y11 = [f11(i) for i in x1]
y12 = [f12(i) for i in x2]
y21 = [f21(i) for i in x1]
y22 = [f22(i) for i in x2]

plt.subplot(221)
plt.plot(x1, y11)
plt.subplot(222)
plt.plot(x2, y12)
plt.subplot(223)
plt.plot(x1, y21)
plt.subplot(224)
plt.plot(x2, y22)
plt.show()