from chroma import make, view
from chroma.sim import Simulation
from chroma.sample import uniform_sphere
from chroma.event import Photons
from chroma.loader import load_bvh
from chroma.generator import vertex
from chroma.camera import Camera
import matplotlib.pyplot as plt

from geometry_cylinder import build_detector

g = build_detector(1000)
g.flatten()
g.bvh = load_bvh(g)
#view(g)

sim = Simulation(g)

# write it to a root file
from chroma.io.root import RootWriter
f = RootWriter('test.root')

# simulate some electrons!
n=1
gun = vertex.particle_gun(['mu-']*n,
                          vertex.constant((0,0,0)),
                          vertex.isotropic(),
                          vertex.flat(500,1000))
i = 0
for ev in sim.simulate(gun,keep_photons_beg=True,keep_photons_end=True,
                       run_daq=False,max_steps=100):
    i +=1
    if i%10 == 0:
        print i
    f.write_event(ev)                      

    #detected = (ev.photons_end.flags & (0x1 << 2)).astype(bool)

    #plt.hist(ev.photons_end.t[detected],100)
    #plt.xlabel('Time (ns)')
    #plt.title('Photon Hit Times')
    #plt.show()

f.close()
