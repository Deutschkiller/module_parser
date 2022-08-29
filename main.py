# from typing_extensions import Self


def Instance():
    def __init__(self,name):
        self.name = name
        self.father = None
        self.child = []
        self.module = None

    def set_father(self,father):
        if(type(father) == "Instance"):
            self.father = father
        else:
            print("invalid father")

    def add_child(self,child):
        if(type(child) == "Instance"):
            self.child.append(child)
        else:
            print("invalid child element")
    
    def rm_child(self,child):
        if(type(child) == "Instance"):
            self.child.remove(child)
        else:
            print("invalid child remove")

    def set_instance(self,module):
        if(type(module) == "Module"):
            self.module = module
        else:
            print("invalid module")

class Module():
    def __init__(self,name) -> None:
        self.name = name
        self.interfaces = []

    def add_if(self,if_type,name):
        self.interfaces.append(Interface(if_type,name))

    def remove_if(self,if_type,name):
        self.interfaces.remove(Interface(if_type,name))

    def show_interfaces(self):
        for e in self.interfaces:
            print(e.if_type+" "+str(e.width)+" "+e.name)

    def print_info(self):
        print("-----------------")
        print("module name:" + self.name)
        self.show_interfaces()
        print("-----------------")
class Interface():
    def __init__(self,if_type,name) -> None:
        self.width = 1
        self.name = name
        self.if_type = if_type

class Verilog_file():
    def __init__(self,path,verilog_type) -> None:
        self.path = path
        self.load_file()
        self.verilog_type = verilog_type
        if(self.verilog_type == "1995"):
            self.parse_module_1995()
    
    def load_file(self):
        with open(self.path,"r") as f:
            self.content = f.readlines()
        return self.content
    
    def parse_module_1995(self): #分析1995格式verilog 分析模块信息，不分析梨花信息
        for line in self.content:
            if line[0:6] == "module":
                self.module = Module(line[6:])
            if line[0:5] == "input":
                self.module.add_if("input",line[5:-1])
            if line[0:6] == "output":
                self.module.add_if("output",line[6:-1])
            if line[0:4] == "wire":
                self.module.add_if("wire",line[4:-1])
            if line[0:3] == "reg":
                self.module.add_if("wire",line[3:-1])

   

            
    def detect_instance(self):
        pass

test_verilog = Verilog_file("./test_verilogs/arp.v","1995")

print(test_verilog.module.interfaces)

test_verilog.module.print_info()