import xml.etree.ElementTree as ET

class Xml:
    def format(self, data, headers, output_file):
        root = ET.Element("Uczestnicy")
        for row in data:
            participant = ET.SubElement(root, "Uczestnik")
            for header, value in zip(headers, row):
                ET.SubElement(participant, header).text = value
        tree = ET.ElementTree(root)
        tree.write(output_file, encoding='utf-8', xml_declaration=True)
        print(f"Data exported to {output_file} in XML format.")
