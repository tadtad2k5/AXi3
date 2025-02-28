import re
import os

class RISCVAssembler:
    def __init__(self):
        self.instruction_map = {
            'lw':    ('0000011', '010', ''),
            'sw':    ('0100011', '010', ''),
            'add':   ('0110011', '000', '0000000'),
            'sub':   ('0110011', '000', '0100000'),
            'and':   ('0110011', '111', '0000000'),
            'or':    ('0110011', '110', '0000000'),
            'xor':   ('0110011', '100', '0000000'),
            'sll':   ('0110011', '001', '0000000'),
            'srl':   ('0110011', '101', '0000000'),
            'sra':   ('0110011', '101', '0100000'),
            'addi':  ('0010011', '000', ''),
            'andi':  ('0010011', '111', ''),
            'ori':   ('0010011', '110', ''),
            'xori':  ('0010011', '100', ''),
            'slli':  ('0010011', '001', ''),
            'srli':  ('0010011', '101', '0000000'),
            'srai':  ('0010011', '101', '0100000'),
            'beq':   ('1100011', '000', ''),
            'bne':   ('1100011', '001', ''),
            'blt':   ('1100011', '100', ''),
            'bge':   ('1100011', '101', ''),
            'ble':   ('1100011', '101', ''),
            'jal':   ('1101111', '', ''),
            'jalr':  ('1100111', '000', ''),
            'auipc': ('0010111', '', ''),
            'j':     ('1101111', '', ''),
        }

        # Chuyen thanh ghi
        # VD: x5 -> 5 de de hieu voi ma may
        self.registers = {f'x{i}': i for i in range(32)}


    def parse_register(self, reg):
        if reg not in self.registers:
            raise ValueError(f"Thanh ghi không hợp lệ: {reg}")
        return self.registers[reg]

    # Bits: so bit imm co the chua
    def parse_immediate(self, imm, bits):
        try:

            # Neu imm co chua '()' thi cat ra, chi lay phan truoc '()'
            # VD: 4(x5) -> 4
            if '(' in imm:
                imm = imm[:imm.index('(')]
                if not imm:
                    imm = '0'

            # Chuyen imm thanh so nguyen
            val = int(imm)

            # Kiem tra hop le voi so bits da duoc de ra truoc do hay khong
            if not (-2**(bits-1) <= val < 2**(bits-1)):
                raise ValueError(f"Immediate {imm} vượt quá {bits} bit")
            return val & ((1 << bits) - 1)
        except ValueError:
            raise ValueError(f"Giá trị immediate không hợp lệ: {imm}")

    
    def clean_line(self, line):

        # Tim kiem bat dau bang '#' va sau '#' xong roi thay the bang ''
        # Ham strip de xoa khoang trang dau va cuoi
        line = re.sub(r'#.*$', '', line).strip()

        # Ti kiem khoang trong lien tiep va thay the bang ''
        return re.sub(r'\s+', ' ', line)

    def encode_instruction(self, inst, labels, current_addr):
        parts = inst.replace(',', ' ').split()
        op = parts[0].lower()
        
        if op not in self.instruction_map:
            raise ValueError(f"Lệnh không xác định: {op}")
            
        opcode, funct3, funct7 = self.instruction_map[op]
        
        try:
            # R-type instructions
            if op in ['add', 'sub', 'and', 'or', 'xor', 'sll', 'srl', 'sra']:
                rd = format(self.parse_register(parts[1]), '05b')
                rs1 = format(self.parse_register(parts[2]), '05b')
                rs2 = format(self.parse_register(parts[3]), '05b')
                return int(f"{funct7}{rs2}{rs1}{funct3}{rd}{opcode}", 2)

            # I-type instructions
            elif op in ['addi', 'andi', 'ori', 'xori', 'slli', 'srli', 'srai']:
                rd = format(self.parse_register(parts[1]), '05b')
                rs1 = format(self.parse_register(parts[2]), '05b')
                imm = format(self.parse_immediate(parts[3], 12), '012b')
                if op in ['slli', 'srli', 'srai']:
                    imm = funct7 + imm[7:]
                return int(f"{imm}{rs1}{funct3}{rd}{opcode}", 2)

            # Load instructions
            elif op == 'lw':
                rd = format(self.parse_register(parts[1]), '05b')
                offset_base = parts[2].split('(')
                imm = format(self.parse_immediate(offset_base[0], 12), '012b')
                rs1 = format(self.parse_register(offset_base[1][:-1]), '05b')
                return int(f"{imm}{rs1}{funct3}{rd}{opcode}", 2)

            # Store instructions
            elif op == 'sw':
                rs2 = format(self.parse_register(parts[1]), '05b')
                offset_base = parts[2].split('(')
                imm = format(self.parse_immediate(offset_base[0], 12), '012b')
                rs1 = format(self.parse_register(offset_base[1][:-1]), '05b')
                imm_11_5 = imm[:7]
                imm_4_0 = imm[7:]
                return int(f"{imm_11_5}{rs2}{rs1}{funct3}{imm_4_0}{opcode}", 2)

            # Branch instructions
            elif op in ['beq', 'bne', 'blt', 'bge', 'ble']:
                if op == 'ble':
                    rs1 = format(self.parse_register(parts[2]), '05b')
                    rs2 = format(self.parse_register(parts[1]), '05b')
                else:
                    rs1 = format(self.parse_register(parts[1]), '05b')
                    rs2 = format(self.parse_register(parts[2]), '05b')
                
                if parts[3] not in labels:
                    raise ValueError(f"Nhãn không tồn tại: {parts[3]}")
                
                offset = (labels[parts[3]] - current_addr) >> 1
                imm = format(offset & 0xFFF, '012b')
                imm_12 = imm[0]
                imm_11 = imm[1]
                imm_10_5 = imm[2:8]
                imm_4_1 = imm[8:]
                
                return int(f"{imm_12}{imm_10_5}{rs2}{rs1}{funct3}{imm_4_1}{imm_11}{opcode}", 2)

            # JAL instruction
            elif op == 'jal' or op == 'j':
                rd = format(0 if op == 'j' else self.parse_register(parts[1]), '05b')
                target = parts[2] if op == 'jal' else parts[1]
                if target not in labels:
                    raise ValueError(f"Nhãn không tồn tại: {target}")
                
                offset = (labels[target] - current_addr) >> 1
                imm = format(offset & 0xFFFFF, '020b')
                imm_20 = imm[0]
                imm_10_1 = imm[10:20]
                imm_11 = imm[9]
                imm_19_12 = imm[1:9]
                
                return int(f"{imm_20}{imm_10_1}{imm_11}{imm_19_12}{rd}{opcode}", 2)

            # JALR instruction
            elif op == 'jalr':
                rd = format(self.parse_register(parts[1]), '05b')
                offset_base = parts[2].split('(')
                imm = format(self.parse_immediate(offset_base[0], 12), '012b')
                rs1 = format(self.parse_register(offset_base[1][:-1]), '05b')
                return int(f"{imm}{rs1}{funct3}{rd}{opcode}", 2)

            # AUIPC instruction
            elif op == 'auipc':
                rd = format(self.parse_register(parts[1]), '05b')
                imm = format(self.parse_immediate(parts[2], 20), '020b')
                return int(f"{imm}{rd}{opcode}", 2)

        except Exception as e:
            raise ValueError(f"Lỗi mã hóa lệnh '{inst}': {str(e)}")

    def assemble(self, input_file, output_file):
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Không tìm thấy file: {input_file}")

        labels = {}
        instructions = []
        current_addr = 0

        with open(input_file, 'r') as f:
            for line in f:
                line = self.clean_line(line)
                if not line:
                    continue

                if ':' in line:
                    label = line[:line.index(':')].strip()
                    labels[label] = current_addr
                    remainder = line[line.index(':')+1:].strip()
                    if remainder:
                        instructions.append((remainder, current_addr))
                        current_addr += 4
                else:
                    instructions.append((line, current_addr))
                    current_addr += 4

        with open(output_file, 'w') as f:
            for inst, addr in instructions:
                try:
                    machine_code = self.encode_instruction(inst, labels, addr)
                    # Đảm bảo viết chữ thường
                    f.write(f"{machine_code:08x}\n")
                except ValueError as e:
                    print(f"Lỗi tại địa chỉ {addr:08X}: {str(e)}")
                    continue

def main():
    assembler = RISCVAssembler()
    input_file = "test.txt"
    output_file = "out.txt"
    
    try:
        assembler.assemble(input_file, output_file)
        print(f"Dịch thành công! Kết quả được lưu tại: {output_file}")
    except Exception as e:
        print(f"Dịch thất bại: {str(e)}")

if __name__ == "__main__":
    main()
