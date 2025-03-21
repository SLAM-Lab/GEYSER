
import copy, math
from geysergen.generator import verilog_generator
from geysergen.utils.v_class import v_class
class avalon_pipline(v_class):
    _ip_name="interface_pipeline"
    def __init__(self,generator:verilog_generator,name:str,CYCLES,DATA_WIDTH,ADDR_WIDTH,MODE=2,parameters:dict={}) -> None:
        self._generator=generator
        generator.register_module(self)
        self._module_instance_name = name
        self._interconnects = []
        self.interface_interconnect_sel = {}
        self._parameters={
            "CYCLES":CYCLES,
            "AWIDTH":ADDR_WIDTH,
            "DWIDTH":DATA_WIDTH,
            "READWRITE_MODE":MODE
            }
        if parameters:
            self._parameters |= parameters
        self._finish_gen=""
        self.pipe_in_interface_definition=copy.deepcopy(avalon_pipline.pipe_in_interface_definition)
        self.avalon_out_interface_definition=copy.deepcopy(avalon_pipline.pipe_out_interface_definition)
        self.pipe_in_interface_definition['ports']['writedata']['width']=self._parameters['DWIDTH']
        self.pipe_in_interface_definition['ports']['readdata']['width']=self._parameters['DWIDTH']
        self.pipe_in_interface_definition['ports']['address']['width']=self._parameters['AWIDTH']
        self.pipe_out_interface_definition['ports']['writedata']['width']=self._parameters['DWIDTH']
        self.pipe_out_interface_definition['ports']['readdata']['width']=self._parameters['DWIDTH']
        self.pipe_out_interface_definition['ports']['address']['width']=self._parameters['AWIDTH']
        # Apply any dynamic port widths
        if MODE == 1:
            del self.pipe_in_interface_definition['ports']['readdata']
            del self.pipe_in_interface_definition['ports']['read']
            del self.pipe_out_interface_definition['ports']['readdata']
            del self.pipe_out_interface_definition['ports']['read']
        elif MODE == 0:
            del self.pipe_in_interface_definition['ports']['writedata']
            del self.pipe_in_interface_definition['ports']['write']
            del self.pipe_out_interface_definition['ports']['writedata']
            del self.pipe_out_interface_definition['ports']['write']

        self.clock_connections = []

        self.pipe_in_connections = []

        self.pipe_out_connections = []

        self._interfaces = [(self.clock_connections,self.clock_interface_definition),(self.pipe_in_connections,self.pipe_in_interface_definition),(self.pipe_out_connections,self.pipe_out_interface_definition),]

    clock_interface_definition = {
        "name": 'clock',
        "type": 'clock',
        "multiconnect": 'false',
        "side": 'sink',
        "ports": {
			'clk':{"name":'clk',"width":1, "dir":'input', "unconnected":'forbidden'},

        },
        
    }


    pipe_in_interface_definition = {
        "name": 'pipe_in',
        "type": 'avalon',
        "multiconnect": 'interconnect',
        "side": 'sink',
        "ports": {
			'writedata':{"name":'writedata_in',"width":256, "dir":'input', "unconnected":'nothing'},
			'readdata':{"name":'readdata_out',"width":256, "dir":'output', "unconnected":'nothing'},
			'address':{"name":'address_in',"width":64, "dir":'input', "unconnected":'nothing'},
			'write':{"name":'write_in',"width":1, "dir":'input', "unconnected":'tie_low'},
			'read':{"name":'read_in',"width":1, "dir":'input', "unconnected":'tie_low'},

        },
        
    }


    pipe_out_interface_definition = {
        "name": 'pipe_out',
        "type": 'avalon',
        "multiconnect": 'interconnect',
        "side": 'source',
        "ports": {
			'writedata':{"name":'writedata_out',"width":256, "dir":'output', "unconnected":'nothing'},
			'readdata':{"name":'readdata_in',"width":256, "dir":'input', "unconnected":'nothing'},
			'address':{"name":'address_out',"width":64, "dir":'output', "unconnected":'nothing'},
			'write':{"name":'write_out',"width":1, "dir":'output', "unconnected":'nothing'},
			'read':{"name":'read_out',"width":1, "dir":'output', "unconnected":'nothing'},

        },
        "pass_clock":"clock",
    }



    def interface_clock(self) -> tuple['avalon_pipline',str]:
        return (self,"clock")


    def interface_pipe_in(self) -> tuple['avalon_pipline',str]:
        return (self,"pipe_in")


    def interface_pipe_out(self) -> tuple['avalon_pipline',str]:
        return (self,"pipe_out")

    def generate(self) -> None:
        # self.d_width=0
        # self.a_width=0
        # read0 = False
        # write0 = False
        # read1 = False
        # write1 = False
        # for int_connections, int_def in self._interfaces:

        #     #We are going to scan for some necessary information

        #     if int_def==self.pipe_in_interface_definition:
        #         for conn in int_connections:
        #             for port in conn:
        #                 if port['type']=='readdata':
        #                     if self.d_width<port['width']:
        #                         self.d_width=port['width']
        #                     read0 = True
        #                 elif port['type']=='writedata':
        #                     write0 = True
        #                     if self.d_width<port['width']:
        #                         self.d_width=port['width']
        #                 elif port['type']=='address':
        #                     if self.a_width<port['width']:
        #                         self.a_width=port['width']

        #     if int_def==self.pipe_out_interface_definition:
        #         for conn in int_connections:
        #             for port in conn:
        #                 if port['type']=='readdata':
        #                     read1 = True
        #                 elif port['type']=='writedata':
        #                     write1 = True
        # if read0 and read1:
        #     r_w =0
        #     if write0 and write1:
        #         r_w =2
        # else:
        #     r_w =1
    
        # self._parameters['READWRITE_MODE']=r_w
        # self._parameters['DWIDTH']=self.d_width
        # self._parameters['AWIDTH']=self.a_width
        super().generate()
