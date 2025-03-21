from lxml import etree
from lxml.etree import _ElementTree,_Element
import json
import argparse
import os, pathlib, io 
def parseIPXact2014Intel(file_path,out_file:str,dir_only=False,excludeCosimPorts=True) -> None:
    xml:_ElementTree = etree.parse(file_path)
    root_xml:_Element = xml.getroot()
    nsmap=root_xml.nsmap
    conduit_warn=False

    # Make sure this is a valid and supported 2014 IPXACT file
    if etree.QName(root_xml).namespace!="http://www.accellera.org/XMLSchema/IPXACT/1685-2014":
        print("ERROR: only version 2014 of ipxact is currently supported")
        exit(-1)
    if etree.QName(root_xml).localname!="component":
        print("ERROR: Ipxact file does not only contain a component")
        exit(-1)
    if nsmap.get("altera")==None:
        print("Only support intel")
        exit(-1)
    #Start pulling the details that we are going to need

    ip_name = root_xml.find("ipxact:name",namespaces=nsmap).text
    local_name = root_xml.find("ipxact:library",namespaces=nsmap).text

    #TODO make sure they are present

    print("Parsing ip {} with name {}".format(ip_name,local_name))

    #First we need to get all of the ports for the ip and any necessary related details
    ports_xml = root_xml.find("ipxact:model",namespaces=nsmap).find("ipxact:ports",namespaces=nsmap)

    ports_data = {}
    for port_xml in ports_xml:
        if port_xml.find("ipxact:isPresent",namespaces=nsmap) != None and port_xml.find("ipxact:isPresent",namespaces=nsmap).text == "0":
            #ignore this port it isn't real
            continue
        if port_xml.find("ipxact:wire",namespaces=nsmap) == None:
            #Doesn't have a wire definition it is meant for TLM and can be ignored
            continue

        #get the actual port_name    
        port_name = port_xml.find("ipxact:name",namespaces=nsmap).text
        #print(port_name)
        wire_xml = port_xml.find("ipxact:wire",namespaces=nsmap)

        #begin populating data
        ports_data[port_name] = {}

        ports_data[port_name]['dir']="input" if wire_xml.find("ipxact:direction",namespaces=nsmap).text=="in" else "output"
        if wire_xml.find("ipxact:vectors",namespaces=nsmap)==None:
            port_width = 1
        else:
            left = int(wire_xml.find("ipxact:vectors",namespaces=nsmap)[0].find("ipxact:left",namespaces=nsmap).text)
            right = int(wire_xml.find("ipxact:vectors",namespaces=nsmap)[0].find("ipxact:right",namespaces=nsmap).text)
            if(left!=0):
                print("ERROR port {} does not start at bit 0 spliced ports are not supported".format(port_name))
            port_width=right+1

        ports_data[port_name]['width']=port_width


    #We have parsed all the ports now les parse the bus interfaces
    bInterfaces_xml = root_xml.find("ipxact:busInterfaces",namespaces=nsmap)
    ip_json = {}
    ip_json['name']=local_name
    ip_json['ip_name']=ip_name
    ip_json['interfaces']=[]
    for inter_xml in bInterfaces_xml: 
        curr_interface = {}
        if inter_xml.find("ipxact:isPresent",namespaces=nsmap) != None and inter_xml.find("ipxact:isPresent",namespaces=nsmap).text == "0":
            #ignore this port it isn't real
            continue
        if inter_xml.find("ipxact:vendorExtensions",namespaces=nsmap) != None:
            a = inter_xml.find("ipxact:vendorExtensions",namespaces=nsmap).XPath("//contains(text(),hls.cosim.name)")
            print(a)
            
        name = inter_xml.find("ipxact:name",namespaces=nsmap).text.lower()
        i_type = inter_xml.find("ipxact:busType",namespaces=nsmap).get("name")
        #TODO there are other interface types besides master and slave. Additionally all conduits are slaves which is problematic an needs to be dealt with
        side = "source" if inter_xml.find("ipxact:master",namespaces=nsmap)!=None else "sink"
        curr_interface['interface_name']=name
        curr_interface['type']=i_type
        curr_interface['side']=side
        curr_interface['interconnect_settings']={}
        curr_interface['ports']={}
        if i_type=="conduit":
            conduit_warn = True
        #Now we need to go through and associate all the ports
        ab_types = inter_xml.find("ipxact:abstractionTypes",namespaces=nsmap)
        if ab_types == None:
            continue
        if len(ab_types)!=1:
            print("ERROR: only one abstraction type currently supported interface {} has {}".format(name,len(ab_types)))
            exit(-1)

        port_maps = ab_types[0].find("ipxact:portMaps",namespaces=nsmap)
        if port_maps == None:
            #No ports defined for this abstraction
            continue
        
        for p_map in port_maps:
            if p_map.find("ipxact:isPresent",namespaces=nsmap) != None and p_map.find("ipxact:isPresent",namespaces=nsmap).text == "0":
                #ignore this port it isn't real
                continue
            if p_map.find("ipxact:isInformative",namespaces=nsmap) != None and p_map.find("ipxact:isInformative",namespaces=nsmap).text =='true':
                #Ignore this port it is informative only
                continue

            l_name = p_map.find("ipxact:logicalPort",namespaces=nsmap).find("ipxact:name",namespaces=nsmap).text
            p_name = p_map.find("ipxact:physicalPort",namespaces=nsmap).find("ipxact:name",namespaces=nsmap).text

            if ports_data.get(p_name)==None:
                print("Interface {} requested port {} which is undefined".format(name,p_name))
                exit(-1)
            
            #TODO need to catch ports being used in multiple places
            curr_interface['ports'][l_name]={}
            curr_interface['ports'][l_name]['name']=p_name
            curr_interface['ports'][l_name]['dir']=ports_data[p_name]['dir']
            curr_interface['ports'][l_name]['width']=ports_data[p_name]['width']

        #Now check the properties for some special keys we might need
        i_params = inter_xml.find("ipxact:parameters",namespaces=nsmap)
        if i_params != None:
            for param in i_params:
                if param.get("parameterId")=="associatedClock":
                    a_clock = param.find("ipxact:value",namespaces=nsmap).text
                    curr_interface['interconnect_settings']['pass_clock']=a_clock
                elif param.get("parameterId")=="associatedReset":
                    a_reset = param.find("ipxact:value",namespaces=nsmap).text
                    curr_interface['interconnect_settings']['pass_reset']=a_reset


        ip_json['interfaces'].append(curr_interface)

    #Everything should be ready write the file
    print("Successfully parsed the IPXACT file")
    if conduit_warn:
        print("Warning: module contains conduit interfaces these do not have their direction defined in IPXACT. As a result GEYSER will always defined them to be a sink. Please manually fix these if this is a issue.")

    if dir_only:
        out_file=out_file+"./{}.vgen.json".format(local_name)
       
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(ip_json, f, ensure_ascii=False, indent=4)    

def parseIPXact2009Xilinx(file_path,out_file:str,dir_only = False, excludeCosimPorts=True) -> None:
    xml:_ElementTree = etree.parse(file_path)
    root_xml:_Element = xml.getroot()
    nsmap=root_xml.nsmap
    conduit_warn = False
    if etree.QName(root_xml).namespace!="http://www.spiritconsortium.org/XMLSchema/SPIRIT/1685-2009":
        print("ERROR: only version 2009 of spirit is currently supported")
        exit(-1)
    if etree.QName(root_xml).localname!="component":
        print("ERROR: spirit file does not only contain a component")
        exit(-1)
    if nsmap.get("xilinx")==None:
        print("Only support xilinx")
        exit(-1)
    #Start pulling the details that we are going to need

    ip_name = root_xml.find("spirit:name",namespaces=nsmap).text
    local_name = root_xml.find("spirit:library",namespaces=nsmap).text

    #TODO make sure they are present

    print("Parsing ip {} with name {}".format(ip_name,local_name))

    #First we need to get all of the ports for the ip and any necessary related details
    ports_xml = root_xml.find("spirit:model",namespaces=nsmap).find("spirit:ports",namespaces=nsmap)

    ports_data = {}
    for port_xml in ports_xml:
        if port_xml.find("spirit:isPresent",namespaces=nsmap) != None and port_xml.find("spirit:isPresent",namespaces=nsmap).text == "0":
            #ignore this port it isn't real
            continue
        if port_xml.find("spirit:wire",namespaces=nsmap) == None:
            #Doesn't have a wire definition it is meant for TLM and can be ignored
            continue

        #get the actual port_name    
        port_name = port_xml.find("spirit:name",namespaces=nsmap).text
        #print(port_name)
        wire_xml = port_xml.find("spirit:wire",namespaces=nsmap)
        #begin populating data
        ports_data[port_name] = {}

        ports_data[port_name]['dir']="input" if wire_xml.find("spirit:direction",namespaces=nsmap).text=="in" else "output"
        if wire_xml.find("spirit:vector",namespaces=nsmap)==None:
            port_width = 1
        else:
            left = int(wire_xml.find("spirit:vector",namespaces=nsmap).find("spirit:left",namespaces=nsmap).text)
            right = int(wire_xml.find("spirit:vector",namespaces=nsmap).find("spirit:right",namespaces=nsmap).text)
            if(right!=0):
                print("ERROR port {} does not start at bit 0 spliced ports are not supported".format(port_name))
            port_width=left+1

        ports_data[port_name]['width']=port_width


    #We have parsed all the ports now les parse the bus interfaces
    bInterfaces_xml = root_xml.find("spirit:busInterfaces",namespaces=nsmap)
    ip_json = {}
    ip_json['name']=local_name
    ip_json['ip_name']=ip_name
    ip_json['interfaces']=[]
    clocks:dict={}
    resets={}
    for inter_xml in bInterfaces_xml: 
        curr_interface = {}
        if inter_xml.find("spirit:isPresent",namespaces=nsmap) != None and inter_xml.find("spirit:isPresent",namespaces=nsmap).text == "0":
            #ignore this port it isn't real
            continue
        if inter_xml.find("spirit:abstractionType",namespaces=nsmap) != None and inter_xml.find("spirit:abstractionType",namespaces=nsmap).xpath('./@spirit:name',namespaces=nsmap)[0].endswith("tlm"):
            #TLM port ignore it
            #It is possible that there are more port types that need to be ignored but this is the only one I know about for now
            continue
        name = inter_xml.find("spirit:name",namespaces=nsmap).text.lower()
        i_type = inter_xml.find("spirit:busType",namespaces=nsmap).xpath('./@spirit:name',namespaces=nsmap)[0]
        if i_type=="conduit":
            conduit_warn = True
        #TODO there are other interface types besides master and slave. Additionally all conduits are slaves which is problematic an needs to be dealt with
        side = "source" if inter_xml.find("spirit:master",namespaces=nsmap)!=None else "sink"
        curr_interface['interface_name']=name
        curr_interface['type']=i_type
        curr_interface['side']=side
        curr_interface['interconnect_settings']={}
        curr_interface['ports']={}
        # print("interface {} ".format(name))
        #Now we need to go through and associate all the ports
        port_maps = inter_xml.find("spirit:portMaps",namespaces=nsmap)
        if port_maps == None:
            #No ports defined for this abstraction
            continue
        
        for p_map in port_maps:
            if p_map.find("spirit:isPresent",namespaces=nsmap) != None and p_map.find("spirit:isPresent",namespaces=nsmap).text == "0":
                #ignore this port it isn't real
                continue
            if p_map.find("spirit:isInformative",namespaces=nsmap) != None and p_map.find("spirit:isInformative",namespaces=nsmap).text =='true':
                #Ignore this port it is informative only
                continue
            
            l_name = p_map.find("spirit:logicalPort",namespaces=nsmap).find("spirit:name",namespaces=nsmap).text.lower()
            p_name = p_map.find("spirit:physicalPort",namespaces=nsmap).find("spirit:name",namespaces=nsmap).text
            if ports_data.get(p_name)==None:
                print("Interface {} requested port {} which is undefined".format(name,p_name))
                exit(-1)
            
            #TODO need to catch ports being used in multiple places
            curr_interface['ports'][l_name]={}
            curr_interface['ports'][l_name]['name']=p_name
            curr_interface['ports'][l_name]['dir']=ports_data[p_name]['dir']
            curr_interface['ports'][l_name]['width']=ports_data[p_name]['width']

        #Now check the properties for some special keys we might need
        i_params = inter_xml.find("spirit:parameters",namespaces=nsmap)
        if i_params != None:
            for param in i_params:
                if param.find("spirit:name",namespaces=nsmap).text == "ASSOCIATED_BUSIF":
                    ref = param.find("spirit:value",namespaces=nsmap).text
                    clocks[name]=ref
                if param.find("spirit:name",namespaces=nsmap).text == "ASSOCIATED_RESET":
                    a_reset = param.find("spirit:value",namespaces=nsmap).text
                    resets[name]=a_reset


        ip_json['interfaces'].append(curr_interface)

    #scan through the associated clocks and associate them with interfaces
    for clock,buses in clocks.items():
        if buses!="" and buses!=None:
            reset = resets.get(clock)
            buses = buses.lower().split(":")
            for i in ip_json['interfaces']:
                if i['interface_name'] in buses:
                    i['interconnect_settings']['pass_clock']=clock
                    if reset!=None:
                        i['interconnect_settings']['pass_reset']=reset.lower()

                

    #Everything should be ready write the file
    print("Successfully parse the IPXACT file")
    if conduit_warn:
        print("Warning: module contains conduit interfaces these ones do not automatically have their direction defined and will always be a sink. Please manually fix these if this is a issue.")
    if dir_only:
        out_file=out_file+"./{}.vgen.json".format(ip_name)
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(ip_json, f, ensure_ascii=False, indent=4)    

def parseIPXACT(file_path,out_file:str,dir_only=False,remove_cosim=False) -> None:
    xml:_ElementTree = etree.parse(file_path)
    root_xml:_Element = xml.getroot()
    if isinstance(file_path,io.IOBase):
        #This is a file object we need to reset it for the parsers
        file_path.seek(0)
    if etree.QName(root_xml).namespace=="http://www.spiritconsortium.org/XMLSchema/SPIRIT/1685-2009":
        print("Detected version IPXACT 2009")
        parseIPXact2009Xilinx(file_path=file_path,out_file=out_file,dir_only=dir_only)
    elif etree.QName(root_xml).namespace=="http://www.accellera.org/XMLSchema/IPXACT/1685-2014":
        print("Detected version IPXACT 2014")
        parseIPXact2014Intel(file_path=file_path,out_file=out_file,dir_only=dir_only,remove_cosim=remove_cosim)
    else:
        print("unsupported ipxact format")
        exit(-1)

def main():
    parser = argparse.ArgumentParser(
                        prog='IPXACT_Parser',
                        description='Parses a ipxact file to generate the required vgen.json for a module')

    parser.add_argument('ipxact_file',type=argparse.FileType('r'),help="path to ipxact file to read")
    parser.add_argument('-o','--out',type=str,help='output location can be a file or folder',default=None)
    parser.add_argument('-r','--remove-cosim', action='store_true',help='Indicate if ipxact_parse should attempt to remove Intel cosim ports')
    args = parser.parse_args()
    dir_only=False
    if args.out != None:
        a = pathlib.Path(args.out)
        filename, file_extension = os.path.splitext(args.out)
        if file_extension!='':
            to_out = args.out
        else:
            if not a.exists():
                os.makedirs(args.out)
            to_out = args.out
            dir_only=True
    else:
        to_out="./"
        dir_only=True

    parseIPXACT(args.ipxact_file,to_out,dir_only=dir_only,excludeCosimPorts=args.remove_cosim)

if __name__ == "__main__":
    main()