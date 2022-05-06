import gdb
import os.path

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

sys.path.append('../')   # For import /modules/
from modules.gdb_connection import BeginSession
from modules.gdb_connection import Shutdown
from modules.gdb_connection import Output
#from modules.memory import DumpMemory
#from modules.memory import AppendMemory
#from modules.memory import RestoreMemory
from modules.memory import ReadMemory
#from modules.memory import WriteMemory
#from modules.call_method import CallMethod

def main():
    print(f'GDB-client version = {gdb.VERSION}\n')

    # Elf-file taken as argument of gdb-client
    elf = gdb.objfiles()[0]
    if elf == None:
        raise gdb.GdbError('Elf-file is not found.')
    elf = elf.filename
    print(f'Elf-file = {elf}\n')

    # Preparing:
    BeginSession.invoke(elf, False) # CLI: (gdb) begin <path-to-elf>
    # State: stop at _start

    # Breakpoint on trap for exception/interrupt
    gdb.Breakpoint('trap')

    # Start execution:
    gdb.Breakpoint('main')
    gdb.execute('continue')
    # State: stop at main()

    # Get register value:
    pc = gdb.parse_and_eval('$pc')
    print(f'\npc = {pc}\n')

    # Inside main():
    frame = gdb.selected_frame()
    gdb.execute('frame')    # Print stack-frame information

    # Set breakpoint at (main + 3 lines):
    bp = gdb.Breakpoint('+3')
    bp.silent = True
    gdb.execute('continue')
    # State: stop at (main + 3 lines)

    # Get object information:
    val_obj = gdb.parse_and_eval('exampleObj')
    print(f'\n{frame.function()}: Object of <{val_obj.type}> allocated at address {val_obj.address}')
    print(f'{frame.function()}: exampleObj.indexMax = {val_obj["indexMax"]}\n')

    # Set watchpoint on local variable 'isErr':
    wp = gdb.Breakpoint('isErr', gdb.BP_WATCHPOINT)
    wp.silent = True
    gdb.execute('continue')
    # State: stop at watchpoint on isErr

    # Get array value:
    val_dstY = gdb.parse_and_eval('dstY')
    print(f'\n{frame.function()}: array <{val_dstY.type}> dstY = {val_dstY}')
    ReadMemory.invoke(f'/tmp/tmp.bin dstY {val_dstY.type.sizeof}', False)  # Dump to file

    # Get local variable:
    var_isErr = frame.read_var('isErr')
    print(f'\n{frame.function()}: err flag <{var_isErr.type}> isErr = {var_isErr}\n')

    # Set finish breakpoint for main():
    gdb.execute('set backtrace past-main on')
    fbp_main = gdb.FinishBreakpoint()
    gdb.execute('continue')
    # State: stop at finish breakpoint after main()

    # Return value from main():
    print(f'\nmain() returns value <{fbp_main.return_value.type}> = {fbp_main.return_value}\n')

    # Output text message to GDB-console:
    if fbp_main.return_value == 0:
        Output.invoke('Ok: Result is Ok!', False)
    else:
        Output.invoke('Err: Result is Failure!', False)

    # End:
    Output.invoke(f'Info: {" End of python-GDB-script ":*^80}', False)
    Shutdown.invoke('', False)  # CLI: (gdb) shutdown


if __name__ == "__main__":
	main()
