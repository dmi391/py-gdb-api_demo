
# py-gdb-api_demo

----

This project provides demonstration of using Python GDB API.  
As the example used embedded RISC-V.

Using Python GDB API allows to expand GDB opportunities.  
Python GDB API allows to create Python script for GDB. Also it is possible to implement custom GDB-commands. It can be used to automate work with GDB. [GDB doc: 23.2 Extending gdb using Python]  
Submodule /modules/ contains custom GDB-commands and custom GDB-functions.  
These ideas can be used for launch automation, test automation and other.  
Details in the Wiki.

## Quick start

Get project:

        $ git clone ...
        $ cd py-gdb-api_demo
        $ git submodule update --init --recursive

Set actual paths in file '/py-gdb-api_demo/paths'.

Build project:

        make

There are two launch configurations for demonstration (setting in file '/py-gdb-api_demo/paths'):

        GDB_SCRIPT="../gdb-py/gdb_launch.py" => Launch execution
        GDB_SCRIPT="../gdb-py/gdb_unit_tests.py" => Launch unit tests

Launch with hardware:

        /launch-sh/openocd_gdb_launch.sh /Debug/py-gdb-api_demo.elf

Launch with Spike:

        /launch-sh/spike_openocd_gdb_launch.sh /Debug/py-gdb-api_demo.elf

----

