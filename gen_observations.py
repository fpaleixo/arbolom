import os, glob, clingo

#-----Configs-----

ss_path = "./encodings/gen_observations.lp"

def on_model(m):
    print (m)

ctl = clingo.Control()

ctl.load(ss_path)
ctl.ground([("base", [])])
ctl.solve(on_model=on_model)
