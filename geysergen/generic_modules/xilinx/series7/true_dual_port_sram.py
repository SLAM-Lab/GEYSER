
import copy, math
from geysergen.generator import verilog_generator
from geysergen.utils.v_class import v_class
class true_dual_port_sram(v_class):
    _ip_name = "true_dual_port_sram"
    def __init__(self,generator:verilog_generator,name:str,MEM_BYTES,DATA_WIDTH,BYTE_ADDRESSING=0,LATENCY=2,parameters:dict={}) -> None:
        self._generator=generator
        generator.register_module(self)
        self._module_instance_name = name
        self._interconnects = []
        self.interface_interconnect_sel = {}
        self._parameters={
            "MEM_BYTES":MEM_BYTES,
            "DATA_WIDTH":DATA_WIDTH,
            "BYTE_ADDRESSING":BYTE_ADDRESSING,
            "LATENCY":LATENCY}
        if parameters:
            self._parameters |= parameters
        self._finish_gen=""
        
        # Apply any dynamic port widths
        self.bram_port_a_interface_definition=copy.deepcopy(true_dual_port_sram.bram_port_a_interface_definition)
        self.bram_port_b_interface_definition=copy.deepcopy(true_dual_port_sram.bram_port_b_interface_definition)
        self.bram_port_a_interface_definition['ports']['din']['width']=self._parameters['DATA_WIDTH']
        self.bram_port_a_interface_definition['ports']['dout']['width']=self._parameters['DATA_WIDTH']
        self.bram_port_a_interface_definition['ports']['we']['width']=int(self._parameters['DATA_WIDTH']/8)
        self.bram_port_a_interface_definition['ports']['addr']['width']=int(math.log2(self._parameters['MEM_BYTES'])) if self._parameters['BYTE_ADDRESSING'] else int(math.log2(self._parameters['MEM_BYTES']/(self._parameters['DATA_WIDTH']/8))) 
        self.bram_port_b_interface_definition['ports']['din']['width']=self._parameters['DATA_WIDTH']
        self.bram_port_b_interface_definition['ports']['dout']['width']=self._parameters['DATA_WIDTH']
        self.bram_port_b_interface_definition['ports']['we']['width']=int(self._parameters['DATA_WIDTH']/8)
        self.bram_port_b_interface_definition['ports']['addr']['width']=int(math.log2(self._parameters['MEM_BYTES'])) if self._parameters['BYTE_ADDRESSING'] else int(math.log2(self._parameters['MEM_BYTES']/(self._parameters['DATA_WIDTH']/8))) 


        self.bram_port_a_connections = []
        self.bram_port_b_connections = []

        self._interfaces = [(self.bram_port_a_connections,self.bram_port_a_interface_definition),(self.bram_port_b_connections,self.bram_port_b_interface_definition),]

    bram_port_a_interface_definition = {
        "name": 'bram_port_a',
        "type": 'bram',
        "multiconnect": 'false',
        "side": 'sink',
        "ports": {
			'din':{"name":'dina',"width":1, "dir":'input', "unconnected":8},
			'dout':{"name":'douta',"width":1, "dir":'output', "unconnected":'nothing'},
			'en':{"name":'ena',"width":1, "dir":'input', "unconnected":'nothing'},
			'we':{"name":'wea',"width":1, "dir":'input', "unconnected":'nothing'},
			'addr':{"name":'addra',"width":1, "dir":'input', "unconnected":'nothing'},
			'clk':{"name":'clka',"width":1, "dir":'input', "unconnected":'nothing'},
			'rst':{"name":'reseta',"width":1, "dir":'input', "unconnected":'nothing'},

        },
        
    }

    bram_port_b_interface_definition = {
        "name": 'bram_port_b',
        "type": 'bram',
        "multiconnect": 'false',
        "side": 'sink',
        "ports": {
			'din':{"name":'dinb',"width":1, "dir":'input', "unconnected":8},
			'dout':{"name":'doutb',"width":1, "dir":'output', "unconnected":'nothing'},
			'en':{"name":'enb',"width":1, "dir":'input', "unconnected":'nothing'},
			'we':{"name":'web',"width":1, "dir":'input', "unconnected":'nothing'},
			'addr':{"name":'addrb',"width":1, "dir":'input', "unconnected":'nothing'},
			'clk':{"name":'clkb',"width":1, "dir":'input', "unconnected":'nothing'},
			'rst':{"name":'resetb',"width":1, "dir":'input', "unconnected":'nothing'},

        },
        
    }



    def interface_bram_port_a(self) -> tuple['true_dual_port_sram',str]:
        return (self,"bram_port_a")

    def interface_bram_port_b(self) -> tuple['true_dual_port_sram',str]:
        return (self,"bram_port_b")

