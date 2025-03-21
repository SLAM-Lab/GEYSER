import json
import argparse
import pathlib
import os
parser = argparse.ArgumentParser(
                    prog='Module Generator',
                    description='Convert a module json description into a python module that can be used in the platform generator')

parser.add_argument('input_file',type=str,help="Path to verilog file to parse")
parser.add_argument('module_name',help="Name to give the module")
parser.add_argument('file_type',choices=['hls','quartus'],help="The type of inst file that is going to be parsed to see examples look in the readme")
parser.add_argument('-o','--out',type=str,help='output location can be a file or folder',default=None)

args = parser.parse_args()

module_name = args.module_name
to_read=args.input_file
to_out ="{}.vgen.json".format(module_name)
if args.out != None:
    a = pathlib.Path(args.out)
    filename, file_extension = os.path.splitext(args.out)
    if file_extension!='':
        to_out = args.out
    else:
        if not a.exists():
            os.makedirs(args.out)
        to_out = args.out+"/{}.vgen.json".format(module_name)

ip_json = {}
ip_json['name']=module_name
ip_json['interfaces']=[]
def parse_hls_inst(to_read, ip_json):
    curr_interface = None
    name_found = False
    with open(to_read) as i_file:
        for line in i_file:
            if not name_found:
                if "(" in line:
                    ip_name = line.split(" ")[0]
                    ip_json['ip_name']=ip_name
                    print("Parsing: ",ip_name)
                    name_found=True
            else:
                if "// Interface:" in line:
                    if curr_interface!=None:
                        ip_json['interfaces'].append(curr_interface)
                    parts = list(filter(None, line.strip().split(' ')))
                    curr_interface = {}
                    curr_interface['interface_name']=parts[2]
                    curr_interface['type']=parts[3][1:]
                    curr_interface['side']=parts[4][:-1]
                    curr_interface['ports']={}
                elif "( ), //" in line:
                    line=line.replace('('," (")
                    parts = list(filter(None, line.strip().split(' ')))
                    curr_interface['ports'][parts[5]]={"name":parts[0][1:],"width":int(parts[4][:-4]),"dir":parts[6]}
    if curr_interface!=None:
        ip_json['interfaces'].append(curr_interface)
    return ip_json
                

def parse_quartus_inst(to_read, ip_json):
    curr_interface = None
    name_found = False
    with open(to_read) as i_file:
        for line in i_file:
            if not name_found:
                if "(" in line:
                    ip_name = line.split(" ")[0].strip()
                    ip_json['ip_name']=ip_name
                    print("Parsing: ",ip_name)
                    name_found=True
            else:
                if "//" in line:
                    #print(line)
                    #Split and check if this is the start of a new interface
                    if not ' .' in line.split("//")[1]:
                        if curr_interface!=None:
                            ip_json['interfaces'].append(curr_interface)
                        curr_interface = {}
                        curr_interface['interface_name']=line.split("//")[1].split(',')[2].split('.')[0].strip()
                        curr_interface['type']='unknown'
                        curr_interface['side']='unknown'
                        curr_interface['ports']={}
                    
                    #now get port name 
                    line=line.replace('('," (")
                    name = line.strip().split(" ")[0][1:]
                    
                    #Now get the helpful information in the comment
                    comment = line.split("//")[1].strip()
                    comment = comment.split(",")
                    dir = comment[0].strip()
                    width = comment[1].split("=")[1].strip()
                    type_n = comment[2].split(".")[1].strip()
                    curr_interface['ports'][type_n]={"name":name,"width":int(width),"dir":dir}
    if curr_interface!=None:
        ip_json['interfaces'].append(curr_interface)
    return ip_json 

with open(to_out, 'w', encoding='utf-8') as f:
    if args.file_type == 'quartus':
        json_data = parse_quartus_inst(to_read,ip_json)
    elif args.file_type == 'hls':
        json_data = parse_hls_inst(to_read,ip_json)
    else:
        print("Invalid file type")
        exit(0)
    json.dump(json_data, f, ensure_ascii=False, indent=4)    