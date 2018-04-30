import csv
import os
import re
import traceback
import math

def parsefloat(string):
    return float(''.join([x for x in string if (x.isdigit() or x == '.')]))

def parse_raw_data(path, file_name, flag, report_file, writer):
    try:
        print path
        # print os.path.dirname(__file__)

        # claaify report title
        title = file_name.split('-')
        title[2] = parsefloat(title[2])
        title.append(flag)
        
        f = open(path, 'r')
        data = f.read()
        data = data.lower()
        f.close

        # analyze tf benchmark report
        loss = []
        train_rate = 0
        for i in range(11): loss.append(None)
        step_count = 0
        data = data.split('\n')
        for item in data:
            item = re.split(r'\t+', item)
            if item[0] == 'step':
                step_count = 11
                continue
            if step_count > 0:
                if math.isnan(float(item[2])): loss[11 - step_count] = None
                else: loss[11 - step_count] = float(item[2])
                step_count -= 1

            if re.match('total images/sec', item[0]):
                locate = re.search('[0-9]*\.[0-9]*', item[0]).span()
                train_rate = parsefloat(item[0])


        print 'Sampling report-------------%s' % file_name
        print 'title: %s' % title
        print 'loss: '
        print loss
        print 'train_rate: %s' % train_rate
        # print ''
        # output to report file
        report = []
        report.append(title[1])
        report.append(title[0])
        report.append(title[2])
        report.append(title[3])
        report.append(train_rate)
        for step in loss:
            report.append(step)
        print report
        print len(report)
        writer.writerow(report)
        print ''

    except Exception as e:
        print Exception
        traceback.print_exc()
