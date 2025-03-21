from pathlib import Path
#This is the main template for the generated interconnect


demux_template = """
avalon_demux1xN #(
.READWRITE_MODE({rw_mode}),
.NUM_SLAVES({n_slaves}),
.DWIDTH({d_width}),
.MAWIDTH({ma_width}),
.SAWIDTH({sa_width})
){name}(
{connections}
);
"""

mux_template = """
avalon_muxNx1 #(.NUM_MASTERS({n_mas}),
    .DWIDTH({d_width}),
    .AWIDTH({a_width}),
	.MASTER0_READWRITE_MODE({m0}),
	.MASTER1_READWRITE_MODE({m1}),
	.MASTER2_READWRITE_MODE({m2}),
	.MASTER3_READWRITE_MODE({m3}))
    {name}
(
{connections}
);
"""

def Assert(result:bool,message:str):
    if result:
        return
    print("Failed check: "+message)
    exit(1)


#TODO deal with negative signals
class avalon_mm_interconnect:
    def __init__(self, name:str, generator) -> None:
        self.name_=name
        self.generator_=generator
        #Register ourself with the generator
        generator.register_interconnect(self)

    #Return the single connection to the sink or source
    def make_interconnect(self,multi_interfaces,side,extras=None) -> dict:
        if side=='sink' or side=='end':
            self.name_=self.name_+'mux'
            return self.make_mux_(multi_interfaces,extras)
        else:
            self.name_=self.name_+'demux'
            return self.make_demux_(multi_interfaces,extras)

    def write(self,output_file) -> None:
        output_file.write(self.to_write_)
    

    def make_demux_(self,multi_interfaces,extras) -> dict:
        Assert(len(multi_interfaces)==2 or len(multi_interfaces)==4,"{} Only two or four avalon interfaces are currently supported in a demux".format(self.name_))

        #Get some preliminary information from the interfaces

        a_width = 0
        d_width = 0
        read = False
        write = False
        for interface in multi_interfaces:
            for sig in interface:
                if sig['type']=='address':
                    if a_width==0:
                        a_width=sig['width']
                    else:
                        Assert(a_width==sig['width'],"DEMUX ERROR: All interfaces must have the same address width {} != {}".format(a_width,sig['width']))
                if 'readdata'==sig['type']:
                    if d_width == 0:
                        d_width = sig['width']
                    else:
                        Assert(d_width==sig['width'],"DEMUX ERROR: All interfaces must have the same data width {} != {}".format(d_width,sig['width']))
                    read=True
                if 'writedata' ==sig['type']:
                    if d_width == 0:
                        d_width = sig['width']
                    else:
                        Assert(d_width==sig['width'],"DEMUX ERROR: All interfaces must have the same data width {} != {}".format(d_width,sig['width']))
                    write=True

        Assert(read or write,"No read or write signals in demux")

        if read and write:
            mode = 2
        elif write:
            mode = 1
        else:
            mode = 0

        if len(multi_interfaces)==2:
            ma_width = a_width+1
        else:
            ma_width = a_width+2
        
        connect_text = ""
        
        add_p = False
        r_data_p = False
        w_data_p = False
        w_p = False
        r_p = False

        count = 1
        if(extras==None or not "clock" in extras):
            self.generator_.fail("demux {} was not provided a clock. Use interconnect_settings to specify clock to be passed".format(self.name_))
        for stuff in extras["clock"]:
            if stuff["type"]=="clk":
                connect_text+= ".clock({}),\n".format(stuff['connection_port_name'])
            if stuff["type"]=="clk_n":
                connect_text+= ".clock(~{}),\n".format(stuff['connection_port_name'])

        for inter_i in multi_interfaces:

            for inter in inter_i:
                if inter['type']=="address":
                    connect_text+= ".avs_m{0}_address({1}),\n".format(count,inter['connection_port_name'])
                    add_p=True
                elif inter['type']=="readdata":
                    connect_text+= ".avs_m{0}_readdata({1}),\n".format(count,inter['connection_port_name'])
                    r_data_p=True
                elif inter['type']=="writedata":
                    connect_text+= ".avs_m{0}_writedata({1}),\n".format(count,inter['connection_port_name'])
                    w_data_p=True
                elif inter['type']=="write":
                    connect_text+= ".avs_m{0}_write({1}),\n".format(count,inter['connection_port_name'])
                    w_p=True
                elif inter['type']=="write_n":
                    connect_text+= ".avs_m{0}_write({1}),\n".format(count,self.generator_.invert_wire(inter['connection_port_name']))
                    w_p=True
                elif inter['type']=="read":
                    connect_text+= ".avs_m{0}_read({1}),\n".format(count,inter['connection_port_name'])
                    r_p=True
                elif inter['type']=="read_n":
                    connect_text+= ".avs_m{0}_read({1}),\n".format(count,self.generator_.invert_wire(inter['connection_port_name']))
                    r_p=True
            count+=1

        name = self.name_
        mconnections = {}

        if add_p:
            mconnections["address"]="mm_s_address_{}".format(name)
            self.generator_.add_wire("mm_s_address_{}".format(name),ma_width)
            connect_text+=".avs_s0_address(mm_s_address_{0}),".format(name)

        if r_data_p:
            mconnections["readdata"]= "mm_s_readdata_{}".format(name)
            self.generator_.add_wire("mm_s_readdata_{}".format(name),d_width)
            connect_text+=".avs_s0_readdata(mm_s_readdata_{0}),".format(name)

        if w_data_p:
            mconnections["writedata"]= "mm_s_writedata_{}".format(name)
            self.generator_.add_wire("mm_s_writedata_{}".format(name),d_width)
            connect_text+=".avs_s0_writedata(mm_s_writedata_{0}),".format(name)

        if w_p:
            mconnections["write"]= "mm_s_write_{}".format(name)
            self.generator_.add_wire("mm_s_write_{}".format(name),1)
            connect_text+=".avs_s0_write(mm_s_write_{0}),".format(name)

        if r_p:
            mconnections["read"]= "mm_s_read_{}".format(name)
            self.generator_.add_wire("mm_s_read_{}".format(name),1)
            connect_text+=".avs_s0_read(mm_s_read_{0}),".format(name)

        connect_text=connect_text[:-1]

        self.to_write_ = demux_template.format(name=self.name_,ma_width=ma_width,sa_width=a_width,n_slaves=len(multi_interfaces),rw_mode=mode,d_width=d_width,connections=connect_text)
        return mconnections

    def make_mux_(self,multi_interfaces,extras) -> dict:
        Assert(len(multi_interfaces)==2 or len(multi_interfaces)==4,"{} Only two or four avalon interfaces are currently supported in a mux".format(self.name_))

        #Get some preliminary information from the interfaces

        a_width = 0
        d_width = 0
        read = [False,False,False,False]
        write = [False,False,False,False]
        count = 0
        for interface in multi_interfaces:
            for sig in interface:
                if sig['type']=='address':
                    if a_width==0:
                        a_width=sig['width']
                    else:
                        Assert(a_width==sig['width'],"MUX {} All interfaces must have the same address width {} != {}".format(self.name_,a_width,sig['width']))
                if 'readdata'==sig['type']:
                    if d_width == 0:
                        d_width = sig['width']
                    else:
                        Assert(d_width==sig['width'],"MUX {} All interfaces must have the same data width {} != {}".format(self.name_,d_width,sig['width']))
                    read[count]=True
                if 'writedata' ==sig['type']:
                    if d_width == 0:
                        d_width = sig['width']
                    else:
                        Assert(d_width==sig['width'],"MUX {} All interfaces must have the same data width {} != {}".format(self.name_,d_width,sig['width']))
                    write[count]=True
            count = count + 1
        
        Assert(read or write,"MUX {}No read or write signals in demux".format(self.name_))

        mode = [0,0,0,0]

        for a in range(0,4):        
            if read[a] and write[a]:
                mode[a] = 2
            elif write[a]:
                mode[a] = 1
            else:
                mode[a] = 0

        connect_text = ""
        
        add_p = False
        r_data_p = False
        w_data_p = False
        w_p = False
        r_p = False
        count = 0
        for inter_i in multi_interfaces:
            for inter in inter_i:
                if inter['type']=="address":
                    connect_text+= ".avs_s{0}_address({1}),\n".format(count,inter['connection_port_name'])
                    add_p=True
                elif inter['type']=="readdata":
                    connect_text+= ".avs_s{0}_readdata({1}),\n".format(count,inter['connection_port_name'])
                    r_data_p=True
                elif inter['type']=="writedata":
                    connect_text+= ".avs_s{0}_writedata({1}),\n".format(count,inter['connection_port_name'])
                    w_data_p=True
                elif inter['type']=="write":
                    connect_text+= ".avs_s{0}_write({1}),\n".format(count,inter['connection_port_name'])
                    w_p=True
                elif inter['type']=="write_n":
                    connect_text+= ".avs_s{0}_write(~{1}),\n".format(count,inter['connection_port_name'])
                    w_p=True
                elif inter['type']=="read":
                    connect_text+= ".avs_s{0}_read({1}),\n".format(count,inter['connection_port_name'])
                    r_p=True
                elif inter['type']=="read_n":
                    connect_text+= ".avs_s{0}_read(~{1}),\n".format(count,inter['connection_port_name'])
                    r_p=True
            count+=1

        name = self.name_
        mconnections = {}

        if add_p:
            mconnections["address"]="mm_m_address_{}".format(name)
            self.generator_.add_wire("mm_m_address_{}".format(name),a_width)
            connect_text+=".avs_m_address(mm_m_address_{0}),".format(name)

        if r_data_p:
            mconnections["readdata"]= "mm_m_readdata_{}".format(name)
            self.generator_.add_wire("mm_m_readdata_{}".format(name),d_width)
            connect_text+=".avs_m_readdata(mm_m_readdata_{0}),".format(name)

        if w_data_p:
            mconnections["writedata"]= "mm_m_writedata_{}".format(name)
            self.generator_.add_wire("mm_m_writedata_{}".format(name),d_width)
            connect_text+=".avs_m_writedata(mm_m_writedata_{0}),".format(name)

        if w_p:
            mconnections["write"]= "mm_m_write_{}".format(name)
            self.generator_.add_wire("mm_m_write_{}".format(name),1)
            connect_text+=".avs_m_write(mm_m_write_{0}),".format(name)

        if r_p:
            mconnections["read"]= "mm_m_read_{}".format(name)
            self.generator_.add_wire("mm_m_read_{}".format(name),1)
            connect_text+=".avs_m_read(mm_m_read_{0}),".format(name)

        connect_text=connect_text[:-1]

        self.to_write_ = mux_template.format(name=self.name_,a_width=a_width,n_mas=len(multi_interfaces),d_width=d_width,connections=connect_text,
                                               m0=mode[0],m1=mode[1],m2=mode[2],m3=mode[3])
        return mconnections