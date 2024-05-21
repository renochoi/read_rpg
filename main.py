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
    print('lwp_n =', lwp_data['lwp_n'])
    print('t_obs =', lwp_data['t_obs'][0:2])
    print(lwp_data.keys())
    #print(lwp_data.values())
    #print(lwp_data.items())

    # Read iwv
    filepath = os.path.join(root_dir, rpg_dir, '220612.IWV')
    iwv_data = rpg.read_iwv(filepath)
    print('iwv_n =', iwv_data['iwv_n'])
    print(iwv_data.keys())

    # Read atn
    filepath = os.path.join(root_dir, rpg_dir, '220612.ATN')
    atn_data = rpg.read_atn(filepath)
    print('atn_n =', atn_data['atn_n'])
    print(atn_data.keys())

    # Read brt
    filepath = os.path.join(root_dir, rpg_dir, '220612.BRT')
    brt_data = rpg.read_brt(filepath)
    print('brt_n =', brt_data['brt_n'])
    print(brt_data.keys())

    # Read met
    filepath = os.path.join(root_dir, rpg_dir, '220612.MET')
    met_data = rpg.read_met(filepath)
    print('met_n =', met_data['met_n'])
    print(met_data.keys())

    # Read tpc
    filepath = os.path.join(root_dir, rpg_dir, '220612.TPC')
    tpc_data = rpg.read_tpc(filepath)
    print('tpc_n =', tpc_data['tpc_n'])
    print(tpc_data.keys())

    # Read tpb
    filepath = os.path.join(root_dir, rpg_dir, '220612.TPB')
    tpb_data = rpg.read_tpb(filepath)
    print('tpb_n =', tpb_data['tpb_n'])
    print(tpb_data.keys())

    # Read hpc
    filepath = os.path.join(root_dir, rpg_dir, '220612.HPC')
    hpc_data = rpg.read_hpc(filepath)
    print('hpc_n =', hpc_data['hpc_n'])
    print(hpc_data.keys())

    '''
    # Read lpr
    filepath = os.path.join(root_dir, rpg_dir, '220612.LPR')
    lpr_data = rpg.read_lpr(filepath)
    print('lpr_n =', lpr_data['lpr_n'])
    print(lpr_data.keys())
    '''

    # Read irt
    filepath = os.path.join(root_dir, rpg_dir, '220612.IRT')
    irt_data = rpg.read_irt(filepath)
    print('irt_n =', irt_data['irt_n'])
    print(irt_data.keys())

    # Read blb
    filepath = os.path.join(root_dir, rpg_dir, '220612.BLB')
    blb_data = rpg.read_blb(filepath)
    print('blb_n =', blb_data['blb_n'])
    print(blb_data.keys())

    # Read sta
    filepath = os.path.join(root_dir, rpg_dir, '220612.STA')
    sta_data = rpg.read_sta(filepath)
    print('sta_n =', sta_data['sta_n'])
    print(sta_data.keys())

    # Read cbh
    filepath = os.path.join(root_dir, rpg_dir, '220612.CBH')
    cbh_data = rpg.read_cbh(filepath)
    print('chb_n =', cbh_data['cbh_n'])
    print(cbh_data.keys())

    # Read blh
    filepath = os.path.join(root_dir, rpg_dir, '220612.BLH')
    blh_data = rpg.read_blh(filepath)
    print('blh_n =', blh_data['blh_n'])
    print(blh_data.keys())

    # Read hkd
    filepath = os.path.join(root_dir, rpg_dir, '220612.HKD')
    hkd_data = rpg.read_hkd(filepath)
    print('hkd_n =', hkd_data['hkd_n'])
    print(hkd_data.keys())

    # Read lv0
    filepath = os.path.join(root_dir, rpg_dir, '220612.LV0')
    lv0_data = rpg.read_lv0(filepath)
    print('lv0_n =', lv0_data['lv0_n'])
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
