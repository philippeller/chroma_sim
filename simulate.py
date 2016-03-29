from chroma import make, view
from chroma.sim import Simulation
from chroma.sample import uniform_sphere
from chroma.event import Photons
from chroma.loader import load_bvh
from chroma.generator import vertex
from chroma.camera import Camera
import matplotlib.pyplot as plt
import sys

from geometry_cylinder import build_detector

g = build_detector()
g.flatten()
g.bvh = load_bvh(g)
#view(g)


ys.exit()

sim = Simulation(g)

n=1
gun = vertex.particle_gun(['mu-']*n,
                          vertex.constant((0,10000,10000)),
                          vertex.constant([1,0,-1]),
                          vertex.constant(1000),
                          vertex.constant(0))

i = 0
for ev in sim.simulate(gun,keep_detected_photons=True,
                       max_steps=100):
    i +=1
    if i%10 == 0:
        print i
    photons = ev.photons_end
    #print 'pos', photons.pos.ravel()
    #print 'dir', photons.dir.ravel()
    #print 'pol', photons.pol.ravel()
    #print 'wavelength', photons.wavelengths[0]
    #print 'time', photons.t[0]
    #print 'last hit', photons.last_hit_triangles[0]
    #print 'flag', photons.flags[0]
    pmt_hits = 0
    for t_id in photons.last_hit_triangles:
        if g.solid_id[int(t_id.get())] == 0:
            pmt_hits += 1
    print pmt_hits, ' out of ', len(photons.last_hit_triangles)

    #channel
    g.solid_id_to_channel_index[g.solid_id[int(t_id.get())]]

    #detected = (ev.photons_end.flags & (0x1 << 2)).astype(bool)

    #plt.hist(ev.photons_end.t[detected],100)
    #plt.xlabel('Time (ns)')
    #plt.title('Photon Hit Times')
    #plt.show()
