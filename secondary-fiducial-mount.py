import cadquery as cq
from workplane import Workplane
from ocp_vscode import *
from settings import Settings

set_defaults(reset_camera=False)

primary_mount_w = 30
primary_clearance = 8.25
pcb_mount_w = 28
pcb_l = 20
wall_t = 2

bolt_hole_d = Settings.bolt_d + Settings.bolt_fit

def fiducial_mount():
    m = Workplane("front")
    slot_l = Settings.bolt_d + wall_t + primary_clearance
    slot_h = Settings.bolt_d + wall_t * 2

    sk0 = cq.Sketch().rarray(primary_mount_w, 1, 2, 1).slot(slot_l, slot_h, 90)
    sk0 = sk0.push([(-primary_mount_w / 2, -slot_l / 2), (primary_mount_w / 2, -slot_l / 2)]).circle((bolt_hole_d) / 2, mode='s')
    sk0 = sk0.reset().push([(0, (slot_l - Settings.bolt_d / 2) - pcb_l / 2 + wall_t / 2)]).rect(primary_mount_w, wall_t)

    sk1 = cq.Sketch().push([(0, (slot_l - Settings.bolt_d / 2))]).rect(primary_mount_w + 2 * wall_t + 1 * Settings.bolt_d , pcb_l)
    # Undersized hole for a bolt to get stuck in (don't want floating nuts/heatsets around components/PCBs)
    sk1 = sk1.rarray(pcb_mount_w, 1, 2, 1).circle((Settings.bolt_d - Settings.bolt_fit) / 2, mode='s')
    sk1 = sk1.reset().circle(primary_mount_w / 8, mode='s')

    m = m.placeSketch(sk0).extrude(wall_t)
    m = m.faces(">Z").workplane().placeSketch(sk1).extrude(wall_t)
    m = m.edges(">Y and |Z").chamfer(pcb_mount_w / 6)
    m = m.edges("|Z").fillet(wall_t)
    m = m.faces("(>Z or <Z)").edges("(not %Circle)").chamfer(wall_t / 4)
    m = m.faces(">Z[1]").edges(">Y").chamfer(wall_t / 4)
    return m

m = fiducial_mount()
show(m)
m.export("fiducial-mount.step")
