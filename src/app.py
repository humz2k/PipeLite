import json
from flask import Flask,request,jsonify,send_file
from remote_pipesteps import *
from multiprocessing import Process, Lock
from multiprocessing.sharedctypes import Value,Array
from ctypes import c_char_p
import time

max_queue_size = 5
app = Flask(__name__)

recently_used = []

my_find = DataFinder()

#outs = {}
def do_queue(queue,cmds):
    remote = Remote()
    count = 0
    while True:
        count += 1
        if count > 1200:
            count = 0
            remote.data_finder.reset()
        print(queue[:])
        if queue[:].count(-1) < max_queue_size:
            current_job_no = queue[0]
            i = 0
            while i < len(queue[:])-1:
                queue[i] = queue[i+1]
                i += 1
            queue[max_queue_size-1] = -1
            #job = outs[current_job_no]

            inp = cmds[current_job_no].value.decode('utf-8').split(";")
            command = inp[0]
            args = inp[1:]

            print("JOB",current_job_no,command)
            if command == "image_math":
                date = args[0]
                user = args[1]
                exposures = [int(i) for i in args[2].split(",")]
                filters = args[3].split(",")
                limit = int(args[4])
                out = "FINISHED:" + ",".join(remote.image_math(date,user,exposures,filters,limit))
                print(out)
                cmds[current_job_no].value = str.encode("FINISHED")
                if count > 900:
                    count = 900

        time.sleep(1)

@app.route('/', methods=['GET'])
def index():
    command = request.args.get('command')

    if command == "ping":
        return jsonify({'alive': '1'})

    if command == "check":
        job_no = int(request.args.get('job'))
        val = 0
        if cmds[job_no].value.decode("utf-8") == "FINISHED":
            val = 1
        return jsonify({'finished': str(val)})

    if command == "download":
        file = request.args.get('file')
        if file in os.listdir() and '.fit' in file:
            return send_file(file, attachment_filename=file)
        return jsonify({'failed': "oh no"})

    if command == "image_math":
        date = request.args.get('date')
        user = request.args.get('user')
        exposures = request.args.get('exposures')
        filters = request.args.get('filters')
        limit = request.args.get('limit')
        count = 0
        while count in recently_used:
            count += 1
        if count > max_queue_size-1:
            return jsonify({'job': 'fail'})
        recently_used.append(count)
        if len(recently_used) > max_queue_size-1:
            recently_used.pop(0)
        #queue[:].append("5")
        #outs[count] = ["image_math",date,user,exposures,filters,limit]
        for i in range(len(queue)):
            if queue[i] == -1:
                queue[i] = count
                out_command = "image_math" + ";" + date+ ";" + user + ";" + exposures + ";" + filters + ";" + limit

                cmds[count].value = str.encode(out_command)

                files = my_find.list_files(date,user,masks = ["RAW","bin1H"] + filters.split(","),limit=int(limit))
                temp_files = []
                for i in files:
                    if "bin1H" in i:
                        temp_files.append(i.replace("_bin1H_","_bin1_"))
                    elif "bin1L" in i:
                        temp_files.append(i.replace("_bin1L_","_bin1_"))
                    else:
                        temp_files.append(i)
                files = temp_files
                files = [i.split("RAW")[0] + "HDR" + i.split("RAW")[1] for i in files]
                for idx,i in enumerate(files):
                    temp = i.split("_")
                    temp[-2] = str(idx)
                    files[idx] = "_".join(temp)
                files = ",".join(files)
                return jsonify({'job': str(count),'files': files})
        return jsonify({'job': 'fail'})
    return jsonify({'What': 'Do You Want'})

if __name__ == '__main__':
    queue = Array("i",[-1]*max_queue_size)
    cmds = [Array("c",200) for i in range(max_queue_size)]
    cmds[0].value = b'0'
    p = Process(target=do_queue, args=(queue,cmds,))
    p.start()
    app.run(debug=True, use_reloader=False)
    p.join()
