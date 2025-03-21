import argparse
import json
import os
import pathlib
from geysergen.utils import json_validation

# Template that is populated whenever a port is added to an interface
port_def_template = (
    '\t\t\t\'{}\':{{"name":\'{}\',"width":{}, "dir":\'{}\', "unconnected":{}}},\n'
)

# Template that is populated to create a interface for the module
interface_def_template = """
    {0}_interface_definition = {{
        "name": '{0}',
        "type": '{1}',
        "multiconnect": '{2}',
        "side": '{3}',
        "ports": {{
{4}
        }},
        {5}
    }}\n"""

# Functions to be used during the connection process.
interface_function_template = """
    def interface_{}(self) -> tuple['{}',str]:
        return (self,"{}")
"""

# Template is populated for every interface. Each interface has an array that holds all the other interfaces
# that are attempting to connect. If there is more than one an interconnect is inserted if available
interface_connection_template = """
        self.{}_connections = []"""

# This is the main class template that is populated for each IP that is integrated with geyser.
module_class_template = """
import copy, math
from geysergen.generator import verilog_generator
from geysergen.utils.v_class import v_class
class {}(v_class):
    _ip_name = \"{}\"
    def __init__(self,generator:verilog_generator,name:str,{}parameters:dict={{}}) -> None:
        self._generator=generator
        generator.register_module(self)
        self._module_instance_name = name
        self._interconnects = []
        self.interface_interconnect_sel = {{}}
        self._parameters={{{}}}
        if parameters:
            self._parameters |= parameters
        self._finish_gen=""
        
        # Apply any dynamic port widths
{}
"""

# Tuples that are placed in the interfaces list
interface_tuple_temp = "(self.{0}_connections,self.{0}_interface_definition),"

# List that is filled with the tuples above
connections_def_temp = """
        self._interfaces = [{}]"""


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="Module_Generator",
        description="Convert a module json description into a python module that can be used in the platform generator",
    )

    parser.add_argument(
        "json_file", type=argparse.FileType("r"), help="Path to json file to read"
    )
    parser.add_argument(
        "--validate-only",
        help="Only validate the file don't generate module",
        action="store_true",
    )
    parser.add_argument(
        "-o",
        "--out",
        type=str,
        help="output location can be a file or folder",
        default=None,
    )
    parser.add_argument(
        "--dump-json",
        help="dump json file which is the original file filled with all default populated values",
        action="store_true",
    )

    def Assert(result: bool, message: str):
        if result:
            return
        print("Failed check: " + message)
        exit(1)

    interface_connection_name_array = []  # Array with every interface name
    interface_connection_arrays = (
        []
    )  # Array for all the code which makes the interface connections empty
    interface_definition_dicts = (
        []
    )  # Array with all the populated interface definition templates
    interface_function_array = (
        []
    )  # Contains all the functions to access the modules interfaces
    port_names = []  # Name of every port claimed by an interface. Used to prevent
    interface_names = (
        []
    )  # Possibly identical to interface_connection_name_array (Maybe Remove)
    clone_list = (
        []
    )  # These interfaces have dynamic parameters. Do a deepcopy so the changes only follow the current instance.
    dynamic_width_ports = []  # The code involved with dynamic port widths.

    # TODO add interface check. If this interface is a standard one we should make sure that no unexpected values are there.

    def parseInterface(to_parse, module_name) -> None:
        int_name = to_parse.get("interface_name")
        Assert(
            int_name != None,
            "Must provide a interface name ('interface_name' key missing)",
        )
        extras = ""
        multi_en = False
        if int_name.count("?") != 0:
            # Check if the user is attempting to make use of the multi key function ensure that they have provided all the needed values. 
            Assert(
                int_name.count("?") <= 1,
                "Can only provide 1 multi name location (more than one '?' in '{}')".format(
                    int_name
                ),
            )
            multi_names = to_parse.get("multi")
            Assert(
                multi_names != None,
                "Must provide the multi name substitutes since '?' present in name '{}'".format(
                    int_name
                ),
            )

            # The following section allows for multi names to be constructed dynamically with inline python code
            add_list = []
            for name in multi_names:
                if type(name) == str:
                    if name[0] == "/":
                        name_list = eval(name[1:])
                        add_list = add_list + name_list
                        multi_names.remove(name)
            Assert(
                len(multi_names) != 0 or len(add_list) != 0,
                "Used dynamic list construction but no elements were produced: {}".format(
                    int_name
                ),
            )
            multi_names = multi_names + add_list

            Assert(
                type(multi_names) == list,
                "multi must be of type list, interface {}".format(int_name),
            )
            Assert(
                len(multi_names) == len(set(multi_names)),
                "The list provided in multi for interface {} had duplicates".format(
                    int_name
                ),
            )
            multi_en = True
        Assert(
            multi_en or to_parse.get("multi") == None,
            "Provided multi name substitutions but no ? present in name '{}'".format(
                int_name
            ),
        )
        connect_side = to_parse.get("side", -1)
        int_type = to_parse.get("type")
        Assert(
            int_type != None,
            "No type set for interface {} can use conduit if you don't care".format(
                int_name
            ),
        )
        multi_connect = to_parse.get("multiconnect", "false")
        Assert(
            multi_connect in ["false", "shared", "interconnect"],
            "Invalid multi connect parameter {}. For interface {}".format(
                int_name, multi_connect
            ),
        )

        # Get interconnect settings
        if "interconnect_settings" in to_parse:
            if "pass_clock" in to_parse["interconnect_settings"]:
                extras += '"pass_clock":"{}",'.format(
                    to_parse["interconnect_settings"]["pass_clock"]
                )
            if "pass_reset" in to_parse["interconnect_settings"]:
                extras += '"pass_reset":"{}",'.format(
                    to_parse["interconnect_settings"]["pass_reset"]
                )

        
        print(
            "Beginning generation of interface {} in module {}".format(
                int_name, module_name
            )
        )
        ports = to_parse.get("ports")
        port_stuff = ""

        port_names_local = []
        port_types = []
        interface_defs = ""
        interface_dynamic_port_widths = []
        for key, val in ports.items():

            Assert(type(val) == dict, "port must a dict")
            port_name = val.get("name", None)
            Assert(
                port_name != None,
                "port {} in {} must be given a name".format(key, int_name),
            )
            port_width = val.get("width", 1)
            port_dir = val.get("dir", None)
            port_unconnected = val.get("unconnected", "nothing")
            # Leave alone if int otherwise add quotes
            if isinstance(port_unconnected, str):
                port_unconnected = "'" + port_unconnected + "'"
            port_param_width = val.get("dynamic_width", None)
            if port_param_width != None:
                interface_dynamic_port_widths.append((key, port_param_width))
            if multi_en:
                Assert(
                    port_name.count("?") <= 1,
                    "Can only provide 1 multi name location (more than one '?' in '{}')".format(
                        val
                    ),
                )
                Assert(
                    port_name.count("?") == 1,
                    "Need to provide 1 multi name location (no '?' in '{}')".format(
                        val
                    ),
                )

            port_names.append(port_name)
            port_types.append(key)

            port_stuff += port_def_template.format(
                key, port_name, port_width, port_dir, port_unconnected
            )

        # Confirm there aren't duplicate port types in a interface
        Assert(
            len(port_names_local) == len(set(port_names_local)),
            "In interface {} two ports share the same name".format(int_name),
        )
        Assert(
            len(port_types) == len(set(port_types)),
            "In interface {} there is a duplicated port".format(int_name),
        )

        # Check that the negative version of a port isn't also present
        def func_rm_neg(a, i) -> None:
            if a[i][-2:] == "_n":
                a[i] = a[i][:-2]  # remove any inverted ports

        list(map(lambda i: func_rm_neg(port_types, i), range(0, len(port_types))))
        Assert(
            len(port_types) == len(set(port_types)),
            "In interface {} there is both a negative logic and positive logic version of a port. (ie clk and clk_n). If this is intentional please rename the positive logic port to have a _p at the end (ie clk_n and clk_p)".format(
                int_name
            ),
        )

        function_stuff = ""
        connection_arr_stuff = ""

        if multi_en:
            for multi_name in multi_names:
                multi_name = str(multi_name)
                interface_names.append(int_name.replace("?", multi_name))
                interface_defs += interface_def_template.format(
                    int_name.replace("?", multi_name),
                    int_type,
                    multi_connect,
                    connect_side,
                    port_stuff.replace("?", multi_name),
                    extras,
                )
                function_stuff += interface_function_template.format(
                    int_name.replace("?", multi_name),
                    module_name,
                    int_name.replace("?", multi_name),
                )
                connection_arr_stuff += interface_connection_template.format(
                    int_name.replace("?", multi_name)
                )
                interface_connection_name_array.append(
                    int_name.replace("?", multi_name)
                )
                if len(interface_dynamic_port_widths) > 0:
                    clone_list.append(int_name.replace("?", multi_name))
                    for p, w in interface_dynamic_port_widths:
                        if w[:1] == "/":
                            dynamic_width_ports.append(
                                "self.{0}_interface_definition['ports']['{1}']['width']={2}".format(
                                    int_name.replace("?", multi_name), p, w[1:]
                                )
                            )
                        else:
                            dynamic_width_ports.append(
                                "self.{0}_interface_definition['ports']['{1}']['width']=self._parameters['{2}']".format(
                                    int_name.replace("?", multi_name), p, w
                                )
                            )
        else:
            interface_names.append(int_name)
            interface_defs = interface_def_template.format(
                int_name, int_type, multi_connect, connect_side, port_stuff, extras
            )
            function_stuff = interface_function_template.format(
                int_name, module_name, int_name
            )
            connection_arr_stuff = interface_connection_template.format(int_name)
            interface_connection_name_array.append(int_name)
            if len(interface_dynamic_port_widths) > 0:
                clone_list.append(int_name)
                for p, w in interface_dynamic_port_widths:
                    if w[:1] == "/":
                        dynamic_width_ports.append(
                            "self.{0}_interface_definition['ports']['{1}']['width']={2}".format(
                                int_name, p, w[1:]
                            )
                        )
                    else:
                        dynamic_width_ports.append(
                            "self.{0}_interface_definition['ports']['{1}']['width']=self._parameters['{2}']".format(
                                int_name, p, w
                            )
                        )

        interface_definition_dicts.append(interface_defs)
        interface_function_array.append(function_stuff)
        interface_connection_arrays.append(connection_arr_stuff)

    args = parser.parse_args()

    with args.json_file as f:
        d = json.load(f)

        # First just validate
        json_validation.validate_json(d)

        # Now populate with default values
        d["interfaces"] = json_validation.populate_defaults(d["interfaces"])

        if args.dump_json:
            wr = open("./test_out.json", "w")
            json.dump(d, wr)

        if args.validate_only:
            print("Your JSON passes validation")
            exit(0)

        if args.out == None:
            fo = open("{}.py".format(d.get("name")), "w")
        else:
            a = pathlib.Path(args.out)
            filename, file_extension = os.path.splitext(args.out)
            if file_extension != "":
                fo = open(args.out, "w")
            else:
                if not a.exists():
                    os.makedirs(args.out)
                fo = open(args.out + "/{}.py".format(d.get("name")), "w")

        module_name = d.get("name")
        ip_name = d.get("ip_name")
        interfaces = d.get("interfaces")

        Assert(module_name != None, "Must provide a module name ('name' key missing)")
        Assert(
            ip_name != None,
            "Must the name of the ip to instantiate ('ip_name' key missing)",
        )
        Assert(interfaces != None, "Must provide ip_interfaces")
        for interface in interfaces:
            parseInterface(interface, module_name=module_name)

        # Scan for anything that we don't allow
        Assert(
            len(interface_names) == len(set(interface_names)),
            "Two interfaces share the same name",
        )
        Assert(
            len(port_names) == len(set(port_names)),
            "Two ports share the same name, these ports are in two separate interfaces",
        )

        # Now we need to scan for params
        set_params = d.get("parameters")
        hidden_params = d.get("hidden_parameters")

        if set_params != None and hidden_params != None:
            for key in set_params.keys():
                Assert(
                    not key in hidden_params.keys(),
                    'The parameter "{}" was found in both parameters and hidden parameters, it must only be specified once'.format(
                        key
                    ),
                )
        null_params = []
        non_null = []
        params_text = ""

        # Now add the params to the generated module
        if set_params != None:
            for key, val in set_params.items():
                if val == None:
                    null_params.append(key)
                else:
                    non_null.append((key, val))
                params_text += '\n\t\t\t"{}":{},'.format(key, key)

        args_text = ""
        for p in null_params:
            args_text += "{},".format(p)
        for name, default in non_null:
            if type(default) == str:
                args_text += '{}="{}",'.format(
                    name, default.replace("'", "\\'").replace('"', '\\"')
                )
            else:
                args_text += "{}={},".format(name, default)
        if hidden_params != None:
            for key, val in hidden_params.items():
                if type(val) == str:
                    if len(val) >= 1 and val[0] == "/":
                        params_text += '\n\t\t\t"{}":({}),'.format(key, val[1:])
                    else:
                        params_text += '\n\t\t\t"{}":"{}",'.format(
                            key, val.replace("'", "\\'").replace('"', '\\"')
                        )
                else:
                    params_text += '\n\t\t\t"{}":{},'.format(key, val)

        if len(args_text) > 2:
            params_text = params_text[:-1]

        # Setup stuff for ports with dynamic widths
        dynamic_text = ""
        for inter in clone_list:
            dynamic_text += "\t\tself.{0}_interface_definition=copy.deepcopy({1}.{0}_interface_definition)\n".format(
                inter, module_name
            )

        for port in dynamic_width_ports:
            dynamic_text += "\t\t" + port + "\n"

        fo.write(
            module_class_template.format(
                module_name, ip_name, args_text, params_text, dynamic_text
            ).replace("\t", "    ")
        )
        for defa in interface_connection_arrays:
            fo.write(defa)
            fo.write("\n")
        t_tuples = ""
        for inter_stuff in interface_connection_name_array:
            t_tuples += interface_tuple_temp.format(inter_stuff, inter_stuff)
        fo.write(connections_def_temp.format(t_tuples))
        fo.write("\n")
        for defa in interface_definition_dicts:
            fo.write(defa)
            fo.write("\n")
        fo.write("\n")
        for defa in interface_function_array:
            fo.write(defa)
            fo.write("\n")


if __name__ == "__main__":
    main()
