"""Create Stratification Files for the 79NG Fjord GETM Setup.

Script by Markus Reinert (IOW, 2020–2023, https://orcid.org/0000-0002-3761-8029).
"""

import xml.etree.ElementTree as ET


XML_file = "configuration.xml"

print(f"Loading settings from {XML_file!r}.")
XML_tree = ET.parse(XML_file)
XML_root = XML_tree.getroot()
assert XML_root.tag == "scenario", "root-element of XML-file is not 'scenario'."


# Extract the stratification from the XML file, defined by layers of
# given temperatures (T) and salinities (S) at given depths (-z).
# Between these z-levels, T and S are linearly interpolated.
stratification = []
XML_stratification = XML_root.find("fjord/stratification")
for level in XML_stratification:
    assert level.tag == "level",\
        f"all elements in stratification must be named 'level', not {child.tag!r}"
    stratification.append([float(level.get(var)) for var in "zST"])
stratification.sort(key=lambda level: level[0], reverse=True)

z_discrete = [level[0] for level in stratification]
S_discrete = [level[1] for level in stratification]
T_discrete = [level[2] for level in stratification]


# Write file with salinity profile
filename = "model/salt_profile.txt"
with open(filename, "w") as f:
    f.write(f"{len(z_discrete)}\n")
    for z_val, S_val in zip(z_discrete, S_discrete):
        f.write(f"{z_val:6} {S_val:3}\n")
print(f"Saved initial salinity stratification as {filename!r}.")


# Write file with temperature profile
filename = "model/temp_profile.txt"
with open(filename, "w") as f:
    f.write(f"{len(z_discrete)}\n")
    for z_val, T_val in zip(z_discrete, T_discrete):
        f.write(f"{z_val:6} {T_val:5}\n")
print(f"Saved initial temperature stratification as {filename!r}.")
