
import copy, math
from geysergen.generator import verilog_generator
from geysergen.utils.v_class import v_class
class compute(v_class):
    _ip_name = "compute_0"
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

        self.ap_ctrl_connections = []

        self.port0_porta_connections = []

        self.port0_portb_connections = []

        self.port1_porta_connections = []

        self.port2_porta_connections = []

        self._interfaces = [(self.ap_clk_connections,self.ap_clk_interface_definition),(self.ap_rst_connections,self.ap_rst_interface_definition),(self.ap_ctrl_connections,self.ap_ctrl_interface_definition),(self.port0_porta_connections,self.port0_porta_interface_definition),(self.port0_portb_connections,self.port0_portb_interface_definition),(self.port1_porta_connections,self.port1_porta_interface_definition),(self.port2_porta_connections,self.port2_porta_interface_definition),]

    ap_clk_interface_definition = {
        "name": 'ap_clk',
        "type": 'clock',
        "multiconnect": 'false',
        "side": 'sink',
        "ports": {
			'clk':{"name":'ap_clk',"width":1, "dir":'input', "unconnected":'nothing'},

        },
        
    }


    ap_rst_interface_definition = {
        "name": 'ap_rst',
        "type": 'reset',
        "multiconnect": 'false',
        "side": 'sink',
        "ports": {
			'rst':{"name":'ap_rst',"width":1, "dir":'input', "unconnected":'nothing'},

        },
        
    }


    ap_ctrl_interface_definition = {
        "name": 'ap_ctrl',
        "type": 'acc_handshake',
        "multiconnect": 'false',
        "side": 'sink',
        "ports": {
			'start':{"name":'ap_start',"width":1, "dir":'input', "unconnected":'nothing'},
			'done':{"name":'ap_done',"width":1, "dir":'output', "unconnected":'nothing'},
			'idle':{"name":'ap_idle',"width":1, "dir":'output', "unconnected":'nothing'},
			'ready':{"name":'ap_ready',"width":1, "dir":'output', "unconnected":'nothing'},

        },
        
    }


    port0_porta_interface_definition = {
        "name": 'port0_porta',
        "type": 'bram',
        "multiconnect": 'interconnect',
        "side": 'source',
        "ports": {
			'clk':{"name":'port0_Clk_A',"width":1, "dir":'output', "unconnected":'nothing'},
			'rst':{"name":'port0_Rst_A',"width":1, "dir":'output', "unconnected":'nothing'},
			'en':{"name":'port0_EN_A',"width":1, "dir":'output', "unconnected":'nothing'},
			'we':{"name":'port0_WEN_A',"width":4, "dir":'output', "unconnected":'nothing'},
			'addr':{"name":'port0_Addr_A',"width":32, "dir":'output', "unconnected":'nothing'},
			'din':{"name":'port0_Din_A',"width":32, "dir":'output', "unconnected":'nothing'},
			'dout':{"name":'port0_Dout_A',"width":32, "dir":'input', "unconnected":8},

        },
        
    }


    port0_portb_interface_definition = {
        "name": 'port0_portb',
        "type": 'bram',
        "multiconnect": 'interconnect',
        "side": 'source',
        "ports": {
			'clk':{"name":'port0_Clk_B',"width":1, "dir":'output', "unconnected":'nothing'},
			'rst':{"name":'port0_Rst_B',"width":1, "dir":'output', "unconnected":'nothing'},
			'en':{"name":'port0_EN_B',"width":1, "dir":'output', "unconnected":'nothing'},
			'we':{"name":'port0_WEN_B',"width":4, "dir":'output', "unconnected":'nothing'},
			'addr':{"name":'port0_Addr_B',"width":32, "dir":'output', "unconnected":'nothing'},
			'din':{"name":'port0_Din_B',"width":32, "dir":'output', "unconnected":'nothing'},
			'dout':{"name":'port0_Dout_B',"width":32, "dir":'input', "unconnected":8},

        },
        
    }


    port1_porta_interface_definition = {
        "name": 'port1_porta',
        "type": 'bram',
        "multiconnect": 'interconnect',
        "side": 'source',
        "ports": {
			'clk':{"name":'port1_Clk_A',"width":1, "dir":'output', "unconnected":'nothing'},
			'rst':{"name":'port1_Rst_A',"width":1, "dir":'output', "unconnected":'nothing'},
			'en':{"name":'port1_EN_A',"width":1, "dir":'output', "unconnected":'nothing'},
			'we':{"name":'port1_WEN_A',"width":4, "dir":'output', "unconnected":'nothing'},
			'addr':{"name":'port1_Addr_A',"width":32, "dir":'output', "unconnected":'nothing'},
			'din':{"name":'port1_Din_A',"width":32, "dir":'output', "unconnected":'nothing'},
			'dout':{"name":'port1_Dout_A',"width":32, "dir":'input', "unconnected":8},

        },
        
    }


    port2_porta_interface_definition = {
        "name": 'port2_porta',
        "type": 'bram',
        "multiconnect": 'interconnect',
        "side": 'source',
        "ports": {
			'clk':{"name":'port2_Clk_A',"width":1, "dir":'output', "unconnected":'nothing'},
			'rst':{"name":'port2_Rst_A',"width":1, "dir":'output', "unconnected":'nothing'},
			'en':{"name":'port2_EN_A',"width":1, "dir":'output', "unconnected":'nothing'},
			'we':{"name":'port2_WEN_A',"width":4, "dir":'output', "unconnected":'nothing'},
			'addr':{"name":'port2_Addr_A',"width":32, "dir":'output', "unconnected":'nothing'},
			'din':{"name":'port2_Din_A',"width":32, "dir":'output', "unconnected":'nothing'},
			'dout':{"name":'port2_Dout_A',"width":32, "dir":'input', "unconnected":8},

        },
        
    }



    def interface_ap_clk(self) -> tuple['compute',str]:
        return (self,"ap_clk")


    def interface_ap_rst(self) -> tuple['compute',str]:
        return (self,"ap_rst")


    def interface_ap_ctrl(self) -> tuple['compute',str]:
        return (self,"ap_ctrl")


    def interface_port0_porta(self) -> tuple['compute',str]:
        return (self,"port0_porta")


    def interface_port0_portb(self) -> tuple['compute',str]:
        return (self,"port0_portb")


    def interface_port1_porta(self) -> tuple['compute',str]:
        return (self,"port1_porta")


    def interface_port2_porta(self) -> tuple['compute',str]:
        return (self,"port2_porta")

