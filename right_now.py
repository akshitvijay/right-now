
import sys
import time
import datetime
import json
import os.path

jsonpath = os.path.join(os.path.dirname(__file__), 'storage/')

def fetch_JSON_data(filepath):
    with open(filepath) as userData:
        data = json.load(userData)
    return data

def write_to_file(filepath,data):
    with open(filepath,'w') as outfile:
        json.dump(data, outfile ,indent=4, sort_keys=True)


def add_event_to_dict(day_events,timestamp,work_text):
    day_events.append({"starttime":timestamp,"eventname":work_text})
    return day_events

def get_current_stamps():
    epochstamp = time.time()
    timestamp = datetime.datetime.fromtimestamp(epochstamp).strftime('%Y-%m-%d %H:%M:%S')
    datestamp = datetime.datetime.fromtimestamp(epochstamp).strftime('%Y-%m-%d')
    return epochstamp,timestamp,datestamp

def createFileIfDoesntExist(filepath):
    if not(os.path.exists(filepath)):
        print 'Creating file '+str(filepath)
        write_to_file(filepath,[])

def add_a_stamp(filepath):
    if len(sys.argv) < 3:
        print "No Event Provided"
        exit()

    work_text = sys.argv[2]
    epochstamp,timestamp,datestamp = get_current_stamps()
    if(len(sys.argv)==5):
        if(sys.argv[3]=='m'):
            minus=sys.argv[4]
            timestamp = editTime(minus)

    work_data = fetch_JSON_data(filepath)
    work_data = add_event_to_dict(work_data,timestamp,work_text)
    write_to_file(filepath,work_data)


def undo_last_stamp(filepath):
    work_data = fetch_JSON_data(filepath)
    work_data = work_data[:-1]
    write_to_file(filepath,work_data)

def print_all_stamps(filepath):
    for event in fetch_JSON_data(filepath):
        print event['starttime'],':',event['eventname']

def editTime(minusVal):
    epochstamp = time.time()
    timestamp = datetime.datetime.fromtimestamp(epochstamp).strftime('%Y-%m-%d %H:%M:%S')
    nutimestamp = datetime.datetime.strptime(timestamp,'%Y-%m-%d %H:%M:%S') - datetime.timedelta(minutes=int(minusVal))
    return str(nutimestamp)

def print_all_durations(outerjsonpath,datestamp):
    if len(sys.argv) > 2:
        datestamp = sys.argv[2]
    filepath = outerjsonpath + str(datestamp) + '.json'
    try:
        events = fetch_JSON_data(filepath)
    except:
        print "Sorry, It seems you have no records for ",datestamp
        exit()
    #event_duration = []
    last_event = {}
    print "Report For",datestamp
    for event in events:
        if(last_event == {}):
            last_event = event
            continue;
        time_difference = unicode_to_timestamp(event['starttime'])- unicode_to_timestamp(last_event['starttime'])
        #event_duration.append({"eventname":last_event['eventname'],"duration":time_difference}) 
        print str(last_event['eventname']),':',str(time_difference)
        last_event = event
        

def unicode_to_timestamp(time_in_unicode):
    return datetime.datetime.strptime(time_in_unicode, '%Y-%m-%d %H:%M:%S')

if __name__=='__main__':
        epochstamp, timestamp, datestamp =  get_current_stamps()
        outerjsonpath = str(os.path.join(os.path.dirname(__file__), 'storage/'))
        jsonpath = outerjsonpath + str(datestamp) + '.json'
        createFileIfDoesntExist(jsonpath)
        PTS_command = sys.argv[1]
        if PTS_command== "add":
            add_a_stamp(jsonpath)
        elif PTS_command == "undo":
            undo_last_stamp(jsonpath)
        elif PTS_command == "show":
            print_all_stamps(jsonpath)
        elif PTS_command == "report":
            print_all_durations(outerjsonpath,datestamp)
        else:
            print("Invalid Command: Try one amongst PTS add <Event>, undo, show or report")

