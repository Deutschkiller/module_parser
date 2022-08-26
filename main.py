from typing_extensions import Self


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
        self.input = []
        self.output = []
        self.parameter = []

    def add_input(self,input):
        self.input.append(input)
    
    def remove_input(self,input):
        self.input.remove(input)

    def add_output(self,output):
        self.output.append(output)
    
    def remove_output(self,output):
        self.output.remove(output)

    def add_parameter(self,parameter):
        self.parameter.append(parameter)
    
    def remove_parameter(self,parameter):
        self.parameter.remove(parameter)

class Verilog_file():
    def __init__(self,path) -> None:
        self.path = path
        self.load_file()
    
    def load_file(self):
        with open(self.path,"r") as f:
            self.content = f.readlines()
        return self.content
    
    def detect_module(self):
        for line in self.content:
            
    def detect_instance(self):
        pass