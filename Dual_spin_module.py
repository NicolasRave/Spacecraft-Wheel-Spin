    #This module contains functions used by one or two of the other files
    
import matplotlib.pyplot as plt
import numpy as np

def attempt_float(x):
    try:
        return float(x)
    except(TypeError, ValueError):
        print('We need a numerical value')
        
def attempt_pfloat(x):
    x=attempt_float(x)
    if type(x)==float and x<0:
        print('We need a numerical strictly positive value')
    else:
        return x
        
        
def inertiae_and_pitchrotsp():
    #taking the inertiae values and the initial pitch rotation speed value
    
    print("You are going to enter, one by one, the three principal inertia moments (in kg.m2) of the spacecraft For example,\
 630000,1365000,and 1665000 ")
 
    I1, I2, I3, Iw= (0,0,0,0)

    while type(I1)!=float:
        I1=attempt_pfloat(input("What are the principal inertia moment (in kg.m2) of the spacecraft according to the roll axis?"))
    while type(I2)!=float:
        I2=attempt_pfloat(input("What are the principal inertia moment (in kg.m2) of the spacecraft according to the pitch axis?"))
    while type(I3)!=float:
        I3=attempt_pfloat(input("What are the principal inertia moment (in kg.m2) of the spacecraft according to the yaw axis?"))

    while type(Iw)!=float:
        Iw=attempt_pfloat(input("What are the spin inertia moment (in kg.m2) of the wheel?"))

    #variable for the pitch rotation speed
    om2=0
        
    while type(om2)!=float:
        om2=attempt_float(input("What is the initial pitch rotation speed, in rad/s? For example, 0.06 "))

    return I1, I2, I3, Iw, om2
            
            
def wplotting(t,sol):
    plt.plot(t,sol[:,0],'y',label='om1(t), rad/s')
    plt.plot(t,sol[:,1],'m',label='om2(t), rad/s')
    plt.plot(t,sol[:,2],'orange',label='om3(t), rad/s')
    plt.legend(loc='best')
    plt.xlabel('t')
    plt.grid()
    plt.show()


def rota(y,t,omw_com,tup,I1,I2,I3,Iw):
    #here, the wheel rotation speed omw(t) is increasing with t (omw(t) = (omw_com/tup)*t) until t be tup.
    #omw_com, in input, is the commanded value, ie omw(tup).
    #(In the doc supplied with the .py files, omega_com is omw_com
    #and t_com is tup).
    #This function allows to follow the variations of vector w
    #with the help of the "odeint" function used in the file which calls
    #the present module.
    #y, in input, is the initial vector w.
    #tup: duration of continuous increase of omw
    om1,om2,om3=y
    k=omw_com/tup
    dydt=[(1/I1)*((I2-I3)*om2*om3+Iw*om3*k*t),(1/I2)*((I3-I1)*om1*om3-Iw*k),(1/I3)*((I1-I2)*om1*om2-Iw*om1*k*t)]

    return dydt


def rota_up(y,t,omw_com,I1,I2,I3,Iw):
    #here, the wheel rotation speed has reached for its commanded value, omw_com.
    #This function allows to follow the variations of vector w
    #with the help of the "odeint" function used in the file which calls
    #the present module.
    om1,om2,om3=y
    dydt=[(1/I1)*((I2-I3)*om2*om3+Iw*om3*omw_com),(1/I2)*((I3-I1)*om1*om3),(1/I3)*((I1-I2)*om1*om2-Iw*om1*omw_com)]

    return dydt

