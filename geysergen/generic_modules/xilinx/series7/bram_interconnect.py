from pathlib import Path
#This is the main template for the generated interconnect


demux_template = """
bram_demux #(
.READWRITE_MODE({rw_mode}),
.NUM_TARGETS({n_slaves}),
.DWIDTH({d_width}),
.MAWIDTH({ma_width}),
.SAWIDTH({sa_width})
){name}(
{connections}
);
"""

mux_template = """
bram_mux #(.NUM_INITIATORS({n_mas}),
    .DWIDTH({d_width}),
    .AWIDTH({a_width}),
	.INITIATOR0_READWRITE_MODE({m0}),
	.INITIATOR1_READWRITE_MODE({m1}),
	.INITIATOR2_READWRITE_MODE({m2}),
	.INITIATOR3_READWRITE_MODE({m3}))
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
class bram_mm_interconnect:
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
        Assert(len(multi_interfaces)==2 or len(multi_interfaces)==4,"{} Only two or four bram interfaces are currently supported in a demux".format(self.name_))

        #Get some preliminary information from the interfaces

        a_width = 0
        d_width = 0
        read = False
        write = False
        addr = False
        for interface in multi_interfaces:
            for sig in interface:
                if sig['type']=='addr':
                    
                    if a_width==0:
                        a_width=sig['width']
                    else:
                        Assert(a_width==sig['width'],"DEMUX ERROR: All interfaces must have the same address width {} != {}".format(a_width,sig['width']))
                    addr = True
                if 'dout'==sig['type']:
                    if d_width == 0:
                        d_width = sig['width']
                    else:
                        Assert(d_width==sig['width'],"DEMUX ERROR: All interfaces must have the same data width {} != {}".format(d_width,sig['width']))
                    read=True
                if 'din' ==sig['type']:
                    if d_width == 0:
                        d_width = sig['width']
                    else:
                        Assert(d_width==sig['width'],"DEMUX ERROR: All interfaces must have the same data width {} != {}".format(d_width,sig['width']))
                    write=True

        Assert(addr,"bram demux requires address line")
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
        add_r = False
        add_c = False
        r_data_p = False
        w_data_p = False
        w_p = False
        r_p = False

        count = 1
        for inter_i in multi_interfaces:

            for inter in inter_i:
                if inter['type']=="addr":
                    connect_text+= ".bram_i{0}_address({1}),\n".format(count,inter['connection_port_name'])
                    add_p=True
                elif inter['type']=="clk":
                    connect_text+= ".bram_i{0}_clk({1}),\n".format(count,inter['connection_port_name'])
                    add_c=True
                elif inter['type']=="rst":
                    connect_text+= ".bram_i{0}_rst({1}),\n".format(count,inter['connection_port_name'])
                    add_r=True
                elif inter['type']=="dout":
                    connect_text+= ".bram_i{0}_readdata({1}),\n".format(count,inter['connection_port_name'])
                    r_data_p=True
                elif inter['type']=="din":
                    connect_text+= ".bram_i{0}_writedata({1}),\n".format(count,inter['connection_port_name'])
                    w_data_p=True
                elif inter['type']=="we":
                    connect_text+= ".bram_i{0}_we({1}),\n".format(count,inter['connection_port_name'])
                    w_p=True
                elif inter['type']=="en":
                    connect_text+= ".bram_i{0}_en({1}),\n".format(count,inter['connection_port_name'])
                    r_p=True
            count+=1

        name = self.name_
        mconnections = {}

        if add_p:
            mconnections["addr"]="mm_s_address_{}".format(name)
            self.generator_.add_wire("mm_s_address_{}".format(name),ma_width)
            connect_text+=".bram_t0_address(mm_s_address_{0}),".format(name)
        if add_c:
            mconnections["clk"]="mm_s_clk_{}".format(name)
            self.generator_.add_wire("mm_s_clk_{}".format(name),1)
            connect_text+=".bram_t0_clk(mm_s_clk_{0}),".format(name)
        if add_r:
            mconnections["rst"]="mm_s_rst_{}".format(name)
            self.generator_.add_wire("mm_s_rst_{}".format(name),1)
            connect_text+=".bram_t0_rst(mm_s_rst_{0}),".format(name)

        if r_data_p:
            mconnections["dout"]= "mm_s_readdata_{}".format(name)
            self.generator_.add_wire("mm_s_readdata_{}".format(name),d_width)
            connect_text+=".bram_t0_readdata(mm_s_readdata_{0}),".format(name)

        if w_data_p:
            mconnections["din"]= "mm_s_writedata_{}".format(name)
            self.generator_.add_wire("mm_s_writedata_{}".format(name),d_width)
            connect_text+=".bram_t0_writedata(mm_s_writedata_{0}),".format(name)

        if w_p:
            mconnections["we"]= "mm_s_we_{}".format(name)
            self.generator_.add_wire("mm_s_we_{}".format(name),d_width//8)
            connect_text+=".bram_t0_we(mm_s_we_{0}),".format(name)

        if r_p:
            mconnections["en"]= "mm_s_en_{}".format(name)
            self.generator_.add_wire("mm_s_en_{}".format(name),1)
            connect_text+=".bram_t0_en(mm_s_en_{0}),".format(name)

        connect_text=connect_text[:-1]

        self.to_write_ = demux_template.format(name=self.name_,ma_width=ma_width,sa_width=a_width,n_slaves=len(multi_interfaces),rw_mode=mode,d_width=d_width,connections=connect_text)
        return mconnections

    def make_mux_(self,multi_interfaces,extras) -> dict:
        Assert(len(multi_interfaces)==2 or len(multi_interfaces)==4,"{} Only two or four bram interfaces are currently supported in a mux".format(self.name_))

        #Get some preliminary information from the interfaces

        a_width = 0
        d_width = 0
        read = [False,False,False,False]
        write = [False,False,False,False]
        count = 0
        for interface in multi_interfaces:
            for sig in interface:
                if sig['type']=='addr':
                    if a_width==0:
                        a_width=sig['width']
                    else:
                        Assert(a_width==sig['width'],"MUX {} All interfaces must have the same address width {} != {}".format(self.name_,a_width,sig['width']))
                if 'dout'==sig['type']:
                    if d_width == 0:
                        d_width = sig['width']
                    else:
                        Assert(d_width==sig['width'],"MUX {} All interfaces must have the same data width {} != {}".format(self.name_,d_width,sig['width']))
                    read[count]=True
                if 'din' ==sig['type']:
                    if d_width == 0:
                        d_width = sig['width']
                    else:
                        Assert(d_width==sig['width'],"MUX {} All interfaces must have the same data width {} != {}".format(self.name_,d_width,sig['width']))
                    write[count]=True
            count = count + 1
        
        Assert(read or write,"MUX {}No read or write signals in mux".format(self.name_))

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
        rst_p = False
        clk_p = False
        count = 0
        for inter_i in multi_interfaces:
            for inter in inter_i:
                if inter['type']=="addr":
                    connect_text+= ".bram_t{0}_address({1}),\n".format(count,inter['connection_port_name'])
                    add_p=True
                elif inter['type']=="dout":
                    connect_text+= ".bram_t{0}_readdata({1}),\n".format(count,inter['connection_port_name'])
                    r_data_p=True
                elif inter['type']=="din":
                    connect_text+= ".bram_t{0}_writedata({1}),\n".format(count,inter['connection_port_name'])
                    w_data_p=True
                elif inter['type']=="we":
                    connect_text+= ".bram_t{0}_we({1}),\n".format(count,inter['connection_port_name'])
                    w_p=True
                elif inter['type']=="en":
                    connect_text+= ".bram_t{0}_en({1}),\n".format(count,inter['connection_port_name'])
                    r_p=True
                elif inter['type']=="rst":
                    connect_text+= ".bram_t{0}_rst({1}),\n".format(count,inter['connection_port_name'])
                    rst_p=True
                elif inter['type']=="clk":
                    connect_text+= ".bram_t{0}_clk({1}),\n".format(count,inter['connection_port_name'])
                    clk_p=True
            count+=1

        name = self.name_
        mconnections = {}

        if add_p:
            mconnections["addr"]="bram_i_address_{}".format(name)
            self.generator_.add_wire("bram_i_address_{}".format(name),a_width)
            connect_text+=".bram_i_address(bram_i_address_{0}),".format(name)
        if clk_p:
            mconnections["clk"]="bram_i_clk_{}".format(name)
            self.generator_.add_wire("bram_i_clk_{}".format(name),1)
            connect_text+=".bram_i_clk(bram_i_clk_{0}),".format(name)
        if rst_p:
            mconnections["rst"]="bram_i_rst_{}".format(name)
            self.generator_.add_wire("bram_i_rst_{}".format(name),1)
            connect_text+=".bram_i_rst(bram_i_rst_{0}),".format(name)

        if r_data_p:
            mconnections["dout"]= "bram_i_readdata_{}".format(name)
            self.generator_.add_wire("bram_i_readdata_{}".format(name),d_width)
            connect_text+=".bram_i_readdata(bram_i_readdata_{0}),".format(name)

        if w_data_p:
            mconnections["din"]= "bram_i_writedata_{}".format(name)
            self.generator_.add_wire("bram_i_writedata_{}".format(name),d_width)
            connect_text+=".bram_i_writedata(bram_i_writedata_{0}),".format(name)

        if w_p:
            mconnections["we"]= "bram_i_we_{}".format(name)
            self.generator_.add_wire("bram_i_we_{}".format(name),d_width//8)
            connect_text+=".bram_i_we(bram_i_we_{0}),".format(name)

        if r_p:
            mconnections["en"]= "bram_i_en_{}".format(name)
            self.generator_.add_wire("bram_i_en_{}".format(name),1)
            connect_text+=".bram_i_en(bram_i_en_{0}),".format(name)

        connect_text=connect_text[:-1]

        self.to_write_ = mux_template.format(name=self.name_,a_width=a_width,n_mas=len(multi_interfaces),d_width=d_width,connections=connect_text,
                                               m0=mode[0],m1=mode[1],m2=mode[2],m3=mode[3])
        return mconnections