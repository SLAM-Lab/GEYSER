## Setup
This is the noxygen example. It is pretty annoying to setup the required graphviz library on windows so I recommend using linux. To run this example on linux please run the following commands to install the required libraries after installing geyser.

```bash
pip install networkx
sudo apt-get install graphviz graphviz-dev
pip install pygraphviz
```

## Usage

Assuming execution on linux run the following commands to generate the required geyser python classes. 
```
module_gen noxy_combiner.gip.json
module_gen noxy_splitter.gip.json
module_gen Router.gip.json
module_gen top.gip.json
```

After that you should be able to run and GEYSER will generate the top level verilog file
```
python3 noxygen_geyser.py
```

## Extras

This version is currently only setup to work with EVAL_100.dot which is a 100x100 mesh router topology. To use other files you need to modify `top.gip.json` and change `"multi":["/list(range(0,10000))"],` to a range (0,"number of routers"). Additionally you must change the used fil in `noxygen_geyser.py`. I have included a few other dot files I generated using a noxygen tool. The number in the file name indicates the Mesh dimensions. 


I included a test bench configured to test a 5x5 mesh (EVAL_5.dot) in the SystemVerilog folder. There are more instructions about using the test bench in the NoxyGen repo https://github.com/madhur19171/NoxyGen. 