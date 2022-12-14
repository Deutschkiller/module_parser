from importlib.util import module_for_loader
from pkgutil import iter_modules
import re
import os
from ssl import VerifyFlags
class Instance():
    def __init__(self,module,name) -> None:
        self.name = name
        self.module = module
        self.child = []
        self.father = None

    def set_instance(self,module):
        if(type(module) == "Module"):
            self.module = module
        else:
            print("invalid module")

    def print_instance(self):
        print("|-"+self.name+" <-- "+ self.module.name)

    def set_child(self,child):
        if type(child) == type(self):
            self.child.append(child)
        else:
            print("invalid instance child type")

    def set_father(self,father):
        if type(father) == type(self):
            self.father = father
        else:
            print("invalid instance father type")

    def show_child(self):
        for i in range(0,self.child):
            print(str(i) + self.child[i].name)

            
class Module():
    def __init__(self,name) -> None:
        self.name = name
        self.interfaces = []
        self.interfaces_input = []
        self.interfaces_output = []
        self.interfaces_dict = dict()
        self.instances = []

    def add_if(self,if_type,name):
        self.interfaces.append(Interface(if_type,name))
        if(if_type == "input"):
            self.interfaces_input.append(Interface("input",name))
        elif(if_type == "output"):
            self.interfaces_output.append(Interface("output",name))

    def remove_if(self,if_type,name):
        self.interfaces.remove(Interface(if_type,name))
        if(if_type == "input"):
            self.interfaces_input.remove(name)
        elif(if_type == "output"):
            self.interfaces_output.remove(name)

    def show_interfaces(self):
        for e in self.interfaces_input:
            print("input " + e.name + " width= "+str(e.width))
        for e in self.interfaces_output:
            print("output " + e.name + " width= "+str(e.width))

    def show_instances(self):
        print("Instances contains:")
        for e in self.instances:
            e.print_instance()
        print("Instances printed")

    def print_info(self):
        print("-----------------")
        print("module name:" + self.name)
        self.show_interfaces()
        self.show_instances()
        print("-----------------")
        
class Interface():
    def __init__(self,if_type,name) -> None:
        self.width = 1
        self.name = name
        self.if_type = if_type
        self.cal_width()

    def cal_width(self):
        
        if re.findall('\[.*?\]',self.name) == []:
            self.width = 1
        elif re.findall('\[.*?\]',self.name) != []:
            # width_text = re.findall('\[.*?\]',self.name)[0]
            self.width = re.findall('\[.*?\:',self.name)[0][1:-1]
        try:
            self.name = re.findall('\w+',self.name)[-1]
        except Exception as E:
            print(E)
            print("!!!!cal_width,debug_info:"+self.name)

class Verilog_file():
    def __init__(self,path,verilog_type) -> None:
        self.path = path
        self.load_file()
        self.gen_text_content_list()
        self.verilog_type = verilog_type
        if(self.verilog_type == "1995"):
            self.parse_module_1995()
        self.detect_instance()
        
    def load_file(self):
        with open(self.path,"r") as f:
            self.content = f.readlines()
        return self.content
    
    def gen_text_content_list(self):
        self.text_content = ""
        for line in self.content:
            self.text_content = self.text_content+line
        self.text_content = re.sub("\/\/.*?\n","",self.text_content)
        self.text_content = re.sub(re.compile("\/\*.*?\*\/",re.DOTALL),"",self.text_content)
        self.text_content_list = self.text_content.split(";")


    def parse_module_1995(self): #??????1995??????verilog ??????????????????????????????????????????
        for line in self.content:
            if re.search('\/',line):
                pass
            elif re.search('\*',line):
                pass
            elif line[0:6] == "module":
                self.module = Module(re.findall("\w+",line)[1])
            elif re.search("\sinput\s",line):
                self.module.add_if("input",line[re.search("input",line).span()[1]:-1])
            elif re.search("\soutput\s",line):
                self.module.add_if("output",line[re.search("output",line).span()[1]:-1])
            elif re.search("\swire\s",line):
                self.module.add_if("wire",line[re.search("wire",line).span()[1]:-1])
            elif re.search("\sreg\s",line):
                self.module.add_if("reg",line[re.search("reg",line).span()[1]:-1])

    def cnt_brackets(self,input_string:str) -> int:
        return input_string.count("(") - input_string.count(")")

    def detect_instance(self):
        linenum = 0
        brackets_cnt = 0
        self.instance_block_list = []
        for block in self.text_content_list:
            if re.search("\.\w+\(\w*\)",block) is not None: #find.();
                self.instance_block_list.append(block)
        for code in self.instance_block_list:  
            code = code.split("end")[-1].split("generate")[-1].split("endtask")[-1].split("else")[-1].split('begin')[-1]
            buffer_string = re.sub(re.compile("\..+?\(.*?\)",re.DOTALL),"",code)# ??????????????????????????????
            # print(buffer_string)
            module_name = re.findall("\w+",buffer_string)[0]
            instance_name = re.findall("\w+",buffer_string)[-1]
            self.module.instances.append(Instance(Module(module_name),instance_name))
            self.module.instances = list(set(self.module.instances))

def parsing_test_verilog():

    module_lists = []

    filelist = os.listdir("./test_verilogs")
    for file in filelist:
        test_verilog = Verilog_file("./test_verilogs/"+file,"1995")
        print("parsing---./test_verilogs/"+file)
        # test_verilog.module.print_info()
        module_lists.append(test_verilog.module)

    for module in module_lists:
        print(module.name)
        print(module.show_instances())


class Design():

    def __init__(self,directory) -> None:
        self.directory = directory
        filelist = os.listdir(self.directory)
        self.module_list=[]
        for file in filelist:
            test_verilog = Verilog_file("./test_verilogs/"+file,"1995")
            self.module_list.append(test_verilog.module)
        self.parse_modules()

    # def parse_modules_legacy(self):
    #     for module in self.module_list:
    #         for i in range(0, len(module.instances)):
    #             for compare_module in self.module_list:
    #                 if compare_module.name == module.instances[i].module.name:
    #                     for child_instance in compare_module.instances:
    #                         module.instances[i].child.append(child_instance)
    #                         print(module.name)
    #                         print(module.instances[i].name)
    #                         print(child_instance.name)
    #                         print(module.instances[i].child)

    def parse_modules(self):
        for i_module in range(len(self.module_list)):
            for i_instance in range(0,len(self.module_list[i_module].instances)):
                for i_compare in range(len(self.module_list)):
                    if self.module_list[i_compare].name == self.module_list[i_module].instances[i_instance].module.name:
                        for i_child_instance in range(len(self.module_list[i_compare].instances)):
                            child_instance = self.module_list[i_compare].instances[i_child_instance]
                            parent_instance = self.module_list[i_module].instances[i_instance]
                            parent_instance.child.append(child_instance)
                            # self.module_list[i_module].instances[i_instance].child.append(
                            #     self.module_list[i_compare].instances[i_child_instance])



    def cal_depth(self,module):
        depth = 0
        while(True):
            if module.instances != []:
                
                module = module.instances[0].module
                depth += 1
            else:
                break
        return depth

    def findout_top_instance(self):
        top_instance = self.module_list[0]
        current_depth = 0
        max_depth = 0
        for module in self.module_list:
            current_depth = self.cal_depth(module)
            print(module.name)
            print(self.cal_depth(module))
            if current_depth > max_depth:
                top_instance = module
                max_depth = current_depth
        return top_instance

design = Design("./test_verilogs")

print(design.module_list[0].instances[0].child)

