import xml.etree.ElementTree as ET

class Xml:
    def format(self, data, output_file):
        root = ET.Element("Uczestnicy")
        for row in data:
            participant = ET.SubElement(root, "Uczestnik")
            for idx, value in enumerate(row):
                ET.SubElement(participant, f"Pole{idx+1}").text = value
        tree = ET.ElementTree(root)
        tree.write(output_file, encoding='utf-8', xml_declaration=True)
        print(f"Dane wyeksportowane do pliku {output_file} w formacie XML.")
