import json
from opentrons import protocol_api, types

CALIBRATION_CROSS_COORDS = {
    '1': {
        'x': 12.13,
        'y': 9.0,
        'z': 0.0
    },
    '3': {
        'x': 380.87,
        'y': 9.0,
        'z': 0.0
    },
    '7': {
        'x': 12.13,
        'y': 258.0,
        'z': 0.0
    }
}
CALIBRATION_CROSS_SLOTS = ['1', '3', '7']
TEST_LABWARE_SLOT = '2'

RATE = 0.25  # % of default speeds
SLOWER_RATE = 0.1

PIPETTE_MOUNT = 'right'
PIPETTE_NAME = 'p20_single_gen2'

TIPRACK_SLOT = '5'
TIPRACK_LOADNAME = 'opentrons_96_tiprack_20ul'

LABWARE_DEF_JSON = """{"ordering":[["A1","B1","C1","D1","E1","F1","G1","H1"],["A2","B2","C2","D2","E2","F2","G2","H2"],["A3","B3","C3","D3","E3","F3","G3","H3"],["A4","B4","C4","D4","E4","F4","G4","H4"],["A5","B5","C5","D5","E5","F5","G5","H5"],["A6","B6","C6","D6","E6","F6","G6","H6"],["A7","B7","C7","D7","E7","F7","G7","H7"],["A8","B8","C8","D8","E8","F8","G8","H8"],["A9","B9","C9","D9","E9","F9","G9","H9"],["A10","B10","C10","D10","E10","F10","G10","H10"],["A11","B11","C11","D11","E11","F11","G11","H11"],["A12","B12","C12","D12","E12","F12","G12","H12"]],"brand":{"brand":"8w_strip_tubes_on_filter_racks","brandId":["custom_HK"]},"metadata":{"displayName":"8w_strip_tubes_on_filter_racks 96 Aluminum Block 250 µL","displayCategory":"aluminumBlock","displayVolumeUnits":"µL","tags":[]},"dimensions":{"xDimension":127.75,"yDimension":85.5,"zDimension":62.49},"wells":{"A1":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":14.38,"y":74.25,"z":42.19},"B1":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":14.38,"y":65.25,"z":42.19},"C1":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":14.38,"y":56.25,"z":42.19},"D1":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":14.38,"y":47.25,"z":42.19},"E1":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":14.38,"y":38.25,"z":42.19},"F1":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":14.38,"y":29.25,"z":42.19},"G1":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":14.38,"y":20.25,"z":42.19},"H1":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":14.38,"y":11.25,"z":42.19},"A2":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":23.38,"y":74.25,"z":42.19},"B2":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":23.38,"y":65.25,"z":42.19},"C2":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":23.38,"y":56.25,"z":42.19},"D2":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":23.38,"y":47.25,"z":42.19},"E2":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":23.38,"y":38.25,"z":42.19},"F2":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":23.38,"y":29.25,"z":42.19},"G2":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":23.38,"y":20.25,"z":42.19},"H2":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":23.38,"y":11.25,"z":42.19},"A3":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":32.38,"y":74.25,"z":42.19},"B3":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":32.38,"y":65.25,"z":42.19},"C3":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":32.38,"y":56.25,"z":42.19},"D3":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":32.38,"y":47.25,"z":42.19},"E3":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":32.38,"y":38.25,"z":42.19},"F3":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":32.38,"y":29.25,"z":42.19},"G3":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":32.38,"y":20.25,"z":42.19},"H3":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":32.38,"y":11.25,"z":42.19},"A4":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":41.38,"y":74.25,"z":42.19},"B4":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":41.38,"y":65.25,"z":42.19},"C4":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":41.38,"y":56.25,"z":42.19},"D4":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":41.38,"y":47.25,"z":42.19},"E4":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":41.38,"y":38.25,"z":42.19},"F4":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":41.38,"y":29.25,"z":42.19},"G4":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":41.38,"y":20.25,"z":42.19},"H4":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":41.38,"y":11.25,"z":42.19},"A5":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":50.38,"y":74.25,"z":42.19},"B5":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":50.38,"y":65.25,"z":42.19},"C5":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":50.38,"y":56.25,"z":42.19},"D5":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":50.38,"y":47.25,"z":42.19},"E5":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":50.38,"y":38.25,"z":42.19},"F5":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":50.38,"y":29.25,"z":42.19},"G5":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":50.38,"y":20.25,"z":42.19},"H5":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":50.38,"y":11.25,"z":42.19},"A6":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":59.38,"y":74.25,"z":42.19},"B6":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":59.38,"y":65.25,"z":42.19},"C6":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":59.38,"y":56.25,"z":42.19},"D6":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":59.38,"y":47.25,"z":42.19},"E6":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":59.38,"y":38.25,"z":42.19},"F6":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":59.38,"y":29.25,"z":42.19},"G6":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":59.38,"y":20.25,"z":42.19},"H6":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":59.38,"y":11.25,"z":42.19},"A7":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":68.38,"y":74.25,"z":42.19},"B7":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":68.38,"y":65.25,"z":42.19},"C7":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":68.38,"y":56.25,"z":42.19},"D7":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":68.38,"y":47.25,"z":42.19},"E7":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":68.38,"y":38.25,"z":42.19},"F7":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":68.38,"y":29.25,"z":42.19},"G7":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":68.38,"y":20.25,"z":42.19},"H7":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":68.38,"y":11.25,"z":42.19},"A8":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":77.38,"y":74.25,"z":42.19},"B8":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":77.38,"y":65.25,"z":42.19},"C8":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":77.38,"y":56.25,"z":42.19},"D8":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":77.38,"y":47.25,"z":42.19},"E8":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":77.38,"y":38.25,"z":42.19},"F8":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":77.38,"y":29.25,"z":42.19},"G8":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":77.38,"y":20.25,"z":42.19},"H8":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":77.38,"y":11.25,"z":42.19},"A9":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":86.38,"y":74.25,"z":42.19},"B9":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":86.38,"y":65.25,"z":42.19},"C9":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":86.38,"y":56.25,"z":42.19},"D9":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":86.38,"y":47.25,"z":42.19},"E9":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":86.38,"y":38.25,"z":42.19},"F9":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":86.38,"y":29.25,"z":42.19},"G9":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":86.38,"y":20.25,"z":42.19},"H9":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":86.38,"y":11.25,"z":42.19},"A10":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":95.38,"y":74.25,"z":42.19},"B10":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":95.38,"y":65.25,"z":42.19},"C10":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":95.38,"y":56.25,"z":42.19},"D10":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":95.38,"y":47.25,"z":42.19},"E10":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":95.38,"y":38.25,"z":42.19},"F10":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":95.38,"y":29.25,"z":42.19},"G10":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":95.38,"y":20.25,"z":42.19},"H10":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":95.38,"y":11.25,"z":42.19},"A11":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":104.38,"y":74.25,"z":42.19},"B11":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":104.38,"y":65.25,"z":42.19},"C11":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":104.38,"y":56.25,"z":42.19},"D11":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":104.38,"y":47.25,"z":42.19},"E11":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":104.38,"y":38.25,"z":42.19},"F11":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":104.38,"y":29.25,"z":42.19},"G11":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":104.38,"y":20.25,"z":42.19},"H11":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":104.38,"y":11.25,"z":42.19},"A12":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":113.38,"y":74.25,"z":42.19},"B12":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":113.38,"y":65.25,"z":42.19},"C12":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":113.38,"y":56.25,"z":42.19},"D12":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":113.38,"y":47.25,"z":42.19},"E12":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":113.38,"y":38.25,"z":42.19},"F12":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":113.38,"y":29.25,"z":42.19},"G12":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":113.38,"y":20.25,"z":42.19},"H12":{"depth":20.3,"totalLiquidVolume":250,"shape":"circular","diameter":5.46,"x":113.38,"y":11.25,"z":42.19}},"groups":[{"metadata":{"wellBottomShape":"v","displayCategory":"tubeRack"},"wells":["A1","B1","C1","D1","E1","F1","G1","H1","A2","B2","C2","D2","E2","F2","G2","H2","A3","B3","C3","D3","E3","F3","G3","H3","A4","B4","C4","D4","E4","F4","G4","H4","A5","B5","C5","D5","E5","F5","G5","H5","A6","B6","C6","D6","E6","F6","G6","H6","A7","B7","C7","D7","E7","F7","G7","H7","A8","B8","C8","D8","E8","F8","G8","H8","A9","B9","C9","D9","E9","F9","G9","H9","A10","B10","C10","D10","E10","F10","G10","H10","A11","B11","C11","D11","E11","F11","G11","H11","A12","B12","C12","D12","E12","F12","G12","H12"]}],"parameters":{"format":"irregular","quirks":[],"isTiprack":false,"isMagneticModuleCompatible":false,"loadName":"8wstriptubesonfilterracks_96_aluminumblock_250ul"},"namespace":"custom_beta","version":1,"schemaVersion":2,"cornerOffsetFromSlot":{"x":0,"y":0,"z":0}}"""
LABWARE_DEF = json.loads(LABWARE_DEF_JSON)
LABWARE_LABEL = LABWARE_DEF.get('metadata', {}).get(
    'displayName', 'test labware')

metadata = {'apiLevel': '2.0'}


def uniq(l):
    res = []
    for i in l:
        if i not in res:
            res.append(i)
    return res


def run(protocol: protocol_api.ProtocolContext):
    tiprack = protocol.load_labware(TIPRACK_LOADNAME, TIPRACK_SLOT)
    pipette = protocol.load_instrument(
        PIPETTE_NAME, PIPETTE_MOUNT, tip_racks=[tiprack])

    test_labware = protocol.load_labware_from_definition(
        LABWARE_DEF,
        TEST_LABWARE_SLOT,
        LABWARE_LABEL,
    )

    num_cols = len(LABWARE_DEF.get('ordering', [[]]))
    num_rows = len(LABWARE_DEF.get('ordering', [[]])[0])
    well_locs = uniq([
        'A1',
        '{}{}'.format(chr(ord('A') + num_rows - 1), str(num_cols))])

    pipette.pick_up_tip()

    def set_speeds(rate):
        protocol.max_speeds.update({
            'X': (600 * rate),
            'Y': (400 * rate),
            'Z': (125 * rate),
            'A': (125 * rate),
        })

        speed_max = max(protocol.max_speeds.values())

        for instr in protocol.loaded_instruments.values():
            instr.default_speed = speed_max

    set_speeds(RATE)

    for slot in CALIBRATION_CROSS_SLOTS:
        coordinate = CALIBRATION_CROSS_COORDS[slot]
        location = types.Location(point=types.Point(**coordinate),
                                  labware=None)
        pipette.move_to(location)
        protocol.pause(
            f"Confirm {PIPETTE_MOUNT} pipette is at slot {slot} calibration cross")

    pipette.home()
    protocol.pause(f"Place your labware in Slot {TEST_LABWARE_SLOT}")

    for well_loc in well_locs:
        well = test_labware.well(well_loc)
        all_4_edges = [
            [well._from_center_cartesian(x=-1, y=0, z=1), 'left'],
            [well._from_center_cartesian(x=1, y=0, z=1), 'right'],
            [well._from_center_cartesian(x=0, y=-1, z=1), 'front'],
            [well._from_center_cartesian(x=0, y=1, z=1), 'back']
        ]

        set_speeds(RATE)
        pipette.move_to(well.top())
        protocol.pause("Moved to the top of the well")

        for edge_pos, edge_name in all_4_edges:
            set_speeds(SLOWER_RATE)
            edge_location = types.Location(point=edge_pos, labware=None)
            pipette.move_to(edge_location)
            protocol.pause(f'Moved to {edge_name} edge')

    # go to bottom last. (If there is more than one well, use the last well first
    # because the pipette is already at the last well at this point)
    for well_loc in reversed(well_locs):
        well = test_labware.well(well_loc)
        set_speeds(RATE)
        pipette.move_to(well.bottom())
        protocol.pause("Moved to the bottom of the well")

        pipette.blow_out(well)

    set_speeds(1.0)
    pipette.return_tip()
