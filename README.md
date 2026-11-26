# read_rpg

Python reader for the binary data files written by **RPG HATPRO** microwave radiometers (RPG Radiometer Physics GmbH).

Each reader decodes one file type byte-by-byte according to the format definitions in Appendix A of the *RPG MWR STD Software Manual* (2015 edition, p. 133 onward) and returns the contents as a Python `dict`.

This repository contains the scripts only. HATPRO data files are not included.

## Supported file types

Manual section and printed page number refer to the RPG MWR STD Software Manual (2015). "File code" is the integer given in the manual for the first four bytes. A reader raises `ValueError` when the code is not one it defines.

| Section | Extension | Content | Method | File code | Status |
|---|---|---|---|---|---|
| A1 (p.133) | `.LWP` | Liquid water path | `read_lwp` | 934501978 | Tested |
| A2 (p.133) | `.IWV` | Integrated water vapour | `read_iwv` | 594811068 | Tested |
| A3 (p.134) | `.ATN` | Atmospheric attenuation | `read_atn` | 7757564 | Tested |
| A4 (p.135) | `.BRT`, `.SPC` | Brightness temperature. Code 666667 is the same layout, used for SPC files | `read_brt` | 666666 / 666667 | Tested |
| A5a (p.135) / A5b (p.136) | `.MET` | Meteorological sensors (old and new format). The new format can add wind speed, wind direction and rain rate | `read_met` | 599658943 / 599658944 | Tested |
| A7 (p.137) | `.TPC` | Temperature profile, full troposphere | `read_tpc` | 780798065 | Tested |
| A8 (p.138) | `.TPB` | Temperature profile, boundary layer | `read_tpb` | 459769847 | Tested |
| A10(1) / A10(2) (p.139) | `.HPC` | Humidity profile. A10(2) adds a relative-humidity block | `read_hpc` | 117343672 / 117343673 | A10(2) tested |
| A11 (p.140) | `.LPR` | Liquid water profile | `read_lpr` | 4567 | Tested (2009 files) |
| A12a / A12b (p.141) | `.IRT` | Infrared radiometer temperatures (old and new format) | `read_irt` | 671112495 / 671112496 | Tested |
| A13b (p.143) | `.BLB` | Boundary-layer BT profiles (new format) | `read_blb` | 567845848 | Tested |
| A14 (p.144) | `.STA` | Stability indices | `read_sta` | 454532 | Tested |
| A15b (p.147) | `CAL.LOG` | Calibration log, new version | `read_cal_log` | 657645 | Not tested |
| A16 (p.151) | `.CBH` | Cloud base height | `read_cbh` | 67777499 | Tested |
| A17 (p.151) | `.BLH` | Boundary-layer height | `read_blh` | 1777786 | Tested |
| A18b (p.152) | `.VLT` | Channel voltages, new version | `read_vlt` | 362118747 | No sample file |
| A19 (p.154) | `.HKD` | Housekeeping data | `read_hkd` | 837854832 | Tested (NumPy 1.26 and 2.4) |
| A20 (p.156) | `ABSCAL.HIS` | Absolute calibration history | `read_abscal_his` | 39583209 | No sample file |
| A21b (p.160) | `.LV0` | Level-zero detector voltages (new format) | `read_lv0` | 111112 | Tested |
| — | `ABSCAL.CLB` | Absolute calibration file (layout inferred, not in the manual) | `read_abscal_clb` | — | Experimental |
| — | `MainFormSize` | Window size of the RPG operating software | `read_MainFormSize`, `write_MainFormSize` | — | Utility |

Not implemented: OLC (A6), WVL (A9), BLB old format (A13a, code 567845847), LV0 old format (A21a, code 111111), TRK (A22), BUFR (A23).

## Requirements

- Python 3 (developed with 3.11)
- `numpy` (the reader module; checked with 1.26 and 2.4)
- `pandas`, `matplotlib` (imported by `main.py`)
- `networkx`, `matplotlib` (only for `rpg_file_type_diagram.py`)

```bash
pip install numpy pandas matplotlib networkx
```

`modules/rpg_reader.py` needs only `numpy`.

## Usage

Run from the repository root so that `modules` can be imported.

```python
from modules.rpg_reader import RPGReader

rpg = RPGReader()
brt = rpg.read_brt("/path/to/220612.BRT")

print(brt["brt_freq"])          # channel frequencies [GHz]
print(brt["t_obs"][0])          # first sample time (datetime)
print(brt["brt_dat"].shape)     # (n_channels, n_samples)
```

Humidity profiles, infrared temperatures, and boundary-layer scans differ by file variant:

```python
hpc = rpg.read_hpc("/path/to/220612.HPC")
hpc["hpc_dat"]                  # absolute humidity [g/m^3], shape (n_levels, n_samples)
hpc["hpc_rh"]                   # relative humidity [%], same shape, for code 117343673
                                # None for A10(1), code 117343672

irt = rpg.read_irt("/path/to/220612.IRT")
irt["irt_dat"]                  # temperatures [°C], shape (n_channels, n_samples)
irt["irt_ang"]                  # elevation/azimuth code, new format (A12b) only
                                # empty for the old format (A12a, code 671112495)

blb = rpg.read_blb("/path/to/220612.BLB")
blb["blb_dat"].shape            # (n_freq, n_ang + 1, n_samples)
blb["blb_ang"]                  # angle value stored in the file
blb["blb_elv"], blb["blb_azm"]  # elevation and azimuth, degrees
blb["blb_dat"][:, -1, :]        # 0° surface temperature, one value per channel
```

`blb_elv` and `blb_azm` follow the manual coding `Ang = sign(El) * (|El| + 1000*Az)`. A plain elevation, such as 90, 30 or 4.2, is returned as that elevation with azimuth 0. A coded value such as 1267438.5 is 138.5° elevation and 267.4° azimuth.

Housekeeping flags use the manual's bit numbering. `hkd_select[N]` is bit N, and bit 1 is the least significant bit of the first byte of `HKDSelect`. Index 0 is unused. A bit value of 0 means that group was not stored; the corresponding entries are `None`.

### Return conventions

- Every method returns a `dict`. Keys carry the file-type prefix (`brt_n`, `tpc_alt`, …).
- `<type>_code` holds the file code from the header; `<type>_n` the number of samples.
- Times are stored in the file as seconds since 2001-01-01 00:00:00 and are returned as `datetime` objects in `t_obs` (`lv0_t` for LV0, `blh_t` for BLH).
- `<type>_timeref`: 1 = UTC, 0 = local time. BRT returns this as `brt_timeref` and BLB as `blb_timeref`.
- `<type>_retrieval` (LWP, IWV, ATN, TPC, TPB, HPC, LPR): 0 = linear regression, 1 = quadratic regression, 2 = neural network. ATN may also be 3 (Tmr).
- Multi-channel or multi-level data are NumPy arrays shaped `(n_channels or n_levels, n_samples)`. `blb_dat` is the exception: `(n_freq, n_ang + 1, n_samples)`.

### Example script

`main.py` reads one local day of HATPRO files and prints the file code and the returned keys. The directory is chosen by host name inside `main()`. Point `rpg_dir` at your own files before running:

```bash
python main.py
```

`rpg_file_type_diagram.py` draws the dependencies between HATPRO file types (LV0 → BRT → retrieved products) with `networkx`.

## Repository layout

```
read_rpg/
├── README.md
├── main.py                    # example driver; set rpg_dir to a local data directory
├── rpg_file_type_diagram.py   # diagram of file-type dependencies
└── modules/
    └── rpg_reader.py          # RPGReader class, one read_* method per file type
```

## Known issues

- A missing path raises `FileNotFoundError`. `write_MainFormSize` still creates its output file when the path is new.
- `read_abscal_clb` follows an inferred layout. The manual gives it no file code, so that method does not check one.
- `.ATS` files with code 7757565 are not read. On one 2023 day the record layout matches ATN with 132 frequencies, but that code is not in the 2015 manual.

## Reference

RPG Radiometer Physics GmbH, *RPG MWR STD Software Manual*, 2015, Appendix A: Data file formats (p. 133 ff.).

## Author

Reno Choi, Specube

Version history (from `modules/rpg_reader.py`):

- 0.1 (2018-09-08): HKD, BRT, TPC, HPC, IRT
- 0.2 (2020-04-04): LWP, IWV, MET, TPB, ATN
- 0.3 (2020-11-11): LPR, BLB, STA, CBH, BLH, VLT, ABSCAL.HIS, LV0
- 0.4 (2026-11-24): HPC relative-humidity block (A10(2)); HKD selection byte masked and read least-significant-bit first; BLB records hold `n_freq*(n_ang+1)` values; IRT old format (A12a); retrieval code 1 documented as quadratic regression; page comments aligned with the 2015 manual
- 0.5 (2026-11-24): plain BLB elevations stay elevations, and coded angles split into elevation and azimuth; `brt_timeref` and `blb_timeref`; a missing file raises `FileNotFoundError`; each documented reader rejects a file code it does not define; MET reads wind speed, wind direction and rain rate when those additional-sensor bits are set
