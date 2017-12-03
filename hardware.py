# -*- coding: utf-8 -*-
# __author__ = 'lidong'

"""
Description:
"""
from operator import add, mul, sub, truediv

memory = []

# Function units of simulator.

def unit_integer(offset, register):
    if isinstance(register, int):
        addr = offset + register
        return memory[addr]
    else:
        raise TypeError('Register should be Int Register.')

def unit_add(op, a, b):
    if op == 'GT':
        return int(a>b)
    elif op == 'EQ':
        return int(a==b)
    elif op == 'LT':
        return int(a<b)
    elif 'ADD' in op:
        return a+b
    elif 'SUB' in op:
        return a-b
    elif 'JEQO' in op:
        return int(a == 1)
    else:
        return 0

def unit_mul(a, b):
    return a * b

def unit_div(a, b):
    return a / b


FuncDict = {'LD': unit_integer,
            'MULT': unit_mul,
            'SUBD': unit_add,
            'DIVD': unit_div,
            'ADDD': unit_add,
            'ADD': unit_add,
            'GT': unit_add,
            'EQ': unit_add,
            'LT': unit_add
            }

class Instruction():
    """
    指令类
    存储指令信息：指令操作，源地址Fi，目标地址Fj，目标地址Fk
    阶段：0.Issue，1.Read operands，2.Execution complete，3.Write result. 4. Finished.
    """
    Stage = ['Ready','Issue', 'Read operands', 'Execution complete', 'Write result','Finished']

    def __init__(self, operation, dest, source1, source2):
        self.operation = operation
        self.dest = dest
        self.source1 = source1
        self.source2 = source2
        self.stage = -1

    def assignUnit(self, funcunit):
        self.funcunit = funcunit

    def issue(self):
        self.stage = 0

    def read_operands(self):
        self.funcunit.read_data()
        self.stage = 1

    def execute(self):
        if self.funcunit.exec():
            self.stage = 2
        else:
            self.stage = 1.5

    def write_result(self):
        self.funcunit.write_result()
        self.stage = 3

    def finished(self):
        self.stage = 4

    def run_one_cycle(self):
        if self.stage == -1:
            self.issue()
        elif self.stage == 0:
            self.read_operands()
        elif self.stage == 1:
            self.execute()
        elif self.stage == 2:
            self.write_result()
        elif self.stage == 3:
            self.finished()

    def release(self):
        self.funcunit.release()
        self.funcunit = None
        self.stage = 4

    def __repr__(self):
        return 'Instruction: {} {} {} {}'.format(self.operation, self.dest, self.source1, self.source2)

    @classmethod
    def ParseInstruction(cls, instructions:str):
        parts = instructions.strip().split()
        dest = ''
        source1 = ''
        source2 = ''
        # 标签
        if len(parts) == 1:
            operation = parts[0].strip(':')
        # 跳转指令
        elif len(parts) == 3:
            operation = parts[0]
            dest = parts[1]
            source1 = parts[2]
        else:
            operation = parts[0]
            dest = parts[1]
            source1 = parts[2]
            source2 = parts[3]
        return cls(operation, dest, source1, source2)


class Register():
    """
    寄存器类
    """
    def __init__(self, no:int, rtype=int):
        self.no = no
        if rtype == int:
            self.name = 'R'+ str(no)
        else:
            self.name = 'F'+ str(no)

        self.occupied = False
        self.value = rtype()
        self.isDest = False
        self.funcunit = None

    def hold(self, funcunit, isDest=False):
        """
        当寄存器是目的寄存器时，需要排他性地占用寄存器
        """
        self.occupied = True
        self.isDest = isDest
        self.funcunit = funcunit

    def release(self):
        """作为目的寄存器被释放"""
        self.occupied = False
        self.isDest = False
        self.funcunit = None
    def __str__(self):
        return self.name

class FunctionUint():
    """
    功能部件类
    """
    def __init__(self, func, name, exec_time):
        self.name = name
        self.busy = False
        self.func = func
        self.op = None
        self.exec_time = exec_time
        self.Fi = None
        self.Fj = None
        self.Fk = None
        self.Qj = None
        self.Qk = None
        self.Rj = True
        self.Rk = True
        self.remain_time = 0

    def assignTask(self, op, fi:Register, fj:Register, fk:Register, inst):
        if isinstance(fi, Register) and fi.occupied:
            return False
        self.inst = inst
        self.op = op
        self.busy = True
        self.Fi = fi
        self.Fj = fj
        self.Fk = fk
        self.remain_time = self.exec_time

        if isinstance(self.Fi, Register):
            self.Fi.hold(self, True)

        if isinstance(self.Fj, Register):
            if self.Fj.occupied:
                self.Qj = self.Fj.funcunit
                self.Rj = False
        else:
            self.Rj = True
            self.Qj = None

        if isinstance(self.Fk, Register):
            if self.Fk.occupied:
                self.Qk = self.Fk.funcunit
                self.Rk = False
        else:
            self.Rk = True
            self.Qk = None

    def check(self):
        is_ready = True
        if isinstance(self.Fj, Register):
            if self.Fj.occupied:
                is_ready = False
                self.info = 'Fj: {} is occupied.'.format(self.Fj.name)
        if isinstance(self.Fk, Register):
            if self.Fk.occupied:
                is_ready = False
                self.info = 'Fk: {} is occupied.'.format(self.Fk.name)
        return is_ready

    def read_data(self):
        if isinstance(self.Fj, int):
            self.a = self.Fj
        else:
            self.a = self.Fj.value

        if isinstance(self.Fk, int):
            self.b = self.Fk
        else:
            self.b = self.Fk.value

    def exec(self):
        self.remain_time -= 1

        if self.remain_time == 0:
            try:
                if self.func == unit_add:
                    self.inst.result = self.func(self.op, self.a, self.b)
                else:
                    self.inst.result = self.func(self.a, self.b)
            except:
                self.inst.result = 0
            return True
        else:
            return False

    def write_result(self):
        if isinstance(self.Fi, Register):
            self.Fi.value = self.inst.result

    def release(self):
        if isinstance(self.Fi, Register):
            self.Fi.release()
        if isinstance(self.Fj, Register):
            self.Fj.release()
        if isinstance(self.Fk, Register):
            self.Fk.release()
        self.op = None
        self.Fi = None
        self.Fj = None
        self.Fk = None
        self.busy = False
        self.op = None
        self.Qj = None
        self.Qk = None
        self.Rj = True
        self.Rk = True
        self.remain_time = 0


    def get_info(self):
        return [self.remain_time, self.name, self.busy,
                self.op, self.Fi, self.Fj, self.Fk,
                self.Qj, self.Qk,self.Rj, self.Rk]

    def __str__(self):
        return self.name