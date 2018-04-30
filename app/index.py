import sys
sys.path.insert(0, './service')

import os
import traceback
import csvHelper
import csv
import time

count = 0

# build report csv file
now = time.strftime('%Y-%m-%d_%H-%M', time.localtime())
report_file = 'data/benchmark-collection_%s.csv' % now 

report = open(report_file , 'w')
writer = csv.writer(report)
para = ['algo', 'process-unit', 'batch', 'flag', 'train_rate', 'step_1', 'step_10', 'step_20', 'step_30', 'step_40', 'step_50', 'step_60', 'step_70', 'step_80', 'step_90', 'step_100']
writer.writerow(para)

for dirname, dirnames, filenames in os.walk('raw-data'):
    try:
        # print dirname
        # print dirnames
        # print filenames
        parse_dir = dirname.split('/')[1].split('-')
        if len(parse_dir) == 1: parse_dir.append('inference')

        if filenames and count < 1:
            # count += 1
            for a_file in filenames:
                raw_path = '%s/%s' % (dirname, a_file)
                csvHelper.parse_raw_data(raw_path, a_file, parse_dir[1], report_file, writer)
        # print dirnames
    except Exception as e:
        print Exception
        traceback.print_exc()

report.close()