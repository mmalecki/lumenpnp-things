import cadquery as cq
from workplane import Workplane
from ocp_vscode import *
from settings import Settings

set_defaults(reset_camera=False)

primary_mount_w = 30
wall_t = 1.2
h = 20
staging_plate_t = 3.1
mount_d = 15.2
mount_l = mount_d + 4 * wall_t

def bin():
    e = primary_mount_w + Settings.bolt_d + 4 * wall_t
    mount_h =Settings.nut_h + 1.5 * wall_t
    b = Workplane("front").rect(e, e).extrude(h)
    b = b.faces(">Z").workplane().rect(e - 2 * wall_t, e - 2 * wall_t).cutBlind(-h + wall_t)
    b = b.faces(">Z").workplane(-mount_h - staging_plate_t).move((e + mount_l) / 2).rect(mount_l, e).extrude(mount_h)

    b = b.faces("<Z[1]").workplane(centerOption="CenterOfBoundBox").move(mount_l / 4, 0).slot2D(mount_l, e / 4).cutThruAll()
    b = b.faces("<Z[2]").workplane(centerOption="CenterOfBoundBox").center(-mount_l / 2 + mount_d, 0).rarray(1, primary_mount_w, 1, 2).nutcatchParallel(Settings.bolt)
    b = b.faces("<Z[2]").workplane(centerOption="CenterOfBoundBox").rarray(1, primary_mount_w, 1, 2).boltHole(Settings.bolt, clearance=0.2)
    b = b.faces(">Z or <Z[1]").edges("not %Circle").chamfer(wall_t / 3)
    b = b.edges("|Y").edges(">>Z[2]").edges("<<X").chamfer(mount_l / 8)
    b = b.faces("<Z or >Z[1]").chamfer(wall_t)
    return b

b = bin()
b.export("discard-bin.step")
show(b)
