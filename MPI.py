from mpi4py import MPI
import json
import time
import re
from datetime import datetime

def gather_senti_by_sum(dict_distri):
    combined_dict = {}
    for d in dict_distri:
        for key, value in d.items():
            if key in combined_dict:
                combined_dict[key] += value
            else:
                combined_dict[key] = value
    return combined_dict

def extract_date_and_hour(datetime_str):
    dt = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    date = dt.date()
    hour = dt.hour
    return date, hour

def safe_skip_lines(file, num_lines):
    for _ in range(num_lines):
        try:
            next(file)
        except StopIteration:
            return

# init
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

filename = "twitter-50mb.json"  # 假设文件是JSON Lines格式

start_time = time.time()

with open(filename, 'r') as file:
    first_line = file.readline()
    total_rows_match = re.search(r'"total_rows":(\d+)', first_line)
    if total_rows_match:
        total_rows = int(total_rows_match.group(1))
    else:
        total_rows = None

total_rows = total_rows

data_part = []
with open(filename, 'r') as file:
    hour_list = []
    day_list = []
    line = file.readline()
    line_num = 1
    tweet_count_byhour = {}
    tweet_count_byday = {}
    sentiments_sum = {}
    sentiments_sum_byday = {}
    while line:
        if((line_num%size)==rank):
            line = line[0:-2]#og file not a standardized json object
            try:
                #re.search(r'"total_rows":(\d+)', first_line)
                json_txt = json.loads(line)
                try:
                    # sentiment_sum += sentiment
                    date, hour = extract_date_and_hour(json_txt['doc']['data'].get('created_at'))
                    if date not in day_list:
                        day_list.append(date)
                        tweet_count_byday[str(date)] = 1
                        sentiments_sum_byday[str(date)] = 0.0
                    else:
                        # sentiments_sum_byday[str(date)] += float(sentiment)
                        tweet_count_byday[str(date)] += 1
                    if [date, hour] not in hour_list:
                        hour_list.append([date, hour])
                        sentiments_sum[str(date)+','+str(hour)] = 0.0
                        tweet_count_byhour[str(date)+','+str(hour)] = 1
                    else: 
                        # sentiments_sum[str(date)+","+str(hour)] += float(sentiment)
                        tweet_count_byhour[str(date)+','+str(hour)] += 1
                except:
                    pass
                try:
                    sentiment = json_txt['doc']['data'].get('sentiment')
                    sentiments_sum_byday[str(date)] += float(sentiment)
                    sentiments_sum[str(date)+","+str(hour)] += float(sentiment)
                except:
                    pass
                # data_part.append(json_txt)
            except:
                pass
        line = file.readline()
        line_num += 1
# print(data_part[0]['doc']['data'].get('sentiment'))
#print("Process {rank} processed {len(data_part)} lines.",rank, len(data_part))

all_dicts = comm.gather(sentiments_sum, root=0)
all_dicts_day = comm.gather(sentiments_sum_byday, root=0)
all_tweet_day = comm.gather(tweet_count_byday, root=0)
all_tweet_hour = comm.gather(tweet_count_byhour, root=0)

if rank == 0:
    # combined_dict = {}
    # for d in all_dicts:
    #     for key, value in d.items():
    #         if key in combined_dict:
    #             combined_dict[key] += value  # 如果键已存在，累加值
    #         else:
    #             combined_dict[key] = value  # 否则，添加键值对
    combined_dict = gather_senti_by_sum(all_dicts)
    combined_dict_day = gather_senti_by_sum(all_dicts_day)
    combined_tweet_hour = gather_senti_by_sum(all_tweet_hour)
    combined_tweet_day = gather_senti_by_sum(all_tweet_day )
    
    max_date, max_value = max(combined_dict.items(), key=lambda item: item[1])
    max_date_day, max_value_day = max(combined_dict_day.items(), key=lambda item: item[1])
    max_date_tweet, max_value_tweet = max(combined_tweet_day.items(), key=lambda item: item[1])
    max_date_tweet_hour, max_value_tweet_hour = max(combined_tweet_hour.items(), key=lambda item: item[1])
    
    print("most happiest hour:", max_date, "sentiment scores:",max_value,"amoung",len(combined_dict),"hours")
    print("most happiest day:", max_date_day, "sentiment scores:",max_value_day,"amoung",len(combined_dict_day),"days")
    print("most active hour:", max_date_tweet_hour, "tweets num:",max_value_tweet_hour, "amoung",len(combined_tweet_hour),"hours")
    print("most active day:", max_date_tweet, "tweets num:",max_value_tweet,"amoung",len(combined_tweet_day),"days")
    
end_time = time.time()

# 输出总行数和读取时间
# print("Total rows:",total_rows)
#print("Time taken to read the first line: seconds", end_time - start_time)
