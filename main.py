import re
import os
class Instance():
    def __init__(self,module,name) -> None:
        self.name = name
        self.module = module
        self.child = None
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
            self.child = child
        else:
            print("invalid instance child type")

    def set_father(self,father):
        if type(father) == type(self):
            self.father = father
        else:
            print("invalid instance father type")

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


    def parse_module_1995(self): #分析1995格式verilog 分析模块信息，不分析梨花信息
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
            buffer_string = re.sub(re.compile("\..+?\(.*?\)",re.DOTALL),"",code)# 删除端口连接的字符串

            module_name = re.findall("\w+",buffer_string)[0]
            instance_name = re.findall("\w+",buffer_string)[-1]
            self.module.instances.append(Instance(Module(module_name),instance_name))

    


# test_verilog.module.print_info()

# test_verilog.detect_instance()

# i = 0
# for e in test_verilog.text_content_list:
#     i+=1
#     print(str(i)+":---------------------------")
#     print(e)
# test_verilog = Verilog_file("./test_verilogs/arp.v","1995")
module_lists = []

filelist = os.listdir("./test_verilogs")
for file in filelist:
    test_verilog = Verilog_file("./test_verilogs/"+file,"1995")
    print("./test_verilogs/"+file)
    test_verilog.module.print_info()
    module_lists.append(test_verilog.module)

# for module in module_lists:
#     print(module.print_info())