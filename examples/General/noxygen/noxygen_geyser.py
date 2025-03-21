import networkx as nx
import pygraphviz as pgv
from Router import Router
from noxy_top import noxy_top
from noxy_splitter import noxy_splitter
from noxy_combiner import noxy_combiner
import geysergen.generator as pgen
import ast
import time

#start = time.time()
G=nx.DiGraph(pgv.AGraph("EVAL_100.dot"))

gen = pgen.verilog_generator("testy.v")
node_count = G.number_of_nodes()
top = noxy_top(gen,"top",DATA_WIDTH=32)
gen.set_root_module(top)
splitters={}
combiners={}

#Parse out the routers
for node_name,node_data in G.nodes(data=True):

    in_stuff=node_data['in'].strip()
    out_stuff=node_data['out'].strip()

    params = {
        "INPUTS":len(in_stuff.split(' ')),
        "OUTPUTS":len(out_stuff.split(' ')),
        "DATA_WIDTH":int(in_stuff.split(' ')[0].split(":")[1]),
        "REQUEST_WIDTH":f"$clog2({len(out_stuff.split(' '))})",
        "VC_FLOW_CONTROL":0
    }|ast.literal_eval("{\""+node_data['NSA'].replace(" ",",\"").replace(":","\":")+"}")


    #create a new router
    new_router = Router(gen,node_name,N=node_count,INDEX=node_data['ID'],parameters=params)
    gen.connect(new_router.interface_clock,top.interface_clock)
    gen.connect(new_router.interface_reset,top.interface_reset)
    new_splitter = noxy_splitter(gen,f"split_{node_name}",INPUTS=params['OUTPUTS'],DATA_WIDTH=params['DATA_WIDTH'])
    splitters[node_name]=new_splitter
    gen.connect(new_router.interface_data_out,new_splitter.interface_data_in)
    gen.connect(top[f"interface_{node_name}_out"],new_splitter.interface_data_out0)
    new_combiner = noxy_combiner(gen,f"combine_{node_name}",INPUTS=params['INPUTS'],DATA_WIDTH=params['DATA_WIDTH'])
    gen.connect(new_router.interface_data_in,new_combiner.interface_data_out)
    gen.connect(top[f"interface_{node_name}_in"],new_combiner.interface_data_in0)
    combiners[node_name]=new_combiner


for edge_0,edge_1,edge_data in G.edges(data=True):
    gen.connect(splitters[edge_0][f'interface_data_{edge_data["from"]}'],combiners[edge_1][f'interface_data_{edge_data["to"]}'])

gen.generate_verilog(run_formatter=False)

#end=time.time()
#print("Time:",end-start)  
    