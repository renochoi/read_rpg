#!/usr/bin/env python3
'''
Created on 8 Sep 2018

@author: Reno Choi (renochoi@korea.kr)

HISTORY: 
        0.1 (08-Sep-2018): HKD, BRT, TPC, HPC, IRT functions
        0.2 (04-Apr-2020): LWP, IWV, MET, TPB, ATN functions
        0.3 (11-Nov-2020): LPR, BLB, STA, CBH, BLH, VLT, ABSCAL.HIS, LV0 functions

DESCRIPTION: Read all Levels of RPG HATPRO data file.
        A1: LWP-Files (*.LWP), Liquid Water Path
        A2: IWV-Files (*.IWV), Integrated Water Vapour
        A3: ATN-Files (*.ATN), Atmospheric Attenuation
        A4: BRT-Files (*.BRT), Brightness Temperature
        A5b: MET-Files (*.MET), Meteorological Sensors (new version)
        A6: (Unavailable) OLC-Files (*.OLC), Oxygen Line Chart
        A7: TPC-Files (*.TPC), Temperature Profile Chart (Full Trop.)
        A8: TPB-Files (*.TPB), Temperature Profile Chart (Boundary Layer)
        A9: (Unavailable) WVL-Files (*.WVL), Water Vapour Line Chart
        A10(1): HPC-Files (*.HPC), Humidity Profile Chart (without RH)
        A10(2): (Unavailable) HPC-Files (*.HPC), Humidity Profile Chart (including RH)
        A11: LPR-Files (*.LPR), Liquid Water Profile Chart
        A12b: IRT-Files (*.IRT), Infrared Radiometer Temperatures (new)
        A13b: BLB-Files (*.BLB), Boundary Layer BT Profiles (new)
        A14: STA-Files (*.STA), Stability Indices
        A15b: (Unavailable) Structure of Calibration Log-File (CAL.LOG), new version
        A16: CBH-Files (*.CBH), Cloud Base Height
        A17: BLH-Files (*.BLH), Boundary Layer Height
        A18b: VLT-Files (*.VLT), Channel Voltage File (new version)
        A19: HKD-Files (*.HKD), Housekeeping Data File
        A20: ABSCAL.HIS, Absolute Calibration History File
        A21b: LV0-Files (*.LV0), Level Zero (Detector Voltages) Files (new)
        A22: (Unavailable) TRK-Files (*.TRK), Satellite Tracking File
        A23: (Unavailable) BUFR (Version 3.0) File Format

REFERENCE: Read all Levels of RPG HATPRO data file.

'''
import os, re, sys
import numpy as np
from datetime import datetime, timedelta
import struct

class RPGReader:
    '''
    def __init__(self,f,*args):
        self.raw_file = raw_file
        self.feather_dir = feather_dir
        if prefix is None: self.prefix = 'icn_metar'
    '''

    #
    # A1: LWP: Liquid Water Path (p.133, RPG_MWR_STD_Software_Manual 2015)
    #
    def read_lwp(self,f,*args):

        if not f: print("Missing argument FN, Please provide input filename.")
        if not os.path.isfile(f): 
            print('Input file is nonexists. Returnning...')

        root = os.path.dirname(f)
        file = os.path.basename(f)

        t_ref = datetime.strptime('20010101000000', "%Y%m%d%H%M%S")
        t_obs = []
        lwp_dat = []
        lwp_ang = []
        with open(f, "rb") as f:
            lwp_code      = struct.unpack('<I', f.read(4))[0]
            lwp_n         = struct.unpack('<I', f.read(4))[0]
            lwp_min       = struct.unpack('<f', f.read(4))[0]
            lwp_max       = struct.unpack('<f', f.read(4))[0]
            lwp_timeref   = struct.unpack('<I', f.read(4))[0]
            # brt_timeref = 1 : UTC
            # brt_timeref = 0 : LST
            lwp_retrieval = struct.unpack('<I', f.read(4))[0]
            # lwp_retrieval = 0 : Linear regression
            # lwp_retrieval = 1 : Cubic-spline regression
            # lwp_retrieval = 2 : Neural Network
            for i in range(lwp_n):
                t = struct.unpack('<i', f.read(4))[0]
                t_obs.append( t_ref + timedelta(seconds=t) )
                rf = f.read(1) # Dummy
                tmp = []
                lwp_dat.append( struct.unpack('<f', f.read(4))[0] )
                lwp_ang.append( struct.unpack('<f', f.read(4))[0] )
        f.close()

        return {'lwp_code': lwp_code,
                'lwp_n': lwp_n,
                'lwp_min': lwp_min,
                'lwp_max': lwp_max,
                'lwp_timeref': lwp_timeref,
                'lwp_retrieval': lwp_retrieval,
                't_obs': t_obs,
                'lwp_dat': lwp_dat,
                'lwp_ang': lwp_ang}

    #
    # A2: IWV: Integrated Water Vapour (p.133, RPG_MWR_STD_Software_Manual 2015)
    #
    def read_iwv(self,f,*args):

        if not f: print("Missing argument FN, Please provide input filename.")
        if not os.path.isfile(f): 
            print('Input file is nonexists. Returnning...')

        root = os.path.dirname(f)
        file = os.path.basename(f)

        t_ref = datetime.strptime('20010101000000', "%Y%m%d%H%M%S")
        t_obs = []
        iwv_dat = []
        iwv_ang = []
        with open(f, "rb") as f:
            iwv_code      = struct.unpack('<I', f.read(4))[0]
            iwv_n         = struct.unpack('<I', f.read(4))[0]
            iwv_min       = struct.unpack('<f', f.read(4))[0]
            iwv_max       = struct.unpack('<f', f.read(4))[0]
            iwv_timeref   = struct.unpack('<I', f.read(4))[0]
            # iwv_timeref = 1 : UTC
            # iwv_timeref = 0 : LST
            iwv_retrieval = struct.unpack('<I', f.read(4))[0]
            # iwv_retrieval = 0 : Linear regression
            # iwv_retrieval = 1 : Cubic-spline regression
            # iwv_retrieval = 2 : Neural Network
            for i in range(iwv_n):
                t = struct.unpack('<i', f.read(4))[0]
                t_obs.append( t_ref + timedelta(seconds=t) )
                rf = f.read(1) # Dummy
                tmp = []
                iwv_dat.append( struct.unpack('<f', f.read(4))[0] )
                iwv_ang.append( struct.unpack('<f', f.read(4))[0] )
        f.close()

        return {'iwv_code': iwv_code,
                'iwv_n': iwv_n,
                'iwv_min': iwv_min,
                'iwv_max': iwv_max,
                'iwv_timeref': iwv_timeref,
                'iwv_retrieval': iwv_retrieval,
                't_obs': t_obs,
                'iwv_dat': iwv_dat,
                'iwv_ang': iwv_ang}

    #
    # A3: ATN: Atmospheric Attenuation (p.134, RPG_MWR_STD_Software_Manual 2015)
    #
    def read_atn(self,f,*args):

        if not f: print("Missing argument FN, Please provide input filename.")
        if not os.path.isfile(f): 
            print('Input file is nonexists. Returnning...')

        root = os.path.dirname(f)
        file = os.path.basename(f)

        t_ref = datetime.strptime('20010101000000', "%Y%m%d%H%M%S")
        t_obs = []
        atn_freq = []
        atn_min = []
        atn_max = []
        atn_t = []
        atn_rain = []
        atn_dat = []
        atn_elv = []

        with open(f, "rb") as f:
            atn_code      = struct.unpack('<i', f.read(4))[0]
            atn_n         = struct.unpack('<i', f.read(4))[0]
            atn_timeref   = struct.unpack('<i', f.read(4))[0]
            atn_retrieval = struct.unpack('<i', f.read(4))[0]
            atn_freqn     = struct.unpack('<i', f.read(4))[0]
            for vname in range(atn_freqn):
                atn_freq.append(struct.unpack('<f', f.read(4))[0] )
            for vname in range(atn_freqn):
                atn_min.append(struct.unpack('<f', f.read(4))[0] )
            for vname in range(atn_freqn):
                atn_max.append(struct.unpack('<f', f.read(4))[0] )
            for i in range(atn_n):
                t = struct.unpack('<i', f.read(4))[0]
                atn_t.append( t_ref + timedelta(seconds=t) )
                atn_rain.append(struct.unpack('<c', f.read(1))[0] )
                tmp = []
                for vname in range(atn_freqn):
                    tmp.append(struct.unpack('<f', f.read(4))[0] )
                if i == 0: atn_dat = np.c_[tmp]
                else:      atn_dat = np.c_[atn_dat, tmp]
                atn_elv.append(struct.unpack('<f', f.read(4))[0] )

        f.close()

        return {'atn_code': atn_code,           #LV0-File Code (=111112)
                'atn_n': atn_n,                 #Number of samples
                'atn_timeref': atn_timeref,                 #Number of samples
                'atn_retrieval': atn_retrieval,                 #Number of samples
                'atn_freqn': atn_freqn,                 #Number of samples
                'atn_freq': atn_freq,                 #Number of samples
                'atn_min': atn_min,                 #Number of samples
                'atn_max': atn_max,                 #Number of samples
                'atn_t': atn_t,                 #Number of samples
                'atn_rain': atn_rain,                 #Number of samples
                'atn_dat': atn_dat,                 #Number of samples
                'atn_elv': atn_elv}                 #Number of samples

    #
    # A4: BRT: Brightness Temperature (p.135, RPG_MWR_STD_Software_Manual 2015)
    #
    def read_brt(self,f,*args):

        if not f: print("Missing argument FN, Please provide input filename.")
        if not os.path.isfile(f): 
            print('Input file is nonexists. Returnning...')

        root = os.path.dirname(f)
        file = os.path.basename(f)

        brt_freq = []
        brt_min = []
        brt_max = []
        t_ref = datetime.strptime('20010101000000', "%Y%m%d%H%M%S")
        t_obs = []
        brt_ang = []
        with open(f, "rb") as f:
            brt_code    = struct.unpack('<I', f.read(4))[0]
            brt_n       = struct.unpack('<I', f.read(4))[0]
            brt_timeref = struct.unpack('<I', f.read(4))[0]
            # brt_timeref = 1 : UTC
            # brt_timeref = 0 : LST
            brt_freqn = struct.unpack('<I', f.read(4))[0]
            for vname in range(brt_freqn):
                brt_freq.append(struct.unpack('<f', f.read(4))[0] )
            for vname in range(brt_freqn):
                brt_min.append( struct.unpack('<f', f.read(4))[0] )
            for vname in range(brt_freqn):
                brt_max.append( struct.unpack('<f', f.read(4))[0] )
            for i in range(brt_n):
                t = struct.unpack('<i', f.read(4))[0]
                t_obs.append( t_ref + timedelta(seconds=t) )
                rf = f.read(1) # Dummy
                tmp = []
                for j in range(brt_freqn): 
                    tmp.append( struct.unpack('<f', f.read(4))[0])
                if i == 0: brt_dat = np.c_[tmp]
                else:      brt_dat = np.c_[brt_dat, tmp]
                brt_ang.append( struct.unpack('<f', f.read(4))[0])
        f.close()

        return {'brt_code': brt_code,
                'brt_n': brt_n,
                'brt timeref': brt_timeref,
                'brt_freqn': brt_freqn,
                'brt_freq': brt_freq,
                'brt_min': brt_min,
                'brt_max': brt_max,
                't_obs': t_obs,
                'brt_dat': brt_dat,
                'brt_ang': brt_ang}

    #
    # A5: MET: Meteorological Sensors (p.135, RPG_MWR_STD_Software_Manual 2015)
    #
    def read_met(self,f,*args):

        if not f: print("Missing argument FN, Please provide input filename.")
        if not os.path.isfile(f): 
            print('Input file is nonexists. Returnning...')

        root = os.path.dirname(f)
        file = os.path.basename(f)

        t_ref = datetime.strptime('20010101000000', "%Y%m%d%H%M%S")
        t_obs = []
        met_rain = [] # Binary [1 or 0]
        met_dat1 = [] # Pressure [hPa]
        met_dat2 = [] # Temperature [K]
        met_dat3 = [] # RH% [%]
        # For STRUC.UNPACK, visit 
        #https://docs.python.org/3/library/struct.html#struct-format-strings
        with open(f, "rb") as f:
            met_code    = struct.unpack('<I', f.read(4))[0]
            met_n       = struct.unpack('<I', f.read(4))[0]
            # For old version
            if (met_code == 599658943):
                met_nsen = 0
            else:
                met_nsen = struct.unpack('<c', f.read(1))[0]
            #rf = f.read(1) # Dummy
            #print( int.from_bytes(rf, byteorder='little') )
            #print( bin(int.from_bytes(rf, byteorder='little'))[2:] )
            #met_nsen.append( bin(int.from_bytes(rf, byteorder='little'))[2:] )
            met_minp    = struct.unpack('=f', f.read(4))[0]
            met_maxp    = struct.unpack('<f', f.read(4))[0]
            met_mint    = struct.unpack('<f', f.read(4))[0]
            met_maxt    = struct.unpack('<f', f.read(4))[0]
            met_minh    = struct.unpack('<f', f.read(4))[0]
            met_maxh    = struct.unpack('<f', f.read(4))[0]
            met_timeref = struct.unpack('<I', f.read(4))[0]
            #t           = struct.unpack('<I', f.read(4))[0]
            #t_obs.append( t_ref + timedelta(seconds=t) )
            #met_rain    = struct.unpack('<b', f.read(1))[0]
            #rf = f.read(1) # Dummy
            for i in range(met_n):
                t           = struct.unpack('<I', f.read(4))[0]
                t_obs.append( t_ref + timedelta(seconds=t) )
                met_rain.append( struct.unpack('<b', f.read(1))[0] )
                # met_rain = 1 : Rain
                # met_rain = 0 : No rain
                met_dat1.append( struct.unpack('<f', f.read(4))[0] )
                met_dat2.append( struct.unpack('<f', f.read(4))[0] )
                met_dat3.append( struct.unpack('<f', f.read(4))[0] )
        f.close()

        return {'met_code': met_code,
                'met_n'   : met_n,
                'met_nsen': met_nsen,
                'met_minp': met_minp,
                'met_maxp': met_maxp,
                'met_mint': met_mint,
                'met_maxt': met_maxt,
                'met_minh': met_minh,
                'met_maxh': met_maxh,
                'met_timeref': met_timeref,
                't_obs': t_obs,
                'met_rain': met_rain,
                'met_dat1': met_dat1,
                'met_dat2': met_dat2,
                'met_dat3': met_dat3}

    #
    # A6: OLC: Oxygen Line Chart (p.137, RPG_MWR_STD_Software_Manual 2015)
    #

    #
    # A7: TPC: Temperature Profile Chart (Full Trop.) (p.137, RPG_MWR_STD_Software_Manual 2015)
    #
    def read_tpc(self,f,*args):

        if not f: print("Missing argument FN, Please provide input filename.")
        if not os.path.isfile(f): 
            print('Input file is nonexists. Returnning...')

        root = os.path.dirname(f)
        file = os.path.basename(f)

        t_ref = datetime.strptime('20010101000000', "%Y%m%d%H%M%S")
        t_obs = []
        tpc_alt = []
        with open(f, "rb") as f:
            tpc_code      = struct.unpack('<I', f.read(4))[0]
            tpc_n         = struct.unpack('<I', f.read(4))[0]
            tpc_min       = struct.unpack('<f', f.read(4))[0]
            tpc_max       = struct.unpack('<f', f.read(4))[0]
            tpc_timeref   = struct.unpack('<I', f.read(4))[0]
            # tpc_timeref = 1 : UTC
            # tpc_timeref = 0 : LST
            tpc_retrieval = struct.unpack('<I', f.read(4))[0]
            # tpc_retrieval = 0 : Linear regression
            # tpc_retrieval = 1 : Cubic-spline regression
            # tpc_retrieval = 2 : Neural Network
            tpc_altn      = struct.unpack('<I', f.read(4))[0]
            for i in range(tpc_altn):
                tpc_alt.append( struct.unpack('<i', f.read(4))[0] )
            for i in range(tpc_n):
                t = struct.unpack('<i', f.read(4))[0]
                t_obs.append( t_ref + timedelta(seconds=t) )
                rf = f.read(1) # Dummy
                tmp = []
                for j in range(tpc_altn): 
                    tmp.append( struct.unpack('<f', f.read(4))[0] )
                if i == 0: tpc_dat = np.c_[tmp]
                else:      tpc_dat = np.c_[tpc_dat, tmp]
        f.close()

        return {'tpc_code': tpc_code,
                'tpc_n': tpc_n,
                'tpc_min': tpc_min,
                'tpc_max': tpc_max,
                'tpc_timeref': tpc_timeref,
                'tpc_retrieval': tpc_retrieval,
                'tpc_altn': tpc_altn,
                't_obs': t_obs,
                'tpc_alt': tpc_alt,
                'tpc_dat': tpc_dat}

    #
    # A8: TPB: Temperature Profile Chart (Boundary Layer) (p.138, RPG_MWR_STD_Software_Manual 2015)
    #
    def read_tpb(self,f,*args):

        if not f: print("Missing argument FN, Please provide input filename.")
        if not os.path.isfile(f): 
            print('Input file is nonexists. Returnning...')

        root = os.path.dirname(f)
        file = os.path.basename(f)

        t_ref = datetime.strptime('20010101000000', "%Y%m%d%H%M%S")
        t_obs = []
        tpb_alt = []
        with open(f, "rb") as f:
            tpb_code      = struct.unpack('<I', f.read(4))[0]
            tpb_n         = struct.unpack('<I', f.read(4))[0]
            tpb_min       = struct.unpack('<f', f.read(4))[0]
            tpb_max       = struct.unpack('<f', f.read(4))[0]
            tpb_timeref   = struct.unpack('<I', f.read(4))[0]
            # tpb_timeref = 1 : UTC
            # tpb_timeref = 0 : LST
            tpb_retrieval = struct.unpack('<I', f.read(4))[0]
            # tpb_retrieval = 0 : Linear regression
            # tpb_retrieval = 1 : Cubic-spline regression
            # tpb_retrieval = 2 : Neural Network
            tpb_altn      = struct.unpack('<I', f.read(4))[0]
            for i in range(tpb_altn):
                tpb_alt.append( struct.unpack('<i', f.read(4))[0] )
            for i in range(tpb_n):
                t = struct.unpack('<i', f.read(4))[0]
                t_obs.append( t_ref + timedelta(seconds=t) )
                rf = f.read(1) # Dummy
                tmp = []
                for j in range(tpb_altn): 
                    tmp.append( struct.unpack('<f', f.read(4))[0] )
                if i == 0: tpb_dat = np.c_[tmp]
                else:      tpb_dat = np.c_[tpb_dat, tmp]
        f.close()

        return {'tpb_code': tpb_code,
                'tpb_n': tpb_n,
                'tpb_min': tpb_min,
                'tpb_max': tpb_max,
                'tpb_timeref': tpb_timeref,
                'tpb_retrieval': tpb_retrieval,
                'tpb_altn': tpb_altn,
                't_obs': t_obs,
                'tpb_alt': tpb_alt,
                'tpb_dat': tpb_dat}

    #
    # A9: WVL: Water Vapour Line Chart (p.138, RPG_MWR_STD_Software_Manual 2015)
    #

    #
    # A10(1): HPC: Humidity Profile Chart (w/out RH) (p.139, RPG_MWR_STD_Software_Manual 2015)
    #
    def read_hpc(self,f,*args):

        if not f: print("Missing argument FN, Please provide input filename.")
        if not os.path.isfile(f): 
            print('Input file is nonexists. Returnning...')

        root = os.path.dirname(f)
        file = os.path.basename(f)

        t_ref = datetime.strptime('20010101000000', "%Y%m%d%H%M%S")
        t_obs = []
        hpc_alt = []
        with open(f, "rb") as f:
            hpc_code      = struct.unpack('<I', f.read(4))[0]
            hpc_n         = struct.unpack('<I', f.read(4))[0]
            hpc_min       = struct.unpack('<f', f.read(4))[0]
            hpc_max       = struct.unpack('<f', f.read(4))[0]
            hpc_timeref   = struct.unpack('<I', f.read(4))[0]
            # hpc_timeref = 1 : UTC
            # hpc_timeref = 0 : LST
            hpc_retrieval = struct.unpack('<I', f.read(4))[0]
            # hpc_retrieval = 0 : Linear regression
            # hpc_retrieval = 1 : Cubic-spline regression
            # hpc_retrieval = 2 : Neural Network
            hpc_altn      = struct.unpack('<I', f.read(4))[0]
            for i in range(hpc_altn):
                hpc_alt.append( struct.unpack('<i', f.read(4))[0] )
            for i in range(hpc_n):
                t = struct.unpack('<i', f.read(4))[0]
                t_obs.append( t_ref + timedelta(seconds=t) )
                rf = f.read(1) # Dummy
                tmp = []
                for j in range(hpc_altn): 
                    tmp.append( struct.unpack('<f', f.read(4))[0] )
                if i == 0: hpc_dat = np.c_[tmp]
                else:      hpc_dat = np.c_[hpc_dat, tmp]
        f.close()

        return {'hpc_code': hpc_code,
                'hpc_n': hpc_n,
                'hpc_min': hpc_min,
                'hpc_max': hpc_max,
                'hpc_timeref': hpc_timeref,
                'hpc_retrieval': hpc_retrieval,
                'hpc_altn': hpc_altn,
                't_obs': t_obs,
                'hpc_alt': hpc_alt,
                'hpc_dat': hpc_dat}

    #
    # A11: LPR: Liquid Water Profile Chart (p.140, RPG_MWR_STD_Software_Manual 2015)
    #
    def read_lpr(self,f,*args):

        if not f: print("Missing argument FN, Please provide input filename.")
        if not os.path.isfile(f): 
            print('Input file is nonexists. Returnning...')

        root = os.path.dirname(f)
        file = os.path.basename(f)

        t_ref = datetime.strptime('20010101000000', "%Y%m%d%H%M%S")
        t_obs = []
        lpr_alt = []
        with open(f, "rb") as f:
            lpr_code      = struct.unpack('<I', f.read(4))[0]
            lpr_n         = struct.unpack('<I', f.read(4))[0]
            lpr_min       = struct.unpack('<f', f.read(4))[0]
            lpr_max       = struct.unpack('<f', f.read(4))[0]
            lpr_timeref   = struct.unpack('<I', f.read(4))[0]
            # lpr_timeref = 1 : UTC
            # lpr_timeref = 0 : LST
            lpr_retrieval = struct.unpack('<I', f.read(4))[0]
            # lpr_retrieval = 0 : Linear regression
            # lpr_retrieval = 1 : Cubic-spline regression
            # lpr_retrieval = 2 : Neural Network
            lpr_altn      = struct.unpack('<I', f.read(4))[0]
            for i in range(lpr_altn):
                lpr_alt.append( struct.unpack('<i', f.read(4))[0] )
            for i in range(lpr_n):
                t = struct.unpack('<i', f.read(4))[0]
                t_obs.append( t_ref + timedelta(seconds=t) )
                rf = f.read(1) # Dummy
                tmp = []
                for j in range(lpr_altn): 
                    tmp.append( struct.unpack('<f', f.read(4))[0] )
                if i == 0: lpr_dat = np.c_[tmp]
                else:      lpr_dat = np.c_[lpr_dat, tmp]
        f.close()

        return {'lpr_code': lpr_code,
                'lpr_n': lpr_n,
                'lpr_min': lpr_min,
                'lpr_max': lpr_max,
                'lpr_timeref': lpr_timeref,
                'lpr_retrieval': lpr_retrieval,
                'lpr_altn': lpr_altn,
                't_obs': t_obs,
                'lpr_alt': lpr_alt,
                'lpr_dat': lpr_dat}

    #
    # A12: IRT: Infrared Radiometer Temperatures (p.141, RPG_MWR_STD_Software_Manual 2015)
    #
    def read_irt(self,f,*args):

        if not f: print("Missing argument FN, Please provide input filename.")
        if not os.path.isfile(f): 
            print('Input file is nonexists. Returnning...')

        root = os.path.dirname(f)
        file = os.path.basename(f)

        t_ref = datetime.strptime('20010101000000', "%Y%m%d%H%M%S")
        t_obs = []
        irt_freq = []
        irt_ang = []
        with open(f, "rb") as f:
            irt_code      = struct.unpack('<I', f.read(4))[0]
            irt_n         = struct.unpack('<I', f.read(4))[0]
            irt_min       = struct.unpack('<f', f.read(4))[0]
            irt_max       = struct.unpack('<f', f.read(4))[0]
            irt_timeref   = struct.unpack('<I', f.read(4))[0]
            # irt_timeref = 1 : UTC
            # irt_timeref = 0 : LST
            irt_freqn     = struct.unpack('<I', f.read(4))[0]
            for i in range(irt_freqn):
                irt_freq.append( struct.unpack('<f', f.read(4))[0] )
            for i in range(irt_n):
                t = struct.unpack('<i', f.read(4))[0]
                t_obs.append( t_ref + timedelta(seconds=t) )
                rf = f.read(1) # Dummy
                tmp = struct.unpack('<f', f.read(4))[0]
                #tmp = []
                #for j in range(irt_freqn): 
                #    tmp.append( struct.unpack('<f', f.read(4))[0] )
                if i == 0: irt_dat = np.c_[tmp]
                else:      irt_dat = np.c_[irt_dat, tmp]
                irt_ang.append( struct.unpack('<f', f.read(4))[0] )
        f.close()

        return {'irt_code': irt_code,
                'irt_n': irt_n,
                'irt_min': irt_min,
                'irt_max': irt_max,
                'irt_timeref': irt_timeref,
                'irt_freqn': irt_freqn,
                'irt_freq': irt_freq,
                't_obs': t_obs,
                'irt_dat': irt_dat,
                'irt_ang': irt_ang}

    #
    # A13b: BLB: Boundary Layer BT Profiles (p.142, RPG_MWR_STD_Software_Manual 2015)
    #
    def read_blb(self,f,*args):

        if not f: print("Missing argument FN, Please provide input filename.")
        if not os.path.isfile(f): 
            print('Input file is nonexists. Returnning...')

        root = os.path.dirname(f)
        file = os.path.basename(f)

        blb_freq = []
        blb_min = []
        blb_max = []
        t_ref = datetime.strptime('20010101000000', "%Y%m%d%H%M%S")
        t_obs = []
        blb_ang = []
        blb_elv = []
        blb_azm = []
        with open(f, "rb") as f:
            blb_code    = struct.unpack('<I', f.read(4))[0]
            blb_n       = struct.unpack('<I', f.read(4))[0]
            blb_freqn   = struct.unpack('<I', f.read(4))[0]
            for vname in range(blb_freqn):
                blb_min.append( struct.unpack('<f', f.read(4))[0] )
            for vname in range(blb_freqn):
                blb_max.append( struct.unpack('<f', f.read(4))[0] )
            blb_timeref = struct.unpack('<I', f.read(4))[0]
            # brt_timeref = 1 : UTC
            # brt_timeref = 0 : LST
            for vname in range(blb_freqn):
                blb_freq.append(struct.unpack('<f', f.read(4))[0] )
            blb_angn = struct.unpack('<I', f.read(4))[0]
            for i in range(blb_angn):
                blb_ang.append( struct.unpack('<f', f.read(4))[0])
                blb_azm.append( blb_ang[i] / 1000. )
                blb_elv.append( blb_ang[i] - blb_azm[i] * 1000. )
            for i in range(blb_n):
                t = struct.unpack('<i', f.read(4))[0]
                t_obs.append( t_ref + timedelta(seconds=t) )
                rf = f.read(1) # Dummy
                tmp = []
                for j in range(blb_freqn): 
                    tmp.append( struct.unpack('<f', f.read(4))[0])
                if i == 0: blb_dat = np.c_[tmp]
                else:      blb_dat = np.c_[blb_dat, tmp]
        f.close()

        return {'blb_code': blb_code,
                'blb_n': blb_n,
                'brt timeref': blb_timeref,
                'blb_freqn': blb_freqn,
                'blb_freq': blb_freq,
                'blb_min': blb_min,
                'blb_max': blb_max,
                't_obs': t_obs,
                'blb_dat': blb_dat,
                'blb_angn': blb_angn,
                'blb_ang': blb_ang,
                'blb_elv': blb_elv,
                'blb_azm': blb_azm}

    #
    # A14: STA: Stability Indices (CAPE etc) (p.144, RPG_MWR_STD_Software_Manual 2015)
    #
    def read_sta(self,f,*args):

        if not f: print("Missing argument FN, Please provide input filename.")
        if not os.path.isfile(f): 
            print('Input file is nonexists. Returnning...')

        root = os.path.dirname(f)
        file = os.path.basename(f)

        t_ref = datetime.strptime('20010101000000', "%Y%m%d%H%M%S")
        nindex = 6
        t_obs = []
        sta_list = []
        sta_ang = []
        with open(f, "rb") as f:
            sta_code      = struct.unpack('<I', f.read(4))[0]
            sta_n         = struct.unpack('<I', f.read(4))[0]
            sta_min       = struct.unpack('<f', f.read(4))[0]
            sta_max       = struct.unpack('<f', f.read(4))[0]
            for i in range(nindex):
                sta_list.append( struct.unpack('<i', f.read(4))[0] )
            sta_timeref   = struct.unpack('<I', f.read(4))[0]
            for i in range(sta_n):
                t = struct.unpack('<i', f.read(4))[0]
                t_obs.append( t_ref + timedelta(seconds=t) )
                rf = f.read(1) # Dummy
                tmp = []
                for j in range(nindex): 
                    tmp.append( struct.unpack('<f', f.read(4))[0] )
                if i == 0: sta_dat = np.c_[tmp]
                else:      sta_dat = np.c_[sta_dat, tmp]
        f.close()

        return {'sta_code': sta_code,
                'sta_n': sta_n,
                'sta_min': sta_min,
                'sta_max': sta_max,
                'sta_list': sta_list,
                'sta_timeref': sta_timeref,
                't_obs': t_obs,
                'sta_dat': sta_dat}

    #
    # A15: CAL.LOG: Calibration Log-File (p.144, RPG_MWR_STD_Software_Manual 2015)
    #
    def read_cal_log(self,f,*args):

        if not f: print("Missing argument FN, Please provide input filename.")
        if not os.path.isfile(f): 
            print('Input file is nonexists. Returnning...')

        root = os.path.dirname(f)
        file = os.path.basename(f)
        fsze = os.path.getsize(f)

        t_ref = datetime.strptime('20010101000000', "%Y%m%d%H%M%S")
        log_caltype = []
        log_time = []
        log_tcalstatus = []
        log_gain = []
        log_tsys = []
        log_lincor = []
        log_chisqr = []
        log_noise = []
        log_n_tcalang = []
        log_r1tcalflg = []
        log_r2tcalflg = []
        log_ch_dvol = []
        log_tauflg = []


        with open(f, "rb") as f:
            log_code      = struct.unpack('<i', f.read(4))[0]

            t = struct.unpack('<i', f.read(4))[0]
            log_stime     = t_ref + timedelta(seconds=t)
            t = struct.unpack('<i', f.read(4))[0]
            log_etime     = t_ref + timedelta(seconds=t)
            log_n_gain    = struct.unpack('<i', f.read(4))[0]
            log_n_noise   = struct.unpack('<i', f.read(4))[0]
            log_n_tcal    = struct.unpack('<i', f.read(4))[0]
            log_n_r1ch    = struct.unpack('<i', f.read(4))[0]
            log_n_r2ch    = struct.unpack('<i', f.read(4))[0]
            log_chfreq    = []
            for vname in range(log_n_r1ch + log_n_r2ch):
                log_chfreq.append(struct.unpack('<f', f.read(4))[0] )

            print(log_n_gain, log_n_noise, log_n_tcal)
            log_n = log_n_gain + log_n_noise + log_n_tcal

            for i in range(log_n):
                log_caltype.append(struct.unpack('<i', f.read(4))[0] )

                t = struct.unpack('<i', f.read(4))[0]
                log_time.append( t_ref + timedelta(seconds=t) )

                if     int(log_caltype[i]) == 0:
                    log_tcalstatus.append( 0 )
                elif   int(log_caltype[i]) == 1:
                    log_tcalstatus.append( 0 )
                else: #int(log_caltype[i]) == 2,3:
                    log_tcalstatus.append( struct.unpack('<i', f.read(4))[0] )

                tmp = []
                for vname in range(log_n_r1ch + log_n_r2ch):
                    tmp.append( struct.unpack('<f', f.read(4))[0] )
                if i == 0: log_gain = np.c_[tmp]
                else:      log_gain = np.c_[log_gain, tmp]


                if     int(log_caltype[i]) == 0:
                    tmp = []
                    for vname in range(log_n_r1ch + log_n_r2ch):
                        tmp.append( -999.0 )
                    if i == 0: log_tsys = np.c_[tmp]
                    else:      log_tsys = np.c_[log_tsys, tmp]
                else: #int(log_caltype[i]) == 1,2,3:
                    tmp = []
                    for vname in range(log_n_r1ch + log_n_r2ch):
                        tmp.append(struct.unpack('<f', f.read(4))[0] )
                    if i == 0: log_tsys = np.c_[tmp]
                    else:      log_tsys = np.c_[log_tsys, tmp]

                if     int(log_caltype[i]) == 0:
                    tmp = []
                    for vname in range(log_n_r1ch + log_n_r2ch):
                        tmp.append( -999.0 )
                    if i == 0: log_lincor = np.c_[tmp]
                    else:       log_lincor = np.c_[log_lincor, tmp]
                    tmp = []
                    for vname in range(log_n_r1ch + log_n_r2ch):
                        tmp.append( -999.0 )
                    if i == 0: log_chisqr = np.c_[tmp]
                    else:      log_chisqr = np.c_[log_chisqr, tmp]
                    tmp = []
                    for vname in range(log_n_r1ch + log_n_r2ch):
                        tmp.append( -999.0 )
                    if i == 0: log_noise = np.c_[tmp]
                    else:      log_noise = np.c_[log_noise, tmp]
                elif   int(log_caltype[i]) == 1:
                    tmp = []
                    for vname in range(log_n_r1ch + log_n_r2ch):
                        tmp.append( -999.0 )
                    if i == 0: log_lincor = np.c_[tmp]
                    else:       log_lincor = np.c_[log_lincor, tmp]
                    tmp = []
                    for vname in range(log_n_r1ch + log_n_r2ch):
                        tmp.append( -999.0 )
                    if i == 0: log_chisqr = np.c_[tmp]
                    else:      log_chisqr = np.c_[log_chisqr, tmp]
                    tmp = []
                    for vname in range(log_n_r1ch + log_n_r2ch):
                        tmp.append( -999.0 )
                    if i == 0: log_noise = np.c_[tmp]
                    else:      log_noise = np.c_[log_noise, tmp]
                else: #int(log_caltype[i]) == 1,2,3:
                    tmp = []
                    for vname in range(log_n_r1ch + log_n_r2ch):
                        tmp.append(struct.unpack('<f', f.read(4))[0] )
                    if i == 0: log_lincor = np.c_[tmp]
                    else:       log_lincor = np.c_[log_lincor, tmp]
                    tmp = []
                    for vname in range(log_n_r1ch + log_n_r2ch):
                        tmp.append(struct.unpack('<f', f.read(4))[0] )
                    if i == 0: log_chisqr = np.c_[tmp]
                    else:      log_chisqr = np.c_[log_chisqr, tmp]
                    tmp = []
                    for vname in range(log_n_r1ch + log_n_r2ch):
                        tmp.append(struct.unpack('<f', f.read(4))[0] )
                    if i == 0: log_noise = np.c_[tmp]
                    else:      log_noise = np.c_[log_noise, tmp]

                if int(log_caltype[i]) == 3: 
                    log_n_tcalang.append( struct.unpack('<i', f.read(4))[0] )
                    tmp = []

                    for vname in range(int(log_n_tcalang[i])):
                        tmp.append(struct.unpack('<f', f.read(4))[0] )
                    if i == 0: log_airmass = np.c_[tmp]
                    else:      log_airmass = np.c_[log_airmass, tmp]
                    log_r1tcalflg.append(struct.unpack('<i', f.read(4))[0] )
                    log_r2tcalflg.append(struct.unpack('<i', f.read(4))[0] )
                    tmp = []
                    for vname in range(log_n_r1ch):
                        for tname in range(log_n_tcalang[i] + 1):
                            tmp.append(struct.unpack('<f', f.read(4))[0] )
                    if i == 0: log_ch_dvol = np.c_[tmp]
                    else:      log_ch_dvol = np.c_[log_ch_dvol, tmp]
                    tmp = []
                    for vname in range(log_n_r1ch):
                        tmp.append(struct.unpack('<i', f.read(4))[0] )
                    if i == 0: log_tauflg = np.c_[tmp]
                    else:      log_tauflg = np.c_[log_tauflg, tmp]
                    tmp = []
                    tmp_offset = []
                    tmp_slope  = []
                    for vname in range(log_n_r1ch):
                        for tname in range( int(log_n_tcalang[-1]) ):
                            tmp.append(struct.unpack('<f', f.read(4))[0] )
                        tmp_offset.append(struct.unpack('<f', f.read(4))[0] )
                        tmp_slope.append(struct.unpack('<f', f.read(4))[0] )
                    if i == 0: 
                        log_tauarray  = np.c_[tmp]
                        log_tauoffset = np.c_[tmp_offset]
                        log_tauslope  = np.c_[tmp_slope]
                    else:
                        log_tauarray  = np.c_[log_tauarray, tmp]
                        log_tauoffset = np.c_[log_tauoffset, tmp_offset]
                        log_tauslope  = np.c_[log_tauslope, tmp_slope]
                else: #int(log_caltype[i]) == 0,1,2:
                    log_n_tcalang.append( -1 )
                    tmp = []

                    for vname in range( 6 ):
                        tmp.append( -999.0 )
                    if i == 0: log_airmass = np.c_[tmp]
                    else:      log_airmass = np.c_[log_airmass, tmp]
                    log_r1tcalflg.append( 0 )
                    log_r2tcalflg.append( 0 )
                    tmp = []
                    for vname in range(log_n_r1ch):
                        for tname in range( 6 + 1 ):
                            tmp.append( -999.0 )
                    if i == 0: log_ch_dvol = np.c_[tmp]
                    else:      log_ch_dvol = np.c_[log_ch_dvol, tmp]
                    tmp = []
                    for vname in range(log_n_r1ch):
                        tmp.append( 0 )
                    if i == 0: log_tauflg = np.c_[tmp]
                    else:      log_tauflg = np.c_[log_tauflg, tmp]
                    tmp = []
                    tmp_offset = []
                    tmp_slope  = []
                    for vname in range(log_n_r1ch):
                        for tname in range( 6 ):
                            tmp.append( -999.0 )
                        tmp_offset.append( -999.0 )
                        tmp_slope.append( -999.0 )
                    if i == 0: 
                        log_tauarray  = np.c_[tmp]
                        log_tauoffset = np.c_[tmp_offset]
                        log_tauslope  = np.c_[tmp_slope]
                    else:
                        log_tauarray  = np.c_[log_tauarray, tmp]
                        log_tauoffset = np.c_[log_tauoffset, tmp_offset]
                        log_tauslope  = np.c_[log_tauslope, tmp_slope]


        f.close()


        return {'log_code': log_code,           #CAL.LOG -File Code (=657645)
                'log_stime': log_stime,         #Time of first sample
                'log_etime': log_etime,         #Time of latest sample
                'log_n_gain': log_n_gain,       #NNumber of recorded gain cal. samples
                'log_n_noise': log_n_noise,     #NNumber of recorded noise cal. samples
                'log_n_tcal': log_n_tcal,       #NNumber of recorded tip curve cal. samples
                'log_n_r1ch': log_n_r1ch,       #NNumber of receiver 1 channels
                'log_n_r2ch': log_n_r2ch,       #NNumber of receiver 2 channels
                'log_chfreq' : log_chfreq,      #Frequencies of Rec1 and Rec2 [GHz]

                'log_caltype' : log_caltype,    #Type of calibration sample 
                                                # (0=gain, 1=noise, 2=tip curve results, 
                                                # 3=tip curve with full fit information)
                'log_time' : log_time,          #Time of gain calibration sample (# of sec. since 1.1.2001)
                'log_tcalstatus':log_tcalstatus,#Status of tip curve calibration (only if CalType1=2 or 3)
                                                # 3 = FAILED, 2 = SUCCESS
                'log_gain' : log_gain,          #Receiver gains for all channels, entry #n [V/K]
                'log_tsys' : log_tsys,          #System noise temps of calibration sample 
                                                # (only if CalType1=1 or CalType1=2 or CalType1=3) [K] 
                'log_lincor' : log_lincor,      #Linear correlations for calibration sample 1 
                                                # (only if CalType1=2 or 3)
                'log_chisqr' : log_chisqr,      #Chi square factors for calibration sample 1 
                                                # (only if CalType1=2 or 3)
                'log_noise' : log_noise,        #Noise source temperatures for calibration sample 1 
                                                # (only if CalType1=2 or 3)

                'log_n_tcalang' : log_n_tcalang,#Number of sky tip for calibration sample 1 
                                                # (only if CalType1= 3)
                'log_airmass' : log_airmass,    #HAirmass array (only if CalType1=3)
                'log_r1tcalflg' : log_r1tcalflg,#1=Skydip enabled for Receiver 1, 0=disabled
                'log_r2tcalflg' : log_r2tcalflg,#1=Skydip enabled for Receiver 1, 0=disabled
                'log_ch_dvol' : log_ch_dvol,    #Sky dip detector voltages (only if CalType1=3). 
                                                # For each frequency the det. Voltage is given at all angles. 
                                                # The last entry is the voltage on the hot target
                'log_tauflg' : log_tauflg,      #Flag that indicates if the Tau calculation during 
                                                # the skydip was successful (0=no, 1=yes, 2=yes, also 
                                                # skydip successful) (only if CalType1=3)

                'log_tauarray' : log_tauarray,  #Tau array for channel 1 
                                                # (only if CalType1=3 and TauSuccess1[0]=1)
                'log_tauosffset': log_tauoffset,#Linear Fit parameter A (offset) for channel 1 
                                                # (only if CalType1=3 and TauSuccess1[0]=1)
                'log_tauslope' : log_tauslope}  #Linear Fit parameter B (slope) for channel 1 
                                                # (only if CalType1=3 and TauSuccess1[0]=1)

    #
    # A16: CBH: Cloud Base Height (p.151, RPG_MWR_STD_Software_Manual 2015)
    #
    def read_cbh(self,f,*args):

        if not f: print("Missing argument FN, Please provide input filename.")
        if not os.path.isfile(f): 
            print('Input file is nonexists. Returnning...')

        root = os.path.dirname(f)
        file = os.path.basename(f)

        t_ref = datetime.strptime('20010101000000', "%Y%m%d%H%M%S")
        t_obs = []
        cbh_dat = []
        with open(f, "rb") as f:
            cbh_code      = struct.unpack('<I', f.read(4))[0]
            cbh_n         = struct.unpack('<I', f.read(4))[0]
            cbh_min       = struct.unpack('<f', f.read(4))[0]
            cbh_max       = struct.unpack('<f', f.read(4))[0]
            cbh_timeref   = struct.unpack('<I', f.read(4))[0]
            for i in range(cbh_n):
                t = struct.unpack('<i', f.read(4))[0]
                t_obs.append( t_ref + timedelta(seconds=t) )
                rf = f.read(1) # Dummy
                cbh_dat.append( struct.unpack('<f', f.read(4))[0] )
        f.close()

        return {'cbh_code': cbh_code,
                'cbh_n': cbh_n,
                'cbh_min': cbh_min,
                'cbh_max': cbh_max,
                'cbh_timeref': cbh_timeref,
                't_obs': t_obs,
                'cbh_dat': cbh_dat}

    #
    # A17: BLH: Boundary Layer Height (p.151, RPG_MWR_STD_Software_Manual 2015)
    #
    def read_blh(self,f,*args):

        if not f: print("Missing argument FN, Please provide input filename.")
        if not os.path.isfile(f): 
            print('Input file is nonexists. Returnning...')

        root = os.path.dirname(f)
        file = os.path.basename(f)

        t_ref = datetime.strptime('20010101000000', "%Y%m%d%H%M%S")
        t_obs = []
        blh_t = []
        blh_rain = []
        blh_dat = []

        with open(f, "rb") as f:
            blh_code      = struct.unpack('<i', f.read(4))[0]
            blh_n         = struct.unpack('<i', f.read(4))[0]
            blh_min       = struct.unpack('<f', f.read(4))[0]
            blh_max       = struct.unpack('<f', f.read(4))[0]
            blh_timeref   = struct.unpack('<i', f.read(4))[0]
            for i in range(blh_n):
                t = struct.unpack('<i', f.read(4))[0]
                blh_t.append( t_ref + timedelta(seconds=t) )
                blh_rain.append(struct.unpack('<c', f.read(1))[0] )
                blh_dat.append(struct.unpack('<f', f.read(4))[0] )

        f.close()

        return {'blh_code': blh_code,       # BLH-File Code (=1777786)
                'blh_n': blh_n,             # Number of recorded samples
                'blh_min': blh_min,         # Minimum of recorded BLH values
                'blh_max': blh_max,         # Maximum of recorded BLH values
                'blh_timeref': blh_timeref, # Time reference (1: UTC, 0: Local Time)
                'blh_t': blh_t,             # Time of sample 1 (# of sec. since 1.1.2001)
                'blh_rain': blh_rain,       # Rainflag of sample n (0: no rain, 1: rain)
                'blh_dat': blh_dat}         # Boundary layer height [m], sample n

    #
    # A18b: VLT: Channel Voltage File (p.152, RPG_MWR_STD_Software_Manual 2015)
    #
    def read_vlt(self,f,*args):

        if not f: print("Missing argument FN, Please provide input filename.")
        if not os.path.isfile(f): 
            print('Input file is nonexists. Returnning...')

        root = os.path.dirname(f)
        file = os.path.basename(f)

        t_ref = datetime.strptime('20010101000000', "%Y%m%d%H%M%S")
        t_obs = []
        vlt_r1freq = []
        vlt_r2freq = []
        vlt_s1r1freq = []
        vlt_s1r2freq = []
        vlt_diagsrc = []
        vlt_datsamplesrc1 = []
        vlt_datsamplesrc2 = []
        vlt_datsamplesrc3 = []
        vlt_datsamplesrc4 = []
        vlt_elapse = []

        with open(f, "rb") as f:
            vlt_code      = struct.unpack('<i', f.read(4))[0]
            vlt_n         = struct.unpack('<i', f.read(4))[0]
            vlt_timeidx   = struct.unpack('<i', f.read(4))[0]
            vlt_slvrec    = struct.unpack('<i', f.read(4))[0]
            vlt_r1freqn   = struct.unpack('<i', f.read(4))[0]
            for vname in range(vlt_r1freqn):
                vlt_r1freq.append(struct.unpack('<f', f.read(4))[0] )
            vlt_r2freqn     = struct.unpack('<i', f.read(4))[0]
            for vname in range(vlt_r2freqn):
                vlt_r2freq.append(struct.unpack('<f', f.read(4))[0] )
            vlt_s1r1freqn   = struct.unpack('<i', f.read(4))[0]
            for vname in range(vlt_s1r1freqn):
                vlt_s1r1freq.append(struct.unpack('<f', f.read(4))[0] )
            vlt_s1r2freqn     = struct.unpack('<i', f.read(4))[0]
            for vname in range(vlt_s1r2freqn):
                vlt_s1r2freq.append(struct.unpack('<f', f.read(4))[0] )
            for vname in range(4):
                vlt_diagsrc.append(struct.unpack('<I', f.read(4))[0] )
            #for i in range(vlt_n):
            for i in range(10):
                tmp = []
                for vname in range(10):
                    tmp.append(struct.unpack('<f', f.read(4))[0] )
                if i == 0: vlt_datsamplesrc1 = np.c_[tmp]
                else:      vlt_datsamplesrc1 = np.c_[vlt_datsamplesrc1, tmp]
                tmp = []
                # for vname in range(7):
                #     tmp.append(struct.unpack('<f', f.read(4))[0] )
                # if i == 0: vlt_datsamplesrc2 = np.c_[tmp]
                # else:      vlt_datsamplesrc2 = np.c_[vlt_datsamplesrc2, tmp]
                # tmp = []
                # for vname in range(7):
                #     tmp.append(struct.unpack('<f', f.read(4))[0] )
                # if i == 0: vlt_datsamplesrc3 = np.c_[tmp]
                # else:      vlt_datsamplesrc3 = np.c_[vlt_datsamplesrc3, tmp]
                # tmp = []
                # for vname in range(4):
                #     tmp.append(struct.unpack('<f', f.read(4))[0] )
                # if i == 0: vlt_datsamplesrc4 = np.c_[tmp]
                # else:      vlt_datsamplesrc4 = np.c_[vlt_datsamplesrc4, tmp]
                vlt_elapse.append(struct.unpack('<f', f.read(4))[0])
                #t = struct.unpack('<i', f.read(4))[0]
                #vlt_elapse.append( t_ref + timedelta(seconds=t) )

        f.close()

        return {'vlt_code': vlt_code,                   # VLT-File Code (=362118747)
                'vlt_n': vlt_n,                         # Number of samples
                'vlt_timeidx': vlt_timeidx,             # Integration time index (0:1sec, 1:2sec, 
                                                        # 2:5 sec, 3:10sec, 4:20sec, 5:30sec, 6:60sec)
                'vlt_slvrec': vlt_slvrec,               # =0: no Slave radiometer data recorded, 
                                                        # =1: Slave radiometer data recorded
                'vlt_r1freqn': vlt_r1freqn,             # Receiver 1 number of frequencies
                'vlt_r1freq': vlt_r1freq,               # Receiver 1 frequencies [GHz]
                'vlt_r2freqn': vlt_r2freqn,             # Receiver 2 number of frequencies
                'vlt_r2freq': vlt_r2freq,               # Receiver 2 frequencies [GHz]
                'vlt_s1r1freqn': vlt_s1r1freqn,         # If SlaveRecord =1: Slave Receiver 1 number of frequencies
                'vlt_s1r1freq': vlt_s1r1freq,           # If SlaveRecord =1: Slave Receiver 1 frequencies [GHz]
                'vlt_s1r2freqn': vlt_s1r2freqn,         # If SlaveRecord =1: Slave Receiver 2 number of frequencies
                'vlt_s1r2freq': vlt_s1r2freq,           # If SlaveRecord =1: Slave Receiver 2 frequencies [GHz]
                'vlt_diagsrc': vlt_diagsrc,             # Type array for the four acquisition channels; 
                                                        # 0=disabled, 1=receiver 1 voltage data, 
                                                        # 2=receiver 2 voltage data, 3=ambient target temp., 
                                                        # 4=env. temp, 5=rec. 1 temp., 6=rec. 2 temp., 
                                                        # 7=bar. Pressure, 8=rel. humidity
                'vlt_datsamplesrc1': vlt_datsamplesrc1, # Data for sample 1 (R1FAnz/R2FAnz floats in 
                'vlt_datsamplesrc2': vlt_datsamplesrc2, # the case of data type=1/2, one float in all 
                'vlt_datsamplesrc3': vlt_datsamplesrc3, # other cases)
                'vlt_datsamplesrc4': vlt_datsamplesrc4, 
                'vlt_elapse': vlt_elapse}               # Time in seconds after measurement start of sample n

    #
    # A19: HKD: Housekeeping Data File (p.154, RPG_MWR_STD_Software_Manual 2015)
    #
    def read_hkd(self,f,*args):

        if not f: print("Missing argument FN, Please provide input filename.")
        if not os.path.isfile(f): 
            print('Input file is nonexists. Returnning...')

        root = os.path.dirname(f)
        file = os.path.basename(f)

        t_ref = datetime.strptime('20010101000000', "%Y%m%d%H%M%S")
        t_obs = []
        hkd_alarm = []
        hkd_lon = []
        hkd_lat = []
        hkd_amb = []
        hkd_sta = []
        hkd_fsh = []
        hkd_qlt = []
        hkd_sts = []
        with open(f, "rb") as f:
            hkd_code     = struct.unpack('<I', f.read(4))[0]
            hkd_n        = struct.unpack('<I', f.read(4))[0]
            hkd_timeref  = struct.unpack('<I', f.read(4))[0]
            tmp          = struct.unpack('<i', f.read(4))[0]
            #hkd_select = f.read(4)
            #print(np.asarray(tmp, dtype=np.uint8))
            hkd_select = np.unpackbits(np.asarray(tmp, dtype=np.uint8))
            #hkd_select[0] = 0
            #hkd_select[1] = 1
            for i in range(hkd_n):
                t = struct.unpack('<I', f.read(4))[0]
                t_obs.append( t_ref + timedelta(seconds=t) )
                #
                # Alarm flag
                #
                # The alarm flag is activated in the following cases:
                #  • interference or failure of a channel that is used in 
                #    one of the retrievals • thermal receiver stability not 
                #    sufficient for measurement
                #  • noise diode failure of one of the receivers
                #  • ambient target thermal sensor not stable
                hkd_alarm.append( struct.unpack('<b', f.read(1))[0] )
                #hkd_alarm.append( f.read(1) ) # Alarm flag
                tmp = []
                # ======================================================
                if hkd_select[1]: # GPS positions
                    hkd_lon.append( struct.unpack('<f', f.read(4))[0] )
                    hkd_lat.append( struct.unpack('<f', f.read(4))[0] )
                else:
                    hkd_lon.append( [None] )
                    hkd_lat.append( [None] )
                    # =====
                if hkd_select[2]: # Ambirent temperature [K]
                # [0]: Ambient target sensor 1
                # [1]: Ambient target sensor 2
                # [2]: Humidity profiler receiver
                # [3]: Temperature profiler receiver
                #
                # The "ambient temperature target sensor" precisely 
                # measures the built-in calibration target temperature. The 
                # precision of that sensor is essential for ALL calibration 
                # procedures. 
                #
                # Usually, two of these sensors are implemented to be able
                # to generate an alarm in the case one of the sensors fails.
                #
                # Receiver1 / Receiver 2: These temperature sensors reflect the
                # physical temperatures of the receiver modules which are 
                # stabilized to an accuracy of < 0.03 K.
                #
                # Typical sensor readings are around 45°C. The thermal receiver
                # stabilization is continuously monitored. If the receiver 
                # temperature is kept constant to within +/- 0.03 K, the status
                # indicator on the right of the temperature display is green. 
                # If it turns to red the stability is worse than this threshold.
                # In addition the actual stabilization values are listed. The 
                # color of the stability status indicator turns to yellow if 
                # not enough temperature samples have been collected to 
                # determine the stability.
                #
                    tmp = [ struct.unpack('<f', f.read(4))[0],
                            struct.unpack('<f', f.read(4))[0],
                            struct.unpack('<f', f.read(4))[0],
                            struct.unpack('<f', f.read(4))[0] ]
                    if i == 0: hkd_amb = np.c_[tmp]
                    else:      hkd_amb = np.c_[hkd_amb, tmp]
                else:
                    if i == 0: hkd_amb = [None,None,None,None]
                    else:      hkd_amb = np.c_[hkd_amb, [None,None,None,None]]
                # =====
                if hkd_select[3]: # Stability [K]
                                  # [0]: Temperature stability of receiver 1
                                  # [1]: Temperature stability of receiver 2
                    #for j in range(2): 
                    #       tmp = ( struct.unpack('<f', f.read(4))[0] )
                    tmp = [ struct.unpack('<f', f.read(4))[0],
                            struct.unpack('<f', f.read(4))[0] ]
                    if i == 0: hkd_sta = np.c_[tmp]
                    else:      hkd_sta = np.c_[hkd_sta, tmp]
                else:
                    if i == 0: hkd_sta = np.c_[[None,None]]
                    else:      hkd_sta = np.c_[hkd_sta, [None,None]]
                # =====
                if hkd_select[4]: # Remaining flash memory [kBytes]
                    hkd_fsh.append( struct.unpack('<I', f.read(4))[0] )
                else:
                    hkd_fsh.append( [None] )
                # =====
                #
                # Status Flags
                #
                # This 4 byte unsigned integer is subdivided into 8 groups 
                # of 4 bits: 
                #
                # MSB yyxx yyxx yyxx yyxx yyxx yyxx yyxx yyxx
                # LSB   LP  STA  TPB  TPC  HPC  DLY  IWV  LWP
                #
                # Each group represents the quality flags of a certain 
                # level 2 product (retrieved data). The ‘xx’ bits are coded
                # in the following way:
                #
                #  • ‘xx’ = 0: this level 2 product is not evaluated for 
                #              quality control 
                #  • ‘xx’ = 1: highest quality level
                #  • ‘xx’ = 2: reduced quality
                #  • ‘xx’ = 3: low quality. This sample should not be used.
                #
                # The ‘yy’ bits are coding the possible reasons for reduced
                # or low quality sampling:
                #
                #  • ‘yy’ = 0: unknown
                #  • ‘yy’ = 1: possible external interference on a receiver
                #              channel or failure of a receiver channel 
                #              that is used in the retrieval of this product.
                #  • ‘yy’ = 2: LWP too high. Athigh rain rates the 
                #              scattering on rain drop scan mask the water
                #              vapour line completely and no humidity 
                #              profiling or IWV determination is possible. 
                #              Also the temperature profiling may be 
                #              affected when the oxygen line channels are 
                #              all saturated due to droplets.
                #  • ‘yy’ = 3: free for future use.
                #
                if hkd_select[5]: # Quality
                    #hkd_qlt.append( struct.unpack('<I', f.read(4))[0] )
                    #tmp = struct.unpack('<I', f.read(4))[0]
                    tmp = bin( struct.unpack('<I', f.read(4))[0] )[2:].zfill(32)
                    tmp = tmp[::-1] # Inverse string (https://stackoverflow.com
                                    # /questions/931092/reverse-a-string-in-
                                    # python)
                    LP_1 = '0' * (8 - len(tmp[0:1]) % 8) + tmp[0:1]
                    LP_2 = '0' * (8 - len(tmp[2:3]) % 8) + tmp[2:3]
                    STA1 = '0' * (8 - len(tmp[4:5]) % 8) + tmp[4:5]
                    STA2 = '0' * (8 - len(tmp[6:7]) % 8) + tmp[6:7]
                    TPB1 = '0' * (8 - len(tmp[8:9]) % 8) + tmp[8:9]
                    TPB2 = '0' * (8 - len(tmp[10:11]) % 8) + tmp[10:11]
                    TPC1 = '0' * (8 - len(tmp[12:13]) % 8) + tmp[12:13]
                    TPC2 = '0' * (8 - len(tmp[14:15]) % 8) + tmp[14:15]
                    HPC1 = '0' * (8 - len(tmp[16:17]) % 8) + tmp[16:17]
                    HPC2 = '0' * (8 - len(tmp[18:19]) % 8) + tmp[18:19]
                    DLY1 = '0' * (8 - len(tmp[20:21]) % 8) + tmp[20:21]
                    DLY2 = '0' * (8 - len(tmp[22:23]) % 8) + tmp[22:23]
                    IWV1 = '0' * (8 - len(tmp[24:25]) % 8) + tmp[24:25]
                    IWV2 = '0' * (8 - len(tmp[26:27]) % 8) + tmp[26:27]
                    LWP1 = '0' * (8 - len(tmp[28:29]) % 8) + tmp[28:29]
                    LWP2 = '0' * (8 - len(tmp[30:31]) % 8) + tmp[30:31]
                    #hkd_qlt.append( np.unpackbits(np.asarray(tmp, dtype=np.uint8)) )
                    hkd_qlt.append( [
                        int(LP_1, 2), # 0:no q, 1:high q, 2:reduced q, 3:low q 
                        int(LP_2, 2), # # 0:unknown, 1:ext. interference, 2: high LWP, 3: free 
                        int(STA1, 2), # 0:no q, 1:high q, 2:reduced q, 3:low q 
                        int(STA2, 2), # # 0:unknown, 1:ext. interference, 2: high LWP, 3: free 
                        int(TPB1, 2), # 0:no q, 1:high q, 2:reduced q, 3:low q 
                        int(TPB2, 2), # 0:unknown, 1:ext. interference, 2: high LWP, 3: free 
                        int(TPC1, 2), # 0:no q, 1:high q, 2:reduced q, 3:low q 
                        int(TPC2, 2), # 0:unknown, 1:ext. interference, 2: high LWP, 3: free 
                        int(HPC1, 2), # 0:no q, 1:high q, 2:reduced q, 3:low q 
                        int(HPC2, 2), # 0:unknown, 1:ext. interference, 2: high LWP, 3: free 
                        int(DLY1, 2), # 0:no q, 1:high q, 2:reduced q, 3:low q 
                        int(DLY2, 2), # 0:unknown, 1:ext. interference, 2: high LWP, 3: free 
                        int(IWV1, 2), # 0:no q, 1:high q, 2:reduced q, 3:low q
                        int(IWV2, 2), # 0:unknown, 1:ext. interference, 2: high LWP, 3: free 
                        int(LWP1, 2), # 0:no q, 1:high q, 2:reduced q, 3:low q
                        int(LWP2, 2) # 0:unknown, 1:ext. interference, 2: high LWP, 3: free
                        ] )
                else:
                    hkd_qlt.append( [None] )
                # =====
                #
                # Status Flags
                #
                # 0 0 0 0 01 01 1 1 0 0 0 0 0 0 0 1111111 0 1111111
                #   | | |  |  | | | | | | | | | |    |    |    |
                #   | | |  |  | | | | | | | | | |    |    |   (01)
                #   | | |  |  | | | | | | | | | |    |   (02)  
                #   | | |  |  | | | | | | | | | |   (03) 
                #   | | |  |  | | | | | | | | |(04)  
                #   | | |  |  | | | | | | | |(05)
                #   | | |  |  | | | | | | |(06)
                #   | | |  |  | | | | | |(07)
                #   | | |  |  | | | | |(08)
                #   | | |  |  | | | |(09)
                #   | | |  |  | | |(10)
                #   | | |  |  | |(11)
                #   | | |  |  |(12)
                #   | | |  | (13)
                #   | | | (14)
                #   | |(15)
                #   |(16)
                #  (17)
                #
                # (01) Bit 1-7: status flags for channel 1 to 7 of the 
                #             humidity profiler receiver. When a bit is set
                #             ‘1’, the corresponding channel is ok, 
                #             otherwise the channel has a malfunction.
                # (02) Bit 8: not used
                # (03) Bit 9-15: status flags for channel 1 to 7 of the 
                #             temperature profiler receiver. When a bit is 
                #             set ‘1’, the corresponding channel is ok, 
                #             otherwise the channel has a malfunction.
                # (04) Bit 16: not used
                # (05) Bit 17: rain flag. ‘1’ means raining, ‘0’ = no rain
                # (06) Bit 18: dew blower speed status. ‘1’ = high speed 
                #            mode, ‘0’ = low speed mode
                # (07) Bit 19: BL-mode flag. ‘1’ = boundary layer scanning 
                #            active, ‘0’ = BL-mode not active
                # (08) Bit 20: ‘1’ = sky tipping calibration running, ‘0’ = 
                #            not active
                # (09) Bit 21: ‘1’ = gain calibration running (using internal
                #            ambient target), ‘0’ = not active
                # (10) Bit 22: ‘1’ = noise calibration running, ‘0’ = not 
                #            active
                # (11) Bit 23: ‘1’ = noise diode of humidity profiler ok, ‘0’
                #            = noise diode not working
                # (12) Bit 24: ‘1’ = noise diode of temperature profiler ok, 
                #            ‘0’ = noise diode not working
                # (13) Bits25,26: receiver1 (humidity profiler) thermal 
                #            stability.‘0’ = unknown, not enough data
                #            samples recorded yet, ‘1’ = stability ok, ‘2’
                #            = not sufficiently stable
                # (14) Bits 27,28: receiver 2 (temperature profiler) thermal 
                #            stability. ‘0’ = unknown, not enough
                #            data samples recorded yet, ‘1’ = stability ok,
                #            ‘2’ = not sufficiently stable
                # (15) Bit 29: power failure flag. ‘1’ = a power failure has 
                #            occurred recently. When a new MDF has been 
                #            started automatically after a power failure, 
                #            the ‘1’ flag is kept for 1000 seconds and 
                #            switching back to ‘0’ afterwards. ‘0’ = no power 
                #            failure occurred.
                # (16) Bit 30: ambient target stability: Some radiometers are
                #            using two ambient target temperature sensors 
                #            for monitoring the target’s physical temperature. 
                #            When the temperature readings of these two sensors
                #            differ by more than 0.3 K, the flag turns to ‘1’. 
                #            ‘0’ = sensors ok.
                # (17) Bit 31: noise diode status: ‘0’ = noise diode is 
                #            turned off for the current sample, ‘1’ = noise 
                #            diode is turned on for the current sample.
                if hkd_select[6]: # Status
                    #hkd_sts.append( struct.unpack('<I', f.read(4))[0] )
                    #tmp = struct.unpack('<I', f.read(4))[0]
                    tmp = bin( struct.unpack('<I', f.read(4))[0] )[2:].zfill(32)
                    tmp = tmp[::-1] # Inverse string (https://stackoverflow.com
                                    # /questions/931092/reverse-a-string-in-
                                    # python)
                    #hkd_sts.append( np.unpackbits(np.asarray(tmp, dtype=np.uint8)) )
                    #hkd_sts.append( tmp )
                    sts_rcvr1 = '0' * (8 - len(tmp[24:25]) % 8) + tmp[24:25]
                    sts_rcvr2 = '0' * (8 - len(tmp[26:27]) % 8) + tmp[26:27]
                    hkd_sts.append( [
                        int(tmp[0]),       # Ch01 
                        int(tmp[1]),       # Ch02 
                        int(tmp[2]),       # Ch03 
                        int(tmp[3]),       # Ch04 
                        int(tmp[4]),       # Ch05 
                        int(tmp[5]),       # Ch06 
                        int(tmp[6]),       # Ch07 
                        int(tmp[8]),       # Ch08 
                        int(tmp[9]),       # Ch09 
                        int(tmp[10]),      # Ch10 
                        int(tmp[11]),      # Ch11 
                        int(tmp[12]),      # Ch12 
                        int(tmp[13]),      # Ch13 
                        int(tmp[14]),      # Ch14 
                        int(tmp[16]),      # Rain flag
                        int(tmp[17]),      # Dew blower speed status
                        int(tmp[18]),      # BL-mode flag
                        int(tmp[19]),      # gain calibration running
                        int(tmp[20]),      # noise calibration running
                        int(tmp[21]),      # noise diode of temperature profiler
                        int(sts_rcvr1, 2), # receiver1 (humidity profiler) 
                                           # thermal stability
                        int(sts_rcvr2, 2), # receiver 2 (temperature profiler)
                                           # thermal stability
                        int(tmp[28]),      # power failure flag 
                        int(tmp[29]),      # ambient target stability
                        int(tmp[30]) ])    # noise diode status
                else:
                    hkd_sts.append( [None] )

            f.close()

        return {'hkd_code': hkd_code,
                'hkd_n': hkd_n,
                'hkd_timeref': hkd_timeref,
                'hkd_select': hkd_select, #HKDSelect
                    # Only the first byte of this integer value is used for 
                    # selection of data groups. The meaning of the various bit
                    # settings of this byte is the following:
                    #
                    #  • Bit 1: When this bit is set to ‘1’, the GPS-position 
                    #           (longitude, latitude) is recorded in this
                    #           file, otherwise not.
                    #  • Bit 2: When this bit is set to ‘1’, the temperature 
                    #           data is recorded in this file, otherwise not. 
                    #  • Bit 3: When this bit is set to ‘1’, the receiver 
                    #           stability data is recorded in this file,
                    #           otherwise not.
                    #  • Bit 4: When this bit is set to ‘1’, the remaining 
                    #           flash memory is recorded in this file,
                    #           otherwise not.
                    #  • Bit 5: When this bit is set to ‘1’, quality flags are 
                    #           recorded in this file, otherwise not.
                    #  • Bit 6: When this bit is set to ‘1’, status flags are 
                    #           recorded in this file, otherwise not.
                't_obs': t_obs,
                'hkd_alarm': hkd_alarm, #Alarm
                'hkd_lon': hkd_lon,
                'hkd_lat': hkd_lat,
                'hkd_amb': hkd_amb,
                'hkd_sta': hkd_sta,
                'hkd_fsh': hkd_fsh,
                'hkd_qlt': hkd_qlt, #Quality Flags
                'hkd_sts': hkd_sts} #Status Flags

    #
    # A20: ABSCAL.HIS: Absolute Calibration History File (p.156, RPG_MWR_STD_Software_Manual 2015)
    #
    def read_abscal_his(self,f,*args, **kwargs):

        if not f: print("Missing argument FN, Please provide input filename.")
        if not os.path.isfile(f): 
            print('Input file is nonexists. Returnning...')
        print(kwargs)
        if not kwargs: skip = 0
        else: skip = kwargs["skip"]
        if not kwargs: eof = 0
        else: eof = kwargs["eof"]

        root = os.path.dirname(f)
        file = os.path.basename(f)
        fsze = os.path.getsize(f)

        t_ref = datetime.strptime('20010101000000', "%Y%m%d%H%M%S")
        t_obs = []
        cal_entlen = []
        cal_inst = []
        cal_r1caltype = []
        cal_r2caltype = []
        cal_r1time = []
        cal_r2time = []
        cal_r1tamb = []
        cal_r2tamb = []
        cal_r1pres = []
        cal_r2pres = []
        cal_r1hot = []
        cal_r2hot = []
        cal_r1cold = []
        cal_r2cold = []
        cal_r1freqn = []
        cal_r1freq = []
        cal_r2freqn = []
        cal_r2freq = []
        cal_flag = []
        cal_gain = []
        cal_noise = []
        cal_sysn = []
        cal_alpha = []

        j = 0

        with open(f, "rb") as f:
            cal_code      = struct.unpack('<i', f.read(4))[0]
            cal_n         = struct.unpack('<i', f.read(4))[0] #+ 635
            if eof > 0: 
                print(int((fsze - 8) / 420))
                cal_n = int((fsze - 8) / 420)
                print('cal_n =', cal_n)
            if skip > 0:
                for j in range(skip):
                    entlen = struct.unpack('<i', f.read(4))[0]
                    f.seek(entlen, 1)
            for i in range(cal_n - skip):
                cal_entlen.append(struct.unpack('<i', f.read(4))[0] )
                cal_inst.append(struct.unpack('<i', f.read(4))[0] )
                cal_r1caltype.append(struct.unpack('<i', f.read(4))[0] )
                cal_r2caltype.append(struct.unpack('<i', f.read(4))[0] )
                t = struct.unpack('<i', f.read(4))[0]
                cal_r1time.append( t_ref + timedelta(seconds=t) )
                t = struct.unpack('<i', f.read(4))[0]
                cal_r2time.append( t_ref + timedelta(seconds=t) )
                cal_r1tamb.append(struct.unpack('<f', f.read(4))[0] )
                cal_r2tamb.append(struct.unpack('<f', f.read(4))[0] )
                cal_r1pres.append(struct.unpack('<f', f.read(4))[0] )
                cal_r2pres.append(struct.unpack('<f', f.read(4))[0] )
                cal_r1hot.append(struct.unpack('<f', f.read(4))[0] )
                cal_r2hot.append(struct.unpack('<f', f.read(4))[0] )
                cal_r1cold.append(struct.unpack('<f', f.read(4))[0] )
                cal_r2cold.append(struct.unpack('<f', f.read(4))[0] )
                for vname in range(5): dummy = struct.unpack('<f', f.read(4))[0]
                #cal_r1freqn.append(struct.unpack('<i', f.read(4))[0] )
                dummy = struct.unpack('<i', f.read(4))[0]
                cal_r1freqn.append( 7 )
                #if cal_r1freqn[i] > 10: break  #Some file has unusual  no. in cal_r1freqn[i]
                tmp = []
                #for vname in range(cal_r1freqn[i]):
                for vname in range(7):
                    tmp.append(struct.unpack('<f', f.read(4))[0] )
                if i == 0: cal_r1freq = np.c_[tmp]
                else:      cal_r1freq = np.c_[cal_r1freq, tmp]
                #cal_r2freqn.append(struct.unpack('<i', f.read(4))[0] )
                dummy = struct.unpack('<i', f.read(4))[0]
                cal_r2freqn.append( 7 )
                tmp = []
                #for vname in range(cal_r2freqn[i]):
                for vname in range(7):
                    tmp.append(struct.unpack('<f', f.read(4))[0] )
                if i == 0: cal_r2freq = np.c_[tmp]
                else:      cal_r2freq = np.c_[cal_r2freq, tmp]
                tmp = []
                #for vname in range(cal_r1freqn[i] + cal_r2freqn[i]):
                for vname in range(7 + 7):
                    tmp.append(struct.unpack('<i', f.read(4))[0] )
                if i == 0: cal_flag = np.c_[tmp]
                else:      cal_flag = np.c_[cal_flag, tmp]
                tmp = []
                #for vname in range(cal_r1freqn[i] + cal_r2freqn[i]):
                for vname in range(7 + 7):
                    tmp.append(struct.unpack('<f', f.read(4))[0] )
                if i == 0: cal_gain = np.c_[tmp]
                else:      cal_gain = np.c_[cal_gain, tmp]
                tmp = []
                #for vname in range(cal_r1freqn[i] + cal_r2freqn[i]):
                for vname in range(7 + 7):
                    tmp.append(struct.unpack('<f', f.read(4))[0] )
                if i == 0: cal_noise = np.c_[tmp]
                else:      cal_noise = np.c_[cal_noise, tmp]
                tmp = []
                #for vname in range(cal_r1freqn[i] + cal_r2freqn[i]):
                for vname in range(7 + 7):
                    dummy = struct.unpack('<f', f.read(4))[0]
                    if (i == 1) and (vname == 11): 
                        print(i, vname, dummy)
                    tmp.append( dummy )
                    #tmp.append(struct.unpack('<f', f.read(4))[0] )
                if i == 0: cal_sysn = np.c_[tmp]
                else:      cal_sysn = np.c_[cal_sysn, tmp]
                tmp = []
                #for vname in range(cal_r1freqn[i] + cal_r2freqn[i]):
                for vname in range(7 + 7):
                    tmp.append(struct.unpack('<f', f.read(4))[0] )
                if i == 0: cal_alpha = np.c_[tmp]
                else:      cal_alpha = np.c_[cal_alpha, tmp]

        f.close()

        return {'cal_code': cal_code,           #HIS-File Code (=39583209)
                'cal_n': cal_n,                 #Number of samples
                'cal_entlen' : cal_entlen,      #Length of entry #1 in bytes
                'cal_inst' : cal_inst,          #1=TEMPRO, 2=HUMPRO, 3=HATPRO, 4=RPG-15-90, 5=LHATPRO, 6=RPG-150-90,
                                                #7= RPG-36-90, 8=RPG-LWP, 9=RPG-LWPU90, 10 =RPG-DP150-90, 11=HALO-KV, 
                                                #12=HALO-183, 13=HALO-119-90
                'cal_r1caltype' : cal_r1caltype,#Calibration type receiver 1, entry #1 
                                                #(0: no calibration, 1: Abs. Cal. With LN, 2:Skydip calibration)
                'cal_r2caltype' : cal_r2caltype,#Calibration type receiver 2, entry #1 
                                                #(0: no calibration, 1: Abs. Cal. With LN, 2:Skydip calibration)
                'cal_r1time' : cal_r1time,      #Time of calibration receiver 1 , entry #1 (# of sec. since 1.1.2001)
                'cal_r2time' : cal_r2time,      #Time of calibration receiver 2 , entry #1 (# of sec. since 1.1.2001)
                'cal_r1tamb' : cal_r1tamb,      #Ambient temperature receiver 1, entry #n [K]
                'cal_r2tamb' : cal_r2tamb,      #Ambient temperature receiver 2, entry #n [K]
                'cal_r1pres' : cal_r1pres,      #Barom. pressure receiver 1, entry #n [mbar]
                'cal_r2pres' : cal_r2pres,      #Barom. pressure receiver 2, entry #n [mbar]
                'cal_r1hot' : cal_r1hot,        #Hotload temp. receiver 1, entry #n [K]
                'cal_r2hot' : cal_r2hot,        #Hotload temp. receiver 2, entry #n [K]
                'cal_r1cold' : cal_r1cold,      #Coldload temp. receiver 1, entry #n [K]
                'cal_r2cold' : cal_r2cold,      #Coldload temp. receiver 2, entry #n [K]
                'cal_r1freqn' : cal_r1freqn,    #Number of receiver 1 channels, entry #n
                'cal_r1freq' : cal_r1freq,      #Frequencies of receiver 1, entry #n
                'cal_r2freqn' : cal_r2freqn,    #Number of receiver 2 channels, entry #n
                'cal_r2freq' : cal_r2freq,      #Frequencies of receiver 2, entry #n
                'cal_flag' : cal_flag,          #Calibration flags for all channels, entry #n (0=not calibrated, 1=calibrated)
                'cal_gain' : cal_gain,          #Receiver gains for all channels, entry #n [V/K]
                'cal_noise' : cal_noise,        #Noise diode temperature for all channels, entry #n [K]
                'cal_sysn' : cal_sysn,          #System noise temperature for all channels, entry #1 [K]
                'cal_alpha' : cal_alpha}        #Non-linearity factors for all channels, entry #1

    #
    # A21: LV0: Level Zero (Detector Voltages) Files (p.158, RPG_MWR_STD_Software_Manual 2015)
    #
    def read_lv0(self,f,*args):

        if not f: print("Missing argument FN, Please provide input filename.")
        if not os.path.isfile(f): 
            print('Input file is nonexists. Returnning...')

        root = os.path.dirname(f)
        file = os.path.basename(f)

        t_ref = datetime.strptime('20010101000000', "%Y%m%d%H%M%S")
        t_obs = []
        lv0_freq = []
        lv0_irwvl = []
        lv0_alpha = []
        lv0_delt = []
        lv0_t = []
        lv0_elv = []
        lv0_azm = []
        lv0_tambmst = []
        lv0_dflagmst = []
        lv0_tambslv = []
        lv0_dflagslv = []
        lv0_t_env = []
        lv0_press = []
        lv0_humid = []
        #lv0_irtmp = []
        with open(f, "rb") as f:
            lv0_code      = struct.unpack('<i', f.read(4))[0]
            lv0_n         = struct.unpack('<i', f.read(4))[0]
            lv0_idmst     = struct.unpack('<i', f.read(4))[0]
            lv0_idslv     = struct.unpack('<i', f.read(4))[0]
            lv0_timeref   = struct.unpack('<i', f.read(4))[0]
            lv0_freqn     = struct.unpack('<i', f.read(4))[0]
            for vname in range(lv0_freqn):
                lv0_freq.append(struct.unpack('<f', f.read(4))[0] )
            lv0_irwvln    = struct.unpack('<i', f.read(4))[0]
            for vname in range(lv0_irwvln):
                lv0_irwvl.append(struct.unpack('<f', f.read(4))[0] )
            lv0_lon       = struct.unpack('<f', f.read(4))[0]
            lv0_lat       = struct.unpack('<f', f.read(4))[0]
            for vname in range(lv0_freqn):
                lv0_alpha.append(struct.unpack('<f', f.read(4))[0] )
            for vname in range(lv0_freqn):
                lv0_delt.append(struct.unpack('<f', f.read(4))[0] )
            for i in range(lv0_n):
                t = struct.unpack('<i', f.read(4))[0]
                lv0_t.append( t_ref + timedelta(seconds=t) )
                #rf = f.read(1) # Dummy
                tmp = []
                for vname in range(lv0_freqn):
                    tmp.append(struct.unpack('<f', f.read(4))[0] )
                if i == 0: lv0_ud = np.c_[tmp]
                else:      lv0_ud = np.c_[lv0_ud, tmp]
                lv0_elv.append(struct.unpack('<f', f.read(4))[0] )
                lv0_azm.append(struct.unpack('<f', f.read(4))[0] )
                lv0_tambmst.append(struct.unpack('<f', f.read(4))[0] )
                lv0_dflagmst.append(struct.unpack('<i', f.read(4))[0] )

                # Status Flags:
                #
                #• Bit 1-7: status flags for channel 1 to 7 of the humidity profiler receiver. 
                #  When a bit is set ‘1’, the corresponding channel is ok, otherwise the channel 
                #  has a malfunction.
                #• Bit 8: not used
                #• Bit 9-15: status flags for channel 1 to 7 of the temperature profiler receiver. 
                #  When a bit is set ‘1’, the corresponding channel is ok, otherwise the channel 
                #  has a malfunction.
                #• Bit 16: not used
                #• Bit 17: rain flag. ‘1’ means raining, ‘0’ = no rain
                #• Bit 18: dew blower speed status. ‘1’ = high speed mode, ‘0’ = low speed mode
                #• Bit 19: BL-mode flag. ‘1’ = boundary layer scanning active, ‘0’ = BL-mode not active
                #• Bit 20: ‘1’ = sky tipping calibration running, ‘0’ = not active
                #• Bit 21: ‘1’ = gain calibration running (using internal ambient target), ‘0’ = not active
                #• Bit 22: ‘1’ = noise calibration running, ‘0’ = not active
                #• Bit 23: ‘1’ = noise diode of humidity profiler ok, ‘0’ = noise diode not working
                #• Bit 24: ‘1’ = noise diode of temperature profiler ok, ‘0’ = noise diode not working
                #• Bits25,26:receiver1(humidityprofiler)thermalstability.‘0’=unknown,notenoughdata
                #  samples recorded yet, ‘1’ = stability ok, ‘2’ = not sufficiently stable
                #• Bits27,28:receiver2(temperatureprofiler)thermalstability.‘0’=unknown,notenough
                #  data samples recorded yet, ‘1’ = stability ok, ‘2’ = not sufficiently stable
                #• Bit 29: power failure flag. ‘1’ = a power failure has occurred recently. When a 
                #  new MDF has been started automatically after a power failure, the ‘1’ flag is kept 
                #  for 1000 seconds and switching back to ‘0’ afterwards. ‘0’ = no power failure occurred.
                #• Bit 30: ambient target stability: Some radiometers are using two ambient target 
                #  temperature sensors for monitoring the target’s physical temperature. When the 
                #  temperature readings of these two sensors differ by more than 0.3 K, the flag turns to
                #  ‘1’. ‘0’ = sensors ok.
                #• Bit 31: noise diode status: ‘0’ = noise diode is turned off for the current sample, 
                #  ‘1’ = noise diode is turned on for the current sample.

                if lv0_idslv != 0:
                    lv0_tambslv.append(struct.unpack('<f', f.read(4))[0] )
                    lv0_dflagslv.append(struct.unpack('<i', f.read(4))[0] )
                else:
                    lv0_tambslv.append( [] )
                    lv0_dflagslv.append( [] )
                tmp = []
                for vname in range(lv0_freqn):
                    tmp.append(struct.unpack('<f', f.read(4))[0] )
                if i == 0: lv0_gain = np.c_[tmp]
                else:      lv0_gain = np.c_[lv0_gain, tmp]
                tmp = []
                for vname in range(lv0_freqn):
                    tmp.append(struct.unpack('<f', f.read(4))[0] )
                if i == 0: lv0_sysn = np.c_[tmp]
                else:      lv0_sysn = np.c_[lv0_sysn, tmp]
                tmp = []
                for vname in range(lv0_freqn):
                    tmp.append(struct.unpack('<f', f.read(4))[0] )
                if i == 0: lv0_nd = np.c_[tmp]
                else:      lv0_nd = np.c_[lv0_nd, tmp]
                lv0_t_env.append(struct.unpack('<f', f.read(4))[0] )
                lv0_press.append(struct.unpack('<f', f.read(4))[0] )
                lv0_humid.append(struct.unpack('<f', f.read(4))[0] )
                tmp = []
                #lv0_irtmp.append(struct.unpack('<f', f.read(4))[0] )
                for vname in range(lv0_irwvln):
                    tmp.append(struct.unpack('<f', f.read(4))[0] )
                if i == 0: lv0_irtmp = np.c_[tmp]
                else:      lv0_irtmp = np.c_[lv0_irtmp, tmp]

        f.close()

        return {'lv0_code': lv0_code,           #LV0-File Code (=111112)
                'lv0_n': lv0_n,                 #Number of samples
                'lv0_idmst': lv0_idmst,         #ID number of Master Radiometer
                'lv0_idslv': lv0_idslv,         #ID number of Slave Radiometer
                'lv0_timeref': lv0_timeref,     #Time Reference (0=Local, 1=UTC)
                'lv0_freqn': lv0_freqn,         #Number of frequencies
                'lv0_freq': lv0_freq,           #Frequencies [GHz]
                'lv0_irwvln': lv0_irwvln,       #Number of IRRs
                'lv0_irwvl': lv0_irwvl,         #IRR wavelengths [micro m]
                'lv0_lon': lv0_lon,             #GPS longitude (refer to FN (3), HKD-files)
                'lv0_lat': lv0_lat,             #GPS latitude (refer to FN (3), HKD-files)
                'lv0_alpha': lv0_alpha,         #Alpha calibration parameters
                'lv0_delt': lv0_delt,           #DelT calibration parameters [K]
                'lv0_t': lv0_t,                 #Time of sample n (# of sec. since 2001.1.1)
                'lv0_ud': lv0_ud,               #Detector Voltages [V] of sample n
                'lv0_elv': lv0_elv,             #Elevation Angle [°] of sample n
                'lv0_azm': lv0_azm,             #Azimuth Angle [°] of sample n
                'lv0_tambmst': lv0_tambmst,     #Black Body Temperature [K] of Master radiometer, sample n
                'lv0_dflagmst': lv0_dflagmst,   #Digital Flags of Master radiometer, sample n, refer to FN (5) of HKD-files
                'lv0_tambslv': lv0_tambslv,     #Black Body Temperature [K] of Slave radiometer, sample n (only if SlaveID ≠ 0)
                'lv0_dflagslv': lv0_dflagslv,   #Digital Flags of Slave radiometer, sample n, refer to FN (5) of HKD-files (only if SlaveID ≠ 0)
                'lv0_gain': lv0_gain,           #Gain calibration parameters [V/K], sample n
                'lv0_sysn': lv0_sysn,           #System Noise Temperature calibration parameters Tsys [K], sample n
                'lv0_nd': lv0_nd,               #Noise Diode Temperature calibration parameters Tn [K], sample n
                'lv0_t_env': lv0_t_env,         #Environmental Temperature [K] of sample n
                'lv0_press': lv0_press,         #Barometric Pressure [mbar] of sample n
                'lv0_humid': lv0_humid,         #Relative Humidity [%] of sample n
                'lv0_irtmp': lv0_irtmp}         #Infrared Radiometer Temperatures [°C] of sample n

    #
    # A22: TRK: Satellite Tracking File (p.163, RPG_MWR_STD_Software_Manual 2015)
    #

    #
    # ??: ABSCAL.CLB: Absolute Calibration File (p.???, RPG_MWR_STD_Software_Manual 2015)
    #
    def read_test(self,f,*args):

        if not f: print("Missing argument FN, Please provide input filename.")
        if not os.path.isfile(f): 
            print('Input file is nonexists. Returnning...')

        root = os.path.dirname(f)
        file = os.path.basename(f)

        t_ref = datetime.strptime('20010101000000', "%Y%m%d%H%M%S")
        t_obs = []
        test_r1time = []
        test_r2time = []
        test_alt = []
        test_unknown = []
        test_r1freq = []
        test_r2freq = []
        test_flag1 = []
        test_flag2 = []
        test_noise = []
        test_sysn = []
        test_alpha = []
        #test_18 = []

        with open(f, "rb") as f:
            test_code      = struct.unpack('<i', f.read(4))[0]
            test_n         = struct.unpack('<i', f.read(4))[0]
            test_min    = struct.unpack('<f', f.read(4))[0]
            test_max    = struct.unpack('<f', f.read(4))[0]
            t = struct.unpack('<i', f.read(4))[0]
            test_r1time.append( t_ref + timedelta(seconds=t) )
            t = struct.unpack('<i', f.read(4))[0]
            test_r2time.append( t_ref + timedelta(seconds=t) )
            test_altn         = struct.unpack('<i', f.read(4))[0]
            for vname in range(test_altn):
                test_alt.append(struct.unpack('<i', f.read(4))[0] )

            rf = f.read(1) # Dummy

            for vname in range(test_altn):
                test_unknown.append(struct.unpack('<f', f.read(4))[0] )
            # t = struct.unpack('<i', f.read(4))[0]
            # test_r1time.append( t_ref + timedelta(seconds=t) )
            # #test_3         = struct.unpack('<i', f.read(4))[0]
            # t = struct.unpack('<i', f.read(4))[0]
            # test_r2time.append( t_ref + timedelta(seconds=t) )
            # #test_4         = struct.unpack('<f', f.read(4))[0]
            # test_r1tamb1         = struct.unpack('<f', f.read(4))[0]
            # test_r2tamb1         = struct.unpack('<f', f.read(4))[0]
            # test_r1press         = struct.unpack('<f', f.read(4))[0]
            # test_r2press         = struct.unpack('<f', f.read(4))[0]
            # test_r1tamb2         = struct.unpack('<f', f.read(4))[0]
            # test_r2tamb2         = struct.unpack('<f', f.read(4))[0]
            # test_r1humid         = struct.unpack('<f', f.read(4))[0]
            # test_r2humid         = struct.unpack('<f', f.read(4))[0]
            # for vname in range(5):
            #     test_unknown.append(struct.unpack('<f', f.read(4))[0] )
            # test_r1freqn        = struct.unpack('<i', f.read(4))[0]
            # for vname in range(test_r1freqn):
            #     test_r1freq.append(struct.unpack('<f', f.read(4))[0] )
            # test_r2freqn        = struct.unpack('<i', f.read(4))[0]
            # for vname in range(test_r2freqn):
            #     test_r2freq.append(struct.unpack('<f', f.read(4))[0] )
            # for vname in range(test_r1freqn + test_r2freqn):
            #     test_flag1.append(struct.unpack('<i', f.read(4))[0] )
            # for vname in range(test_r1freqn + test_r2freqn):
            #     test_flag2.append(struct.unpack('<i', f.read(4))[0] )
            # for vname in range(test_r1freqn + test_r2freqn):
            #     test_noise.append(struct.unpack('<f', f.read(4))[0] )
            # for vname in range(test_r1freqn + test_r2freqn):
            #     test_sysn.append(struct.unpack('<f', f.read(4))[0] )
            # for vname in range(test_r1freqn + test_r2freqn):
            #     test_alpha.append(struct.unpack('<f', f.read(4))[0] )

        f.close()

        return {'test_code': test_code,           #LV0-File Code (=111112)
                'test_n': test_n,                 #Number of samples
                'test_min': test_min,                 #Number of samples
                'test_max': test_max,                 #Number of samples
                'test_r1time': test_r1time,                 #Number of samples
                'test_r2time': test_r2time,                 #Number of samples
                'test_altn': test_altn,                 #Number of samples
                'test_alt': test_alt,                 #Number of samples
                # 'test_r1tamb1': test_r1tamb1,                 #Number of samples
                # 'test_r2tamb1': test_r2tamb1,                 #Number of samples
                # 'test_r1press': test_r1press,                 #Number of samples
                # 'test_r2press': test_r2press,                 #Number of samples
                # 'test_r1tamb2': test_r1tamb2,                 #Number of samples
                # 'test_r2tamb2': test_r2tamb2,                 #Number of samples
                # 'test_r1humid': test_r1humid,                 #Number of samples
                # 'test_r2humid': test_r2humid,                 #Number of samples
                'test_unknown': test_unknown}                 #Number of samples
                # 'test_r1freqn': test_r1freqn,
                # 'test_r1freq': test_r1freq,
                # 'test_r2freqn': test_r2freqn,
                # 'test_r2freq': test_r2freq,
                # 'test_flag1': test_flag1,
                # 'test_flag2': test_flag2,
                # 'test_noise': test_noise,
                # 'test_sysn': test_sysn,
                # 'test_alpha': test_alpha}

    #
    # ??: ABSCAL.CLB: Absolute Calibration File (p.???, RPG_MWR_STD_Software_Manual 2015)
    #
    def read_abscal_clb(self,f,*args):

        if not f: print("Missing argument FN, Please provide input filename.")
        if not os.path.isfile(f): 
            print('Input file is nonexists. Returnning...')

        root = os.path.dirname(f)
        file = os.path.basename(f)

        t_ref = datetime.strptime('20010101000000', "%Y%m%d%H%M%S")
        t_obs = []
        cal_r1time = []
        cal_r2time = []
        cal_unknown = []
        cal_r1freq = []
        cal_r2freq = []
        cal_flag1 = []
        cal_flag2 = []
        cal_noise = []
        cal_sysn = []
        cal_alpha = []
        #cal_18 = []

        with open(f, "rb") as f:
            cal_code      = struct.unpack('<i', f.read(4))[0]
            cal_n         = struct.unpack('<i', f.read(4))[0]
            cal_r1flag    = struct.unpack('<i', f.read(4))[0]
            cal_r2flag    = struct.unpack('<i', f.read(4))[0]
            t = struct.unpack('<i', f.read(4))[0]
            cal_r1time.append( t_ref + timedelta(seconds=t) )
            #cal_3         = struct.unpack('<i', f.read(4))[0]
            t = struct.unpack('<i', f.read(4))[0]
            cal_r2time.append( t_ref + timedelta(seconds=t) )
            #cal_4         = struct.unpack('<f', f.read(4))[0]
            cal_r1tamb1         = struct.unpack('<f', f.read(4))[0]
            cal_r2tamb1         = struct.unpack('<f', f.read(4))[0]
            cal_r1press         = struct.unpack('<f', f.read(4))[0]
            cal_r2press         = struct.unpack('<f', f.read(4))[0]
            cal_r1tamb2         = struct.unpack('<f', f.read(4))[0]
            cal_r2tamb2         = struct.unpack('<f', f.read(4))[0]
            cal_r1humid         = struct.unpack('<f', f.read(4))[0]
            cal_r2humid         = struct.unpack('<f', f.read(4))[0]
            for vname in range(5):
                cal_unknown.append(struct.unpack('<f', f.read(4))[0] )
            cal_r1freqn        = struct.unpack('<i', f.read(4))[0]
            for vname in range(cal_r1freqn):
                cal_r1freq.append(struct.unpack('<f', f.read(4))[0] )
            cal_r2freqn        = struct.unpack('<i', f.read(4))[0]
            for vname in range(cal_r2freqn):
                cal_r2freq.append(struct.unpack('<f', f.read(4))[0] )
            for vname in range(cal_r1freqn + cal_r2freqn):
                cal_flag1.append(struct.unpack('<i', f.read(4))[0] )
            for vname in range(cal_r1freqn + cal_r2freqn):
                cal_flag2.append(struct.unpack('<i', f.read(4))[0] )
            for vname in range(cal_r1freqn + cal_r2freqn):
                cal_noise.append(struct.unpack('<f', f.read(4))[0] )
            for vname in range(cal_r1freqn + cal_r2freqn):
                cal_sysn.append(struct.unpack('<f', f.read(4))[0] )
            for vname in range(cal_r1freqn + cal_r2freqn):
                cal_alpha.append(struct.unpack('<f', f.read(4))[0] )

        f.close()

        return {'cal_code': cal_code,           #LV0-File Code (=111112)
                'cal_n': cal_n,                 #Number of samples
                'cal_r1flag': cal_r1flag,                 #Number of samples
                'cal_r2flag': cal_r2flag,                 #Number of samples
                'cal_r1time': cal_r1time,                 #Number of samples
                'cal_r2time': cal_r2time,                 #Number of samples
                'cal_r1tamb1': cal_r1tamb1,                 #Number of samples
                'cal_r2tamb1': cal_r2tamb1,                 #Number of samples
                'cal_r1press': cal_r1press,                 #Number of samples
                'cal_r2press': cal_r2press,                 #Number of samples
                'cal_r1tamb2': cal_r1tamb2,                 #Number of samples
                'cal_r2tamb2': cal_r2tamb2,                 #Number of samples
                'cal_r1humid': cal_r1humid,                 #Number of samples
                'cal_r2humid': cal_r2humid,                 #Number of samples
                'cal_unknown': cal_unknown,                 #Number of samples
                'cal_r1freqn': cal_r1freqn,
                'cal_r1freq': cal_r1freq,
                'cal_r2freqn': cal_r2freqn,
                'cal_r2freq': cal_r2freq,
                'cal_flag1': cal_flag1,
                'cal_flag2': cal_flag2,
                'cal_noise': cal_noise,
                'cal_sysn': cal_sysn,
                'cal_alpha': cal_alpha}

    #
    # MainFormSize: Read screen size of the operating SW
    #
    def read_MainFormSize(self,f,*args):

        if not f: print("Missing argument FN, Please provide input filename.")
        if not os.path.isfile(f): 
            print('Input file is nonexists. Returnning...')

        root = os.path.dirname(f)
        file = os.path.basename(f)

        brt_freq = []
        with open(f, "rb") as f:
            mfs_code    = struct.unpack('<I', f.read(4))[0]
            mfs_horz    = struct.unpack('<I', f.read(4))[0]
            mfs_vert    = struct.unpack('<I', f.read(4))[0]
        f.close()

        return {'mfs_code': mfs_code,
                'mfs_horz': mfs_horz,
                'mfs_vert': mfs_vert}

    #
    # MainFormSize: Write screen size of the operating SW
    #
    def write_MainFormSize(self,f,h,v,*args):

        if not f: print("Missing argument FN, Please provide input filename.")
        if not os.path.isfile(f): 
            print('Input file is nonexists. Returnning...')
        if not h: h = 1024
        if not v: v = 768

        fw = open(f,'wb')

        fw.write(struct.pack("=I", 9))
        fw.write(struct.pack("=I", h))
        fw.write(struct.pack("=I", v))
        fw.close()

# ================================================================================================
# ================================================================================================
# ================================================================================================

if __name__ == '__main__':    # 프로그램의 시작점일 때만 아래 코드 실행

    # Sample code
    import pandas as pd
    import sys, os
    from pandas import Series
    rpg = RPGReader()

    '''
    #
    # Test 'read_cal_log' function
    #

    root = "/Users/reno/Downloads/210819_cal_history/CAL.LOGs"
    print("Reading file... ", "CAL1.LOG")
    df = rpg.read_cal_log( os.path.join(root, "CAL1.LOG") )

    print(df)
    '''

    '''
    #
    # Read multiple HIS files
    #

    directory = "/Users/reno/Downloads/210819_cal_history"

    file = []
    name = []
    for root, dirs, files in os.walk(directory):
        for f in files:
            if f.endswith('.HIS'):
                file += [f]
                temp = f.split(".")
                name += [ temp[0] ]


    for j in range(len(file)):

        print("Reading file... ", file[j])
        kwargs = {"skip":0, "eof":1}
        df = rpg.read_abscal_his( os.path.join(root, file[j]), **kwargs )

        df_elements = [   'entlen',      'inst', 'r1caltype', 'r2caltype',    'r1time', 
                        'r2time',    'r1tamb',    'r2tamb',    'r1pres',    'r2pres', 
                        'r1hot',     'r2hot',    'r1cold',    'r2cold',   'r1freqn', 
                        'r1freq',   'r2freqn',    'r2freq',      'flag',      'gain',
                        'noise',      'sysn',     'alpha']
        df_hdrtypes = [          0,           0,           0,           0,          0,
                                0,           0,           0,           0,          0,
                                0,           0,           0,           0,          0,
                                1,           0,           2,           3,          3,
                                3,           3,           3]
        receiver_1    = ["ch01", "ch02", "ch03", "ch04", "ch05", "ch06", "ch07"]
        receiver_2    = ["ch08", "ch09", "ch10", "ch11", "ch12", "ch13", "ch14"] 

        data = []
        for i in range(len(df_elements)):
            if i == 0: 
                data = pd.DataFrame(df['cal_entlen'], columns=[df_elements[0]])
            else:
                if df_hdrtypes[i] == 0:
                    data[df_elements[i]] = df[''.join(['cal_', df_elements[i]])]
                elif df_hdrtypes[i] == 1:
                    data[ [df_elements[i] + '_' + sub for sub in receiver_1] ] = df[ ''.join(['cal_', df_elements[i]]) ].T
                elif df_hdrtypes[i] == 2:
                    data[ [df_elements[i] + '_' + sub for sub in receiver_2] ] = df[ ''.join(['cal_', df_elements[i]]) ].T
                else:
                    data[ [df_elements[i] + '_' + sub for sub in [*receiver_1, *receiver_2]] ] = df[ ''.join(['cal_', df_elements[i]]) ].T

        fout = '.'.join([name[j], "csv"])
        print(fout, df["cal_n"])
        data.to_csv( fout )
    '''

    #
    # Read a single HIS file
    #

    root = "/Users/reno/Downloads/210819_cal_history"
    print("Reading file... ", "ABSCAL1_5.HIS")
    kwargs = {"skip":3621, "eof":1}
    df = rpg.read_abscal_his( os.path.join(root, "ABSCAL1_5.HIS"), **kwargs )

    print('No of records: ', df["cal_n"])

    df_elements = [   'entlen',      'inst', 'r1caltype', 'r2caltype',    'r1time', 
                    'r2time',    'r1tamb',    'r2tamb',    'r1pres',    'r2pres', 
                    'r1hot',     'r2hot',    'r1cold',    'r2cold',   'r1freqn', 
                    'r1freq',   'r2freqn',    'r2freq',      'flag',      'gain',
                    'noise',      'sysn',     'alpha']
    df_hdrtypes = [          0,           0,           0,           0,          0,
                            0,           0,           0,           0,          0,
                            0,           0,           0,           0,          0,
                            1,           0,           2,           3,          3,
                            3,           3,           3]
    receiver_1    = ["ch01", "ch02", "ch03", "ch04", "ch05", "ch06", "ch07"]
    receiver_2    = ["ch08", "ch09", "ch10", "ch11", "ch12", "ch13", "ch14"] 

    data = []
    for i in range(len(df_elements)):
        if i == 0: 
            data = pd.DataFrame(df['cal_entlen'], columns=[df_elements[0]])
        else:
            if df_hdrtypes[i] == 0:
                data[df_elements[i]] = df[''.join(['cal_', df_elements[i]])]
            elif df_hdrtypes[i] == 1:
                data[ [df_elements[i] + '_' + sub for sub in receiver_1] ] = df[ ''.join(['cal_', df_elements[i]]) ].T
            elif df_hdrtypes[i] == 2:
                data[ [df_elements[i] + '_' + sub for sub in receiver_2] ] = df[ ''.join(['cal_', df_elements[i]]) ].T
            else:
                data[ [df_elements[i] + '_' + sub for sub in [*receiver_1, *receiver_2]] ] = df[ ''.join(['cal_', df_elements[i]]) ].T

    print(data)
    print(data['sysn_ch11'])
    #fout = '.'.join([name[j], "csv"])
    #print(fout, df["cal_n"])
    #data.to_csv( fout )

    '''
    ## make csv file from each dataframe, please fill the data_name 
    globals()["cal_" + str(r1_data_name)].to_csv(daou + "cal_%s.csv" % r1_data_name)
    '''