Finish documenting a number of different files

- [ ] v_class
- [x] ipxact parse
- [ ] module_gen
- [x] ipxact_def parse
- [x] generator (just a bit)
- [ ] json validation

General Documentation improvements
- [ ]  Document auto_interconnect insertion behavior and the bus matrix format
- [ ]  Create a flow diagram for how the Geyser generation process works.
- [ ]  Document GEYSERs ability to connect inverted interfaces 

Possibly insert a Xilinx example
- [ ]  This could be a good chance to have a full blown tutorial from start to finish
- [ ]  If the tutorial can simulate with a provided test bench that would be bonus points. 
- [ ]  Quartus equivalent could also be nice but no longer have access.

Add better GIP documentation
- [ ]  add the json definition that GIP is generated from
- [ ]  talk about general GIP behavior
- [ ]  walk through the process of documenting IP/modules with GIP

Document the top-level design process
- [ ]  defining the modules with GIP (reverse directions? maybe just make this part of the command or this might already be handled by the generator need to check in)
- [ ]  Talk about the different top level options

Limitations section
- [ ]  talk about interconnects not currently working with top-level interfaces
- [ ]  talk about unconnected behavior not working with top level
- [ ]  Add anything else.

Extra
- [ ]  Publish a pypi package
- [ ]  Clean up repo so it only refers to GEYSER
- [ ]  Rework IPXACT parsing. Probably use something like BeautifulSoup
- [ ]  Fix issues that can occur with different vendors giving the same interface a different definition eg amba and xilinx with AXI-Lite


# Future improvements

- [ ]  interconnect class to base interconnects off of
- [ ]  ability to disable inverted name connection
- [ ]  vectorized port support. Multiple ports can be on one wire and select their necessary bits
- [ ] add a generic 2022 ipxact parser. 
- [ ] add feature where users can add documentation for parameters in GIP if desired something like the following maybe
- [ ] add feature where users can restrict parameter values
    ```json
    "parameters":{
        "MEM_BYTES":{
            "val":null,
            "description":"The total number of bytes that should be present in the memory"
        },
        "DATA_WIDTH":32,
        "LATENCY":{
            "val":2,
            "description":"set the latency of this module",
            "valid":{
                "low":1,
                "high":64
            }
        }
    }
    ```
- [ ] add ability to convert from GIP to 2022 IPXACT. 