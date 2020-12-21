import csv
import glob
import xml.etree.ElementTree

OUTPUT_FILE = "merged.csv"

# final result: each entry corresponds to a dictionary
records_dicts = []

for xml_file in sorted(glob.glob("*.xml")):
    print("parsing {}".format(xml_file))
    tree = xml.etree.ElementTree.parse(xml_file)
    root = tree.getroot()
    assert root.tag == "ovidresults"

    # make sure the root has only one child: "records"
    root_children = list(iter(root))
    assert len(root_children) == 1
    records = root_children[0]
    assert records.tag == "records"

    # get number of records
    records_list = list(iter(records))
    print("{} records".format(len(records_list)))

    # parse the records
    for record in records_list:
        record_dict = {}
        assert record.tag == "record"

        # parse the fields of a record
        for field in record:
            assert field.tag == "F"

            assert "L" in field.attrib
            field_name = field.attrib["L"]

            # concatenate all field elements
            field_value = ""
            for field_element in field:
                assert field_element.tag == "T" or field_element.tag == "D"
                if field_element.text is not None:
                    field_value += field_element.text

                if field_element.tail is not None:
                    field_value += field_element.tail

            # store the field
            record_dict[field_name] = field_value.strip()
        records_dicts.append(record_dict)

print("{} records in total".format(len(records_dicts)))

# get the complete set of fields
fields = set()
for record_dict in records_dicts:
    for field in record_dict.keys():
        fields.add(field)

# print the result as csv
with open(OUTPUT_FILE, 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, sorted(fields))
    dict_writer.writeheader()
    dict_writer.writerows(records_dicts)

print("csv written to {}".format(OUTPUT_FILE))
