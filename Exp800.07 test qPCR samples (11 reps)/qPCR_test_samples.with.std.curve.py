# imports
from opentrons import protocol_api

# metadata
metadata = {
    'protocolName': 'Test qPCR Samples Using Opt Fwd and Rev and Probe Concentrations',
    'author': 'Harley King <harley.king@luminultra.com>',
    'description': 'Creates a 96w plate of optimal primer and probe concentrations to qPCR samples. Also creates a std curve.',
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

def tip_heightsEpp(init_vol, steps, vol_dec):
    vols = []
    heights = []
    # these values originate from Excel spreadsheet "Exp803..."
    p0=-0.272820744
    p1=0.019767959
    p2=2.00442E-06
    p3=-8.99691E-09
    p4=6.72776E-12
    p5=-1.55428E-15
    if init_vol > 2000:
        offset = 12 # model out of range; see sheet
    else:
        offset = 11 #mm Need to add offset to ensure tip reaches below liquid level
    for i in range(steps):
        x = init_vol-vol_dec*i
        vols.append(x)
        h = p5*x**5+p4*x**4+p3*x**3+p2*x**2+p1*x**1 + p0
        h = h-offset
        if h < 8: # prevent negative heights; go to bottom to avoid air aspirant above certain height
            h = 0        
            heights.append(h)
        else:
            heights.append(round(h, 1))
    return heights

# splits aspiration volume into equal parts 
# returns list with equal volumes
def split_asp(tot, max_vol):
    n =1
    if tot/n > max_vol: # if total greater than max
       while tot/n > max_vol: # increment n until some tot/n < max_vol
            n+=1
            if tot/n == max_vol: # if tot evently divided e.g. 1000
                subvol = tot/n
                return [subvol]*n
            if tot/(n+1) < max_vol: # if tot <> evenly divided e.g. 417.3
                subvol = tot/(n+1)
                return [subvol]*(n+1) # return # aspiration steps
    else: # if total less than max
        return [tot/n]

def run(protocol: protocol_api.ProtocolContext):

    # LABWARE
    fuge_rack = protocol.load_labware('vwr_24_tuberack_1500ul', '1')
    stds_rack = protocol.load_labware('vwr_24_tuberack_1500ul', '2')
    tiprack300 = protocol.load_labware('opentrons_96_filtertiprack_200ul', '8')
    tiprack20 = protocol.load_labware('opentrons_96_filtertiprack_20ul', '9')
    tempdeck = protocol.load_module('tempdeck', '10')
    # plate = tempdeck.load_labware('amplifyt_96_aluminumblock_300ul')
    plate = tempdeck.load_labware('abi_96_wellplate_250ul')

    # PIPETTES
    p300 = protocol.load_instrument(
        'p300_single_gen2', 'left', tip_racks=[tiprack300]
    )
    p20 = protocol.load_instrument(
        'p20_single_gen2', 'right', tip_racks=[tiprack20]
    )
     
    # REAGENTS
    # sds_rack
    
    std_1 = stds_rack['A1'] # 990ul WATER
    std_2 = stds_rack['A2'] # 900ul WATER
    std_3 = stds_rack['A3'] # 900ul WATER
    std_4 = stds_rack['A4'] # 900ul WATER
    std_5 = stds_rack['A5'] # 900ul WATER
    std_6 = stds_rack['A6'] # 900ul WATER 
    std_7 = stds_rack['B1'] # 900ul WATER
    std_8 = stds_rack['B2'] # 900ul WATER
    std_9 = stds_rack['B3'] # 900ul WATER
    std_10 = stds_rack['B4'] # 900ul WATER
    std_11= stds_rack['B5'] # 900ul WATER
    std_12 = stds_rack['B6'] # 900ul WATER
    std_13 = stds_rack['C1'] # 900ul WATER
    std_14 = stds_rack['C2'] # 900ul WATER
    std_15 = stds_rack['D2'] # 900ul WATER


    std_1mix = stds_rack['C3'] # empty
    std_2mix = stds_rack['C4'] # empty
    std_3mix = stds_rack['C5'] # empty
    std_4mix = stds_rack['C6'] # empty
    std_5mix = stds_rack['D3'] # empty
    std_6mix = stds_rack['D4'] # empty
    std_7mix = stds_rack['D5'] # empty
    NTC_mix = stds_rack['D6'] # empty, receives sN_mix and WATER as NTC
    
    #fuge_rack
    MIX_master = fuge_rack['D1'] # see sheet, but ~2075
    WATER = fuge_rack['A1'] # 1500ul WATER
   
   # user-prepared samples can be placed here.
    samp_1 = fuge_rack['B1'] # e.g. 0.625uM # empty
    samp_2 = fuge_rack['B2'] # e.g. 1.25uM # empty
    samp_3 = fuge_rack['B3'] # e.g. 2.5uM # empty
    samp_4 = fuge_rack['B4'] # e.g. 5.0uM # empty
    samp_5 = fuge_rack['B5'] # e.g. 7.5uM # empty
    samp_6 = fuge_rack['B6'] # e.g. 10uM # empty
    
    # user inputs
    p300_max_vol = 200
    mix_master_tot = 96*18*1.2 # total vol of mastermix
    mmix_XFR_std_mix = 3*18*1.14 # transfer this amount to the std mix intermediate tubes that will receive DNA
    std_dna_XFR_to_std_int=3*2*1.14	#transfer this amount DNA to std_int_tubes to mix and aliquot to 3 wells
    mmix_XFR_samp_wells = 18*12*1.1 # how much mastermix transferred as bolus to well A1, B1..F1 to receive DNA
    samp_dna_XFR_to_wells = 2*12*1.1 # 26.4 2ul in 12 wells + excess
    
    # lists
    # the DNA from these tubes will be used to create a std curve    
    std_tubes = [std_3, std_4, std_5, std_6, std_7, std_8, std_9, WATER] 
    # this tube numbering is for OT-2. DNA is added to these tubes, mixed and aliquoted to plate
    std_mixes = [std_1mix, std_2mix, std_3mix, std_4mix, std_5mix, std_6mix, std_7mix, NTC_mix]
    # the location of the std wells
    std_wells = ['G1', 'G4', 'G7', 'G10', 'H1', 'H4', 'H7', 'H10']
    # the location of the std wells. Mastermix added here.
    samp_wells = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1']
    # from which tubes should OT2 draw for 11 replicates. Can be std tubes for LOD...
    samp_sources = [std_8, std_9, std_10, std_11, std_12, std_13]
    # or can be from user processed tubes. 
    # samp_sources = [samp_1, samp_2, samp_3, samp_4, samp_5, samp_6]
    
    
    # ### COMMANDS ######
    # Mastermix contains primers and probe. Everything except DNA. Aliquot to 6 tubes.
    # transfer sN_mix to intermediate tubes (std_mixes)
    p300.pick_up_tip()
    p300.flow_rate.aspirate = 92.86 #default
    p300.flow_rate.dispense = 92.86 #default
    mmix_h = tip_heightsEpp(mix_master_tot, len(std_mixes), mmix_XFR_std_mix)
    # print ("mix_master_tot", mix_master_tot)
    # print (len(std_mixes))
    # print (mmix_XFR_std_mix)
    # print ("mmix_h", mmix_h)
    p300.mix(6, 200, MIX_master.bottom(mmix_h[0])) # top tip height
    p300.flow_rate.aspirate = 30
    p300.flow_rate.dispense = 40
    # p300.well_bottom_clearance.aspirate = std_mix_heights[0] #mm 
    for i, tube in enumerate(std_mixes):
        # p300.well_bottom_clearance.aspirate = h #mm
        p300.aspirate(mmix_XFR_std_mix, MIX_master.bottom(mmix_h[i])) # 18 * 3 * 1.12-0.05= 54 + 6 =60ul
        protocol.delay(seconds=2) #tip equilibrate
        p300.move_to(MIX_master.bottom(35)) # excess tip fluid condense 
        protocol.delay(seconds=3) #tip droplets slide
        p300.touch_tip(v_offset=-2)
        p300.dispense(mmix_XFR_std_mix, tube.bottom(4))
        p300.blow_out(tube.bottom(8))
    p300.drop_tip()
    p300.flow_rate.aspirate = 92.86 #reset to default
    p300.flow_rate.dispense = 92.86 #reset to default
   
    # transfer std DNA into intermediate std_mixes tubes and then to plate
    for std, intTube, well in zip(std_tubes, std_mixes, std_wells):
        p20.pick_up_tip()
        p300.pick_up_tip()
        p20.flow_rate.aspirate = 4
        p20.flow_rate.dispense = 4
        p20.aspirate(std_dna_XFR_to_std_int, std) #aspirate from std_1 into std_mix (intermediate tube) e.g. 6.42 ul
        protocol.delay(seconds=2) #equilibrate
        p20.touch_tip()
        p20.dispense(std_dna_XFR_to_std_int, intTube)
        # p20.move_to(intTube.bottom(3))
        p20.flow_rate.aspirate = 7.56
        p20.flow_rate.dispense = 7.56
        p20.mix(2, 20, intTube.bottom(3)) #ensure vol in tip in intTube and washed
        p20.blow_out()
        p300.move_to(intTube.bottom(40)) #prevent tip from crashing into tube cap
        p300.mix(7, 50, intTube.bottom(3))
        protocol.delay(seconds=2)
        # p300.move_to(intTube.bottom(10)) #prevent air bubbles in mmix during blow out
        p300.blow_out(intTube.bottom(10))
        p20.move_to(intTube.bottom(40))
        p20.flow_rate.aspirate = 4
        p20.flow_rate.dispense = 4
        for x in range(0,3): # need int 1, 2, and 3
            p20.aspirate(20, intTube.bottom(2)) 
            protocol.delay(seconds=2) #equilibrate
            # find digits in well, G1 and G10 and puts into list
            findNums = [int(i) for i in well.split()[0] if i.isdigit()]
            # joins nums from list [1, 0] -> 10 type = string
            colNum = ''.join(map(str, findNums))
            # this finds row
            row = well.split()[0][0]
            dest = row+str(int(colNum)+x) # row + neighbor well i.e. 1, 2
            p20.dispense(20, plate[dest].bottom(2))
            protocol.delay(seconds=2)
            p20.move_to(plate[dest].bottom(6))
            p20.blow_out()
            # p20.touch_tip()
        p300.drop_tip()
        p20.drop_tip()
    p20.flow_rate.aspirate = 7.56
    p20.flow_rate.dispense = 7.56

    # transfer mastermix bolus to beginning wells to receive sample
    samp_h = tip_heightsEpp(mix_master_tot-mmix_XFR_std_mix, len(samp_wells), mmix_XFR_samp_wells)
    p300.pick_up_tip()
    for i, well in enumerate(samp_wells):
        vols = split_asp(mmix_XFR_samp_wells, p300_max_vol) #split 237.60 into 2 asp steps
        for j, vol in enumerate(vols): # loop through each vol
            p300.flow_rate.aspirate = 40 #default
            p300.flow_rate.dispense = 40 #default
            p300.aspirate(vol, MIX_master.bottom(samp_h[i]))
            protocol.delay(seconds=2)
            p300.dispense(vol, plate[well].bottom(4*j+5))
            protocol.delay(seconds=1)
            p300.blow_out(plate[well].bottom(14))
            p300.touch_tip()
    p300.drop_tip()

    # add dna to first wells, mix, and aliquot to neighbors
    # six samples, can be changed in the user inputs
    for i, (sample, well) in enumerate(zip(samp_sources, samp_wells)):
        p300.pick_up_tip()
        p20.pick_up_tip()
        p300.flow_rate.aspirate = 92.86 
        p300.flow_rate.dispense = 92.86
        p300.mix(3, 200, sample) # mix the sample
        p300.flow_rate.aspirate = 30
        p300.flow_rate.dispense = 40
        p300.aspirate(samp_dna_XFR_to_wells, sample.bottom(2)) # sample vol may vary. Goto bottom.
        p300.move_to(sample.bottom(25)) # relieve pressure if tip at bottom
        protocol.delay(seconds=2)
        p300.touch_tip()
        p300.dispense(samp_dna_XFR_to_wells, plate[well].bottom(3))
        p300.flow_rate.aspirate = 92.86 
        p300.flow_rate.dispense = 92.86
        p300.mix(3, 200, plate[well].bottom(5)) # vol = 26.4 + 237.6 = 264
        p300.flow_rate.aspirate = 30 
        p300.flow_rate.dispense = 40
        p300.mix(1, 200, plate[well].bottom(3))
        p300.move_to(plate[well].bottom(14))
        protocol.delay(seconds=2)
        p300.blow_out(plate[well].bottom(16))
        p300.touch_tip()
        for x in range(1,12): # need int 1, 2, and 12
            # find digits in well, G1 and G10 and puts into list
            findNums = [int(d) for d in well.split()[0] if d.isdigit()]
            # joins nums from list [1, 0] -> 10 type = string
            colNum = ''.join(map(str, findNums))
            # this finds row
            row = well.split()[0][0]
            dest = row+str(int(colNum)+x) # row + neighbor well i.e. 1, 2
            p20.flow_rate.aspirate = 7.56
            p20.flow_rate.dispense = 7.56
            p20.aspirate(20, plate[well].bottom(2))
            protocol.delay(seconds=2) #equilibrate
            p20.move_to(plate[well].bottom(16)) 
            protocol.delay(seconds=2) #droplets coalescing
            p20.touch_tip()
            p20.dispense(20, plate[dest].bottom(2))
            protocol.delay(seconds=2)
            # p20.move_to(plate[dest].bottom(4))
            p20.blow_out(plate[dest].bottom(6))
        p20.drop_tip()
        p300.drop_tip()