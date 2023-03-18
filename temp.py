import glob
import re
import json
import datetime
from typing import List, Any, Union

#devices_dir = '/mnt/415CFF12578113C9/CODE/2019-01-01-pi1w'
devices_dir = '/sys/bus/w1/devices/'

crc = re.compile(r"crc=\w{2} (\w+)")
t_C = re.compile(r"t=(-*\d+)")
sn_expr = re.compile(r'/(\w{2}-\w*)/w1_slave')

def read_temperature(filename="onewire.json", msg=1, jsonout=False):
    sn  = []
    ts = datetime.datetime.now()
    date_str = ts.strftime("%Y.%m.%d-%H:%M:%S")
    data_num: List[List[Union[float, Any]]] = []
    out =  {"timestamp": date_str}
    ser_temp =[]
    for ii in glob.glob(devices_dir+'/*/w1_slave'):
        fid = open(ii,'r')
        raw = fid.readlines()
        fid.close()

        if msg>1:
            print(raw)

        if len(raw) == 2:
            if "YES" in crc.findall(raw[0]):
                temp = t_C.findall(raw[1])
                sn   = sn_expr.findall(ii)

                if len(temp) == 1:
                    try:
                        temp_c = float(temp[0])/1000
                        ser_temp.append( {"sn": sn[0], "temp": temp_c})
                        data_num.append([sn[0], temp_c])
                    except Exception as identifier:
                        print(identifier)


    out['data'] = ser_temp
    json_string = json.dumps(out)

    # fid = open(filename, "w")
    # fid.write("{0}".format(json_string))
    # fid.close()

    if jsonout:
        return json_string
    else:
        return data_num


if __name__ == "__main__":
     print(f"{read_temperature()}")
