import requests, json, time, os, csv
from datetime import date as dt
from datetime import timedelta

old_date = dt(2011, 1, 1)
end_date = dt.today()
new_date = end_date - timedelta(319)
script = int(input('BSE Script Number: '))

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

# print(y['Table'][count]['CATEGORYNAME'].split('/')[0].rstrip())
# print('https://www.bseindia.com/xml-data/corpfiling/AttachLive/%s' %y['Table'][count]['DT_TM'][:10])

def full_rec_download(script, start_date, end_date):
    url = 'https://api.bseindia.com/BseIndiaAPI/api/AnnGetData/w?strCat=-1&strPrevDate={0}&strScrip={1}&strSearch=P&strToDate={2}&strType=C'.format(dt.strftime(start_date, '%Y%m%d'), script, dt.strftime(end_date, '%Y%m%d'))
    result = requests.get(url, headers=headers)
    f = result.content.decode()
    y = json.loads(f)
    print('API Response Received')
    data_file = open('full_record.csv', 'w')
    csv_writer = csv.writer(data_file)
    name = y['Table'][0]['SLONGNAME']
    for count in range(len(y['Table'])):
        download_data = y['Table'][count]
        if count == 0:
            header = download_data.keys()
            csv_writer.writerow(header)
        csv_writer.writerow(download_data.values())
    print(f"Full Record Downloaded for {name}!")

def live_download_NEW(script, start_date, end_date, hist_or_live):
    url = 'https://api.bseindia.com/BseIndiaAPI/api/AnnGetData/w?strCat=-1&strPrevDate={0}&strScrip={1}&strSearch=P&strToDate={2}&strType=C'.format(dt.strftime(start_date, '%Y%m%d'), script, dt.strftime(end_date, '%Y%m%d'))
    result = requests.get(url, headers=headers)
    f = result.content.decode()
    y = json.loads(f)
    print('API Response Received')
    data_file = open('download_record.csv', 'a')
    csv_writer = csv.writer(data_file)
    for count in range(len(y['Table'])): 
        if y['Table'][count]['CATEGORYNAME'] == 'Result':
            to_download = ('https://www.bseindia.com/xml-data/corpfiling/Attach{0}/{1}'.format(hist_or_live, y['Table'][count]['ATTACHMENTNAME']))
            download_data = y['Table'][count]
            name = y['Table'][0]['SLONGNAME']
            cat = y['Table'][count]['CATEGORYNAME'].split('/')[0].rstrip()
            dis_date = str(y['Table'][count]['DT_TM'][:10])
            dis_time_hour = y['Table'][count]['DT_TM'].split('T')[1].split(':')[0]
            dis_time_minute = y['Table'][count]['DT_TM'].split('T')[1].split(':')[1]
            if y['Table'][count]['Fld_Attachsize'] is None:
                global stated_size
                stated_size = 0
            else: 
                stated_size = y['Table'][count]['Fld_Attachsize']
            if not os.path.exists(f'{cat}'):
                os.makedirs(f'{cat}')
            print(f'Downloading: {cat} {dis_date}')
            download = requests.get(to_download, headers=headers)
            filename = f'{cat}\{name} - {cat} - {dis_date} {dis_time_hour}{dis_time_minute}.pdf'
            open(filename, 'wb').write(download.content)
            act_size = os.stat(filename).st_size
            if act_size >= stated_size:
                print(f'Download Successful! Stated Size: {stated_size} Actual Size: {act_size}')
            else:
                print(f'Download not Successful :( Stated Size: {stated_size} Actual Size: {act_size}')
            if count == 0:
                header = download_data.keys()
                csv_writer.writerow(header)
            csv_writer.writerow(download_data.values())
            time.sleep(2)

def live_download_OLD(script, start_date, end_date):
    url = 'https://api.bseindia.com/BseIndiaAPI/api/AnnGetData/w?strCat=-1&strPrevDate={0}&strScrip={1}&strSearch=P&strToDate={2}&strType=C'.format(dt.strftime(start_date, '%Y%m%d'), script, dt.strftime(end_date, '%Y%m%d'))
    result = requests.get(url, headers=headers)
    f = result.content.decode()
    y = json.loads(f)
    print('API Response Received')
    data_file = open('download_record.csv', 'a')
    csv_writer = csv.writer(data_file)
    for count in range(len(y['Table'])):
        if y['Table'][count]['CATEGORYNAME'] == 'Result':
            year = str(y['Table'][count]['DT_TM'][:4])
            month = str(int(y['Table'][count]['DT_TM'][5:7]))
            to_download = ('https://www.bseindia.com/xml-data/corpfiling/CorpAttachment/{0}/{1}/{2}'.format(year, month, y['Table'][count]['ATTACHMENTNAME']))
            download_data = y['Table'][count]
            name = y['Table'][0]['SLONGNAME']
            dis_date = str(y['Table'][count]['DT_TM'][:10])
            dis_time_hour = y['Table'][count]['DT_TM'].split('T')[1].split(':')[0]
            dis_time_minute = y['Table'][count]['DT_TM'].split('T')[1].split(':')[1]
            if y['Table'][count]['CATEGORYNAME'] is None:
                global cat
                cat = 'NO CAT'
            else:
                cat = y['Table'][count]['CATEGORYNAME'].split('/')[0].rstrip()
            if y['Table'][count]['Fld_Attachsize'] is None:
                global stated_size
                stated_size = 0
            else: 
                stated_size = y['Table'][count]['Fld_Attachsize']
            if not os.path.exists('{0}'.format(cat)):
                os.makedirs('{0}'.format(cat))
            print('Downloading: {0} {1}'.format(cat, dis_date))
            download = requests.get(to_download, headers=headers)
            filename = f'{cat}\{name} - {cat} - {dis_date} {dis_time_hour}{dis_time_minute}.pdf'
            open(filename, 'wb').write(download.content)
            act_size = os.stat(filename.format(cat, dis_date)).st_size
            if act_size >= stated_size:
                print('Download Successful! Stated Size: {0} Actual Size: {1}'.format(stated_size, act_size))
            else:
                print('Download not Successful :( Stated Size: {0} Actual Size: {1}'.format(stated_size, act_size))
            if count == 0:
                header = download_data.keys()
                csv_writer.writerow(header)
            csv_writer.writerow(download_data.values())
            time.sleep(2)
            

full_rec_download(script = script, start_date=old_date, end_date=end_date)
live_download_NEW(script=script, start_date=new_date, end_date=end_date, hist_or_live='Live')
live_download_NEW(script=script, start_date=dt(2018, 7, 19), end_date=new_date, hist_or_live='His')
live_download_OLD(script=script, start_date=dt(2011, 1, 1), end_date=dt(2018, 7, 19))