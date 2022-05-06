import gdb
import os.path
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

sys.path.append('../')   # For import /modules/
from modules.gdb_connection import BeginSession
from modules.gdb_connection import Shutdown
from modules.gdb_connection import Output

from xmethod import ExampleClassMatcher

import unittest

hp = 0  # Heap pointer


def setUpModule():
    print(f'GDB-client version = {gdb.VERSION}\n')

    # Elf-file taken as argument of gdb-client
    elf = gdb.objfiles()[0]
    if elf == None:
        raise gdb.GdbError('Elf-file is not found.')
    elf = elf.filename
    print(f'Elf-file = {elf}\n')

    # Preparing:
    BeginSession.invoke(elf, False)
    # State: stop at _start

    # Breakpoint on trap for exception/interrupt
    gdb.Breakpoint('trap')

    # Start execution:
    gdb.Breakpoint('main')
    gdb.execute('continue')
    # State: stop at main()

    # Heap pointer:
    global hp
    hp = int(gdb.parse_and_eval('$sp')) + 0x130     #0x100f0100

#********************************************************************************

class TestComputeDual(unittest.TestCase):
    '''Tests for function computeDual(int32_t val)'''

    def setUp(self):
        '''For each test-method'''
        if (int(gdb.parse_and_eval('$pc')) == int(gdb.parse_and_eval('trap').address)):
            self.skipTest('Skip due to exception that was earlier')

    def test_computeDual_0(self):
        '''Test for function computeDual(int32_t val)'''
        result = int(gdb.parse_and_eval('computeDual(0)'))
        self.assertEqual(result, 0)
    
    def test_computeDual_neg(self):
        '''Test for function computeDual(int32_t val)'''
        result = int(gdb.parse_and_eval('computeDual(-5)'))
        self.assertEqual(result, -10)

    def test_computeDual_pos(self):
        '''Test for function computeDual(int32_t val)'''
        result = int(gdb.parse_and_eval('computeDual(6)'))
        self.assertEqual(result, 12)

#********************************************************************************

class TestExampleClass(unittest.TestCase):
    '''Tests for methods of ExampleClass without creating class object'''

    class_addr = int(gdb.lookup_global_symbol('ExampleClass::ExampleClass').value().address)

    def setUp(self):
        '''For each test-method'''
        if (int(gdb.parse_and_eval('$pc')) == int(gdb.parse_and_eval('trap').address)):
            self.skipTest('Skip due to exception that was earlier')

    def test_computeFactorial_0(self):
        '''Test for method ExampleClass::computeFactorial(uint32_t n)'''
        result = int(gdb.parse_and_eval(f'((ExampleClass*){self.class_addr})->computeFactorial(0)'))
        self.assertEqual(result, 1)

    def test_computeFactorial_1(self):
        '''Test for method ExampleClass::computeFactorial(uint32_t n)'''
        result = int(gdb.parse_and_eval(f'((ExampleClass*){self.class_addr})->computeFactorial(4)'))
        self.assertEqual(result, 24)

    def test_findIndexMaxElement(self):
        '''Test for method ExampleClass::findIndexMaxElement(uint32_t len, int32_t* src)'''
        array = b"\x00\x00\x00\x00\x04\x00\x00\x00\x07\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00" #{0, 4, 7, 2, 2}
        length = 5
        inferior = gdb.selected_inferior()
        inferior.write_memory(hp, array, length*4) #Address = heap = start sp + 0x100

        result = int( gdb.parse_and_eval(f'((ExampleClass*){self.class_addr})->\
        findIndexMaxElement({length}, (int*){hp})') )   #ret value
        self.assertEqual(result, 2)

    def test_computeAxpy(self):
        '''Test for method ExampleClass::computeAxpy(uint32_t len, int32_t* dstY, int32_t a, int32_t* srcX, int32_t* srcY).
        Method ExampleClass::computeAxpy(...) contains nested call this->findIndexMaxElement(...)'''
        resultY = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" #{0, 0, 0, 0}
        a = 2
        arrayX = b"\x01\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00" #{1, 1, 1, 1}
        arrayY = b"\x00\x00\x00\x00\x03\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00" #{0, 3, 1, 2}
        length = 4
        inferior = gdb.selected_inferior()
        inferior.write_memory(hp, resultY, length*4)
        inferior.write_memory(hp+0x100, arrayX, length*4)
        inferior.write_memory(hp+0x200, arrayY, length*4)

        result = int( gdb.parse_and_eval(f'((ExampleClass*){self.class_addr})->\
        computeAxpy({length}, (int*){hp}, {a}, (int*){hp+0x100}, (int*){hp+0x200})') )   #ret value
        resultY = inferior.read_memory(hp, length*4).tobytes()   #Computed resultY == {2, 5, 3, 4}

        self.assertEqual(result, 1)
        self.assertEqual(resultY, b'\x02\x00\x00\x00\x05\x00\x00\x00\x03\x00\x00\x00\x04\x00\x00\x00')

    def test_0read_init_mask(self):
        '''Read initial value of static field ExampleClass::mask'''
        result = int(gdb.parse_and_eval('ExampleClass::mask'))
        self.assertEqual(result, 0xff)

    def test_applyMask(self):
        '''Test for static method ExampleClass::applyMask(uint32_t val)'''
        mask_val = 0x01f0

        gdb.parse_and_eval(f'ExampleClass::mask = {mask_val}')
        mask_field = int(gdb.parse_and_eval('ExampleClass::mask'))

        result = int(gdb.parse_and_eval('ExampleClass::applyMask(0x237e)'))   #0x170
        self.assertEqual(mask_field, mask_val)
        self.assertEqual(result, 0x0170)

#********************************************************************************

class TestExampleClassObject(unittest.TestCase):
    '''Tests for object exampleObj of ExampleClass'''

    @classmethod
    def setUpClass(cls):
        '''Setup for test-class TestExampleClassObject.
        Execute C++ code created object exampleObj'''
        print('\n')
        if (int(gdb.parse_and_eval('$pc')) != int(gdb.parse_and_eval('trap').address)): #If not at exception trap now
            # Set breakpoint at (main + 3 lines):
            gdb.Breakpoint('+3')
            gdb.execute('continue')
            # State: stop at (main + 3 lines)
        #Register Xmethod for tests with xmethods
        gdb.xmethod.register_xmethod_matcher(None, ExampleClassMatcher())

    def setUp(self):
        '''For each test-method'''
        if (int(gdb.parse_and_eval('$pc')) == int(gdb.parse_and_eval('trap').address)):
            self.skipTest('Skip due to exception that was earlier')

    def test_Xmethod_mustException(self):
        '''Tests with Xmethod: replace method exampleObj.mustException(...)'''
        '''Original method exampleObj.mustException(...) causes to exception'''
        result = int(gdb.parse_and_eval('exampleObj.mustException(2)'))
        self.assertEqual(result, 20)

    def test_xmethod_getFieldIndexMax(self):
        '''Tests with Xmethod: add new xmethod exampleObj.getFieldIndexMax(...)'''
        '''Original object exampleObj do not contains method .getFieldIndexMax(...)'''
        value = 0x2b
        gdb.parse_and_eval(f'exampleObj.indexMax = {value}')

        result = int(gdb.parse_and_eval('exampleObj.getFieldIndexMax()'))
        self.assertEqual(result, value)

    def test_computeFactorial_0(self):
        '''Test for object method exampleObj.computeFactorial(uint32_t n)'''
        result = int(gdb.parse_and_eval('exampleObj.computeFactorial(0)'))
        self.assertEqual(result, 1)

    def test_computeFactorial_1(self):
        '''Test for object method exampleObj.computeFactorial(uint32_t n)'''
        result = int(gdb.parse_and_eval('exampleObj.computeFactorial(5)'))
        self.assertEqual(result, 120)

    def test_findIndexMaxElement(self):
        '''Test for object method exampleObj.findIndexMaxElement(uint32_t len, int32_t* src)'''
        array = b"\x00\x00\x00\x00\x04\x00\x00\x00\x07\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00" #{0, 4, 7, 2, 2}
        length = 5
        inferior = gdb.selected_inferior()
        inferior.write_memory(hp, array, length*4) #Address = heap = start sp + 0x100

        result = int(gdb.parse_and_eval(f'exampleObj.findIndexMaxElement({length}, (int*){hp})'))
        self.assertEqual(result, 2)

    def test_computeAxpy(self):
        '''Test for object method exampleObj.computeAxpy(uint32_t len, int32_t* dstY, int32_t a, int32_t* srcX, int32_t* srcY).
        Method ExampleClass::computeAxpy(...) contains nested call this->findIndexMaxElement(...)'''
        resultY = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" #{0, 0, 0, 0}
        a = 2
        arrayX = b"\x01\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00" #{1, 1, 1, 1}
        arrayY = b"\x00\x00\x00\x00\x03\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00" #{0, 3, 1, 2}
        length = 4
        inferior = gdb.selected_inferior()
        inferior.write_memory(hp, resultY, length*4)
        inferior.write_memory(hp+0x100, arrayX, length*4)
        inferior.write_memory(hp+0x200, arrayY, length*4)

        result = int(gdb.parse_and_eval(f'exampleObj.computeAxpy({length}, (int*){hp}, {a}, (int*){hp+0x100}, (int*){hp+0x200})'))
        resultY = inferior.read_memory(hp, length*4).tobytes()   #Computed resultY == {2, 5, 3, 4}

        self.assertEqual(result, 1)
        self.assertEqual(resultY, b'\x02\x00\x00\x00\x05\x00\x00\x00\x03\x00\x00\x00\x04\x00\x00\x00')

    def test_applyMask(self):
        '''Test for static method ExampleClass::applyMask(uint32_t val) of object exampleObj'''
        obj = gdb.parse_and_eval('exampleObj')
        mask_val = 0x01f0

        gdb.parse_and_eval(f'exampleObj.mask = {mask_val}')
        mask_field = int(obj['mask'])

        result = int(gdb.parse_and_eval('exampleObj.applyMask(0x237e)'))   #0x170
        self.assertEqual(mask_field, mask_val)
        self.assertEqual(result, 0x0170)

    def test_objectField(self):
        '''Test for access object field exampleObj.indexMax'''
        obj = gdb.parse_and_eval('exampleObj')
        init_field_val = int(obj['indexMax'])

        value = 0x1a
        gdb.parse_and_eval(f'exampleObj.indexMax = {value}')
        result = int(obj['indexMax'])

        self.assertEqual(init_field_val, 0xcf)
        self.assertEqual(result, value)

#********************************************************************************

if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2, catchbreak=True)

    # Finish GDB-session:
    time.sleep(2)   #For unittest output finishing
    print('\n')
    Output.invoke(f'Info: {" End of python-GDB-script ":*^80}', False)
    Shutdown.invoke('', False)
