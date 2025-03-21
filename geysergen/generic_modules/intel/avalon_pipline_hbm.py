
import copy, math
from geysergen.generator import verilog_generator
from geysergen.utils.v_class import v_class
class avalon_pipline_hbm(v_class):
    _ip_name="full_pipeline"
    def __init__(self,generator:verilog_generator,name:str,CYCLES,parameters:dict={}) -> None:
        self._generator=generator
        generator.register_module(self)
        self._module_instance_name = name
        self._interconnects = []
        self.interface_interconnect_sel = {}
        self._parameters={
            "CYCLES":CYCLES}
        if parameters:
            self._parameters |= parameters
        self._finish_gen=""
        
        # Apply any dynamic port widths


        self.clock_connections = []

        self.reset_connections = []

        self.pipe_in_connections = []

        self.pipe_out_connections = []

        self._interfaces = [(self.clock_connections,self.clock_interface_definition),(self.reset_connections,self.reset_interface_definition),(self.pipe_in_connections,self.pipe_in_interface_definition),(self.pipe_out_connections,self.pipe_out_interface_definition),]

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
			'clk':{"name":'reset',"width":1, "dir":'None', "unconnected":'forbidden'},

        },
        
    }


    pipe_in_interface_definition = {
        "name": 'pipe_in',
        "type": 'avalon',
        "multiconnect": 'interconnect',
        "side": 'sink',
        "ports": {
			'waitrequest':{"name":'s0_waitrequest',"width":1, "dir":'output', "unconnected":'nothing'},
			'writedata':{"name":'s0_writedata',"width":256, "dir":'input', "unconnected":'nothing'},
			'address':{"name":'s0_address',"width":29, "dir":'input', "unconnected":'nothing'},
			'burstcount':{"name":'s0_burstcount',"width":1, "dir":'input', "unconnected":'nothing'},
			'readdata':{"name":'s0_readdata',"width":256, "dir":'output', "unconnected":'nothing'},
			'readdatavalid':{"name":'s0_readdatavalid',"width":1, "dir":'output', "unconnected":'nothing'},
			'write':{"name":'s0_write',"width":1, "dir":'input', "unconnected":'tie_low'},
			'read':{"name":'s0_read',"width":1, "dir":'input', "unconnected":'tie_low'},
			'byteenable':{"name":'s0_byteenable',"width":32, "dir":'input', "unconnected":'tie_high'},

        },
        
    }


    pipe_out_interface_definition = {
        "name": 'pipe_out',
        "type": 'avalon',
        "multiconnect": 'interconnect',
        "side": 'source',
        "ports": {
			'waitrequest':{"name":'m0_waitrequest',"width":1, "dir":'input', "unconnected":'nothing'},
			'writedata':{"name":'m0_writedata',"width":256, "dir":'output', "unconnected":'nothing'},
			'address':{"name":'m0_address',"width":29, "dir":'output', "unconnected":'nothing'},
			'burstcount':{"name":'m0_burstcount',"width":1, "dir":'output', "unconnected":'nothing'},
			'readdata':{"name":'m0_readdata',"width":256, "dir":'input', "unconnected":'nothing'},
			'readdatavalid':{"name":'m0_readdatavalid',"width":1, "dir":'input', "unconnected":'nothing'},
			'write':{"name":'m0_write',"width":1, "dir":'output', "unconnected":'nothing'},
			'read':{"name":'m0_read',"width":1, "dir":'output', "unconnected":'nothing'},
			'byteenable':{"name":'m0_byteenable',"width":32, "dir":'output', "unconnected":'nothing'},

        },
        "pass_clock":"clock",
    }



    def interface_clock(self) -> tuple['avalon_pipline_hbm',str]:
        return (self,"clock")


    def interface_reset(self) -> tuple['avalon_pipline_hbm',str]:
        return (self,"reset")


    def interface_pipe_in(self) -> tuple['avalon_pipline_hbm',str]:
        return (self,"pipe_in")


    def interface_pipe_out(self) -> tuple['avalon_pipline_hbm',str]:
        return (self,"pipe_out")
    
    def generate(self):
        self.d_width=1
        self.a_width=1
        self.b_width=1
        for int_connections, int_def in self._interfaces:

            #We are going to scan for some necessary information

            if int_def==self.pipe_in_interface_definition:
                for conn in int_connections:
                    for port in conn:
                        if port['type']=='readdata':
                            if self.d_width<port['width']:
                                self.d_width=port['width']
                        elif port['type']=='writedata':
                            if self.d_width<port['width']:
                                self.d_width=port['width']
                        elif port['type']=='address':
                            if self.a_width<port['width']:
                                self.a_width=port['width']
                        elif port['type']=='burstcount':
                            if self.b_width<port['width']:
                                self.b_width=port['width']
        self._parameters['BURSTCOUNT_WIDTH']=self.b_width
        self._parameters['DATA_WIDTH']=self.d_width
        self._parameters['HDL_ADDR_WIDTH']=self.a_width

        super().generate()

