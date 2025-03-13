# Kênh địa chỉ đọc
class ReadAddressChannel:
    def __init__(self):
        self.ARADDR = 0
        self.ARLEN = 0
        self.ARSIZE = 0
        self.ARBURST = 0
        self.ARVALID = 0
        self.ARREADY = 0

    def send_request(self, addr, length, size, burst):
        self.ARADDR = addr
        self.ARLEN = length
        self.ARSIZE = size
        self.ARBURST = burst
        self.ARVALID = 1
        print(f"Read Address Channel: Sent request to {addr}")

# Kênh địa chỉ ghi
class WriteAddressChannel:
    def __init__(self):
        self.AWADDR = 0
        self.AWLEN = 0
        self.AWSIZE = 0
        self.AWBURST = 0
        self.AWVALID = 0
        self.AWREADY = 0

    def send_request(self, addr, length, size, burst):
        self.AWADDR = addr
        self.AWLEN = length
        self.AWSIZE = size
        self.AWBURST = burst
        self.AWVALID = 1
        print(f"Write Address Channel: Sent request to {addr}")

# Kênh dữ liệu đọc
class ReadDataChannel:
    def __init__(self):
        self.RDATA = 0
        self.RRESP = 0
        self.RLAST = 0
        self.RVALID = 0
        self.RREADY = 0

    def receive_data(self, data):
        self.RDATA = data
        self.RVALID = 1
        print(f"Read Data Channel: Received data {data}")

# Kênh dữ liệu ghi
class WriteDataChannel:
    def __init__(self):
        self.WDATA = 0
        self.WLAST = 0
        self.WVALID = 0
        self.WREADY = 0

    def send_data(self, data):
        self.WDATA = data
        self.WVALID = 1
        print(f"Write Data Channel: Sent data {data}")

# Kênh phản hồi ghi
class WriteResponseChannel:
    def __init__(self):
        self.BRESP = 0
        self.BVALID = 0
        self.BREADY = 0

    def receive_response(self, resp):
        self.BRESP = resp
        self.BVALID = 1
        print(f"Write Response Channel: Received response {resp}")

# Master chứa các kênh
class AXIMaster:
    def __init__(self):
        self.ar = ReadAddressChannel()
        self.aw = WriteAddressChannel()
        self.r = ReadDataChannel()
        self.w = WriteDataChannel()
        self.b = WriteResponseChannel()

    def read_request(self, addr):
        self.ar.send_request(addr, length=4, size=2, burst=1)

    def write_request(self, addr, data):
        self.aw.send_request(addr, length=4, size=2, burst=1)
        self.w.send_data(data)

# Slave chứa các kênh
class AXISlave:
    def __init__(self):
        self.ar = ReadAddressChannel()
        self.aw = WriteAddressChannel()
        self.r = ReadDataChannel()
        self.w = WriteDataChannel()
        self.b = WriteResponseChannel()

    def process_read(self, master):
        if master.ar.ARVALID:
            self.ar.ARREADY = 1
            self.r.receive_data(1234)

    def process_write(self, master):
        if master.aw.AWVALID:
            self.aw.AWREADY = 1
            self.w.WREADY = 1
            self.b.receive_response(0)  # 0 = OK response

# Quản lý giao tiếp giữa Master và Slave
class AXITransaction:
    def __init__(self):
        self.master = AXIMaster()
        self.slave = AXISlave()

    def execute_read(self, addr):
        self.master.read_request(addr)
        self.slave.process_read(self.master)

    def execute_write(self, addr, data):
        self.master.write_request(addr, data)
        self.slave.process_write(self.master)

# Khởi tạo giao thức AXI
axi = AXITransaction()

# Test đọc và ghi
axi.execute_read(0x1000)
axi.execute_write(0x2000, 5678)
