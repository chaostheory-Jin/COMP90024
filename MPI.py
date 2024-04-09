from mpi4py import MPI
import json
import time
import re
def create_index(filename):
    index = []  # 存储每行的起始偏移量
    offset = 0
    with open(filename, 'r') as file:
        while line := file.readline():
            index.append(offset)
            offset += len(line.encode('utf-8'))  # 更新偏移量
    return index

def safe_skip_lines(file, num_lines):
    """安全地跳过文件中的num_lines行"""
    for _ in range(num_lines):
        try:
            next(file)
        except StopIteration:
            # 已到达文件末尾，直接返回
            return

def read_lines_range(filename, start_line, end_line):
    """从文件中读取指定范围内的行，每行应为一个独立的JSON对象"""
    data = []  # 用于存储读取的数据
    with open(filename, 'r') as file:
        for current_line, line in enumerate(file, start=1):
            if current_line >= start_line:
                if current_line > end_line:
                    break  # 如果当前行号超过结束行，停止读取
                json_obj = file.readline()  # 假设每行是一个有效的JSON字符串
                data.append(json_obj)
    return data

def read_lines_with_index(filename, index, start_line, end_line):
    data = []
    with open(filename, 'r') as file:
        file.seek(index[start_line - 1])  # 跳到起始行
        for _ in range(start_line, end_line + 1):
            line = file.readline()
            if not line:
                break  # 如果文件结束，则停止
            json_obj = file.readline() 
            data.append(json_obj)
    return data

def read_from_line(filename, start_line):
    """从指定行开始读取JSON对象"""
    data = []  # 用于存储读取的数据
    with open(filename, 'r') as file:
        for current_line, line in enumerate(file, start=1):
            if current_line >= start_line:
                json_obj = json.loads(line)  # 假设每行是一个有效的JSON字符串
                data.append(json_obj)
    return data

# 初始化MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

filename = "twitter-50mb.json"  # 假设文件是JSON Lines格式
#filename = "twitter-1mb.json"
# 确定文件的总行数（简化处理：假设这一信息已知或在进程0中预先计算并分发）
index = create_index(filename)
start_time = time.time()

with open(filename, 'r') as data:
    data_ = json.load(data)
row = data.get("rows")
length = len(row)
print(f"rows len:{length}")
# 读取文件的第一行以获取总行数
with open(filename, 'r') as file:
    first_line = file.readline()
    # total_rows_info = json.loads(first_line)
    total_rows_match = re.search(r'"total_rows":(\d+)', first_line)
    # 将匹配的结果转换为整数
    if total_rows_match:
        total_rows = int(total_rows_match.group(1))
    else:
        total_rows = None

    #total_rows = first_line.get("total_rows", 0)

total_rows = total_rows
total_rows = 50001
# 计算每个进程的行数分配
rows_per_process = total_rows // size
extra_rows = total_rows % size

# 确定每个进程的起始和结束行号
start_row = rank * rows_per_process + min(rank, extra_rows)
end_row = start_row + rows_per_process - 1
if rank < extra_rows:
    end_row += 1

# 打开文件并跳到起始行
data_part = []
#with open(filename, 'r') as file:
    # for i in range(start_row):
    #     next(file)  # 跳过不属于当前进程处理的行
    # safe_skip_lines(file, start_row)
#    for i in range(start_row, end_row + 1):
#        line = file.readline()
#        if not line:
#            break  # 文件可能比计算的行数短
#        data_part.append(line)
data_part = read_lines_with_index(filename,index, start_row, end_row + 1)
# 示例：每个进程打印处理的行数
print(f"Process {rank} processed {len(data_part)} lines.startrows:{start_row},endrows:{end_row}")

# 此处，每个进程可以独立处理它读取的数据部分，或者使用MPI操作进行数据交换或汇总
end_time = time.time()

# 输出总行数和读取时间
#print("Total rows:",total_rows)
print("Time taken to read the first line: seconds", end_time - start_time)
