#!/usr/bin/env python3
'''
Created on 25 Jun 2024

@author: Reno Choi (renochoi@korea.kr)

HISTORY:
        0.1 (25-Jun-2024): Directed graph of relationships between HATPRO
                file types
        0.2 (24-Nov-2026): Header added, same form as modules/rpg_reader.py.
                Reader changes of this date (HPC relative humidity, HKD
                selection bits, full BLB scan, both IRT formats) are in
                RPGReader 0.4 and are not drawn here

DESCRIPTION: Draw a directed graph of RPG HATPRO file types.
        Edges run from the level-zero and housekeeping files toward the
        brightness temperatures and the retrieved products.

REFERENCE: RPG_MWR_STD_Software_Manual 2015, Appendix A (file formats).

'''
# Retry generating the diagram

import matplotlib.pyplot as plt
import networkx as nx

# Create a directed graph
G = nx.DiGraph()

# Add nodes
nodes = [
    "LV0 (Detector Voltages)",
    "HKD (Housekeeping Data)",
    "BRT (Brightness Temperature)",
    "IRT (Infrared Radiometer Temperatures)",
    "ATN (Atmospheric Attenuation)",
    "LWP (Liquid Water Path)",
    "IWV (Integrated Water Vapour)",
    "LPR (Liquid Water Profile)",
    "CBH (Cloud Base Height)",
    "TPC (Temperature Profile Chart, Full Trop.)",
    "TPB (Temperature Profile Chart, Boundary Layer)",
    "HPC (Humidity Profile Chart)",
    "BLB (Boundary Layer BT Profiles)",
    "STA (Stability Indices)",
    "BLH (Boundary Layer Height)",
    "VLT (Channel Voltage File)",
    "ABSCAL.HIS (Absolute Calibration History)"
]

G.add_nodes_from(nodes)

# Add edges representing relationships
edges = [
    ("LV0 (Detector Voltages)", "BRT (Brightness Temperature)"),
    ("LV0 (Detector Voltages)", "VLT (Channel Voltage File)"),
    ("VLT (Channel Voltage File)", "BRT (Brightness Temperature)"),
    ("HKD (Housekeeping Data)", "BRT (Brightness Temperature)"),
    ("BRT (Brightness Temperature)", "TPC (Temperature Profile Chart, Full Trop.)"),
    ("BRT (Brightness Temperature)", "TPB (Temperature Profile Chart, Boundary Layer)"),
    ("BRT (Brightness Temperature)", "HPC (Humidity Profile Chart)"),
    ("BRT (Brightness Temperature)", "BLB (Boundary Layer BT Profiles)"),
    ("IRT (Infrared Radiometer Temperatures)", "CBH (Cloud Base Height)"),
    ("BRT (Brightness Temperature)", "LWP (Liquid Water Path)"),
    ("BRT (Brightness Temperature)", "IWV (Integrated Water Vapour)"),
    ("BRT (Brightness Temperature)", "LPR (Liquid Water Profile)"),
    ("BRT (Brightness Temperature)", "STA (Stability Indices)"),
    ("BRT (Brightness Temperature)", "BLH (Boundary Layer Height)"),
    ("BRT (Brightness Temperature)", "ATN (Atmospheric Attenuation)")
]

G.add_edges_from(edges)

# Define the layout
pos = nx.spring_layout(G, seed=42)

# Draw the graph
plt.figure(figsize=(15, 10))
nx.draw(G, pos, with_labels=True, node_size=3000, node_color="lightblue", font_size=9, font_weight="bold", arrowsize=20, edge_color="gray")

# Draw edge labels
edge_labels = {edge: "" for edge in edges}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)

plt.title("Relationships Between HATPRO File Types")
plt.show()
