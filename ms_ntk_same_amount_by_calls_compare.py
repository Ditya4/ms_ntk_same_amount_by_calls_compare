from os import path


class MsCalls:
    def __init__(self, index=None, switch_id=None, uni_a=None, uni_b=None,
                 bill_dtm=None, inc_tg=None, duration=None,
                 cdr_set=None, substr_service_type=None, outblock=None):
        self.index = index
        self.switch_id = switch_id
        self.uni_a = uni_a
        self.uni_b = uni_b
        self.bill_dtm = bill_dtm
        self.inc_tg = inc_tg
        self.duration = duration
        self.cdr_set = cdr_set
        self.substr_service_type = substr_service_type
        self.outblock = outblock
        # calculated fields
        self.hash = self.hash_create()
        

    def __str__(self):
        '''
        we return a string which almost looks like a list with str value
        of every field in record
        '''
        list_of_values = [str((t)) for name, t in self.__dict__.items()
                          if type(t).__name__ != "function" and
                          not name.startswith("__")]
        line_to_return = "[" + " , ".join(list_of_values) + "]"
        return line_to_return
    
    def hash_create(self):
        hash = ''  # len(self.uni_b) == 12 and 
        if str(self.uni_b)[:3] == '380':
            uni_b = self.uni_b[3:]
        else:
            uni_b = self.uni_b
        if str(self.uni_a)[:3] == '380':
            uni_a = str(self.uni_a)[3:]
        else:
            uni_a = '0'  # for 8800 and international A 
        
        hash = (str(self.switch_id) + uni_a + uni_b +
                str(self.inc_tg) +
                str(self.bill_dtm).replace('.', '').replace(' ', '').replace(':', '') +
                str(self.duration))
        return hash


class NtkCalls:
    def __init__(self, index=None, recipient_id=None, number_a=None, number_b=None,
                 date_start=None, duration=None, inc_tg=None,
                 call_type=None, cdr_set_id=None):
        self.index = index
        self.recipient_id = recipient_id
        self.number_a = number_a
        self.number_b = number_b
        self.date_start = date_start
        self.duration = duration
        self.inc_tg = inc_tg
        self.call_type = call_type
        self.cdr_set_id = cdr_set_id
        # calculated fields
        self.hash = self.hash_create()

    def __str__(self):
        '''
        we return a string which almost looks like a list with str value
        of every field in record
        '''
        list_of_values = [str((t)) for name, t in self.__dict__.items()
                          if type(t).__name__ != "function" and
                          not name.startswith("__")]
        line_to_return = "[" + " , ".join(list_of_values) + "]"
        return line_to_return
    
    def hash_create(self):
        hash = ''  # len(self.number_b) == 10 and
        if str(self.number_b)[0] == '0':
            number_b = str(self.number_b[1:])
        else:
            number_b = str(self.number_b)
        #=======================================================================
        # if str(self.uni_a)[:3] == '380':
        #     uni_a = str(self.uni_a)[3:]
        # else:
        #     uni_a = str(self.uni_a)
        #=======================================================================
        
        hash = (str(self.recipient_id) + str(self.number_a) + number_b +
                str(self.inc_tg) +
                str(self.date_start).replace('.', '').replace(' ', '').replace(':', '') +
                str(self.duration))
        return hash

def read_ntk_calls(folder, file_name):
    ntk_calls_file_name = path.join(folder, file_name)
    ntk_calls_file = open(ntk_calls_file_name)
    ntk_calls_lines = ntk_calls_file.readlines()
    size_of_ntk_calls_list = len(ntk_calls_lines)
    for index in range(size_of_ntk_calls_list):
        ntk_calls_lines[index] = (
               ntk_calls_lines[index].rstrip())
    ntk_calls = [None] * size_of_ntk_calls_list
    in_ntk_calls_list_index = 0
    out_ntk_calls_list_index = 0
    while in_ntk_calls_list_index < size_of_ntk_calls_list:
        line_split = (
               ntk_calls_lines[in_ntk_calls_list_index].split("\t"))
        if line_split[-1] == "\n":
            line_split.pop()
        # print(in_ntk_calls_list_index, "line_split =", line_split)
        if len(line_split) == 8:
            ntk_calls[out_ntk_calls_list_index] = (
                            NtkCalls(out_ntk_calls_list_index,
                            *line_split))
            in_ntk_calls_list_index += 1
            out_ntk_calls_list_index += 1
        else:
            print(f"Error in line from file = {file_name}",
                  f"with index = {in_ntk_calls_list_index}",
                  f"with value {line_split}",
                  f"wait for 8 parameters",
                  f"and got {len(line_split)}")
            size_of_ntk_calls_list -= 1
            in_ntk_calls_list_index += 1
            ntk_calls.pop()
    return ntk_calls


def read_ms_calls(folder, file_name):
    ms_calls_file_name = path.join(folder, file_name)
    ms_calls_file = open(ms_calls_file_name)
    ms_calls_lines = ms_calls_file.readlines()
    size_of_ms_calls_list = len(ms_calls_lines)
    for index in range(size_of_ms_calls_list):
        ms_calls_lines[index] = (
               ms_calls_lines[index].rstrip())
    ms_calls = [None] * size_of_ms_calls_list
    in_ms_calls_list_index = 0
    out_ms_calls_list_index = 0
    while in_ms_calls_list_index < size_of_ms_calls_list:
        line_split = (
               ms_calls_lines[in_ms_calls_list_index].split("\t"))
        if line_split[-1] == "\n":
            line_split.pop()
        # print(in_ms_calls_list_index, "line_split =", line_split)
        if len(line_split) == 9:
            ms_calls[out_ms_calls_list_index] = (
                            MsCalls(out_ms_calls_list_index,
                            *line_split))
            in_ms_calls_list_index += 1
            out_ms_calls_list_index += 1
        else:
            print(f"Error in line from file = {file_name}",
                  f"with index = {in_ms_calls_list_index}",
                  f"with value {line_split}",
                  f"wait for 9 parameters",
                  f"and got {len(line_split)}")
            size_of_ms_calls_list -= 1
            in_ms_calls_list_index += 1
            ms_calls.pop()
    return ms_calls



# main for ntk_calls part():
ntk_calls_folder = "D:\python\double_dno\ms_ntk_in_same_amount\station 3203"
ntk_calls_file_name = "3203_1_day_ntk.txt"
list_of_ntk_calls = read_ntk_calls(ntk_calls_folder, ntk_calls_file_name)
print("ntk_calls_list:")
for record in list_of_ntk_calls:
    print(record)
    

# main for ms_calls part():
ms_calls_folder = "D:\python\double_dno\ms_ntk_in_same_amount\station 3203"
ms_calls_file_name = "3203_1_day_ms.txt"
list_of_ms_calls = read_ms_calls(ms_calls_folder, ms_calls_file_name)
print("ms_calls_list:")
#===============================================================================
# for record in list_of_ms_calls:
#     print(record)
#===============================================================================

hash_calls = dict()
for record in list_of_ms_calls:
    hash_calls.update({record.hash: record})
print("len(hash_calls) =", len(hash_calls))
for record in list_of_ntk_calls:
    try:
        hash_calls.pop(record.hash)
        #print('good')
    except:
        print(record)
        pass
print("len(hash_calls) =", len(hash_calls))

for hash, call in hash_calls.items():
    print(call)
    
    