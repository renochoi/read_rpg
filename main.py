#!/usr/bin/env python3
'''
Created on 25 Jun 2024

@author: Reno Choi (renochoi@korea.kr)

HISTORY:
        0.1 (25-Jun-2024): Read one day of HATPRO files and print returned keys
        0.2 (24-Nov-2026): Header added. Calls RPGReader 0.4, which reads the
                HPC relative-humidity block, HKD selection bits, the full BLB
                scan, and both IRT formats

DESCRIPTION: Example driver for modules/rpg_reader.RPGReader.
        Opens one day of RPG HATPRO binary files and prints the file code
        and the dictionary keys returned by each reader.

REFERENCE: RPG_MWR_STD_Software_Manual 2015, Appendix A (file formats).
        Readers are implemented in modules/rpg_reader.py.

'''
import os
import platform
import pandas as pd
import matplotlib.pyplot as plt
from modules.rpg_reader import RPGReader

def main():

    root_dir = os.path.dirname(os.path.abspath(__file__))

    node = platform.node()
    if node == 'Renos-MacBook-Air.local':
        rpg_dir = 'dain/Y2022/M06/D12'
    elif node == 'DESKTOP-MBL1SJO':
        rpg_dir = '/Users/reno/Downloads/icn_amos'

    # Initialize readers
    rpg = RPGReader()

    # Read lwp
    filepath = os.path.join(root_dir, rpg_dir, '220612.LWP')
    lwp_data = rpg.read_lwp(filepath)
    print('lwp_code =', lwp_data['lwp_code'])
    print('t_obs =', lwp_data['t_obs'][0:2])
    print(lwp_data.keys())
    #print(lwp_data.values())
    #print(lwp_data.items())

    # Read iwv
    filepath = os.path.join(root_dir, rpg_dir, '220612.IWV')
    iwv_data = rpg.read_iwv(filepath)
    print('iwv_code =', iwv_data['iwv_code'])
    print(iwv_data.keys())

    # Read atn
    filepath = os.path.join(root_dir, rpg_dir, '220612.ATN')
    atn_data = rpg.read_atn(filepath)
    print('atn_code =', atn_data['atn_code'])
    print(atn_data.keys())

    # Read brt
    filepath = os.path.join(root_dir, rpg_dir, '220612.BRT')
    brt_data = rpg.read_brt(filepath)
    print('brt_code =', brt_data['brt_code'])
    print(brt_data.keys())

    # Read met
    filepath = os.path.join(root_dir, rpg_dir, '220612.MET')
    met_data = rpg.read_met(filepath)
    print('met_code =', met_data['met_code'])
    print(met_data.keys())

    # Read tpc
    filepath = os.path.join(root_dir, rpg_dir, '220612.TPC')
    tpc_data = rpg.read_tpc(filepath)
    print('tpc_code =', tpc_data['tpc_code'])
    print(tpc_data.keys())

    # Read tpb
    filepath = os.path.join(root_dir, rpg_dir, '220612.TPB')
    tpb_data = rpg.read_tpb(filepath)
    print('tpb_code =', tpb_data['tpb_code'])
    print(tpb_data.keys())

    # Read hpc
    filepath = os.path.join(root_dir, rpg_dir, '220612.HPC')
    hpc_data = rpg.read_hpc(filepath)
    print('hpc_code =', hpc_data['hpc_code'])
    print(hpc_data.keys())

    '''
    # Read lpr
    filepath = os.path.join(root_dir, rpg_dir, '220612.LPR')
    lpr_data = rpg.read_lpr(filepath)
    print('lpr_code =', lpr_data['lpr_code'])
    print(lpr_data.keys())
    '''

    # Read irt
    filepath = os.path.join(root_dir, rpg_dir, '220612.IRT')
    irt_data = rpg.read_irt(filepath)
    print('irt_code =', irt_data['irt_code'])
    print(irt_data.keys())

    # Read blb
    filepath = os.path.join(root_dir, rpg_dir, '220612.BLB')
    blb_data = rpg.read_blb(filepath)
    print('blb_code =', blb_data['blb_code'])
    print(blb_data.keys())

    # Read sta
    filepath = os.path.join(root_dir, rpg_dir, '220612.STA')
    sta_data = rpg.read_sta(filepath)
    print('sta_code =', sta_data['sta_code'])
    print(sta_data.keys())

    # Read cbh
    filepath = os.path.join(root_dir, rpg_dir, '220612.CBH')
    cbh_data = rpg.read_cbh(filepath)
    print('chb_code =', cbh_data['cbh_code'])
    print(cbh_data.keys())

    # Read blh
    filepath = os.path.join(root_dir, rpg_dir, '220612.BLH')
    blh_data = rpg.read_blh(filepath)
    print('blh_code =', blh_data['blh_code'])
    print(blh_data.keys())

    # Read hkd
    filepath = os.path.join(root_dir, rpg_dir, '220612.HKD')
    hkd_data = rpg.read_hkd(filepath)
    print('hkd_code =', hkd_data['hkd_code'])
    print(hkd_data.keys())

    # Read lv0
    filepath = os.path.join(root_dir, rpg_dir, '220612.LV0')
    lv0_data = rpg.read_lv0(filepath)
    print('lv0_code =', lv0_data['lv0_code'])
    print(lv0_data.keys())
        
    '''
    # Time series plot
    plt.figure()
    filtered_data['visibility'].plot()
    plt.xlabel('Date/Time')
    plt.ylabel('Visibility')
    plt.title('Time Series Plot of Visibility')
    plt.show()
    '''

if __name__ == "__main__":
    main()
