#AXI3
#Class
# Dat - Uy
# 17/02/2025
print("Project AXI3")
#AXI3 : Master side and Slave side
# tách riêng từng kênh, xem các packet
class AXI3:
    def __init_(self):
        self.AR = ""
        self.R = ""
        self.AW = ""
        self.W = ""
        self.B = ""
        self.ARVALID = False
        self.ARREADY = False
        self.RVALID = False
        self.RREADY = False
        self.AWVALID = False
        self.AWREADY = False
        self.WVALID = False
        self.WREADY = False
        self.BVALID = False
        self.BREADY = False
        self.burst_type = ""
    def update_program_counter(self, new_pc): # nhận dữ liệu từ pc
        self.program_counter = new_pc

    def get_program_counter(self):
        return self.program_counter
        
    def set_burst_type(self, burst_type):
        self.burst_type = burst_type
        
    def set_axsize(self, axsize):
        self.axsize = axsize
        
    def set_arvalid(self, value):
        self.ARVALID = value

    def set_rready(self, value):
        self.RREADY = value

    def set_awvalid(self, value):
        self.AWVALID = value

    def set_wvalid(self, value):
        self.WVALID = value

    def set_bready(self, value):
        self.BREADY = value

        # = VAILD/Ready
'''   Kênh AR sẽ có tín hiệu ARVALID (master) và tín hiệu ARREADY (slave).
Kênh R sẽ có tín hiệu RVALID (slave) và tín hiệu RREADY (master) .
Kênh AW sẽ có tín hiệu AWVALID (master) và tín hiệu AWREADY (slave). 
Kênh W sẽ có tín hiệu WVALID (master) và tín hiệu WREADY (slave) .
Kênh B sẽ có tín hiệu BVALID (slave) và tín hiệu BREADY (master) .
'''
#
class Master(AXI3):
    def __init__(self):
        super().__init__()
        self.AR = "ARVALID"
        self.R = "RREADY"
        self.AW = "AWVALID"
        self.W = "WVALID"
        self.B = "BREADY"
    def AxSize(self, value):
        if value == '000': return '1 bytes in transfer'
        if value == '001': return '2 bytes in transfer'
        if value == '010': return '4 bytes in transfer'
        if value == '011': return '8 bytes in transfer'
        if value == '100': return '16 bytes in transfer'
        if value == '101': return '32 bytes in transfer'
        if value == '110': return '64 bytes in transfer'
        if value == '111': return '128 bytes in transfer'
    def AxBURST(self, value):
        if value == '00': return 'FIXED'
        if value == '01': return 'INCR'
        if value == '10': return 'WRAP'
        if value == '11': return 'Reserved'
    def RRESP_BRESP(self, value):
        if value == '00': return 'OKAY'
        if value == '01': return 'EXOKAY'
        if value == '10': return 'SLVERR'
        if value == '11': return 'DECERR'
    def AxPROT(self, value): #Protection signal
        if value == '000': return 'Unprivileged access, data access'
        if value == '001': return 'Unprivileged access, instruction access'
        if value == '010': return 'Privileged access, data access'
        if value == '011': return 'Privileged access, instruction access'
        if value == '100': return 'Secure access, data access'
        if value == '101': return 'Secure access, instruction access'
        if value == '110': return 'Reserved'
        if value == '111': return 'Reserved'
    def reset_signals(self):
        self.ARVALID = False
        self.RREADY = False
        self.AWVALID = False
        self.WVALID = False
        self.BREADY = False
    def check_signals(self): #Kiểm tra tín hiệu
        return self.ARVALID, self.ARREADY, self.RVALID, self.RREADY, self.AWVALID, self.AWREADY, self.WVALID, self.WREADY, self.BVALID, self.BREADY
    def print_signals(self):
        signals = self.check_signals()
        for signal, state in signals.items():
            print(f"{signal}: {state}")
    def read_address_channel(self):
        if self.AR == "ARVALID":
            return True
        return False

    def write_address_channel(self):
        if self.AW == "AWVALID":
            return True
        return False

    def write_data_channel(self):
        if self.W == "WVALID":
            return True
        return False

    def read_data_channel(self):
        if self.R == "RREADY":
            return True
        return False

    def write_response_channel(self):
        if self.B == "BREADY":
            return True
        return False
class Slave(AXI3):
    def __init__(self):
        super().__init__()
        self.ARREADY = False
        self.RVALID = False
        self.AWREADY = False
        self.WREADY = False
        self.BVALID = False

    def set_arready(self, value):
        self.ARREADY = value

    def set_rvalid(self, value):
        self.RVALID = value

    def set_awready(self, value):
        self.AWREADY = value

    def set_wready(self, value):
        self.WREADY = value

    def set_bvalid(self, value):
        self.BVALID = value
    def reset_signals(self):
        self.ARREADY = False
        self.RVALID = False
        self.AWREADY = False
        self.WREADY = False
        self.BVALID = False

    def read_address_channel(self):
        if self.ARREADY:
            return "ARREADY is True"
        return "ARREADY is False"

    def read_data_channel(self):
        if self.RVALID:
            return "RVALID is True"
        return "RVALID is False"

    def write_address_channel(self):
        if self.AWREADY:
            return "AWREADY is True"
        return "AWREADY is False"

    def write_data_channel(self):
        if self.WREADY:
            return "WREADY is True"
        return "WREADY is False"

    def write_response_channel(self):
        if self.BVALID:
            return "BVALID is True"
        return "BVALID is False"
    
class TransistorRead(AXI3):
    def __init__(self):
        super().__init__()
        self.data = None
        self.RVALID = False
        self.RREADY = False

    def read_data(self):
        if self.RVALID and self.RREADY:
            return self.data
        return "Khong the doc"

    def set_data(self, data):
        self.data = data

    def reset_data(self):
        self.data = None

    def check_signals(self):
        return {
            "RVALID": self.RVALID,
            "RREADY": self.RREADY
        }

    def print_signals(self):
        signals = self.check_signals()
        for signal, state in signals.items():
            print(f"{signal}: {state}")

    def is_data_available(self):
        return self.data is not None

class TransistorWrite(AXI3):
    def __init__(self):
        super().__init__()
        self.data = None
        self.WVALID = False
        self.WREADY = False

    def write_data(self, data):
        if self.WVALID and self.WREADY:
            self.data = data
            return "Ghi thanh cong"
        return "Khong the ghi"

    def get_data(self):
        return self.data

    def reset_data(self):
        self.data = None

    def check_signals(self):
        return {
            "WVALID": self.WVALID,
            "WREADY": self.WREADY
        }

    def print_signals(self):
        signals = self.check_signals()
        for signal, state in signals.items():
            print(f"{signal}: {state}")

    def is_data_available(self):
        return self.data is not None

    
    
        
