# -*- coding: utf-8 -*-
# __author__ = 'lidong'

"""
Description:
"""

import hardware

class Simulator():
    """
    核心
    """
    def __init__(self, init_info):
        """
        初始化
        :param init_info 初始化信息，包括存储空间大小，加法乘法除法，
        """
        hardware.memory.clear()
        hardware.memory.extend(0 for i in range(init_info['mem_size']))
        self.registers = [hardware.Register(i, int) for i in range(32)]
        self.fregisters = [hardware.Register(i, float) for i in range(32)]
        if init_info['add_count'] == 1:
            self.adduints = [hardware.FunctionUint(hardware.unit_add, 'Add', init_info['add_delay'])]
        else:
            self.adduints = [hardware.FunctionUint(hardware.unit_add, 'Add' + str(i + 1), init_info['add_delay']) for i in range(init_info['add_count'])]

        self.intunits = [hardware.FunctionUint(hardware.unit_integer, 'Integer', 1)]

        if init_info['mul_count'] == 1:
            self.mulunits = [hardware.FunctionUint(hardware.unit_mul, 'Mult', init_info['mul_delay'])]
        else:
            self.mulunits = [hardware.FunctionUint(hardware.unit_mul, 'Mult' + str(i + 1), init_info['mul_delay']) for i in range(init_info['mul_count'])]

        if init_info['div_count'] == 1:
            self.divunits = [hardware.FunctionUint(hardware.unit_div, 'Divide', init_info['div_delay'])]
        else:
            self.divunits = [hardware.FunctionUint(hardware.unit_div, 'Divide' + str(i + 1), init_info['div_delay']) for i in range(init_info['div_count'])]

    def load_code(self, code:str):
        insts = code.strip().split('\n')
        self.instructions = [hardware.Instruction.ParseInstruction(i.strip()) for i in insts if i.strip()]
        self.stall_instructions = []

        self.stall_instructions.extend(self.instructions)
        self.running_instructions = []
        self.finished_instructions = []
        self.status_diagram = [[None]*4 for i in range(len(self.instructions))]
        self.exec_index = 0
        self.instructions_status = []
    def run_one_cycle(self, cycle):
        self.info = ''
        # 先把运行完毕的寄存器的资源释放
        for inst in self.running_instructions:
             if inst.stage == 3:
                 self.collectResource(inst)

        for inst in self.running_instructions:
            if inst.stage == 0:
                is_ready = self.checkForReadOperands(inst)
                if is_ready:
                    i = self.instructions.index(inst)
                    self.status_diagram[i][1] = cycle
                    inst.read_operands()
                    self.info += '{} Read operands.\n'.format(inst)

            elif inst.stage == 1 or inst.stage == 1.5:
                inst.execute()
                i = self.instructions.index(inst)
                self.status_diagram[i][2] = cycle
                self.info += '{} Execute.\n'.format(inst)

            elif inst.stage == 2:
                is_ready = self.checkForWriteResult(inst)
                if is_ready:
                    i = self.instructions.index(inst)
                    self.status_diagram[i][3] = cycle
                    inst.write_result()
                    self.info += '{} Write result.\n'.format(inst)
        if self.stall_instructions:
            inst = self.stall_instructions[0]
            u = self.checkForIssue(inst)
            if u:
                dest = self.get_register(inst.dest)
                source1 = self.get_register(inst.source1)
                source2 = self.get_register(inst.source2)
                if not dest.occupied:
                    u.assignTask(inst.operation, dest, source1, source2)
                    inst.assignUnit(u)
                    inst.issue()
                    self.stall_instructions.remove(inst)
                    self.running_instructions.append(inst)
                    i = self.instructions.index(inst)
                    self.status_diagram[i][0] = cycle
                else:
                    self.info += '\n!!!WAW hazard: {} Because of {}.\n\n'.format(inst, dest.funcunit)

        if len(self.finished_instructions) == len(self.instructions):
            self.finish = True
        else:
            self.finish = False

    def checkForIssue(self, inst):
        if inst.operation.lower() == 'ld':
            for u in self.intunits:
                if u.busy == False:
                    return u
        elif inst.operation.lower() == 'multd':
            for u in self.mulunits:
                if u.busy == False:
                    return u
        elif inst.operation.lower() == 'subd':
            for u in self.adduints:
                if u.busy == False:
                    return u
        elif inst.operation.lower() == 'divd':
            for u in self.divunits:
                if u.busy == False:
                    return u
        elif inst.operation.lower() == 'addd':
            for u in self.adduints:
                if u.busy == False:
                    return u

    def checkForReadOperands(self,inst):
        is_ready = True
        index = self.running_instructions.index(inst)

        for i in self.running_instructions[:index]:
            if inst.funcunit.Fj == i.funcunit.Fi or inst.funcunit.Fk == i.funcunit.Fi:
                is_ready = False
                self.info += '\n!!!RAW hazard: {} Because of {}.\n\n'.format(inst, i)
                break
        return is_ready

    def checkForWriteResult(self, inst):
        index = self.running_instructions.index(inst)
        for i in self.running_instructions[:index]:
            if (inst.dest == i.source1 or inst.dest == i.source2) and i.stage <= 1:
                self.info += '\n!!!WAR hazard: {} Because of {}.\n\n'.format(inst, i)
                return False
        return True

    def collectResource(self, inst):
        inst.release()
        self.info += '{} finished.\n'.format(inst)
        self.running_instructions.remove(inst)
        self.finished_instructions.append(inst)
        for i in self.running_instructions:
            if i.source1 == inst.dest:
                i.funcunit.Qj = None
                i.funcunit.Rj = True
            if inst.dest == i.source2:
                i.funcunit.Qk = None
                i.funcunit.Rk = True

    def get_register(self, name:str):
        if name.startswith('R'):
            return self.registers[int(name[1:])]
        elif name.startswith('F'):
            return self.fregisters[int(name[1:])]
        else:
            return int(name[:-1])

    def get_all_units(self):
        units = self.intunits + self.mulunits + self.adduints + self.divunits
        return units

    def get_registers(self):
        return self.registers

    def get_floatregisters(self):
        return self.fregisters
