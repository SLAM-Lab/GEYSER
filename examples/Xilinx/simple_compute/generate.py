from geysergen import generator
from geysergen.generator import GenerateType
from geysergen.generic_modules.xilinx.series7.true_dual_port_sram import true_dual_port_sram
from compute import compute
from compute2 import compute2
from top_level import top_level


gen = generator.verilog_generator("top.v")
top = top_level(gen,"top_level")
gen.set_root_module(top)

comp = compute(gen,"compute")
comp2 = compute2(gen,"compute2")

mem1 = true_dual_port_sram(gen,"mem1",32*4,32,parameters={"BYTE_ADDRESSING":1})
mem2 = true_dual_port_sram(gen,"mem2",64*4,32,parameters={"BYTE_ADDRESSING":1})
mem3 = true_dual_port_sram(gen,"mem3",32*4,32,parameters={"BYTE_ADDRESSING":1})
mem5 = true_dual_port_sram(gen,"mem5",64*4,32,parameters={"BYTE_ADDRESSING":1})
mem4 = true_dual_port_sram(gen,"mem4",64*4,32,parameters={"BYTE_ADDRESSING":1})

#Wire up the top and compute 
gen.connect(comp.interface_ap_clk,top.interface_ap_clk)
gen.connect(comp.interface_ap_rst,top.interface_ap_rst)
gen.connect(comp.interface_ap_ctrl,top.interface_ap_ctrl0)
gen.connect(comp2.interface_ap_clk,top.interface_ap_clk)
gen.connect(comp2.interface_ap_rst,top.interface_ap_rst)
gen.connect(comp2.interface_ap_ctrl,top.interface_ap_ctrl1)

#Wire up the compute to the memory
gen.connect(mem1.interface_bram_port_a,comp.interface_port0_porta)
gen.connect(mem1.interface_bram_port_b,comp.interface_port0_portb)
gen.connect(mem3.interface_bram_port_a,comp.interface_port0_porta)
gen.connect(mem3.interface_bram_port_b,comp.interface_port0_portb)
gen.connect(mem1.interface_bram_port_a,comp2.interface_port0_porta)
gen.connect(mem1.interface_bram_port_b,comp2.interface_port0_portb)
gen.connect(mem3.interface_bram_port_a,comp2.interface_port0_porta)
gen.connect(mem3.interface_bram_port_b,comp2.interface_port0_portb)
gen.connect(mem4.interface_bram_port_a,comp2.interface_port1_porta)
gen.connect(mem5.interface_bram_port_a,comp2.interface_port2_porta)



gen.connect(mem2.interface_bram_port_a,comp.interface_port1_porta)
gen.connect(mem2.interface_bram_port_b,comp.interface_port2_porta)



gen.generate_verilog(False)