The GEYSER Intellectual Property (GIP) format is designed to reduce the effort involved with documenting modules from simple to complex. This documentation may not cover every key or special feature of GIP and users should consult the GIP keys documentation for a full lists of supported keys. This documentation is written with standard module definitions in mind. There will be a section at the end which discusses writing GIP files for top level modules.

### Introduction
GIP defines HDL components/IP using JSON. JSON was chosen due to its readable and concise format compared to XML which is used by IPXACT. Values are assigned to a set of standard keys to document a module and its interfaces. The two most basic keys in GIP are `name` and `ip_name`. The first, `name` documents the name that will be used for the component within python. The second `ip_name` defines the name that the module has in verilog. An example of a using these two keys can be seen below.

```json
{
    "name":"user_readable_name",
    "ip_name":"custom_module_v128_0_1"
}
```

### Interfaces
GEYSER doesn't aim to make users do port level connections. As such GEYSER handles connectivity at the interface level allowing many ports to be bundled. As a result a modules GIP definition needs to document all of a modules ports and the interfaces that the ports correspond with. GIP aims to reduce the amount of information required from the user by  as much information as possible to be prepopulated. The following sections will highlight all of the information that can be documented about an interface. However in real world use it is expected that users will only need to define a smaller subset.

### Basic Interface Documentation
The following expanded example shows how a simple avalon interface could be defined in the module from the previous example.
```json
{
    "name":"user_readable_name",
    "ip_name":"custom_module_v128_0_1"
}
```