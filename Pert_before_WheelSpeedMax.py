
# coding: utf-8


#Let's probe whether a value of a spinning wheel rotation speed omw, determined in order to preserve the stabilization
# of a spacecraft in assuming that no perturbation happens before this omw has been established,
#will assure this stabilization in case a perturbation intervenes before the spinning wheel reaches for the  
#target speed rotation. (NB: the spinning wheel speed rotation increases constantly by k rad.s-2 until omw(tup)).

#The "full" equations are [d(om1)/dt, d(om2)/dt, d(om2)/dt] =  
#[(1/I1)*((I2-I3)*om2*om3+Iw*om3*k*t),(1/I2)*((I3-I1)*om1*om3-Iw*k),(1/I3)*((I1-I2)*om1*om2-Iw*om1*k*t)]
#and the "simplified" ones, ie when the spinning wheel is at its 
#constant target speed, are [d(om1)/dt, d(om2)/dt, d(om2)/dt] =  
#[(1/I1)*((I2-I3)*om2*om3+Iw*om3*omw),(1/I2)*((I3-I1)*om1*om3),(1/I3)*((I1-I2)*om1*om2-Iw*om1*omw)]

import numpy as np
from scipy.integrate import odeint
import Dual_spin_module as wheel
import math



#the Ii are the inertial moments around the principal axes of the spacecraft
#Iw is the spin inertial moment of the wheel (which, here, is chosen along the 2nd principal axis of the spacecraft)
#omw is the rotation speed of the wheel; until t=tcom, omw(t)=k*t, and when t>tcom, omw(t)=omw(tcom)=k*tcom=omw_com  (where k is
#no more that the constant of proportionality k=omw_com/tcom)

#duration to reach for omw_com
tup=15

#taking the inertiae values and the initial pitch rotation speed value
I1, I2, I3, Iw, om2=wheel.inertiae_and_pitchrotsp()


if om2>0:

    lim2=(I2/I3)*om2*(I3-I2)/Iw
    lim1=(I2/I1)*om2*(I1-I2)/Iw

    print("""For a stabilization along the intermediate (here the second one) principal axis, with om2
    chosen = {0} rd.s-1, the value of a positive omw_com would be higher than (I2/I3)*om2*(I3-I2)/Iw, ie higher than {1} rd.s-1, and
    the value of a negative omw_com, would be less than (I2/I1)*(I1-I2)/Iw, ie less than {2} rd.s-1.
    But those limits had been determined, (to ensure an equation of the kind d2(wi)/dt2=mu*wi with mu<0), with w2 being constant 
    and omw(t) having reached for the targeted value omw_com when a perturbation intervenes,
    such that mu is considered remaining negative.
    So now, those limits are no longer guaranteed stabilizing; However let's cast
    the integration with a perturbation occuring before the spinning wheel reaches for the target rotation speed.""".format(om2, lim2, lim1))

    print('Chosen initial rotation vector (in body frame): y0=[0,{0},0]'.format(om2))

    print('Case of a stabilization pursuit with commanded wheel rotation speed > {0} rd.s-1.'.format(lim2))

    omw_com=float(input("Which value of commanded wheel rotation speed do you want?"))

    #Initial body frame rotation speed vector of the spacecraft
    y0=[0,om2,0]


    print('perturbations at a chosen timedate t=1s; until this timedate, "full" unperturbed equations ran')
    t1=np.linspace(0,1,1000)


    sol=odeint(wheel.rota,y0,t1,(omw_com,tup,I1,I2,I3,Iw))


    wheel.wplotting(t1,sol)

    #Of course, om1 (=sol[999,0]) and om3 (=sol[999,2]) have been left, until now, equal to 0 rad.s-1
    #Then let's change [sol[999,0],sol[999,1],sol[999,2]] = [0,sol[999,1],0] into
    #[np.pi/400, sol[999,1]+np.pi/350, np.pi/500], introducing arbitrary slight perturbations

    #The data given at the end of the above integration are
    y0=sol[999]
    #We introduce the mentionned slight perturbations
    y0[0:3]=[np.pi/400,sol[999,1]+np.pi/350,np.pi/500]

    t2=np.linspace(1,15,10000)

    print('Then, and during the next 14s, "full" but "perturbed" equations still run:')

    sol=odeint(wheel.rota,y0,t2,(omw_com,tup,I1,I2,I3,Iw))


    wheel.wplotting(t2,sol)

    #The data given at the end of the above integration are
    y0=sol[9999]

    t3=np.linspace(15,1500,100000)

    print('Finally, during the next 1485s, equations keep on running with omw at its commanded value omw_com')

    sol=odeint(wheel.rota_up,y0,t3,(omw_com,I1,I2,I3,Iw))


    wheel.wplotting(t3,sol)



else:
    if om2<0:

        lim1=(I2/I3)*om2*(I3-I2)/Iw
        lim2=(I2/I1)*om2*(I1-I2)/Iw

        print('Chosen initial rotation vector (in body frame): y0=[0,{0},0]'.format(om2))

        print("""For a stabilization along the intermediate (here the second one) principal axis, with om2
                chosen = {0} rd.s-1, the value of a negative omw_com should be, according to what which has been established
                 in the file linked to Readme, less than  (I2/I3)*om2*(I3-I2)/Iw, ie less than {1} rd.s-1; and if
                the value of omw_com is chosen positive, omw_com should be more than (I2/I1)*om2*(I1-I2)/Iw,
                 ie higher than {2} rd.s-1. But those limits had been determined, (to ensure an equation of the kind
                 d2(wi)/dt2=mu*wi with mu<0), with w2 being constant and omw(t) having reached for the targeted value omw_com
                 when a perturbation intervenes, such that mu is considered remaining negative.
                So now, those limits are no longer guaranteed stabilizing; However let's cast
                the integration with a perturbation occuring before the spinning wheel reaches for
                 the target rotation speed.""".format(om2, lim1, lim2))

        print('Chosen initial rotation vector (in body frame): y0=[0,{0},0]'.format(om2))

        print('Case of stabilization pursuit with omw_com < {0} rd.s-1'.format(lim1))

        omw_com=float(input("Which value of commanded wheel rotation speed do you want?"))

        #Initial body frame rotation speed vector of the spacecraft
        y0=[0,om2,0]

        print('perturbations at a chosen timedate t=1s; until this timedate, "full" unperturbed equations ran')
        t1=np.linspace(0,1,1000)


        sol=odeint(wheel.rota,y0,t1,(omw_com,tup,I1,I2,I3,Iw))


        wheel.wplotting(t1,sol)

        #Of course, om1 (=sol[999,0]) and om3 (=sol[999,2]) have been left, until now, equal to 0 rad.s-1
        #Then let's change [sol[999,0],sol[999,1],sol[999,2]] = [0,sol[999,1],0] into
        #[np.pi/400, sol[999,1]+np.pi/350, np.pi/500], introducing arbitrary slight perturbations

        #The data given at the end of the above integration are
        y0=sol[999]
        #We introduce the mentionned slight perturbations
        y0[0:3]=[np.pi/400,sol[999,1]+np.pi/350,np.pi/500]

        t2=np.linspace(1,15,10000)

        print('Then, and during the next 14s, "full" but "perturbed" equations still run:')

        sol=odeint(wheel.rota,y0,t2,(omw_com,tup,I1,I2,I3,Iw))


        wheel.wplotting(t2,sol)

        #The data given at the end of the above integration are
        y0=sol[9999]

        t3=np.linspace(15,1500,100000)

        print('Finally, during the next 1485s, equations keep on running with omw at its commanded value omw_com')

        sol=odeint(wheel.rota_up,y0,t3,(omw_com,I1,I2,I3,Iw))


        wheel.wplotting(t3,sol)

