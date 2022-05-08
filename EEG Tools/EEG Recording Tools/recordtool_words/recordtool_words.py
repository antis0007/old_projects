import numpy as np
import pandas as pd
import os
from os.path import dirname
from pylsl import StreamInlet, resolve_byprop
from sklearn.linear_model import LinearRegression
from time import time, sleep, strftime, gmtime
import muselsl
LSL_EEG_CHUNK = 12
LSL_SCAN_TIMEOUT = 5
LSL_BUFFER = 360

autovar = 0 #This variable is used for adding a number at the end
#record code modified from muse-lsl-master
# Records a fixed duration of EEG data from an LSL stream into a CSV file
def record_auto(duration, filename, autovar, newdir, dejitter=False, data_source="EEG"):
    chunk_length = LSL_EEG_CHUNK
    if data_source == "PPG":
        chunk_length = LSL_PPG_CHUNK
    if data_source == "ACC":
        chunk_length = LSL_ACC_CHUNK
    if data_source == "GYRO":
        chunk_length = LSL_GYRO_CHUNK

    if not filename:
        filename = os.path.join(os.getcwd(
        ), "%s_recording_%s.csv" % (data_source, strftime('%Y-%m-%d-%H.%M.%S', gmtime())))

    print("Looking for a %s stream..." % (data_source))
    streams = resolve_byprop('type', data_source, timeout=LSL_SCAN_TIMEOUT)

    if len(streams) == 0:
        print("Can't find %s stream." % (data_source))
        return

    print("Started acquiring data.")
    inlet = StreamInlet(streams[0], max_chunklen=chunk_length)
    # eeg_time_correction = inlet.time_correction()

    #print("Looking for a Markers stream...")
    #marker_streams = resolve_byprop(
        #'name', 'Markers', timeout=LSL_SCAN_TIMEOUT)

    #if marker_streams:
        #inlet_marker = StreamInlet(marker_streams[0])
    #else:
    inlet_marker = False
    #print("Can't find Markers stream.")

    info = inlet.info()
    description = info.desc()

    Nchan = info.channel_count()

    ch = description.child('channels').first_child()
    ch_names = [ch.child_value('label')]
    for i in range(1, Nchan):
        ch = ch.next_sibling()
        ch_names.append(ch.child_value('label'))

    res = []
    timestamps = []
    markers = []
    t_init = time()
    time_correction = inlet.time_correction()
    print('Start recording at time t=%.3f' % t_init)
    print('Time correction: ', time_correction)
    while (time() - t_init) < duration:
        try:
            data, timestamp = inlet.pull_chunk(timeout=1.0,
                                               max_samples=chunk_length)

            if timestamp:
                res.append(data)
                timestamps.extend(timestamp)
            if inlet_marker:
                marker, timestamp = inlet_marker.pull_sample(timeout=0.0)
                if timestamp:
                    markers.append([marker, timestamp])
        except KeyboardInterrupt:
            break

    time_correction = inlet.time_correction()
    print('Time correction: ', time_correction)

    res = np.concatenate(res, axis=0)
    timestamps = np.array(timestamps) + time_correction

    if dejitter:
        y = timestamps
        X = np.atleast_2d(np.arange(0, len(y))).T
        lr = LinearRegression()
        lr.fit(X, y)
        timestamps = lr.predict(X)

    res = np.c_[timestamps, res]
    data = pd.DataFrame(data=res, columns=['timestamps'] + ch_names)

##    if inlet_marker:
##        n_markers = len(markers[0][0])
##        for ii in range(n_markers):
##            data['Marker%d' % ii] = 0
##        # process markers:
##        for marker in markers:
##            # find index of markers
##            ix = np.argmin(np.abs(marker[1] - timestamps))
##            for ii in range(n_markers):
##                data.loc[ix, 'Marker%d' % ii] = marker[0][ii]

    #directory = os.path.dirname(filename)
    directory = newdir
    if not os.path.exists(newdir):
        os.makedirs(newdir)
    print(newdir)
    newfilename = str(filename+"_"+str(autovar)+".csv")
    data.to_csv(os.path.join(newdir,newfilename), float_format='%.3f', index=False)

    print('Done - wrote file: ' + newfilename)
if __name__ == "__main__":
    autonext = False
    print("muse-lsl recording tool:")
    print("type /h for help")
    print("type /a to enter auto mode, or enter to continue")
    inp = input("")
    if inp == "/a":
        autonext = True
        word = str(input("Enter word to auto log: "))
        timer = float(input("Enter time for auto log: "))
        newdir= str(str(dirname(os.getcwd()))+"\\words\\"+word)
        listfiles = os.listdir(newdir) 
        autovar = len(listfiles)
        print(autovar)
        print(newdir)
    while True:
        if autonext == False:
            word = input("> ")            
            time = int(input("Input time to record: "))
            record(time)
            print('Recording has ended')
        if autonext == True:
            input("Enter to begin recording") 
            record_auto(timer,word,autovar,newdir)
            print('Recording has ended')
            autovar+=1
