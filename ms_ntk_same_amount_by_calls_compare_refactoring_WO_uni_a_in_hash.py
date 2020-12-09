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
        if '380800' in self.uni_b[:6] or self.uni_b in ('38032121', '380321580'):
            self.hash = self.hash_create_with_a()
        else:
            self.hash = self.hash_create_wo_a()
        

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
    
    def hash_create_with_a(self):
        hash = ''  # len(self.uni_b) == 12 and 
        if str(self.uni_b)[:3] == '380':
            uni_b = self.uni_b[3:]
        else:
            uni_b = self.uni_b
            
        if str(self.uni_a)[:3] == '380':
            uni_a = str(self.uni_a)[3:]
        else:
            uni_a = '0'  # for 8800 and international A 
         
        
        hash = (str(self.switch_id) +
                uni_a + 
                uni_b +
                str(self.inc_tg) +
                str(self.bill_dtm).replace('.', '').replace(' ', '').replace(':', '') +
                str(self.duration))
        return hash
        
    
    def hash_create_wo_a(self):
        hash = ''  # len(self.uni_b) == 12 and 
        if str(self.uni_b)[:3] == '380':
            uni_b = self.uni_b[3:]
        else:
            uni_b = self.uni_b
            
        #=======================================================================
        # if str(self.uni_a)[:3] == '380':
        #     uni_a = str(self.uni_a)[3:]
        # else:
        #     uni_a = '0'  # for 8800 and international A 
        # 
        #=======================================================================
        
        hash = (str(self.switch_id) +
                #uni_a + 
                uni_b +
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
        if number_b[:2] == '10':
            self.number_b = number_b[2:]
        if '800' in self.number_b[:3] or self.number_b in ('032121', '0321580'):
            self.hash = self.hash_create_with_a()
        else:
            self.hash = self.hash_create_wo_a()
        
        # self.hash = self.hash_create()
        

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
    
    def hash_create_with_a(self):
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
        
        hash = (str(self.recipient_id) +
                str(self.number_a) + 
                number_b +
                str(self.inc_tg) +
                str(self.date_start).replace('.', '').replace(' ', '').replace(':', '') +
                str(self.duration))
        return hash
    
    def hash_create_wo_a(self):
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
        
        hash = (str(self.recipient_id) +
                # str(self.number_a) + 
                number_b +
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

#3203

#===============================================================================
# ntk_calls_folder = "D:\python\double_dno\ms_ntk_same_amount_by_calls_compare\ms_ntk_in_same_amount\station 3203"
# ntk_calls_file_name = "3203_1_day_ntk.txt"
#===============================================================================

#3200

#===============================================================================
# ntk_calls_folder = "D:\python\double_dno\ms_ntk_same_amount_by_calls_compare\ms_ntk_in_same_amount\station 3200"
# ntk_calls_file_name = "3200_1_day_ntk.txt"
#===============================================================================

# 3205

#===============================================================================
# ntk_calls_folder = "D:\python\double_dno\ms_ntk_same_amount_by_calls_compare\ms_ntk_in_same_amount\station 3205"
# ntk_calls_file_name = "3205_20_day_ntk.txt"
#===============================================================================

# 4462

ntk_calls_folder = "D:\python\double_dno\ms_ntk_same_amount_by_calls_compare\ms_ntk_in_same_amount\station 4462"
ntk_calls_file_name = "4462_20_day_ntk.txt"

list_of_ntk_calls = read_ntk_calls(ntk_calls_folder, ntk_calls_file_name)
print("ntk_calls_list:")

#===============================================================================
# for record in list_of_ntk_calls:
#     # print(record)
#     pass
#===============================================================================

# main for ms_calls part():

# 3203
#===============================================================================
# ms_calls_folder = "D:\python\double_dno\ms_ntk_same_amount_by_calls_compare\ms_ntk_in_same_amount\station 3203"
# ms_calls_file_name = "3203_1_day_ms.txt"
#===============================================================================

# 3200 we have error what we classify 0(sometimes 1)second duration length
#      with uni_a = 380322000000

#===============================================================================
# ms_calls_folder = "D:\python\double_dno\ms_ntk_same_amount_by_calls_compare\ms_ntk_in_same_amount\station 3200"
# ms_calls_file_name = "3200_1_day_ms.txt"
#===============================================================================

# 3205
# 764 , 3205 , 380443937659 , 38032112 , 03.09.2020 11:18:12 , 1902 , 5 , 3267 , 1 , 2

#===============================================================================
# ms_calls_folder = "D:\python\double_dno\ms_ntk_same_amount_by_calls_compare\ms_ntk_in_same_amount\station 3205"
# ms_calls_file_name = "3205_20_day_ms.txt"
#===============================================================================

#4462

ms_calls_folder = "D:\python\double_dno\ms_ntk_same_amount_by_calls_compare\ms_ntk_in_same_amount\station 4462"
ms_calls_file_name = "4462_20_day_ms.txt"


list_of_ms_calls = read_ms_calls(ms_calls_folder, ms_calls_file_name)
print("ms_calls_list:")

#===============================================================================
# for record in list_of_ms_calls:
#     if record.uni_a == '380987009285':
#             print('ms', record.hash)
#===============================================================================

#===============================================================================
#             
# for record in list_of_ntk_calls:
#     if record.number_a == '987009285':
#             print('ntk', record.hash)
#===============================================================================

hash_calls = dict()
hash_already_exist_counter = 0
error_hash_already_exist = open(path.join(ntk_calls_folder,
        'error_hash_already_exist.txt'),'w')
for record in list_of_ms_calls:
    if record.hash in hash_calls:
        print('double:', record, file=error_hash_already_exist)
        hash_already_exist_counter += 1
    else:
        hash_calls.update({record.hash: record})
error_hash_already_exist.close()
print('hash already exist error count =', hash_already_exist_counter)
print("len(hash_calls) =", len(hash_calls))
error_during_finding_this_hash_in_dict = open(path.join(ntk_calls_folder,
        'error_during_finding_this_hash_in_dict.txt'),'w')
except_counter = 0
for call in list_of_ntk_calls:
    try:
        hash_calls.pop(call.hash)
        # print('good')
    except:
        # if record.number_a == '987009285':
        # print('except:', call)
        print('except:', call, file=error_during_finding_this_hash_in_dict)
        except_counter += 1
error_during_finding_this_hash_in_dict.close()
print('except_counter =', except_counter)
print("len(hash_calls) =", len(hash_calls))

calls_what_left_if_dict_after_poping = open(path.join(ntk_calls_folder,
        'calls_what_left_if_dict_after_poping.txt'),'w')
for hash, call in hash_calls.items():
    if call.duration != '0':
        print(call, file=calls_what_left_if_dict_after_poping)
    pass
calls_what_left_if_dict_after_poping.close()
    
    