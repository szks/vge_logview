#!/usr/bin/env python3

import re
import sys
import datetime
import matplotlib.pyplot as plt


re_job_name = re.compile('(.*)_\d{8}_\d{4}_\d{6}\.sh\.\d+')


def get_job_name(s):
    return re_job_name.match(s).group(1)


def color_mapper(id):
    colormap = [ "r", "g", "b", "y", "m", "k" ]
    c = id % len(colormap)
    return colormap[c]


def get_timestamp(s):
    dt = datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S.%f")
    return dt.timestamp()


if __name__ == '__main__':

    if not len(sys.argv) in [2, 3]:
        print('usage: %s joblist.csv [output.pdf]' % sys.argv[0])
        sys.exit(1)

    input_csv = sys.argv[1]
    output_pdf = None
    if len(sys.argv) == 3: output_pdf = sys.argv[2]

    f = open(input_csv, 'r')
    f.readline()  # skip header

    job_list = []
    start = datetime.datetime.now().timestamp()

    for line in f:
        (jobid, status, sendvgetime, bulkjob_id,
        finish_time,start_time,worker,return_code,
        filename,elapsed_time,genomon_pid,max_task,
        command_id,unique_jobid,sendtoworker) = line.rstrip('\n').split(',')

        start = min(start, get_timestamp(sendvgetime))
        s = get_timestamp(start_time)
        f = get_timestamp(finish_time)
        #print(jobid, bulkjob_id, genomon_pid, unique_jobid)
        #print(unique_jobid, filename)
        #print(jobid, unique_jobid, bulkjob_id, filename, max_task)

        job_list.append((int(worker), s, f, int(unique_jobid)))

        if bulkjob_id == '0':
            unique_job = get_job_name(filename)
            if max_task != '0':
                unique_job += ' (x' + max_task + ')'
            print (unique_jobid, unique_job)
    
    #print(start)
    #print(job_list)

    for node, s, f, id in job_list:
        plt.hlines(node, s-start, f-start, colors=color_mapper(id), lw=5)
        plt.text(s-start, node+0.25, str(id), fontsize=9)

    plt.xlabel('Time (sec)')
    plt.ylabel('Nodes')

    if output_pdf:
        import matplotlib
        from matplotlib.backends.backend_pdf import PdfPages
        matplotlib.rcParams['pdf.fonttype'] = 42
        matplotlib.rcParams['savefig.dpi'] = 300
        pdf = PdfPages(output_pdf)
        pdf.savefig()
        pdf.close()
    else:
        plt.show()

