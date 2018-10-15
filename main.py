import csv
import xml.dom.minidom
import xml.etree.ElementTree as ET

ENPASS_FILE_NAME = 'Enpass.csv'


key_map = {
    "用户名称": "UserName",
    "电子邮件": "UserName",
    "密码": "Password",
    "网址": "URL",
    "Username": "UserName",
    "Email": "UserName"
}


def modify_fields_inplace(fields):
    is_user_name_replaced = False
    for idx, item in enumerate(fields):
        new_field = key_map.get(item, item)
        if new_field == 'UserName':
            if is_user_name_replaced:
                continue
            is_user_name_replaced = True
        fields[idx] = new_field

def create_entry(data):
    entry = ET.Element('Entry')
    for key, value in data:
        entry_item = ET.SubElement(entry, "String")
        ET.SubElement(entry_item, "Key").text = key
        ET.SubElement(entry_item, "Value").text = value
    return entry


keepass = ET.Element('KeePassFile')
root = ET.SubElement(keepass, "Root")
group = ET.SubElement(root, "Group")
root_name = ET.SubElement(group, "Name")
root_name.text = "Root"

with open(ENPASS_FILE_NAME, 'r') as F:
    csv_f = csv.reader(F)
    next(csv_f) # skip header
    for item in csv_f:
        title = item[0]
        note = item[-1]
        data = item[1:-1]
        fields = data[::2]
        values = data[1::2]
        fields.append('Title')
        values.append(title)
        fields.append('Notes')
        values.append(note)
        modify_fields_inplace(fields)
        data = zip(fields, values)
        entry = create_entry(data)
        group.append(entry)

xml = xml.dom.minidom.parseString(ET.tostring(keepass, 'utf-8'))
pretty_xml_as_string = xml.toprettyxml()

with open('Enpass2Keepass.xml', 'w') as F:
    F.write(pretty_xml_as_string)

