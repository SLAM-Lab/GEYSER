from lxml import etree
from lxml.etree import _ElementTree, _Element
import json
import argparse
import os, pathlib


def parseIPXactBusDef2009Xilinx(
    file_path: str, out_file: str, dir_only: bool = False
) -> None:
    """
    parse the passed ipxact file for a interface definition and use it to generate a schema file
    """
    xml: _ElementTree = etree.parse(file_path)
    root_xml: _Element = xml.getroot()
    nsmap = root_xml.nsmap
    if (
        etree.QName(root_xml).namespace
        != "http://www.spiritconsortium.org/XMLSchema/SPIRIT/1685-2009"
    ):
        print("ERROR: only version 2009 of spirit is currently supported")
        exit(-1)
    if etree.QName(root_xml).localname != "abstractionDefinition":
        print("ERROR: spirit file does not only contain a component")
        exit(-1)
    if nsmap.get("xilinx") == None:
        print("Only support xilinx")
        exit(-1)
    # Start pulling the details that we are going to need

    i_name = root_xml.find("spirit:busType", namespaces=nsmap).xpath(
        "./@spirit:name", namespaces=nsmap
    )[0]

    vendor = root_xml.find("spirit:vendor", namespaces=nsmap).text

    # TODO make sure they are present

    print("Parsing interface {}".format(i_name))

    # First we need to get all of the ports for the ip and any necessary related details
    ports_xml = root_xml.find("spirit:ports", namespaces=nsmap)

    all_port_data = []
    for port_xml in ports_xml:
        if (
            port_xml.find("spirit:isPresent", namespaces=nsmap) != None
            and port_xml.find("spirit:isPresent", namespaces=nsmap).text == "0"
        ):
            # ignore this port it isn't real
            continue
        if port_xml.find("spirit:wire", namespaces=nsmap) == None:
            # Doesn't have a wire definition it is meant for TLM and can be ignored
            continue
        # get the actual port_name
        port_name = port_xml.find("spirit:logicalName", namespaces=nsmap).text.lower()
        wire_xml = port_xml.find("spirit:wire", namespaces=nsmap)
        # begin populating data
        port_data = {}
        port_data["name"] = port_name

        port_data["m_dir"] = (
            "input"
            if wire_xml.find("spirit:onMaster", namespaces=nsmap)
            .find("spirit:direction", namespaces=nsmap)
            .text
            == "in"
            else "output"
        )
        if (
            wire_xml.find("spirit:onMaster", namespaces=nsmap).find(
                "spirit:width", namespaces=nsmap
            )
            != None
        ):
            port_width = int(
                wire_xml.find("spirit:onMaster", namespaces=nsmap)
                .find("spirit:width", namespaces=nsmap)
                .text
            )
            port_data["width"] = port_width

        if wire_xml.find("spirit:defaultValue", namespaces=nsmap) != None:
            val = int(wire_xml.find("spirit:defaultValue", namespaces=nsmap).text)
            if val == 0:
                port_data["default"] = "tie_low"
            else:
                port_data["default"] = val
        all_port_data.append(port_data)
    # We now have all of the actual interface definitions we can start constructing the schema

    json_data = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "urn:interfaces:{}".format(i_name),
        "type": "object",
        "description": "{}, {} interface definition".format(vendor, i_name),
        "allOf": [
            {
                "properties": {
                    "type": {
                        "description": "The interface type",
                        "type": "string",
                        "const": "{}".format(i_name),
                    },
                    "multiconnect": {
                        "description": "Behavior if multiple interfaces connected",
                        "type": "string",
                        "default": "false",
                    },
                    "ports": {
                        "type": "object",
                        "description": "Contains ports and their definitions",
                        "properties": {},
                    },
                }
            },
            {
                "if": {"properties": {"side": {"enum": ["sink", "end"]}}},
                "then": {
                    "properties": {
                        "ports": {
                            "type": "object",
                            "description": "Contains ports and their definitions",
                            "properties": {},
                        }
                    }
                },
                "else": {
                    "properties": {
                        "ports": {
                            "type": "object",
                            "description": "Contains ports and their definitions",
                            "properties": {},
                        }
                    }
                },
            },
        ],
    }

    for data in all_port_data:
        # populate the shared width data
        if data.get("width") != None:
            temp = {
                "type": "object",
                "properties": {"width": {"const": data.get("width")}},
            }
            json_data["allOf"][0]["properties"]["ports"]["properties"][
                data["name"]
            ] = temp

        # populate the individual directions and the tie on the input
        temp = {
            "type": "object",
            "properties": {"dir": {"const": data["m_dir"], "default": data["m_dir"]}},
        }
        if data["m_dir"] == "input" and data.get("default") != None:
            temp["properties"]["unconnected"] = {"default": data["default"]}
        json_data["allOf"][1]["else"]["properties"]["ports"]["properties"][
            data["name"]
        ] = temp

        dir = "input" if data["m_dir"] == "output" else "output"
        temp = {"type": "object", "properties": {"dir": {"const": dir, "default": dir}}}
        if dir == "input" and data.get("default") != None:
            temp["properties"]["unconnected"] = {"default": data["default"]}
        json_data["allOf"][1]["then"]["properties"]["ports"]["properties"][
            data["name"]
        ] = temp

    print("Successfully parse the IPXACT file")
    if dir_only:
        out_file = out_file + "./{}.schema.json".format(i_name)

    # Everything should be ready write the file
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="IPXACT_Interface_Parser",
        description="Parses a ipxact file to generate the required schema.json for a interface",
    )

    parser.add_argument(
        "ipxact_file", type=argparse.FileType("r"), help="path to ipxact file to read"
    )
    parser.add_argument(
        "-o",
        "--out",
        type=str,
        help="output location can be a file or folder",
        default=None,
    )
    args = parser.parse_args()
    dir_only = False
    if args.out != None:
        a = pathlib.Path(args.out)
        filename, file_extension = os.path.splitext(args.out)
        if file_extension != "":
            to_out = args.out
        else:
            if not a.exists():
                os.makedirs(args.out)
            to_out = args.out
            dir_only = True
    else:
        to_out = "./"
        dir_only = True

    parseIPXactBusDef2009Xilinx(args.ipxact_file, to_out, dir_only=dir_only)


if __name__ == "__main__":
    main()

# parseIPXact2009Xilinx("aximm_rtl.xml", "test.schema.json")
