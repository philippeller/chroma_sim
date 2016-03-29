from chroma import make, view
from chroma.geometry import Solid, Geometry
from chroma.detector import Detector
from chroma.transform import make_rotation_matrix
from chroma.demo.optics import glass, ice, water,vacuum, r7081hqe_photocathode
from chroma.demo.optics import black_surface
import numpy as np

def build_dom():
    """Returns a simple photodetector Solid. The photodetector is a sphere of
    size `size` constructed out of a glass envelope with a photosensitive
    face on the inside of the glass envelope."""
    glass_thickness = 10 #mm
    size = 100 #mm
    # outside of the glass envelope
    outside_mesh = make.sphere(size)
    # inside of the glass envelope
    inside_mesh = make.sphere(size-glass_thickness)

    # outside solid with ice on the outside, and glass on the inside
    outside_solid = Solid(outside_mesh,glass,ice)    

    inside_surface = r7081hqe_photocathode
    inside_color = 0x00ff00

    # construct the inside solid
    inside_solid = Solid(inside_mesh,vacuum,glass,surface=inside_surface,
                         color=inside_color)

    # you can add solids and meshes!
    return outside_solid + inside_solid

def build_detector():
    """Returns a cubic detector made of cubic photodetectors."""
    world_size = 1000000 # 1 km

    d = Detector(ice)

    #add DOMs at locations x,y,z
    
    channel_id = 0

    for x in np.arange(-500000,500001,100000):
        for y in np.arange(-500000,500001,100000):
            for z in np.arange(-500000,500001,100000):
                d.add_pmt(build_dom(),displacement=(x,y,z),channel_id=channel_id)
                channel_id += 1

    world = Solid(make.box(world_size,world_size,world_size),ice,vacuum,color=0x33ffffff)
    d.add_solid(world)

    return d

