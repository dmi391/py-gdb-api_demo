OUTPUT_ARCH("riscv")
ENTRY(_start)

MEMORY
{
  RAM_MEM 				: ORIGIN = 0x10000000, LENGTH = 0xFFFFF
}

SECTIONS
{

. = 0x10000000;

.init :
{
  KEEP (*(SORT_NONE(.init)))
} > RAM_MEM

.text ALIGN(8) :
{
  *(.text)
} > RAM_MEM

.interrupt_handler ALIGN(8) :
{
  *(.interrupt_handler)
} > RAM_MEM

.rodata ALIGN(8) :
{
  *(.rodata)
} > RAM_MEM


.preinit_array ALIGN(8) :
{
  PROVIDE_HIDDEN (__preinit_array_start = .);
  KEEP (*(.preinit_array))
  PROVIDE_HIDDEN (__preinit_array_end = .);
} > RAM_MEM

.init_array ALIGN(8) :
{
  PROVIDE_HIDDEN (__init_array_start = .);
  KEEP (*(SORT_BY_INIT_PRIORITY(.init_array.*) SORT_BY_INIT_PRIORITY(.ctors.*)))
  KEEP (*(.init_array EXCLUDE_FILE (*crtbegin.o *crtbegin?.o *crtend.o *crtend?.o ) .ctors))
  PROVIDE_HIDDEN (__init_array_end = .);
} > RAM_MEM


.data ALIGN(8) :
  {
    *(.data)
  } > RAM_MEM
  .sdata ALIGN(8) :
  {
    PROVIDE( __global_pointer$ = . + 0x800 );
    *(.sdata)
  } > RAM_MEM
  PROVIDE(_edata = .);


PROVIDE( __bss_start = . );
.bss ALIGN(8) :
{
  *(.sbss)
  *(.bss)
} > RAM_MEM
PROVIDE( __bss_end = . );


  PROVIDE(exit = .);
  _exit = exit;


  PROVIDE( _end = . );
  PROVIDE( end = . );

 PROVIDE( _sp = 0x100f0000);  /*stack*/

}