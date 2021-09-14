# imports
from opentrons import protocol_api

# metadata
metadata = {
    'protocolName': 'Create Pos Control Dilution Series for qPCR',
    'author': 'Harley King <harley.king@luminultra.com>',
    'description': 'Create a 12-tube pos control dilution series on a 24-well rack.',
    'apiLevel': '2.11'
}
##########################
# functions
# calculates ideal tip height for entering liquid
def tip_heights(init_vol, steps, vol_dec):
    vols = []
    heights = []
    # these values originate from Excel spreadsheet "Exp803..."
    p0=0.029502064
    p1=0.084625954
    p2=-0.000174864
    p3=2.18373E-07
    p4=-1.30599E-10
    p5=2.97839E-14
    if init_vol > 1499:
        offset = 14 # model out of range; see sheet
    else:
        offset = 7 #mm Need to add offset to ensure tip reaches below liquid level
    for i in range(steps):
        x = init_vol-vol_dec*i
        vols.append(x)
        h = p5*x**5+p4*x**4+p3*x**3+p2*x**2+p1*x**1 + p0
        h = h-offset
        if h < 8: # prevent negative heights; go to bottom to avoid air aspirant above certain height
            h = 1        
            heights.append(h)
        else:
            heights.append(round(h, 1))
    return heights

def run(protocol: protocol_api.ProtocolContext):

    # LABWARE
    fuge_rack = protocol.load_labware('vwr_24_tuberack_1500ul', '4')
    tiprack300 = protocol.load_labware('opentrons_96_filtertiprack_200ul', '8')
    tiprack20 = protocol.load_labware('opentrons_96_filtertiprack_20ul', '9')
    tempdeck = protocol.load_module('tempdeck', '10')
    stds_plate = tempdeck.load_labware('abi_96_wellplate_250ul')
    
    # PIPETTES
    p300 = protocol.load_instrument(
        'p300_single_gen2', 'left', tip_racks=[tiprack300]
    )
    p20 = protocol.load_instrument(
        'p20_single_gen2', 'right', tip_racks=[tiprack20]
    )
     
    # REAGENTS 
    std_1 = fuge_rack['A1'] # diluted standard
    std_2 = fuge_rack['A2']
    std_3 = fuge_rack['A3']
    std_4 = fuge_rack['A4']
    std_5 = fuge_rack['A5']
    std_6 = fuge_rack['A6'] 
    std_7 = fuge_rack['B1']
    std_8 = fuge_rack['B2']
    std_9 = fuge_rack['B3']
    std_10 = fuge_rack['B4']
    std_15 = fuge_rack['C3']
    std_11 = fuge_rack['B5']
    std_12 = fuge_rack['B6']
    std_13 = fuge_rack['C1']
    std_14 = fuge_rack['C2']
    # pos_control = fuge_rack['D1'] # pos control @1uM
    mmix = fuge_rack['D6'] # 1332ul
    water = fuge_rack['D5'] # 1500ul water
    
    # CALCS
    mix_per_well = 15 #how much volume (ul) mastermix should be in each well?
    overage = 0.125 # e.g. twenty percent waste as decimal
    reps = 4 #how many replicates of each std?
    multiwell_mix = mix_per_well*reps*(1+overage) # 18*4*(1+0.125) = 81
    sample_per_well = 5
    multisample_mix = sample_per_well*reps*(1+overage)
    # LISTS
    probe_wells=['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'A6', 'B6', 'C6', 'D6', 'E6', 'F6', 'G6', 'H6']
    std_wells = [std_1, std_2, std_3, std_4, std_5, std_6, std_7, std_8, std_9, std_10, std_11, std_12, std_13, std_14, std_15, water]
    # tip_heights = [26.4,25.2,24,22.8,21.5,20.1,18.7,17.3,15.9,14.5,13.1,11.6,10,8,4.4,1]
    
   
    #### COMMANDS ######
    # Mix, pipette mastermix containing probe to each well on plate 
    p300.pick_up_tip()
    p300.mix(3, 200, mmix.bottom(20)) #first height
    for well, h in zip(probe_wells, tip_heights(1584, len(std_wells), multiwell_mix)):
        p300.aspirate(multiwell_mix, mmix.bottom(h), rate=0.75) # 18 * 4 = 72 + 9 =81ul
        protocol.delay(seconds=2) #tip equilibrate
        p300.move_to(mmix.bottom(35)) # excess tip fluid condense 
        protocol.delay(seconds=2) #tip droplets slide
        p300.touch_tip(v_offset=-4) #touch 3 mm below surface
        p300.dispense(multiwell_mix, stds_plate[well])
        p300.touch_tip()
    p300.drop_tip()
    
    # add pos control stds to PROBE mmxs into plate wells and dispense into neighboring wells
    for i in range(len(std_wells)): #loop 13x, water tube last
        # p20.pick_up_tip()
        p300.pick_up_tip() #double barrel
        p20.pick_up_tip()
        # p20.distribute(
        #     multisample_mix,
        #     std_wells[i].bottom(20),
        #     stds_plate[probe_wells[i]].bottom(2),
        #     new_tip='always',
        #     touch_tip=True
        # )
        p300.aspirate(multisample_mix, std_wells[i].bottom(20)) # transer 8ul from oligo mix to mmix spot
        p300.touch_tip() 
        p300.dispense(multisample_mix, stds_plate[probe_wells[i]].bottom(2), rate=0.6) #dispense into 54ul in sybr_wells[i] on plate
        protocol.delay(seconds=2)
        # p20.mix(2, 20, stds_plate[probe_wells[i]].bottom(4)) # remove inside soln
        # p20.move_to(stds_plate[probe_wells[i]].bottom(10)) #above mmix solution
        # protocol.delay(seconds=2)
        # p300.blow_out(stds_plate[probe_wells[i]].bottom(14))
        # p300.touch_tip()
        # p300.move_to(stds_plate[probe_wells[i]].bottom(40)) # add this so it doesn't crash into plate
        p300.mix(4, 50, stds_plate[probe_wells[i]].bottom(2), rate=0.5) # can't be mixed homogenously with p20 #ivetried
        p300.move_to(stds_plate[probe_wells[i]].bottom(10)) #above mmix solution
        protocol.delay(seconds=2) #outside fluid coalesce 
        p300.blow_out(stds_plate[probe_wells[i]].bottom(12))
        p300.touch_tip()
        # transfer to adjacent wells
        for x in range(1,5): # need int 1, 2, 3 and 4.
            p20.aspirate(20, stds_plate[probe_wells[i]].bottom(2), rate=0.75) # asp from 54ul, dispense to neighbor well
            protocol.delay(seconds=2) #equilibrate
            # find digits in well, A1 and A10 and puts into list
            findNums = [int(i) for i in probe_wells[i].split()[0] if i.isdigit()]
            # joins nums from list [1, 0] -> 10 type = string
            colNum = ''.join(map(str, findNums))
            # this finds row
            row = probe_wells[i].split()[0][0]
            # put it all together into a destination well
            dest = row+str(int(colNum)+x) # row + neighbor well i.e. 1, 2
            p20.dispense(20, stds_plate[dest].bottom(2), rate=0.75)
            p20.touch_tip()
        p300.drop_tip()
        p20.drop_tip()