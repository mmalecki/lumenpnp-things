import cadquery as cq
from workplane import Workplane
from ocp_vscode import *
from settings import Settings

set_defaults(reset_camera=False)

fit = Settings.fit
loose_fit = Settings.loose_fit
padding = 8

t = 3.2
standoff_d = 5
standoff_h = 3.6

rpi_w = 56
rpi_mount = [58, 49, ]

rpi_bolt = "M2.5"
rpi_h = 12.5
insert_d = 3.2 # CNC Kitchen M2 heatset insert
insert_h = 4

v_slot_d = Settings.v_slot_d

profile_d = 20
w = rpi_mount[0] + padding * 2 + t * 2
pi_h = rpi_mount[1] + padding * 2 + t * 2
h = pi_h + v_slot_d

def rpi_m(w):
    return w.rect(rpi_mount[0], rpi_mount[1], forConstruction=True).vertices()

def mount():
    mount = (Workplane("XZ").rect(w, h))
    mount = mount.extrude(t)

    mount.faces(">Y").workplane(centerOption="CenterOfBoundBox").tag("front").center(0, -v_slot_d / 2).tag("pi_front").end()
    mount.faces("<Y").workplane(centerOption="CenterOfBoundBox").center(0, -v_slot_d / 2).tag("pi_back").end()

    mount_h = standoff_h + rpi_h
    # v-slot mount and guard against falling elements
    mount = mount.workplaneFromTagged("front").move(0, h / 2 - v_slot_d / 2).rect(w, v_slot_d).extrude(mount_h)
    mount = mount.faces(">Y").workplane(centerOption="CenterOfBoundBox").move(0, -v_slot_d / 6).rect(w / 2, v_slot_d).cutBlind(-mount_h)
    mount = mount.rarray(w * 3/4, 1, 2, 1).cboreBoltHole(Settings.v_slot_bolt, clearance=loose_fit, cboreDepth=mount_h - t, headClearance=loose_fit * 4)

    # Save some filament.
    mount = mount.workplaneFromTagged("pi_front").polygon(6, rpi_mount[0]).cutThruAll()
    mount = mount.edges("|Y").fillet(t)

    # The actual Raspberry Pi mount
    mount = rpi_m(mount.workplaneFromTagged("pi_front")).circle(standoff_d / 2).extrude(standoff_h)

    mount = rpi_m(mount.workplaneFromTagged("pi_back")).nutcatchParallel(rpi_bolt)
    mount = rpi_m(mount.workplaneFromTagged("pi_back")).boltHole(rpi_bolt, clearance = loose_fit)
    mount = mount.faces(">Y[2]").edges("%Circle").fillet(standoff_h / 2)

    mount = mount.faces(">Y").edges().fillet(t / 2)

    return mount

m = mount()
show(m)
m.export("rpi-mount.step")
