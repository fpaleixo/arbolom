import os, glob, clingo
from clingo.application import ApplicationOptions

#-----Configs-----

observation_number = "2"
time_steps = "3"
model_path = "./lp_models/6.lp"
ss_path = "./encodings/gen_observations.lp"



#-----Auxiliary Functions-----

def on_model(m):
    print (m)



#-----Main-----

ctl = clingo.Control(arguments=["-c e=" + observation_number, "-c t=" + time_steps])

ctl.load(model_path)
ctl.load(ss_path)
ctl.ground([("base", [])])
ctl.solve(on_model=on_model)

