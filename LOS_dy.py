from scipy.io import readsav
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as sp
#Read SAV file
data = readsav(r"C:\Users\aravi\Downloads\cme_nofil_noheat_gcsfit_VAR80.SAV")
x = data['r']/(7*(10**10))
y = data['th']
z = data['phi']
rho = data['rho']
temp = data['Temp']
Rl = np.zeros(np.size(x))
R_l = []
for i in range(0,np.size(x)):
    R_l = np.zeros(np.size(z))
    for j in range(0,np.size(y)):
        for k in range(0,np.size(z)):
            R_l[k] = rho[k][j][i]
    Rl[i] = np.mean(R_l)


X=np.zeros(np.size(x)*np.size(y)*np.size(z))
Y=np.zeros(np.size(x)*np.size(y)*np.size(z))
Z=np.zeros(np.size(x)*np.size(y)*np.size(z))
T=np.zeros(np.size(x)*np.size(y)*np.size(z))
p=0
for i in range(0,np.size(x)):
    for j in range(0,np.size(y)):
        for k in range(0,np.size(z)):
            #R2.append(np.log10(rho[k][j][i]))
            T[p]=(temp[k][j][i])
            X[p]=(x[i])
            Y[p]=(y[j])
            Z[p]=(z[k])
            p+=1
R2 = np.zeros(np.size(x)*np.size(y)*np.size(z))
p=0
for i in range(0,np.size(x)):
    for j in range(0,np.size(y)):
        for k in range(0,np.size(z)):
            R2[p]=(rho[k][j][i]/Rl[i])
            p+=1

def sph2cart(r, th, ph):
    x = r * np.sin(th) * np.cos(ph)
    y = r * np.sin(th) * np.sin(ph)
    z = r * np.cos(th)
    return x, y, z

nx,ny,nz = sph2cart(X,Y,Z)

k = []
l = []
m = []
o = []
n = []
#fig = plt.figure(figsize = (10, 7))
#ax = plt.axes(projection ="3d")

for i in range(0,np.size(nx),1000):
    k.append(nx[i])
    l.append(ny[i])
    m.append(nz[i])
    n.append(R2[i])
    o.append(T[i])

data =[]
for i in range(np.size(l)):
    data.append([k[i],l[i],m[i]])
v = np.array(n)
v1 = np.array(o)
data = np.array(data)
linInter_R = sp.LinearNDInterpolator(data,v)
linInter_T = sp.LinearNDInterpolator(data,v1)

y_1 = []
Y_1 = []
x2 = []
z2 = []
for p in np.linspace(min(k),max(k),200):
    for q in np.linspace(min(m),max(m),200):
        for r in np.linspace(min(l),max(l),200):
            y_1.append(r)
        Y_1.append(y_1)
        x2.append(p)
        z2.append(q)
        y_1 = []

data_int =[]
for p in range(len(x2)):
    for q in Y_1[p]:
        data_int.append([x2[p],q,z2[p]])

data_int = np.array(data_int)
rho_int = linInter_R(data_int)

r_min = min(n)
for i in range(np.size(rho_int)):
    if np.isnan(rho_int[i]):
        rho_int[i] = r_min

T_int = linInter_T(data_int)
t_min = min(o)
for i in range(np.size(T_int)):
    if np.isnan(T_int[i]):
        T_int[i] = t_min
T_int_log = np.log10(T_int)

df = pd.read_csv(r"D:\IIA PROJECT\r33-5nm.csv")

from scipy import interpolate
x = df['log10Te'].values
y = df['response'].values
f = interpolate.interp1d(x, y)

rho_int_f =[]
y_max = len(Y_1)*len(Y_1[0])
for p in range(0,y_max,len(Y_1[0])):
    rho_int_f.append(rho_int[p:p+len(Y_1[0])]*f(T_int_log[p:p+len(Y_1[0])]))

rho_int_f = np.array(rho_int_f)
rho_int_f1 = rho_int_f**2

int_value =[]
for p in range((len(Y_1))):
    int_value.append(np.trapz(rho_int_f1[p],Y_1[p]))

int_value = np.array(int_value)
T_int_log = np.log10(T_int)

plt.scatter( x2 , z2 , c = int_value, cmap = 'plasma' )
plt.colorbar(label='Integral Rho^2.R(T).dy')
plt.xlabel('X')
plt.ylabel('Z')
plt.show ()