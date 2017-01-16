#!/usr/bin/env python
# Copyright (c) 2015 Dell Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# THIS CODE IS PROVIDED ON AN *AS IS* BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT
# LIMITATION ANY IMPLIED WARRANTIES OR CONDITIONS OF TITLE, FITNESS
# FOR A PARTICULAR PURPOSE, MERCHANTABLITY OR NON-INFRINGEMENT.
#
# See the Apache Version 2.0 License for specific language governing
# permissions and limitations under the License.

import cps
import cps_utils

import nas_os_if_utils as nas_if
import nas_front_panel_map as fp
import cps_object
import event_log as ev
import time
import bytearray_utils as ba

media_type_to_str = {
    0: "Not Applicable",
    1: "Not Present",
    2: "Unknown",
    3: "Not Supported",
    4: "SFPPLUS 10GBASE USR",
    5: "SFPPLUS 10GBASE SR",
    6: "SFPPLUS 10GBASE LR",
    7: "SFPPLUS 10GBASE ER",
    8: "SFPPLUS 10GBASE ZR",
    9: "SFPPLUS 10GBASE CX4",
    10: "SFPPLUS 10GBASE LRM",
    11: "SFPPLUS 10GBASE T",
    12: "SFPPLUS 10GBASE CUHALFM",
    13: "SFPPLUS 10GBASE CU1M",
    14: "SFPPLUS 10GBASE CU2M",
    15: "SFPPLUS 10GBASE CU3M",
    16: "SFPPLUS 10GBASE CU5M",
    17: "SFPPLUS 10GBASE CU7M",
    18: "SFPPLUS 10GBASE CU10M",
    19: "SFPPLUS 10GBASE ACU7M",
    20: "SFPPLUS 10GBASE ACU10M",
    21: "SFPPLUS 10GBASE ACU15M",
    22: "SFPPLUS 10GBASE DWDM",
    23: "SFPPLUS 10GBASE DWDM 40KM",
    24: "SFPPLUS 10GBASE DWDM 80KM",
    25: "QSFP 40GBASE SR4",
    26: "QSFP 40GBASE SR4 EXT",
    27: "QSFP 40GBASE LR4",
    28: "QSFP 40GBASE LM4",
    29: "QSFP 40GBASE PSM4 LR",
    30: "QSFP 40GBASE PSM4 1490NM",
    31: "QSFP 40GBASE PSM4 1490NM 1M",
    32: "QSFP 40GBASE PSM4 1490NM 3M",
    33: "QSFP 40GBASE PSM4 1490NM 5M",
    34: "4x1 1000BASE T",
    35: "QSFP 40GBASE CR4 HALFM",
    36: "QSFP 40GBASE CR4 1M",
    37: "QSFP 40GBASE CR4 2M",
    38: "QSFP 40GBASE CR4 3M",
    39: "QSFP 40GBASE CR4 5M",
    40: "QSFP 40GBASE CR4 7M",
    41: "QSFP 40GBASE CR4 10M",
    42: "QSFP 40GBASE CR4 50M",
    43: "QSFP 40GBASE CR4",
    44: "4x10 10GBASE CR1 HALFM",
    45: "4x10 10GBASE CR1 1M",
    46: "4x10 10GBASE CR1 3M",
    47: "4x10 10GBASE CR1 5M",
    48: "4x10 10GBASE CR1 7M",
    49: "SFPPLUS FC 8GBASE SR",
    50: "SFPPLUS FC 8GBASE IR",
    51: "SFPPLUS FC 8GBASE MR",
    52: "SFPPLUS FC 8GBASE LR",
    53: "SFP SX",
    54: "SFP LX",
    55: "SFP ZX",
    56: "SFP CX",
    57: "SFP DX",
    58: "SFP T",
    59: "SFP FX",
    60: "SFP CWDM",
    61: "SFP IR1",
    62: "SFP LR1",
    63: "SFP LR2",
    64: "SFP BX10",
    65: "SFP PX",
    66: "4x10 10GBASE SR AOC XXM",
    67: "QSFP 40GBASE SM4",
    68: "QSFP 40GBASE ER4",
    69: "4x10 10GBASE CR1 2M",
    70: "SFPPLUS 10GBASE ZR TUNABLE",
    71: "QSFP28 100GBASE SR4",
    72: "QSFP28 100GBASE LR4",
    73: "QSFP28 100GBASE CWDM4",
    74: "QSFP28 100GBASE PSM4 IR",
    75: "QSFP28 100GBASE CR4",
    76: "QSFP28 100GBASE AOC",
    77: "QSFP28 100GBASE CR4 HALFM",
    78: "QSFP28 100GBASE CR4 1M",
    79: "QSFP28 100GBASE CR4 2M",
    80: "QSFP28 100GBASE CR4 3M",
    81: "QSFP28 100GBASE CR4 4M",
    82: "QSFP28 100GBASE CR4 5M",
    83: "QSFP28 100GBASE CR4 7M",
    84: "QSFP28 100GBASE CR4 10M",
    85: "QSFP28 100GBASE CR4 50M",
    86: "4X25 25GBASE CR1 HALFM",
    87: "4X25 25GBASE CR1 1M",
    88: "4X25 25GBASE CR1 2M",
    89: "4X25 25GBASE CR1 3M",
    90: "4X25 25GBASE CR1 4M",
    91: "4X25 25GBASE CR1",
    92: "2X50 50GBASE CR2 HALFM",
    93: "2X50 50GBASE CR2 1M",
    94: "2X50 50GBASE CR2 2M",
    95: "2X50 50GBASE CR2 3M",
    96: "2X50 50GBASE CR2 4M",
    97: "2X50 50GBASE CR2",
    98: "SFP28 25GBASE CR1",
    99: "SFP28 25GBASE CR1 HALFM",
    100: "SFP28 25GBASE CR1 1M",
    101: "SFP28 25GBASE CR1 2M",
    102: "SFP28 25GBASE CR1 3M",
    103: "QSFPPLUS 50GBASE CR2",
    104: "QSFPPLUS 50GBASE CR2 1M",
    105: "QSFPPLUS 50GBASE CR2 2M",
    106: "QSFPPLUS 50GBASE CR2 3M",
    107: "QSFP 40GBASE BIDI",
    108: "QSFP 40GBASE AOC",
    109: "QSFP28 100GBASE LR4 LITE",
    110: "QSFP28 100GBASE ER4",
    111: "QSFP28 100GBASE ACC",
    112: "SFP28 25GBASE SR",
    113: "SFPPLUS 10GBASE SR AOCXXM",
    114: "SFP BX10 UP",
    115: "SFP BX10 DOWN",
    116: "SFP BX40 UP",
    117: "SFP BX40 DOWN",
    118: "SFP BX80 UP",
    119: "SFP BX80 DOWN",
    120: "QSFP28 100GBASE PSM4 PIGTAIL",
    121: "QSFP28 100GBASE SWDM4",
    122: "QSFP 40GBASE PSM4 PIGTAIL",
}

cps_utils.add_attr_type('base-pas/media/port', 'uint8_t')
cps_utils.add_attr_type('base-pas/media/slot', 'uint8_t')
cps_utils.add_attr_type('base-pas/media/present', 'uint8_t')
cps_utils.add_attr_type('base-pas/media/type', 'uint32_t')

def get_media_str(media_type):
    return media_type_to_str[media_type]

def get_media_type_from_str(media_str):
    for media_type in media_type_to_str:
        if media_type_to_str[media_type] == media_str:
            return media_type
    return None



# return True is the media type is SFP. The function depends on the Media type name.
def is_media_type_SFP(media_type):
    media_str =  get_media_str(media_type)
    if media_str.find("SFP ", 0) >=0:
        return True
    else:
        return False

def get_all_media_info():
    obj = cps_object.CPSObject(module='base-pas/media', qual='observed')
    media_list = []
    cps.get([obj.get()], media_list)
    return media_list


def get_media_info(media_id):
    obj = cps_object.CPSObject(
        module='base-pas/media',
        qual='observed',
        data={'slot': 1,
              'port': media_id})
    media_list = []
    cps.get([obj.get()], media_list)
    return media_list

def get_media_channel_info(media_id):
    obj = cps_object.CPSObject(
        module='base-pas/media-channel',
        qual='observed',
        data={'slot': 1,
              'port': media_id})
    media_channel_list = []
    cps.get([obj.get()], media_channel_list)
    return media_channel_list

def get_base_media_info(media_type):
    obj = cps_object.CPSObject(
        module='base-media/media-info',
        qual='observed',
        data={'media-type': media_type})
    base_media_info_list = []
    cps.get([obj.get()], base_media_info_list)
    return base_media_info_list

def nas_set_media_type_by_phy_port(npu, phy_port, media_type):
    port = cps_object.CPSObject(
        module='base-if-phy/physical',
        data={'npu-id': npu,
              'port-id': phy_port,
              'phy-media': media_type})
    nas_if.log_info(" port id : "+str(port.get_attr_data('port-id'))+". media type: "+str(media_type))
    ch = {'operation': 'set', 'change': port.get()}
    cps.transaction([ch])


def nas_set_media_type_by_media_id(slot, media_id, media_type):
    l = []
    o = cps_object.CPSObject(
        module='base-if-phy/front-panel-port',
        data={
              'media-id': media_id})
    cps.get([o.get()], l)

    if len(l) == 0:
        nas_if.log_err("No such port found... for medial "+str(media_id))
        return

    port_list = nas_if.physical_ports_for_front_panel_port(
        cps_object.CPSObject(obj=l[0]))
    if len(port_list) == 0:
        nas_if.log_err("There are no physical ports for front panel port ")
        nas_if.log_err(l[0])
        return

    for port in port_list:
        nas_if.log_info(" port id : "+str(port.get_attr_data('port-id'))+". media type: "+str(media_type))
        port.add_attr('phy-media', media_type)
        ch = {'operation': 'set', 'change': port.get()}
        cps.transaction([ch])

def media_led_set(slot, media_id, channel, speed):
    media_channel = cps_object.CPSObject(module='base-pas/media-channel', qual='target', data=
                                         {'slot': slot, 'port': media_id, 'channel': channel, 'speed': speed})
    ch = {'operation': 'set', 'change': media_channel.get()}
    nas_if.log_info("set speed for media Id : "+str(media_id)+" channel "+str(channel)+" speed "+str(speed))
    cps.transaction([ch])

def media_transceiver_set(slot, media_id, channel, enable):
    media_channel = cps_object.CPSObject(module='base-pas/media-channel', qual='target', data=
                                         {'slot': slot, 'port': media_id, 'state': enable})
    if channel != None:
        media_channel.add_attr('channel', channel)
    ch = {'operation': 'set', 'change': media_channel.get()}
    cps.transaction([ch])

def if_media_type_set(pas_media_obj):
    try:
        media_id = pas_media_obj.get_attr_data('port')
        media_type = pas_media_obj.get_attr_data('type')
    except:
        nas_if.log_err("media Id or media type is not present in the media event")
        return
    # fetch FP info from media ID
    l = nas_if.nas_os_fp_list(d={'media-id':media_id})
    if len(l) == 0:
        nas_if.log_err("No such port found... for media  "+str(media_id))
        return

    # fetch PHY port list for the FP port
    port_list = nas_if.physical_ports_for_front_panel_port(
        cps_object.CPSObject(obj=l[0]))
    if len(port_list) == 0:
        nas_if.log_err("There are no physical ports for front panel port ")
        nas_if.log_err(l[0])
        return

    # create interface set RPC obj for each phy port in the list and send it
    for p in port_list:
        npu = p.get_attr_data('npu-id')
        port = p.get_attr_data('port-id')
        fanout = p.get_attr_data('fanout-mode')
        hwport = p.get_attr_data('hardware-port-id')

        nas_if.log_info("send if rpc for media id set for phy port "+str(port))
        ifobj = cps_object.CPSObject(module='dell-base-if-cmn/set-interface', data={
        'dell-base-if-cmn/set-interface/input/operation': 3,
        'base-if-phy/if/interfaces/interface/npu-id': npu,
        'base-if-phy/if/interfaces/interface/port-id': port,
        'base-if-phy/if/interfaces/interface/phy-media': media_type,
        'if/interfaces/interface/type':"ianaift:ethernetCsmacd"})
        ch = {'operation': 'rpc', 'change': ifobj.get()}
        cps.transaction([ch])
        if_name = ba.ba_to_str(ch['change']['data']['if/interfaces/interface/name'], len(_if_name))
        if_details = nas_if.nas_os_if_list(d={'if/interfaces/interface/name':if_name})
        enable = ba.from_ba(if_details[0]['data']['if/interfaces/interface/enabled'],"uint64_t")
        fp_details = fp.find_port_by_hwport(npu, hwport)
        if fanout == 2:  # then it is in 4x10G fanout mode BASE_PORT_BREAKOUT_MODE_BREAKOUT_4X1
            _lane = fp_details.lane
        else:    # non-fanout mode 1x40g mode
            _lane = None # enable/disable all channels. Do not pass Lane #
        media_transceiver_set(1, fp_details.media_id, _lane, enable)
    nas_if.log_info("setting media id: " + str(media_id) + " media type: " + str(media_type))

def set_media_info(pas_media_obj):
    slot = pas_media_obj.get_attr_data('slot')
    media_id = pas_media_obj.get_attr_data('port')
    media_type = pas_media_obj.get_attr_data('type')
# PAS sends slot # 1 based but for NAS slot number is 0 based
    nas_set_media_type_by_media_id((slot - 1), media_id, media_type)
    nas_if.log_info("setting media id: " + str(media_id) + " media type: " + str(media_type))


def monitor_media_event():
    handle = cps.event_connect()
    nas_if.log_info(" registering for media")
    cps.event_register(handle, cps.key_from_name('observed', 'base-pas/media'))

    while True:
        media = cps.event_wait(handle)
        obj = cps_object.CPSObject(obj=media)
        set_media_info(obj)

# TODO, it's indirect way to find if hald is ready for servicing phy port
# object set/get


def phy_port_service_wait():
    while True:
        l = nas_if.nas_os_phy_list()
        if l is not None:
            return l
        time.sleep(1)


def init_nas_media_info():

    # Wait for PHY ports service readiness
    l = phy_port_service_wait()
    media_list = get_all_media_info()
    if media_list is None:
        return None
    for media in media_list:
        obj = cps_object.CPSObject(obj=media)
        set_media_info(obj)

def led_control_get():
    media = cps_object.CPSObject(module='base-pas/media-config',qual='observed',data={'slot':1})
    l = []
    cps.get([media.get()],l)
    media_config = cps_object.CPSObject(obj=l[0])
    led_control = media_config.get_attr_data('led-control')
    return led_control

def get_default_media_setting(_media_type, def_param):
    base_media_info_list = get_base_media_info(_media_type)
    for j in base_media_info_list:
        obj = cps_object.CPSObject(obj=j)
        if def_param == 'speed':
            _def_attr = nas_if.get_cps_attr(obj,'speed')
        elif def_param == 'duplex':
            _def_attr = nas_if.get_cps_attr(obj,'duplex')
        elif def_param == 'autoneg':
            _def_attr = nas_if.get_cps_attr(obj,'autoneg')
    return _def_attr




