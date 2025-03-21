
import copy, math
from geysergen.generator import verilog_generator
from geysergen.utils.v_class import v_class
class top_level(v_class):
    _ip_name = "top"
    def __init__(self,generator:verilog_generator,name:str,parameters:dict={}) -> None:
        self._generator=generator
        generator.register_module(self)
        self._module_instance_name = name
        self._interconnects = []
        self.interface_interconnect_sel = {}
        self._parameters={}
        if parameters:
            self._parameters |= parameters
        self._finish_gen=""
        
        # Apply any dynamic port widths


        self.ap_clk_connections = []

        self.ap_rst_connections = []

        self.ap_ctrl0_connections = []

        self.ap_ctrl1_connections = []

        self._interfaces = [(self.ap_clk_connections,self.ap_clk_interface_definition),(self.ap_rst_connections,self.ap_rst_interface_definition),(self.ap_ctrl0_connections,self.ap_ctrl0_interface_definition),(self.ap_ctrl1_connections,self.ap_ctrl1_interface_definition),]

    ap_clk_interface_definition = {
        "name": 'ap_clk',
        "type": 'clock',
        "multiconnect": 'shared',
        "side": 'source',
        "ports": {
			'clk':{"name":'ap_clk',"width":1, "dir":'output', "unconnected":'nothing'},

        },
        
    }


    ap_rst_interface_definition = {
        "name": 'ap_rst',
        "type": 'reset',
        "multiconnect": 'shared',
        "side": 'source',
        "ports": {
			'rst':{"name":'ap_rst',"width":1, "dir":'None', "unconnected":'nothing'},

        },
        
    }


    ap_ctrl0_interface_definition = {
        "name": 'ap_ctrl0',
        "type": 'acc_handshake',
        "multiconnect": 'false',
        "side": 'source',
        "ports": {
			'start':{"name":'ap_start0',"width":1, "dir":'None', "unconnected":'nothing'},
			'done':{"name":'ap_done0',"width":1, "dir":'None', "unconnected":'nothing'},
			'idle':{"name":'ap_idle0',"width":1, "dir":'None', "unconnected":'nothing'},
			'ready':{"name":'ap_ready0',"width":1, "dir":'None', "unconnected":'nothing'},

        },
        
    }


    ap_ctrl1_interface_definition = {
        "name": 'ap_ctrl1',
        "type": 'acc_handshake',
        "multiconnect": 'false',
        "side": 'source',
        "ports": {
			'start':{"name":'ap_start1',"width":1, "dir":'None', "unconnected":'nothing'},
			'done':{"name":'ap_done1',"width":1, "dir":'None', "unconnected":'nothing'},
			'idle':{"name":'ap_idle1',"width":1, "dir":'None', "unconnected":'nothing'},
			'ready':{"name":'ap_ready1',"width":1, "dir":'None', "unconnected":'nothing'},

        },
        
    }



    def interface_ap_clk(self) -> tuple['top_level',str]:
        return (self,"ap_clk")


    def interface_ap_rst(self) -> tuple['top_level',str]:
        return (self,"ap_rst")


    def interface_ap_ctrl0(self) -> tuple['top_level',str]:
        return (self,"ap_ctrl0")


    def interface_ap_ctrl1(self) -> tuple['top_level',str]:
        return (self,"ap_ctrl1")

