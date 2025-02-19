#AXI3
#Class
# Dat - Uy
# 17/02/2025
print("Project AXI3")
#AXI3 : Master side and Slave side
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
    
    


    
    
        
