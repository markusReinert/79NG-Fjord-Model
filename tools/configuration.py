"""Class to handle the GETM configuration XML file.

By Markus Reinert (IOW, 2024, https://orcid.org/0000-0002-3761-8029).
"""

from xml.etree import ElementTree as ET


class Configuration:
    def __init__(self, path="configuration.xml"):
        print(f"Loading settings from {path!r}.")
        XML_tree = ET.parse(path)
        self.XML_root = XML_tree.getroot()
        assert self.XML_root.tag == "scenario", "root-element of XML-file is not 'scenario'."

    def get_element(self, variable_path):
        element = self.XML_root.find(variable_path)
        assert element is not None, f"no variable found in path {variable_path!r}."
        return element

    def get_text(self, variable_path):
        element = self.get_element(variable_path)
        return element.text

    def get_file_path(self, variable_path):
        filename = self.get_text(variable_path)
        return f"model/{filename}"
