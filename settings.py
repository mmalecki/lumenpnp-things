import cq_queryabolt as queryabolt

class Settings:
    fit = 0.2
    loose_fit = 0.5
    v_slot_d = 20
    v_slot_bolt = "M4"
    bolt = "M3"
    bolt_d = queryabolt.boltData(bolt)['diameter']
    bolt_fit = fit
