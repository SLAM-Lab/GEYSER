
import copy, math
from geysergen.generator import verilog_generator
from geysergen.utils.v_class import v_class
class avalon_byte_to_word(v_class):
    _ip_name="Avalon_Byte_to_Word"
    def __init__(self,generator:verilog_generator,name:str,DATA_WIDTH,ADDR_WIDTH,BURSTCOUNT_WIDTH=1,read_write=2,parameters:dict={}) -> None:
        """
        read_write
        0 = read 
        1 = write
        2 = both
        """
        self._generator=generator
        generator.register_module(self)
        self._module_instance_name = name
        self._interconnects = []
        self.interface_interconnect_sel = {}
        self._parameters={
            "DATA_WIDTH":DATA_WIDTH,
            "ADDR_WIDTH":ADDR_WIDTH,
            "BURSTCOUNT_WIDTH":BURSTCOUNT_WIDTH,
            "SYMBOL_WIDTH":8}
        if parameters:
            self._parameters |= parameters
        self._finish_gen=""
        
        # Apply any dynamic port widths
        self.avalon_in_interface_definition=copy.deepcopy(avalon_byte_to_word.avalon_in_interface_definition)
        self.avalon_out_interface_definition=copy.deepcopy(avalon_byte_to_word.avalon_out_interface_definition)
        self.avalon_in_interface_definition['ports']['burstcount']['width']=self._parameters['BURSTCOUNT_WIDTH']
        self.avalon_in_interface_definition['ports']['byteenable']['width']=int(self._parameters['DATA_WIDTH']/self._parameters['SYMBOL_WIDTH'])
        self.avalon_in_interface_definition['ports']['writedata']['width']=self._parameters['DATA_WIDTH']
        self.avalon_in_interface_definition['ports']['readdata']['width']=self._parameters['DATA_WIDTH']
        self.avalon_in_interface_definition['ports']['address']['width']=self._parameters['ADDR_WIDTH']
        self.avalon_out_interface_definition['ports']['burstcount']['width']=self._parameters['BURSTCOUNT_WIDTH']
        self.avalon_out_interface_definition['ports']['byteenable']['width']=int(self._parameters['DATA_WIDTH']/self._parameters['SYMBOL_WIDTH'])
        self.avalon_out_interface_definition['ports']['writedata']['width']=self._parameters['DATA_WIDTH']
        self.avalon_out_interface_definition['ports']['readdata']['width']=self._parameters['DATA_WIDTH']
        self.avalon_out_interface_definition['ports']['address']['width']=self._parameters['ADDR_WIDTH']-int(math.log2(self._parameters['DATA_WIDTH']/8))

        if read_write == 1:
            del self.avalon_in_interface_definition['ports']['readdata']
            del self.avalon_in_interface_definition['ports']['readdatavalid']
            del self.avalon_in_interface_definition['ports']['read']
            del self.avalon_out_interface_definition['ports']['readdata']
            del self.avalon_out_interface_definition['ports']['readdatavalid']
            del self.avalon_out_interface_definition['ports']['read']
        elif read_write == 0:
            del self.avalon_in_interface_definition['ports']['writedata']
            del self.avalon_in_interface_definition['ports']['write']
            del self.avalon_out_interface_definition['ports']['writedata']
            del self.avalon_out_interface_definition['ports']['write']

        self.clock_connections = []

        self.avalon_in_connections = []

        self.avalon_out_connections = []

        self._interfaces = [(self.clock_connections,self.clock_interface_definition),(self.avalon_in_connections,self.avalon_in_interface_definition),(self.avalon_out_connections,self.avalon_out_interface_definition),]

    clock_interface_definition = {
        "name": 'clock',
        "type": 'clock',
        "multiconnect": 'false',
        "side": 'sink',
        "ports": {
			'clk':{"name":'clk',"width":1, "dir":'input', "unconnected":'forbidden'},

        },
        
    }


    avalon_in_interface_definition = {
        "name": 'avalon_in',
        "type": 'avalon',
        "multiconnect": 'interconnect',
        "side": 'sink',
        "ports": {
			'waitrequest':{"name":'s0_waitrequest',"width":1, "dir":'output', "unconnected":'nothing'},
			'readdatavalid':{"name":'s0_readdatavalid',"width":1, "dir":'output', "unconnected":'nothing'},
			'burstcount':{"name":'s0_burstcount',"width":1, "dir":'input', "unconnected":'nothing'},
			'byteenable':{"name":'s0_byteenable',"width":1, "dir":'input', "unconnected":'tie_high'},
			'writedata':{"name":'s0_writedata',"width":1, "dir":'input', "unconnected":'nothing'},
			'readdata':{"name":'s0_readdata',"width":1, "dir":'output', "unconnected":'nothing'},
			'address':{"name":'s0_address',"width":1, "dir":'input', "unconnected":'nothing'},
			'write':{"name":'s0_write',"width":1, "dir":'input', "unconnected":'tie_low'},
			'read':{"name":'s0_read',"width":1, "dir":'input', "unconnected":'tie_low'},

        },
        
    }


    avalon_out_interface_definition = {
        "name": 'avalon_out',
        "type": 'avalon',
        "multiconnect": 'interconnect',
        "side": 'source',
        "ports": {
			'waitrequest':{"name":'m0_waitrequest',"width":1, "dir":'input', "unconnected":'nothing'},
			'readdatavalid':{"name":'m0_readdatavalid',"width":1, "dir":'input', "unconnected":'nothing'},
			'burstcount':{"name":'m0_burstcount',"width":1, "dir":'output', "unconnected":'nothing'},
			'byteenable':{"name":'m0_byteenable',"width":1, "dir":'output', "unconnected":'nothing'},
			'writedata':{"name":'m0_writedata',"width":1, "dir":'output', "unconnected":'nothing'},
			'readdata':{"name":'m0_readdata',"width":1, "dir":'input', "unconnected":'nothing'},
			'address':{"name":'m0_address',"width":1, "dir":'output', "unconnected":'nothing'},
			'write':{"name":'m0_write',"width":1, "dir":'output', "unconnected":'nothing'},
			'read':{"name":'m0_read',"width":1, "dir":'output', "unconnected":'nothing'},

        },
        "pass_clock":"clock",
    }



    def interface_clock(self) -> tuple['avalon_byte_to_word',str]:
        return (self,"clock")


    def interface_avalon_in(self) -> tuple['avalon_byte_to_word',str]:
        return (self,"avalon_in")


    def interface_avalon_out(self) -> tuple['avalon_byte_to_word',str]:
        return (self,"avalon_out")

