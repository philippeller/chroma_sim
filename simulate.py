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

g = build_detector(10000)
g.flatten()
g.bvh = load_bvh(g)
#view(g)

#print g.solids[0].mesh.triangles

#sys.exit()

sim = Simulation(g)

# write it to a root file
#from chroma.io.root import RootWriter
#f = RootWriter('test.root')

# simulate some electrons!
n=1
# why does that not work..?
gun = vertex.particle_gun(particle_name_iter=['mu-']*n,
                          #vertex.constant((0,10000,10000)),
                          #vertex.isotropic(),
                          #vertex.flat(500,1000))
                          pos_iter=[(0,10000,10000)]*n,
                          dir_iter=[(0,-1,-1)]*n,
                          ke_iter=[1000]*n,
                          t0_iter=[0]*n)

#gun = vertex.constant_particle_gun(['mu-']*n, (0,10000,10000), (0,-1,-1), 1000)
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

    #f.write_event(ev)                      

    #detected = (ev.photons_end.flags & (0x1 << 2)).astype(bool)

    #plt.hist(ev.photons_end.t[detected],100)
    #plt.xlabel('Time (ns)')
    #plt.title('Photon Hit Times')
    #plt.show()

#f.close()
