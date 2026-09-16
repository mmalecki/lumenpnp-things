import cadquery as cq
from workplane import Workplane
from ocp_vscode import *
from settings import Settings

set_defaults(reset_camera=False)

primary_mount_w = 30
pcb_l = 20
pcb_t = 1.7
pcb_w = 30
wall_t = 1.2
h = 5.75
fit = 0.15
outset = 1

bolt_hole_d = Settings.bolt_d + Settings.bolt_fit

def fiducial_mount():
    w = pcb_w + Settings.bolt_d + 6 * wall_t
    l = pcb_l + wall_t
    m = Workplane("front").rect(l, w).extrude(h + pcb_t * 1.5)
    m = m.edges("|Z").chamfer(w / 5)
    m = m.faces(">Z").workplane().move(wall_t / 2, 0).rect(pcb_l + fit, pcb_w - outset).cutBlind(-pcb_t / 2)
    m = m.faces(">Z").workplane(-pcb_t / 2).move(wall_t / 2, 0).rect(pcb_l + fit, pcb_w + fit).cutBlind(-pcb_t)
    m = m.faces("<Z").workplane().rect(l, w / 4).cutBlind(-3.2)
    m = m.faces(">Z").workplane().center(wall_t / 2, 0).rarray(1, primary_mount_w, 1, 2).boltHole("M3", clearance=0.2)
    m = m.edges("|X").edges("<<Z[1]").chamfer(outset / 4)
    m = m.edges("|X").edges(">>Z[1]").chamfer(w / 16)
    m = m.faces("(>Z or <Z)").edges("(not %Circle)").chamfer(wall_t / 4)
    m = m.edges("|Z").chamfer(wall_t / 4)
    return m

m = fiducial_mount()
show(m)
m.export("fiducial-mount.step")
m.export("fiducial-mount.stl")
