"""Definitions that are useful to create Matplotlib figures.

By Markus Reinert (IOW, 2024–2026, https://orcid.org/0000-0002-3761-8029).
"""

# Conversion factor from inches to cm; useful to specify the figure size in cm
cm = 1 / 2.54

def extend_cbar(dmin, dmax, vmin, vmax):
    return {"extend": (
        "both" if dmin < vmin and dmax > vmax else
        "min" if dmin < vmin else
        "max" if dmax > vmax else
        "neither"
    )}
