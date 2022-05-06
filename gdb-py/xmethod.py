import gdb
import sys
import os.path

from gdb.xmethod import XMethod

#********************************************************************************

class ExampleClass_getFieldIndexMax(gdb.xmethod.XMethod):
    '''Addition extra method (Xmethod) 'getFieldIndexMax()' to the object'''
    def __init__(self):
        gdb.xmethod.XMethod.__init__(self, 'getFieldIndexMax')

    def get_worker(self, method_name):
        if method_name == 'getFieldIndexMax':
            return ExampleClassWorker_getFieldIndexMax()


class ExampleClass_mustExeptReplace(gdb.xmethod.XMethod):
    '''Replacement the object method 'mustException(int)' with Xmethod'''
    def __init__(self):
        gdb.xmethod.XMethod.__init__(self, 'mustException')

    def get_worker(self, method_name):
        if method_name == 'mustException':
            return ExampleClassWorker_mustExeptReplace()


class ExampleClassMatcher(gdb.xmethod.XMethodMatcher):
    def __init__(self):
        gdb.xmethod.XMethodMatcher.__init__(self, 'ExampleClassMatcher')
        # List of methods managed by this matcher
        self.methods = [ExampleClass_getFieldIndexMax(), ExampleClass_mustExeptReplace()]

    def match(self, class_type, method_name):
        if class_type.tag != 'ExampleClass':
            return None
        workers = []
        for method in self.methods:
            if method.enabled:
                worker = method.get_worker(method_name)
                if worker:
                    workers.append(worker)
        return workers
#********************************************************************************

class ExampleClassWorker_getFieldIndexMax(gdb.xmethod.XMethodWorker):
    def get_arg_types(self):
        return None

    def get_result_type(self, obj):
        return gdb.lookup_type('int')

    def __call__(self, obj):
        return obj['indexMax']


class ExampleClassWorker_mustExeptReplace(gdb.xmethod.XMethodWorker):
    def get_arg_types(self):
        return gdb.lookup_type('int')

    def get_result_type(self, obj, value):
        return gdb.lookup_type('int')

    def __call__(self, obj, value):
        return value * 10
#********************************************************************************
