import ftplib
import pandas as pd
from io import StringIO
from flask import request, current_app
import json

def connect_ftp():
    ftp_host = 'ftp.bom.gov.au'
    ftp = ftplib.FTP(ftp_host)
    ftp.login()
    return ftp

def change_directory(ftp, state, stationname):
    path = f'/anon/gen/clim_data/IDCKWCDEA0/tables/{state}/{stationname}/'
    ftp.cwd(path)

def download_and_process_file_bi(ftp, filename):
    import io
    bio = io.BytesIO()
    ftp.retrbinary('RETR ' + filename, bio.write)
    bio.seek(0)
    
    lines = bio.getvalue().split(b'\r\n')
    
    del lines[0:10]
    del lines[2]
    
    lines[0] = lines[0].strip() + lines[1]
    del lines[1]
    
    processed_data = b'\n'.join(lines).decode('ISO-8859-1')
    
    processed_data_io = StringIO(processed_data)
    
    df = pd.read_csv(processed_data_io)
    print(df)


def download_and_process_file(ftp, filename, stationname, date):
    sio = StringIO()
    ftp.retrbinary('RETR ' + filename, lambda data: sio.write(data.decode('ISO-8859-1')))
    sio.seek(0)
    lines = sio.readlines()
    del lines[0:10]
    del lines[2]
    columns_line_11 = lines[0].strip().split(',')
    columns_line_12 = lines[1].strip().split(',')

    # 合并第11行和第12行对应列的字符串
    merged_line = [a + b for a, b in zip(columns_line_11, columns_line_12)]
    lines[0] = ','.join(merged_line) + '\n'  # 重新组合成一行，并添加换行符
    del lines[1]
    del lines[-1]
    processed_data = StringIO(''.join(lines))
    df = pd.read_csv(processed_data)

    # df.rename(columns={'Unnamed: 0': 'location', 'Unnamed: 1': 'date'}, inplace=True)
    df = df.iloc[:, [0, 1, 3, 5, 6]]
    df.columns = ['location', 'date', 'rain', 'maxTemp', 'minTemp']
    # df.columns = ['location', 'date', 'rain', 'maxTemp', 'minTemp']
    # df = df.drop(df.index[-1])
    # new_date = df['date'].str.split('\/', expand=True)
    # df["day"] = new_date[0].astype(int)
    # df["month"] = new_date[1].astype(int)
    # df["year"] = new_date[2].astype(int)
    # output_filename = f"{stationname}-{date}.csv"
    # df.to_csv(output_filename)
    # print(f"File saved as {output_filename}")
    df = df.fillna(0)
    df.replace('', 0, inplace=True)
    df.replace(' ', 0, inplace=True)
    df.replace('  ', 0, inplace=True) 
    
    json_data = df.to_dict(orient='records')
    # json_data = json.loads(json_data)
    for item in json_data:
        date_parts = item['date'].split('/')
        item['day'] = date_parts[0]
        item['month'] = date_parts[1]
        item['year'] = date_parts[2]
        # del item['date']
    return json_data


# def main(state, stationname, date):
#     ftp = connect_ftp()
#     try:
#         change_directory(ftp, state, stationname)
#         filename = f"{stationname}-{date}.csv"
#         download_and_process_file(ftp, filename, stationname, date)
#     finally:
#         ftp.quit()


# state = 'qld'
# stationname = 'warwick'
# date = '202404'
# main(state, stationname, date)

def main():
    try:
        state = request.headers['X-Fission-Params-State']
        date = request.headers['X-Fission-Params-Date']
        stationname = request.headers['X-Fission-Params-Station']
    except KeyError:
         state = None
         date = None
         stationname = None

    # current_app.logger.info(f'Received request: ${request.headers}')
    # state = request.args.get('state', 'qld')
    # date = request.args.get('date', '202404')
    # stationname = request.args.get('stationname', 'warwick')
    
    ftp = connect_ftp()
    try:
        change_directory(ftp, state, stationname)
        filename = f"{stationname}-{date}.csv"
        json_data = download_and_process_file(ftp, filename, stationname, date)
    

    finally:
        ftp.quit()
    # json_data = json.dumps(json_data)    
    res = {}
    res['data'] = json_data
    res = json.dumps(res)
    return res