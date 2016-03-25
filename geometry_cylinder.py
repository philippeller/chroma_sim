from chroma import make, view
from chroma.geometry import Solid, Geometry
from chroma.detector import Detector
from chroma.transform import make_rotation_matrix
from chroma.demo.optics import glass, ice, water,vacuum, r7081hqe_photocathode
from chroma.demo.optics import black_surface
import numpy as np

def build_pd(size, glass_thickness):
    """Returns a simple photodetector Solid. The photodetector is a sphere of
    size `size` constructed out of a glass envelope with a photosensitive
    face on the inside of the glass envelope facing up."""
    # outside of the glass envelope
    outside_mesh = make.sphere(size)
    # inside of the glass envelope
    inside_mesh = make.sphere(size-glass_thickness)

    # outside solid with ice on the outside, and glass on the inside
    outside_solid = Solid(outside_mesh,glass,ice)    

    # now we need to determine the triangles which make up
    # the top face of the inside mesh, because we are going to place
    # the photosensitive surface on these triangles
    # do this by seeing which triangle centers are at the maximum z
    # coordinate
    z = inside_mesh.get_triangle_centers()[:,2]
    top = z == max(z)

    # see np.where() documentation
    # Here we make the photosensitive surface along the top face of the inside
    # mesh. The rest of the inside mesh is perfectly absorbing.
    inside_surface = r7081hqe_photocathode
    inside_color = 0x00ff00

    # construct the inside solid
    inside_solid = Solid(inside_mesh,vacuum,glass,surface=inside_surface,
                         color=inside_color)

    # you can add solids and meshes!
    return outside_solid + inside_solid

def build_detector(size=100):
    """Returns a cubic detector made of cubic photodetectors."""
    d = Detector(ice)
    glass_thickness = 10

    d.add_pmt(build_pd(size,glass_thickness),
                    displacement=(0,0,0),channel_id=1)

    world = Solid(make.box(10000,10000,10000),ice,vacuum,
                  color=0x33ffffff)
    d.add_solid(world)

    return d

