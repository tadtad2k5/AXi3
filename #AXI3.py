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
        self.AR = "ARVAILD"
        self.R = "RREADY"
        self.AW = "AWVAILD"
        self.W = "WVAILD"
        self.B = "BREADY"
    def read_address_channel(self):
        if self.AR == "ARVAILD":
            return True
        return False
    
    


    
    
        
