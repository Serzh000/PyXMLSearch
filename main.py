import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
import time
from sys import argv

path = argv[1]
word = argv[2]


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def find_files(path, word):
    flag = False
    file_name = str(time.strftime("%Y%m%d-%H%M%S") + ".xml")
    output_file = open(file_name, "w", encoding="utf-8")
    out_root = ET.Element("data")
    for filename in os.listdir(path):
        if not filename.endswith(".xml"): continue
        fullname = os.path.join(path, filename)
        with open(fullname, "r", encoding="utf-8") as content:
            out_content = ET.Element("content")
            con = content.readlines()
            for line in con:
                if word in line:
                    flag = True
                    out_num = ET.Element("number")
                    out_num.text = u"".join(str(con.index(line) + 1).strip())
                    out_content.append(out_num)
                    out_text = ET.Element("text")
                    out_text.text = u"".join(str(line).strip())
                    out_content.append(out_text)
                if flag:
                    out_file = ET.Element("file", name=str(fullname).strip())
            if flag:
                out_file.append(out_content)
        if flag:
            out_root.append(out_file)
        flag = False
    print(prettify(out_root), file=output_file)
    print("File " + file_name + " created!")


def main():
    find_files(path, word)


if __name__ == '__main__':
    main()
