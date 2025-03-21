from abc import ABC
class v_class():
    """
    This is the baseline class used by all GEYSER IP classes. 
    Contains shared functions to make updating easier.
    """
    _parameters:dict 
    _interfaces:list[tuple[list, dict]]
    _ip_name:str
    _module_instance_name:str

    # The final string created after the generate phase. 
    # This is what will be written to the output file in the write stage. 
    _finish_gen:str

    # Tracks all of the currently constructed interconnects during the generate phase. 
    # Mainly to make debugging easier.
    _interconnects:list

    # This keeps track of what interconnect should be inserted for each interface. 
    # The interconnect that is active during the last connect event for each specific 
    # interface is the one that will be inserted 
    interface_interconnect_sel:dict

    # This template is what is populated and written to the final verilog file
    __verilog_base_template = """
    {} {} {} (
    {}
    );
    """
    # Allow access to the interfaces through a dict style access on the class
    def __getitem__(self, key):
        return getattr(self, key)

    def generate(self):
        gen_base = ""
        param_base = ""
        if self._parameters:
            param_base = "#("
            for param_name,val in self._parameters.items():
                if type(val)==str and not "'" in val:
                    param_base+="	.{}(\"{}\"),\n".format(param_name,val)
                else:
                    param_base+="	.{}({}),\n".format(param_name,val)
            param_base=param_base[0:-2] #Remove trailing comma
            param_base += ")"
        for int_connections, int_def in self._interfaces:
            curr_connections = {}
            for t,port in int_def['ports'].items():
                if port['dir']=='input' and port['unconnected'] != 'nothing':
                    curr_connections[t]=port['unconnected']
                else:
                    curr_connections[t]=""
            if len(int_connections)>0:
                if len(int_connections)==1:
                    # Simple connection
                    for connect_data in int_connections[0]:
                        if connect_data['type'] in int_def['ports']:
                            curr_connections[connect_data['type']]="    .{}({}),\n".format(int_def['ports'][connect_data['type']]['name'],connect_data['connection_port_name'])
                        elif connect_data['type'][-2:]=="_n":
                            if connect_data['type'][:-2] in int_def['ports']:
                                curr_connections[connect_data['type'][:-2]]="	.{}(~{}),\n".format(int_def['ports'][connect_data['type'][:-2]]['name'],connect_data['connection_port_name'])
                        else:
                            if connect_data['type']+"_n" in int_def['ports']:
                                curr_connections[connect_data['type']+"_n"]="	.{}(~{}),\n".format(int_def['ports'][connect_data['type']+"_n"]['name'],connect_data['connection_port_name'])
                else:
                    if int_def['multiconnect']=='false':
                        print("ERROR: Attempted to connect two interfaces to module {}, interface {}.".format(self._module_instance_name,int_def['name']))
                        print("This interface is not configured to support multiconnect")
                        exit(1)
                    elif int_def['multiconnect']=='shared':
                            pre_connected = {}
                            for connection in int_connections:
                                for connect_data in connection:
                                    pre_name = pre_connected.get(int_def['ports'][connect_data['type']]['name'],None)
                                    if pre_name!=None:
                                        if int_def['ports'][connect_data['type']]['dir']!='output':
                                            self._generator.fail("Shared connections on input ports are not allowed! Module {}, interface {}, port {}".format(self._module_instance_name,int_def['name'],connect_data['type']))
                                        # Module is already hooked up at this point just tie into the wire
                                        self._generator.add_assignment(connect_data['connection_port_name'],pre_name) 
                                    else:
                                        curr_connections[connect_data['type']]="	.{}({}),\n".format(int_def['ports'][connect_data['type']]['name'],connect_data['connection_port_name'])
                                        pre_connected[int_def['ports'][connect_data['type']]['name']]=connect_data['connection_port_name']
                    elif int_def['multiconnect']=='interconnect':
                        #We are going to have to generate an interconnect
                        the_interconnect = self.interface_interconnect_sel.get(int_def['name'])
                        #self._generator.find_interconnect(int_def['type'])("{}_{}_inter".format(self._module_instance_name,int_def['name']),self._generator)
                        if the_interconnect==None:
                            print("Failed to find interconnect for interface {} type {}".format(int_def['name'],int_def['type']))
                            exit(1)
                        the_interconnect = the_interconnect("{}_{}_inter".format(self._module_instance_name,int_def['name']),self._generator)
                        extras = {}
                        if(int_def.get('pass_clock',None)!=None):    
                            clk_inter = getattr(self,"{}_connections".format(int_def['pass_clock']))
                            extras['clock']=clk_inter[0]
                        if(int_def.get('pass_reset',None)!=None):    
                            reset_inter = getattr(self,"{}_connections".format(int_def['pass_reset']))
                            extras['reset']=reset_inter[0]
                        
                        interconnect_connections = the_interconnect.make_interconnect(int_connections,int_def['side'],extras)
                        self._interconnects.append(the_interconnect)
                        for mod_name, our_name in interconnect_connections.items():
                            if mod_name in int_def['ports']:
                                curr_connections[mod_name]="	.{}({}),\n".format(int_def['ports'][mod_name]['name'],our_name)
                            elif mod_name[-2:]=="_n":
                                if mod_name[:-2] in int_def['ports']:
                                    if int_def['ports'][mod_name[:-2]]['dir']=="output":
                                        self._generator.add_wire(our_name+"_flip",int_def['ports'][mod_name[:-2]]['width'])
                                        self._generator.add_assignment(our_name,"~"+our_name+"_flip")
                                        curr_connections[mod_name[:-2]]="	.{}({}),\n".format(int_def['ports'][mod_name[:-2]]['name'],our_name+"_flip")
                                    else:
                                        curr_connections[mod_name[:-2]]="	.{}(~{}),\n".format(int_def['ports'][mod_name[:-2]]['name'],our_name)
                            else:
                                if mod_name+"_n" in int_def['ports']:
                                    if int_def['ports'][mod_name+"_n"]['dir']=="output":
                                        self._generator.add_wire(our_name+"_flip",int_def['ports'][mod_name+"_n"]['width'])
                                        self._generator.add_assignment(our_name,"~"+our_name+"_flip")
                                        curr_connections[mod_name+"_n"]="	.{}({}),\n".format(int_def['ports'][mod_name+"_n"]['name'],our_name+"_flip")
                                    else:
                                        curr_connections[mod_name+"_n"]="	.{}(~{}),\n".format(int_def['ports'][mod_name+"_n"]['name'],our_name) 
            for t,connect in curr_connections.items():
                if connect == 'forbidden':
                    self._generator.fail("Interface {}, port {} was left unconnected in {} which is not allowed".format(int_def['name'],t,self._module_instance_name))
                elif connect == 'tie_high':
                    gen_base+=".{}({{{}{{1'b1}}}}),\n".format(int_def['ports'][t]['name'],int_def['ports'][t]['width'])
                elif connect == 'tie_low':
                    gen_base+=".{}({}'d0),\n".format(int_def['ports'][t]['name'],int_def['ports'][t]['width'])
                elif isinstance(connect,int):
                    gen_base+=".{}({}'d{}),\n".format(int_def['ports'][t]['name'],int_def['ports'][t]['width'],connect)
                elif connect != '': #Don't print empty ones
                    gen_base+=connect
        gen_base = gen_base[0:-2] #Remove trailing comma
        self._finish_gen = self.__verilog_base_template.format(self._ip_name,param_base,self._module_instance_name,gen_base)

    def write(self, output):
        output.write(self._finish_gen)