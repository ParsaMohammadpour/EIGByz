# E.I.G Byz algorithm
This repo, was the second code assignment of distributed systems 
course. Here I have implemented **EIG Byz (Exponential 
Information Gathering algorithm)** for **Byzantine** failures.
This code has two parts:
<br/>
<br/>
- ### EIGByz without Auth:
    In this part, we have implemented the algorithm without **digital
signature**. Then we run simulation and see that algorithm works 
or not for different simulation parameters like different process
number, different byzantine process number and different step number.
Then as we see in simulations, this algorithm can only work for f+1 rounds
which f is number of byzantine process and only in case that we have n > 3f
where n is number of all processes that we have.
<br/>
- ### EIGByz with Auth:
    In this part, we have implemented the algorithm with **digital
signature**. For this purpose we added digital signature to each message
that holds signed message and value. When we are sending others processes
messages, we **sign their signed message** in order to be verified that 
if message was from that process with that value. Then we run simulation and see that algorithm works 
or not for different simulation parameters like different process
number, different byzantine process number and different step number.
Then as we see in simulations, this algorithm works so much better. 
It doesn't even require to have n > 3f condition or even rounds equal to
f+1. So this algorithm for sure works much better. 
<br/>
<br/>
The part of code that is used for generating tree, which is located
in external folder in [plot_tree.py](https://github.com/ParsaMohammadpour/EIGByz/blob/main/external/plot_tree.py)
file, is taken from [this](https://epidemicsonnetworks.readthedocs.io/en/latest/_modules/EoN/auxiliary.html#hierarchy_pos)
link. And the digital signature part was taken from [this](https://pypi.org/project/cryptidy/)
link.