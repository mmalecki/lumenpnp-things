import cq_queryabolt as queryabolt
import cadquery as cq

wallT = 2.4
looseFit = 0.5
fit = 0.2

bolt = "M4"


extD = 20
caseFit = looseFit
extSpacing = 20
caseL = 130
caseH = 20.5
caseHoldW = 20
caseHoldL = caseL + 1 * wallT
caseInset = extD / 4

usbClearance = 3
usbSideClearance = 8

l = caseHoldL + extD + wallT - caseInset

class Workplane(queryabolt.WorkplaneMixin, cq.Workplane):
    pass

def mount():
    # Extrude the main holding feature
    m = Workplane("YZ").rect(caseHoldW, caseH + 2 * wallT + caseFit).extrude(l)

    # Cut into it for case clearance
    m = m.faces(">Y").workplane(centerOption="CenterOfBoundBox").tag("cutout").move(-extD / 2 + caseInset / 2, 0).rect(caseL + caseFit, caseH + caseFit).cutBlind(-caseHoldW + wallT)
    # And USB port clearance...
    m = m.workplaneFromTagged("cutout").move(-extD / 2 + caseInset / 2, 0).rect(caseL - 2 * wallT - 2 * usbSideClearance, caseH - 2 * usbClearance).cutBlind(-caseHoldW)

    # Put a little space between us and the extrusion we're holding onto
    m = m.faces(">Z").workplane(centerOption="CenterOfBoundBox").move(-l / 2 + extD / 2, 0).rect(caseHoldW, extD).extrude(extSpacing - caseFit / 2)

    # And get us something to hold on with
    h = caseH + 2 * wallT + extD + extSpacing
    m = m.faces("<Z").workplane(centerOption="CenterOfBoundBox").move(-l / 2 + extD / 2, 0).cboreBoltHole(bolt, clearance = fit, cboreDepth=h/2 + wallT)

    # Chamfers, fillets, etc.
    m = m.faces("<Z").edges("<X").fillet(extD / 4)
    m = m.faces("<Z[2]").edges("<X").fillet(extSpacing / 2)
    m = m.faces(">Y[1]").edges("|X or |Z").fillet(wallT / 2)
    m = m.faces(">Y").chamfer(wallT / 3)
    m = m.faces("<Y").chamfer(wallT / 3)
    m = (m.edges("<<Y[3]").fillet(wallT/ 3))
    return m

show_object(mount(), name="mount")
