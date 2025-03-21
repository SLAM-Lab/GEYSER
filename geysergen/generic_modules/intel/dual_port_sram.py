
import copy, math
from geysergen.generator import verilog_generator
from geysergen.utils.v_class import v_class
class dual_port_sram(v_class):
    _ip_name="dual_port_sram"
    def __init__(self,generator:verilog_generator,name:str,MEM_BYTES,D_WIDTH,WORD_ADD=1,parameters:dict={}) -> None:
        self._generator=generator
        generator.register_module(self)
        self._module_instance_name = name
        self._interconnects = []
        self.interface_interconnect_sel = {}
        self._parameters={
            "MEM_BYTES":MEM_BYTES,
            "D_WIDTH":D_WIDTH,
            "WORD_ADD":WORD_ADD,
            "A_WIDTH":(int(math.ceil(math.log2(MEM_BYTES))-(0 if WORD_ADD!=1 else math.log2(D_WIDTH/8))))}
        if parameters:
            self._parameters |= parameters
        self._finish_gen=""
        
        # Apply any dynamic port widths
        self.ava_memory_0_interface_definition=copy.deepcopy(dual_port_sram.ava_memory_0_interface_definition)
        self.ava_memory_1_interface_definition=copy.deepcopy(dual_port_sram.ava_memory_1_interface_definition)
        self.ava_memory_0_interface_definition['ports']['writedata']['width']=self._parameters['D_WIDTH']
        self.ava_memory_0_interface_definition['ports']['readdata']['width']=self._parameters['D_WIDTH']
        self.ava_memory_0_interface_definition['ports']['address']['width']=self._parameters['A_WIDTH']
        self.ava_memory_0_interface_definition['ports']['byteenable']['width']=int(self._parameters['D_WIDTH']/8)
        self.ava_memory_1_interface_definition['ports']['writedata']['width']=self._parameters['D_WIDTH']
        self.ava_memory_1_interface_definition['ports']['readdata']['width']=self._parameters['D_WIDTH']
        self.ava_memory_1_interface_definition['ports']['address']['width']=self._parameters['A_WIDTH']
        self.ava_memory_1_interface_definition['ports']['byteenable']['width']=int(self._parameters['D_WIDTH']/8)


        self.clock_connections = []

        self.reset_connections = []

        self.ava_memory_0_connections = []
        self.ava_memory_1_connections = []

        self._interfaces = [(self.clock_connections,self.clock_interface_definition),(self.reset_connections,self.reset_interface_definition),(self.ava_memory_0_connections,self.ava_memory_0_interface_definition),(self.ava_memory_1_connections,self.ava_memory_1_interface_definition),]

    clock_interface_definition = {
        "name": 'clock',
        "type": 'clock',
        "multiconnect": 'false',
        "side": 'sink',
        "ports": {
			'clk':{"name":'clk',"width":1, "dir":'input', "unconnected":'forbidden'},

        },
        
    }


    reset_interface_definition = {
        "name": 'reset',
        "type": 'reset',
        "multiconnect": 'false',
        "side": 'sink',
        "ports": {
			'reset':{"name":'reset',"width":1, "dir":'input', "unconnected":'forbidden'},
			'reset_req':{"name":'reset_req',"width":1, "dir":'input', "unconnected":'nothing'},

        },
        
    }


    ava_memory_0_interface_definition = {
        "name": 'ava_memory_0',
        "type": 'avalon',
        "multiconnect": 'interconnect',
        "side": 'sink',
        "ports": {
			'writedata':{"name":'writedata_0',"width":1, "dir":'input', "unconnected":'nothing'},
			'readdata':{"name":'readdata_0',"width":1, "dir":'output', "unconnected":'nothing'},
			'address':{"name":'address_0',"width":1, "dir":'input', "unconnected":'nothing'},
			'write':{"name":'write_0',"width":1, "dir":'input', "unconnected":'tie_low'},
			'byteenable':{"name":'byteenable_0',"width":1, "dir":'input', "unconnected":'tie_high'},
			'read':{"name":'read_0',"width":1, "dir":'input', "unconnected":'tie_low'},

        },
        
    }

    ava_memory_1_interface_definition = {
        "name": 'ava_memory_1',
        "type": 'avalon',
        "multiconnect": 'interconnect',
        "side": 'sink',
        "ports": {
			'writedata':{"name":'writedata_1',"width":1, "dir":'input', "unconnected":'nothing'},
			'readdata':{"name":'readdata_1',"width":1, "dir":'output', "unconnected":'nothing'},
			'address':{"name":'address_1',"width":1, "dir":'input', "unconnected":'nothing'},
			'write':{"name":'write_1',"width":1, "dir":'input', "unconnected":'tie_low'},
			'byteenable':{"name":'byteenable_1',"width":1, "dir":'input', "unconnected":'tie_high'},
			'read':{"name":'read_1',"width":1, "dir":'input', "unconnected":'tie_low'},

        },
        
    }



    def interface_clock(self) -> tuple['dual_port_sram',str]:
        return (self,"clock")


    def interface_reset(self) -> tuple['dual_port_sram',str]:
        return (self,"reset")


    def interface_ava_memory_0(self) -> tuple['dual_port_sram',str]:
        return (self,"ava_memory_0")

    def interface_ava_memory_1(self) -> tuple['dual_port_sram',str]:
        return (self,"ava_memory_1")

