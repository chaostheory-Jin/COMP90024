from mpi4py import MPI
import json
import time
import re

def safe_skip_lines(file, num_lines):
    """安全地跳过文件中的num_lines行"""
    for _ in range(num_lines):
        try:
            next(file)
        except StopIteration:
            # 已到达文件末尾，直接返回
            return

# 初始化MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

filename = "twitter-50mb.json"  # 假设文件是JSON Lines格式

# 确定文件的总行数（简化处理：假设这一信息已知或在进程0中预先计算并分发）
start_time = time.time()

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
with open(filename, 'r') as file:
    # for i in range(start_row):
    #     next(file)  # 跳过不属于当前进程处理的行
    #safe_skip_lines(file, start_row)
    #for i in range(start_row, end_row + 1):
        # line = file.readline()
        # if not line:
        #     break  # 文件可能比计算的行数短
        # data_part.append(line)
    line = file.readline()
    line_num = 1
    sentiment_sum = 0
    while line:
        if((line_num%size)==rank):
            line = line[0:-2]
            try:
                #re.search(r'"total_rows":(\d+)', first_line)
                json_txt = json.loads(line)
                try:
                    sentiment = json_txt['doc']['data'].get('sentiment')
                    sentiment_sum += sentiment
                except:
                    pass
                
                data_part.append(json_txt)
            except:
                pass
        line = file.readline()
        line_num += 1
# print(data_part[0]['doc']['data'].get('sentiment'))
print(f"Process {rank} processed {len(data_part)} lines,{sentiment_sum}.",rank, len(data_part),sentiment_sum)

# 此处，每个进程可以独立处理它读取的数据部分，或者使用MPI操作进行数据交换或汇总
end_time = time.time()

# 输出总行数和读取时间
# print("Total rows:",total_rows)
print("Time taken to read the first line: seconds", end_time - start_time)

