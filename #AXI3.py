#AXI3
#Class
# Dat - Uy
# 17/02/2025
print("Project AXI3")
#AXI3 : Master side and Slave side
class AXI3:
    def __init__(self):
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
        self.ARVALID = False
        self.RREADY = False
        self.AWVALID = False
        self.WVALID = False
        self.BREADY = False
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
        self.ARREADY = False
        self.RVALID = False
        self.AWREADY = False
        self.WREADY = False
        self.BVALID = False
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
#READ
class Master_ReadAddressChannel(Master):
    def __init__(self):
        super().__init__()
        self.AR = ""
        self.ARADDR = None
        self.ARLEN = None
        self.ARSIZE = None
        self.ARBURST = None
        self.ARVALID = False

    def set_address(self, address):
        self.ARADDR = address

    def set_length(self, length):
        self.ARLEN = length

    def set_size(self, size):
        self.ARSIZE = size

    def set_burst(self, burst):
        self.ARBURST = burst

    def validate_address(self):
        if self.ARADDR is not None and self.ARLEN is not None and self.ARSIZE is not None and self.ARBURST is not None:
            self.ARVALID = True
        else:
            self.ARVALID = False

    def get_address_info(self):
        return {
            "ARADDR": self.ARADDR,
            "ARLEN": self.ARLEN,
            "ARSIZE": self.ARSIZE,
            "ARBURST": self.ARBURST,
            "ARVALID": self.ARVALID
        }

    def print_address_info(self): #kiem tra thông tin địa chỉ
        address_info = self.get_address_info()
        for key, value in address_info.items():
            print(f"{key}: {value}")
class Slave_ReadAddressChannel(Slave):
    def __init__(self):
        super().__init__()
        self.ARREADY = False

    def set_arready(self, value):
        self.ARREADY = value

    def process_read_request(self):
        if self.ARREADY:
            print("Processing read request...")
            # Thực hiện các thao tác xử lý yêu cầu đọc tại đây
            self.ARREADY = False  # Reset tín hiệu ARREADY sau khi xử lý xong
        else:
            print("Read request is not ready.")

class Master_ReadDataChannel(Master):
    def __init__(self):
            super().__init__()
            self.R = ""
            self.RREADY = False
    
    def set_rready(self, value):
            self.RREADY = value
    
    def process_read_data(self):
            if self.RREADY:
                print("Processing read data...")
                # Thực hiện các thao tác xử lý dữ liệu đọc tại đây
                self.RREADY = False  # Reset tín hiệu RREADY sau khi xử lý xong
            else:
                print("Read data is not ready.")
class Slave_ReadDataChannel(Slave):
    def __init__(self):
        super().__init__()
        self.RVALID = False
        self.RRESP = None
        self.RDATA = None
        self.RLAST = None

    def set_rvalid(self, value):
        self.RVALID = value

    def set_rresp(self, response):
        self.RRESP = response

    def set_rdata(self, data):
        self.RDATA = data

    def set_rlast(self, last):
        self.RLAST = last

    def validate_data(self):
        if self.RDATA is not None and self.RRESP is not None:
            self.RVALID = True
        else:
            self.RVALID = False

    def get_data_info(self):
        return {
            "RDATA": self.RDATA,
            "RRESP": self.RRESP,
            "RLAST": self.RLAST,
            "RVALID": self.RVALID
        }

    def print_data_info(self): #kiem tra thông tin dữ liệu
        data_info = self.get_data_info()
        for key, value in data_info.items():
            print(f"{key}: {value}")

    def process_read_data(self):
        if self.RVALID:
            print("Processing read data...")
            # Thực hiện các thao tác xử lý dữ liệu đọc tại đây
            self.RVALID = False  # Reset tín hiệu RVALID sau khi xử lý xong
        else:
            print("Read data is not ready.")
#WRITE
class Master_WriteAddressChannel(Master):
    def __init__(self):
        super().__init__()
        self.AW = ""
        self.AWADDR = None
        self.AWLEN = None
        self.AWSIZE = None
        self.AWBURST = None
        self.AWVALID = False

    def set_address(self, address):
        self.AWADDR = address

    def set_length(self, length):
        self.AWLEN = length

    def set_size(self, size):
        self.AWSIZE = size

    def set_burst(self, burst):
        self.AWBURST = burst

    def validate_address(self): #kiem tra dia chi co hop le hay khong
        if self.AWADDR is not None and self.AWLEN is not None and self.AWSIZE is not None and self.AWBURST is not None:
            self.AWVALID = True 
        else:
            self.AWVALID = False

    def get_address_info(self):
        return {
            "AWADDR": self.AWADDR,
            "AWLEN": self.AWLEN,
            "AWSIZE": self.AWSIZE,
            "AWBURST": self.AWBURST,
            "AWVALID": self.AWVALID
        }

    def print_address_info(self): #kiem tra thông tin địa chỉ
        address_info = self.get_address_info()
        for key, value in address_info.items():
            print(f"{key}: {value}")
class Slave_WriteAddressChannel(Slave):
    def __init__(self):
        super().__init__()
        self.AWREADY = False

    def set_awready(self, value):
        self.AWREADY = value

    def process_write_request(self):
        if self.AWREADY:
            print("Processing write request...")
            # Thực hiện các thao tác xử lý yêu cầu ghi tại đây
            self.AWREADY = False  # Reset tín hiệu AWREADY sau khi xử lý xong
        else:
            print("Write request is not ready.")
class Master_WriteDataChannel(Master):
    def __init__(self):
        super().__init__()
        self.W = ""
        self.WDATA = None
        self.WLAST = None
        self.WVALID = False
    def set_data(self, data):
        self.WDATA = data
    def set_last(self, last):
        self.WLAST = last
    def validate_data(self):
        if self.WDATA is not None:
            self.WVALID = True
        else:
            self.WVALID = False
    def get_data_info(self):
        return {
            "WDATA": self.WDATA,
            "WLAST": self.WLAST,
            "WVALID": self.WVALID
        }
    def print_data_info(self): #kiem tra thông tin dữ liệu
        data_info = self.get_data_info()
        for key, value in data_info.items():
            print(f"{key}: {value}")
class Slave_WriteDataChannel(Slave):
    def __init__(self):
        super().__init__()
        self.WREADY = False
    def set_wready(self, value):
        self.WREADY = value
    def process_write_data(self):
        if self.WREADY:
            print("Processing write data...")
            # Thực hiện các thao tác xử lý dữ liệu ghi tại đây
            self.WREADY = False  # Reset tín hiệu WREADY sau khi xử lý xong
        else:
            print("Write data is not ready.")
class Master_WriteResponseChannel(Master):
    def __init__(self):
        super().__init__()
        self.B = ""
        self.BREADY = False
    def set_bready(self, value):
        self.BREADY = value
    def process_write_response(self):
        if self.BREADY:
            print("Processing write response...")
            # Thực hiện các thao tác xử lý phản hồi ghi tại đây
            self.BREADY = False  # Reset tín hiệu BREADY sau khi xử lý xong
        else:
            print("Write response is not ready.")
class Slave_WriteResponseChannel(Slave):
    def __init__(self):
        super().__init__()
        self.BVALID = False
        self.BRESP = None
    def set_bvalid(self, value):
        self.BVALID = value
    def set_bresp(self, response):
        self.BRESP = response
    def validate_response(self): #kiem tra phản hồi co hop le hay khong
        if self.BRESP is not None:
            self.BVALID = True
        else:
            self.BVALID = False
    def get_response_info(self):
        return {
            "BRESP": self.BRESP,
            "BVALID": self.BVALID
        }
    def print_response_info(self): #kiem tra thông tin phản hồi
        response_info = self.get_response_info()
        for key, value in response_info.items():
            print(f"{key}: {value}")
    def process_write_response(self):
        if self.BVALID:
            print("Processing write response...")
            # Thực hiện các thao tác xử lý phản hồi ghi tại đây
            self.BVALID = False
#TEST
