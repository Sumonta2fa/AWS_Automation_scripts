from datetime import datetime, timedelta

def bulk_date(d1, d2):
    delta = d2 - d1 # timedelta
    data = []
    for i in range(delta.days + 1):
        date = (d1 + timedelta(i))
        print(date.strftime('%Y%m%d'))
        data.append(date.strftime('%Y%m%d'))
    return data

def format_date(partision_date, date_op, prefix_path):
    #op format
    #OR (dt='2018-09-19-08-00' AND key LIKE '201802%/AU/%.avro')

    f = open('glacier_restore_date_format_output.txt', 'a')
    for data in date_op:
        string = 'OR (dt=\'{}\' AND key LIKE \'{}{}\') \n'.format(partision_date, data, prefix_path)
        f.write(string)
    f.close()

def random_filter_file(file, partision_date, prefix_path):
    d_list = []
    f = open(file, 'r')
    for line in f.readlines():
        line = line.strip('\n')
        #     print(repr(line))
        try:
            # filter date format 23/03/2018
            date_time_obj = datetime.strptime(line, '%d/%m/%Y')
        except:
            # filter date format 2018/03/23
            date_time_obj = datetime.strptime(line, '%d-%m-%Y')
        date_op = date_time_obj.date().strftime('%Y%m%d')
        print('I/O:', line, date_op, len(date_op))
        d_list.append(date_op)
    return d_list


def prefix_op(zone, d_list):
    f = open('glacier_restore_date_format_output.txt', 'a')
    for data in d_list:
        string = '"{}{}",\n'.format(data, zone)
        f.write(string)
    f.close()

if __name__ == '__main__':
    partision_date = '2018-09-19-08-00'
    prefix_path = '/AU/%.avro'
    zone = '/AU/'
    N = 120

    #Clean the output file
    open('glacier_restore_date_format_output.txt', 'w').close()
    #calculate transition date from today
    date_N_days_ago = datetime.now() - timedelta(days=N)
    date_N_days_ago = "120 days ago date: "+str(date_N_days_ago)
    f = open('glacier_restore_date_format_output.txt', 'w')
    f.writelines(date_N_days_ago)
    f.close()
    #
    # ## If random date file given
    # # collect date from file
    # file = 'D:\Scripts\PY\Jupyter-data\\files\s3_restore_date.txt'
    # d_list = random_filter_file(file, partision_date, prefix_path)
    # format_date(partision_date, d_list, prefix_path)
    # prefix_op(zone, d_list)


    ##if bulk date mention

    d1 = datetime(2018, 3, 24)  # start date
    d2 = datetime(2018, 9, 24)  # end date
    date_op = bulk_date(d1, d2)
    format_date(partision_date, date_op, prefix_path)
    prefix_op(zone, date_op)