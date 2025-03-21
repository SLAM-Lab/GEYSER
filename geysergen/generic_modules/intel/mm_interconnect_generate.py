from pathlib import Path
#This is the main template for the generated interconnect
mega_template_mux = """
module mm_mux_{7}_{1}_{3}(
    input wire rsi_reset,
    input wire csi_clk,

   {0}

    output wire [{1}:0] mm_m_address, //max 63
    output wire [{2}:0] mm_m_byteenable, //max 127
    output wire mm_m_read,
    input wire [{3}:0]mm_m_readdata, //max 1023
    output wire mm_m_write,
    output wire [{3}:0]mm_m_writedata,
    input wire mm_m_waitrequest,
    input wire mm_m_readdatavalid
);

reg [{1}:0] avs_mf_address_reg = {4}'b0;
reg [{2}:0] avs_mf_byteenable_reg = {5}'b0;
reg [{3}:0] avs_mf_writedata_reg = {6}'b0;
reg avs_mf_write_reg = 1'b0;
reg avs_mf_read_reg = 1'b0;
reg [{3}:0] avs_sm_readdata_reg = {6}'b0;

{11}

reg [8:0] transfer_count = 0;

reg [{7}:0] trigger = 0;

//Send request Mux
always @({8} mm_m_waitrequest,rsi_reset) begin
    if (rsi_reset) begin
        trigger = {7}'b0;
    end
    else {9} begin
        {10}
        avs_mf_address_reg = {4}'b0;
        avs_mf_byteenable_reg = {5}'b0;
        avs_mf_writedata_reg = {6}'b0;
        avs_mf_write_reg = 1'b0;
        avs_mf_read_reg = 1'b0;
    end
end

always @(csi_clk) begin
    if(rsi_reset)begin
        transfer_count<=0;
    end
    else begin
        if(avs_mf_write_reg|avs_mf_read_reg) begin
            if (!mm_m_readdatavalid) begin //If they trigger at the same time we just leave the current value
                transfer_count<=transfer_count+1;
            end
        end 
        else if (mm_m_readdatavalid&(transfer_count!=0)) begin //If they trigger at the same time we just leave the current value
            transfer_count<=transfer_count-1;
        end
    end
end

{12}

assign mm_m_write = avs_mf_write_reg;
assign mm_m_read = avs_mf_read_reg;
assign mm_m_address = avs_mf_address_reg;
assign mm_m_writedata = avs_mf_writedata_reg;
assign mm_m_byteenable = avs_mf_byteenable_reg;

endmodule
"""

input_interfaces_template="""
input wire [{1}:0] mm_s_address_{0}, //max 63
input wire [{2}:0] mm_s_byteenable_{0}, //max 127
input wire mm_s_read_0,
output wire [{3}:0]mm_s_readdata_{0}, //max 1023
input wire mm_s_write_0,
input wire [{3}:0]mm_s_writedata_{0},
output wire mm_s_waitrequest_{0},
output wire mm_s_readdatavalid_{0},
"""

sensitivity_template="""
mm_s_write_{0}, mm_s_read_{0},mm_s_writedata_{0},mm_s_address_{0}, mm_s_byteenable_{0},"""

combinatorial_template = """
if (mm_s_read_{0}) begin
        trigger = (1<<{0});
        mm_s_waitrequest_{0}_reg = mm_m_waitrequest;
        avs_mf_address_reg = mm_s_address_{0};
        avs_mf_byteenable_reg = mm_s_byteenable_{0};
        avs_mf_writedata_reg = {1}'b0;
        avs_mf_write_reg = 1'b0;
        avs_mf_read_reg = 1'b1;
    end
else if (mm_s_write_{0}) begin
        trigger = (1<<{0});
        mm_s_waitrequest_{0}_reg = mm_m_waitrequest;
        avs_mf_address_reg = mm_s_address_{0};
        avs_mf_byteenable_reg = mm_s_byteenable_{0};
        avs_mf_writedata_reg = mm_s_writedata_{0};
        avs_mf_write_reg = 1'b1;
        avs_mf_read_reg = 1'b0;
    end
else"""

def_reg_temp = """
reg mm_s_waitrequest_{0}_reg;
"""

reset_waitrequest_template = """
mm_s_waitrequest_{0}_reg = 1'b0;
"""

assign_template = """
assign mm_s_readdata_{0} = mm_m_readdata;
assign mm_s_readdatavalid_{0} = (trigger&(1<<{0}))&&((transfer_count!=0)||(avs_mf_write_reg|avs_mf_read_reg))?mm_m_readdatavalid:1'b0;
assign mm_s_waitrequest_{0} = mm_s_waitrequest_{0}_reg;
"""
mod_def = "mm_mux_{0}_{1}_{2} mm_mux_{0}_{1}_{2}_{3}({4});"

# sink_connection = {
#     "address":"mm_m_address",
#     "byteenable": "mm_m_byteenable",
#     "readdata": "mm_m_readdata",
#     "writedata": "mm_m_writedata",
#     "readdatavalid": "mm_m_readdatavalid",
#     "waitrequest": "mm_m_waitrequest",
#     "write": "mm_m_write",
#     "read": "mm_m_read"
# }


demux_template = """
IC_demux1xN #(
.READWRITE_MODE({rw_mode}),
.NUM_SLAVES({n_slaves}),
.DWIDTH({d_width}),
.MAWIDTH({ma_width}),
.SAWIDTH({sa_width})
){name}(
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
    def make_interconnect(self,multi_interfaces,side) -> dict:
        if side=='sink' or side=='end':
            self.name_=self.name_+'mux'
            return self.make_mux_(multi_interfaces)
        else:
            self.name_=self.name_+'demux'
            return self.make_demux_(multi_interfaces)

    def write(self,output_file) -> None:
        output_file.write(self.to_write_)
    

    def make_demux_(self,multi_interfaces) -> dict:
        Assert(len(multi_interfaces)==2 or len(multi_interfaces==4),"Only two or four avalon interfaces are currently supported in a demux")

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
        count = 0
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
                    connect_text+= ".avs_m{0}_write(~{1}),\n".format(count,inter['connection_port_name'])
                    w_p=True
                elif inter['type']=="read":
                    connect_text+= ".avs_m{0}_read({1}),\n".format(count,inter['connection_port_name'])
                    r_p=True
                elif inter['type']=="read_n":
                    connect_text+= ".avs_m{0}_read(~{1}),\n".format(count,inter['connection_port_name'])
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

    def make_mux_(self,multi_interfaces) -> dict:
        self.mod_int = ""
        address_w = None
        byte_en_w = 1
        data_w = None
        interface_count = len(multi_interfaces)
        
        #This is a mux
        for item in multi_interfaces[0]:
            if item['type']=="address":
                address_w = item['width']
                byte_en_w = int(item['width']/8)
            elif item['type']=="readdata":
                data_w = item['width']
            elif item['type']=="writedata":
                data_w = item['width']

        add_p = False
        r_data_p = False
        w_data_p = False
        w_p = False
        r_p = False
        r_val_p=False
        w_req_p=False
        b_en_p=False
        count = 0
        for inter_i in multi_interfaces:
            for inter in inter_i:
                if inter['type']=="address":
                    self.mod_int+= ".mm_s_address_{0}({1}),\n".format(count,inter['connection_port_name'])
                    add_p=True
                elif inter['type']=="readdata":
                    self.mod_int+= ".mm_s_readdata_{0}({1}),\n".format(count,inter['connection_port_name'])
                    r_data_p=True
                elif inter['type']=="writedata":
                    self.mod_int+= ".mm_s_writedata_{0}({1}),\n".format(count,inter['connection_port_name'])
                    w_data_p=True
                elif inter['type']=="write":
                    self.mod_int+= ".mm_s_write_{0}({1}),\n".format(count,inter['connection_port_name'])
                    w_p=True
                elif inter['type']=="write_n":
                    self.mod_int+= ".mm_s_write_{0}(~{1}),\n".format(count,inter['connection_port_name'])
                    w_p=True
                elif inter['type']=="read":
                    self.mod_int+= ".mm_s_read_{0}({1}),\n".format(count,inter['connection_port_name'])
                    r_p=True
                elif inter['type']=="read_n":
                    self.mod_int+= ".mm_s_read_{0}(~{1}),\n".format(count,inter['connection_port_name'])
                    r_p=True
                elif inter['type']=="readdatavalid":
                    self.mod_int+= ".mm_s_readdatavalid_{0}({1}),\n".format(count,inter['connection_port_name'])
                    r_val_p=True
                elif inter['type']=="readdatavalid_n":
                    self.mod_int+= ".mm_s_readdatavalid_{0}({1}),\n".format(count,self.generator_.invert_wire(inter['connection_port_name'],inter['width']))
                    r_val_p=True
                elif inter['type']=="waitrequest":
                    self.mod_int+= ".mm_s_waitrequest_{0}({1}),\n".format(count,inter['connection_port_name'])
                    w_req_p=True
                elif inter['type']=="waitrequest_n":
                    self.mod_int+= ".mm_s_waitrequest_{0}({1}),\n".format(count,self.generator_.invert_wire(inter['connection_port_name'],inter['width']))
                    w_req_p=True
                elif inter['type']=="byteenable":
                    self.mod_int+= ".mm_s_byteenable_{0}({1}),\n".format(count,inter['connection_port_name'])
                    b_en_p=True
                elif inter['type']=="byteenable_n":
                    self.mod_int+= ".mm_s_byteenable_{0}(~{1}),\n".format(count,inter['connection_port_name'])
                    b_en_p=True
            count+=1
        
        assert(address_w!=None and data_w!=None)
        file_name = "./generated/mm_mux_{0}_{1}_{2}.v".format(interface_count,address_w,data_w)

        if not Path(file_name).exists():  
            interface_string = ""
            sense_string = ""
            comb_string = ""
            reg_string = ""
            wait_string = ""
            assign_string = ""

            for i in range(interface_count):
                interface_string+=input_interfaces_template.format(i,address_w,byte_en_w,data_w)
                sense_string+=sensitivity_template.format(i)
                comb_string+=combinatorial_template.format(i,data_w-1)
                reg_string+=def_reg_temp.format(i)
                wait_string+=reset_waitrequest_template.format(i)
                assign_string+=assign_template.format(i)
            Path(file_name).parent.mkdir(exist_ok=True, parents=True)
            with open(file_name,"w+") as fs:
                fs.write(mega_template_mux.format(interface_string,address_w-1,byte_en_w-1,data_w-1,address_w,byte_en_w,data_w,
                                                    interface_count,sense_string,comb_string,wait_string,reg_string,assign_string))
                fs.close()

        name = self.name_
        mconnections = {}

        if add_p:
            mconnections["address"]="mm_m_address_{}".format(name)
            self.generator_.add_wire("mm_m_address_{}".format(name),address_w)
            self.mod_int+=".mm_m_address(mm_m_address_{0}),".format(self.name_)

        if b_en_p:
            mconnections["byteenable"]= "mm_m_byteenable_{}".format(name)
            self.generator_.add_wire("mm_m_byteenable_{}".format(name),byte_en_w)
            self.mod_int+=".mm_m_byteenable(mm_m_byteenable_{0}),".format(self.name_)

        if r_data_p:
            mconnections["readdata"]= "mm_m_readdata_{}".format(name)
            self.generator_.add_wire("mm_m_readdata_{}".format(name),data_w)
            self.mod_int+=".mm_m_readdata(mm_m_readdata_{0}),".format(self.name_)

        if w_data_p:
            mconnections["writedata"]= "mm_m_writedata_{}".format(name)
            self.generator_.add_wire("mm_m_writedata_{}".format(name),data_w)
            self.mod_int+=".mm_m_writedata(mm_m_writedata_{0}),".format(self.name_)

        if r_val_p:
            mconnections["readdatavalid"]= "mm_m_readdatavalid_{}".format(name)
            self.generator_.add_wire("mm_m_readdatavalid_{}".format(name),1)
            self.mod_int+=".mm_m_readdatavalid(mm_m_readdatavalid_{0}),".format(self.name_)
        
        if w_req_p:
            mconnections["waitrequest"]= "mm_m_waitrequest_{}".format(name)
            self.generator_.add_wire("mm_m_waitrequest_{}".format(name),1)
            self.mod_int+=".mm_m_waitrequest(mm_m_waitrequest_{0}),".format(self.name_)

        if w_p:
            mconnections["write"]= "mm_m_write_{}".format(name)
            self.generator_.add_wire("mm_m_write_{}".format(name),1)
            self.mod_int+=" .mm_m_write(mm_m_write_{0}),".format(self.name_)

        if r_p:
            mconnections["read"]= "mm_m_read_{}".format(name)
            self.generator_.add_wire("mm_m_read_{}".format(name),1)
            self.mod_int+=".mm_m_read(mm_m_read_{0}),".format(self.name_)

        self.mod_int=self.mod_int[:-1]

        self.to_write_=mod_def.format(interface_count,address_w,data_w,self.name_,self.mod_int)

        #This function could also be in charge of bit width adaptation if desired. 
        return mconnections