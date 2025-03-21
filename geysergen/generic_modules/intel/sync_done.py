
import copy, math
from geysergen.generator import verilog_generator
from geysergen.utils.v_class import v_class
class sync_done(v_class):
    _ip_name="sync_done"
    def __init__(self,generator:verilog_generator,name:str,CHANNEL_COUNT,parameters:dict={}) -> None:
        self._generator=generator
        if CHANNEL_COUNT<1 or CHANNEL_COUNT>16:
            self._generator.fail("Sync Done - {} had {} done inputs specified must be in range [1,16]".format(name,CHANNEL_COUNT))
        generator.register_module(self)
        self._module_instance_name = name
        self._interconnects = []
        self.interface_interconnect_sel = {}
        self._parameters={
            "CHANNEL_COUNT":CHANNEL_COUNT}
        if parameters:
            self._parameters |= parameters
        self._finish_gen=""
        
        # Apply any dynamic port widths


        self.clock_connections = []

        self.reset_connections = []

        self.done_0_in_connections = []
        self.done_1_in_connections = []
        self.done_2_in_connections = []
        self.done_3_in_connections = []
        self.done_4_in_connections = []
        self.done_5_in_connections = []
        self.done_6_in_connections = []
        self.done_7_in_connections = []
        self.done_8_in_connections = []
        self.done_9_in_connections = []
        self.done_10_in_connections = []
        self.done_11_in_connections = []
        self.done_12_in_connections = []
        self.done_13_in_connections = []
        self.done_14_in_connections = []
        self.done_15_in_connections = []

        self.synched_done_out_connections = []

        self._interfaces = [(self.clock_connections,self.clock_interface_definition),(self.reset_connections,self.reset_interface_definition),(self.done_0_in_connections,self.done_0_in_interface_definition),(self.done_1_in_connections,self.done_1_in_interface_definition),(self.done_2_in_connections,self.done_2_in_interface_definition),(self.done_3_in_connections,self.done_3_in_interface_definition),(self.done_4_in_connections,self.done_4_in_interface_definition),(self.done_5_in_connections,self.done_5_in_interface_definition),(self.done_6_in_connections,self.done_6_in_interface_definition),(self.done_7_in_connections,self.done_7_in_interface_definition),(self.done_8_in_connections,self.done_8_in_interface_definition),(self.done_9_in_connections,self.done_9_in_interface_definition),(self.done_10_in_connections,self.done_10_in_interface_definition),(self.done_11_in_connections,self.done_11_in_interface_definition),(self.done_12_in_connections,self.done_12_in_interface_definition),(self.done_13_in_connections,self.done_13_in_interface_definition),(self.done_14_in_connections,self.done_14_in_interface_definition),(self.done_15_in_connections,self.done_15_in_interface_definition),(self.synched_done_out_connections,self.synched_done_out_interface_definition),]

    clock_interface_definition = {
        "name": 'clock',
        "type": 'clock',
        "multiconnect": 'false',
        "side": 'sink',
        "ports": {
			'clk':{"name":'fpga_clk',"width":1, "dir":'input', "unconnected":'forbidden'},

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


    done_0_in_interface_definition = {
        "name": 'done_0_in',
        "type": 'conduit',
        "multiconnect": 'false',
        "side": 'sink',
        "ports": {
			'valid':{"name":'done_ch0',"width":1, "dir":'input', "unconnected":'nothing'},

        },
        
    }

    done_1_in_interface_definition = {
        "name": 'done_1_in',
        "type": 'conduit',
        "multiconnect": 'false',
        "side": 'sink',
        "ports": {
			'valid':{"name":'done_ch1',"width":1, "dir":'input', "unconnected":'nothing'},

        },
        
    }

    done_2_in_interface_definition = {
        "name": 'done_2_in',
        "type": 'conduit',
        "multiconnect": 'false',
        "side": 'sink',
        "ports": {
			'valid':{"name":'done_ch2',"width":1, "dir":'input', "unconnected":'nothing'},

        },
        
    }

    done_3_in_interface_definition = {
        "name": 'done_3_in',
        "type": 'conduit',
        "multiconnect": 'false',
        "side": 'sink',
        "ports": {
			'valid':{"name":'done_ch3',"width":1, "dir":'input', "unconnected":'nothing'},

        },
        
    }

    done_4_in_interface_definition = {
        "name": 'done_4_in',
        "type": 'conduit',
        "multiconnect": 'false',
        "side": 'sink',
        "ports": {
			'valid':{"name":'done_ch4',"width":1, "dir":'input', "unconnected":'nothing'},

        },
        
    }

    done_5_in_interface_definition = {
        "name": 'done_5_in',
        "type": 'conduit',
        "multiconnect": 'false',
        "side": 'sink',
        "ports": {
			'valid':{"name":'done_ch5',"width":1, "dir":'input', "unconnected":'nothing'},

        },
        
    }

    done_6_in_interface_definition = {
        "name": 'done_6_in',
        "type": 'conduit',
        "multiconnect": 'false',
        "side": 'sink',
        "ports": {
			'valid':{"name":'done_ch6',"width":1, "dir":'input', "unconnected":'nothing'},

        },
        
    }

    done_7_in_interface_definition = {
        "name": 'done_7_in',
        "type": 'conduit',
        "multiconnect": 'false',
        "side": 'sink',
        "ports": {
			'valid':{"name":'done_ch7',"width":1, "dir":'input', "unconnected":'nothing'},

        },
        
    }

    done_8_in_interface_definition = {
        "name": 'done_8_in',
        "type": 'conduit',
        "multiconnect": 'false',
        "side": 'sink',
        "ports": {
			'valid':{"name":'done_ch8',"width":1, "dir":'input', "unconnected":'nothing'},

        },
        
    }

    done_9_in_interface_definition = {
        "name": 'done_9_in',
        "type": 'conduit',
        "multiconnect": 'false',
        "side": 'sink',
        "ports": {
			'valid':{"name":'done_ch9',"width":1, "dir":'input', "unconnected":'nothing'},

        },
        
    }

    done_10_in_interface_definition = {
        "name": 'done_10_in',
        "type": 'conduit',
        "multiconnect": 'false',
        "side": 'sink',
        "ports": {
			'valid':{"name":'done_ch10',"width":1, "dir":'input', "unconnected":'nothing'},

        },
        
    }

    done_11_in_interface_definition = {
        "name": 'done_11_in',
        "type": 'conduit',
        "multiconnect": 'false',
        "side": 'sink',
        "ports": {
			'valid':{"name":'done_ch11',"width":1, "dir":'input', "unconnected":'nothing'},

        },
        
    }

    done_12_in_interface_definition = {
        "name": 'done_12_in',
        "type": 'conduit',
        "multiconnect": 'false',
        "side": 'sink',
        "ports": {
			'valid':{"name":'done_ch12',"width":1, "dir":'input', "unconnected":'nothing'},

        },
        
    }

    done_13_in_interface_definition = {
        "name": 'done_13_in',
        "type": 'conduit',
        "multiconnect": 'false',
        "side": 'sink',
        "ports": {
			'valid':{"name":'done_ch13',"width":1, "dir":'input', "unconnected":'nothing'},

        },
        
    }

    done_14_in_interface_definition = {
        "name": 'done_14_in',
        "type": 'conduit',
        "multiconnect": 'false',
        "side": 'sink',
        "ports": {
			'valid':{"name":'done_ch14',"width":1, "dir":'input', "unconnected":'nothing'},

        },
        
    }

    done_15_in_interface_definition = {
        "name": 'done_15_in',
        "type": 'conduit',
        "multiconnect": 'false',
        "side": 'sink',
        "ports": {
			'valid':{"name":'done_ch15',"width":1, "dir":'input', "unconnected":'nothing'},

        },
        
    }


    synched_done_out_interface_definition = {
        "name": 'synched_done_out',
        "type": 'conduit',
        "multiconnect": 'false',
        "side": 'source',
        "ports": {
			'valid':{"name":'done_all_channels',"width":1, "dir":'output', "unconnected":'nothing'},

        },
        
    }



    def interface_clock(self) -> tuple['sync_done',str]:
        return (self,"clock")


    def interface_reset(self) -> tuple['sync_done',str]:
        return (self,"reset")


    def interface_done_0_in(self) -> tuple['sync_done',str]:
        return (self,"done_0_in")

    def interface_done_1_in(self) -> tuple['sync_done',str]:
        return (self,"done_1_in")

    def interface_done_2_in(self) -> tuple['sync_done',str]:
        return (self,"done_2_in")

    def interface_done_3_in(self) -> tuple['sync_done',str]:
        return (self,"done_3_in")

    def interface_done_4_in(self) -> tuple['sync_done',str]:
        return (self,"done_4_in")

    def interface_done_5_in(self) -> tuple['sync_done',str]:
        return (self,"done_5_in")

    def interface_done_6_in(self) -> tuple['sync_done',str]:
        return (self,"done_6_in")

    def interface_done_7_in(self) -> tuple['sync_done',str]:
        return (self,"done_7_in")

    def interface_done_8_in(self) -> tuple['sync_done',str]:
        return (self,"done_8_in")

    def interface_done_9_in(self) -> tuple['sync_done',str]:
        return (self,"done_9_in")

    def interface_done_10_in(self) -> tuple['sync_done',str]:
        return (self,"done_10_in")

    def interface_done_11_in(self) -> tuple['sync_done',str]:
        return (self,"done_11_in")

    def interface_done_12_in(self) -> tuple['sync_done',str]:
        return (self,"done_12_in")

    def interface_done_13_in(self) -> tuple['sync_done',str]:
        return (self,"done_13_in")

    def interface_done_14_in(self) -> tuple['sync_done',str]:
        return (self,"done_14_in")

    def interface_done_15_in(self) -> tuple['sync_done',str]:
        return (self,"done_15_in")


    def interface_synched_done_out(self) -> tuple['sync_done',str]:
        return (self,"synched_done_out")
    
    def generate(self):
        for i in range(0,16):
            a = getattr(self,"done_{}_in_connections".format(i))
            if i>=self._parameters["CHANNEL_COUNT"]:
                if(len(a)!=0):
                    self._generator.fail("done_sync {}: Connected done_{}_in but only specified {} done signals".format(self.module_instance_name_,i,self.parameters_["CHANNEL_COUNT"]))
            else:
                if(len(a)==0):
                    self._generator.fail("done_sync {}: done_{}_in is unconnected but {} done signals are expected".format(self.module_instance_name_,i,self.parameters_["CHANNEL_COUNT"]))

        return super().generate()

