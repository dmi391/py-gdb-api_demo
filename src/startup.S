/*
 * startup.S
 *
 * 		Author: PehotinDO
 */

.section .init

// Entry point symbol
.globl _start
.type _start,@function
_start:

// gp and sp initialization
.option push
.option norelax
	la		gp, __global_pointer$
.option pop
	la		sp, _sp

// Clear bss section
	la		a0, __bss_start
	la		a1, __bss_end
	bgeu	a0, a1, 2f
1:
	sw		zero, (a0)
	addi	a0, a0, 4
	bltu	a0, a1, 1b
2:

// Interrupt/Exception trap
	la		t0, trap
	csrw	mtvec, t0

// Enable FPU and Hwacha
	call	mstatus_fs_xs

// Call global destructors (not necessary for embedded)
/*	la		a0, __libc_fini_array
	call	atexit
*/
// Call global constructors
	call	__libc_init_array

// argc = argv = 0
	li		a0, 0
	li		a1, 0
	call	main
	nop
trap:
	j		trap
//	tail exit	//not necessary for embedded


//========================================

// _init() called in __libc_init_array()
// extern "C" void __attribute__((weak)) _init(void){}
.globl _init
.type _init,@function
_init:
	//Any additional user initializations (not global constructors)
	//Default empty
	ret


// Enable FPU and Hwacha
.globl mstatus_fs_xs
.type _init,@function
mstatus_fs_xs:
	li		t0, 0x1E000
	csrs	mstatus, t0
	ret

//========================================
