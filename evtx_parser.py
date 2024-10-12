import Evtx.Evtx as evtx
import xmltodict

def read_evtx(file_path):
    with open('fout.txt', 'w') as f:
        with evtx.Evtx(file_path) as log:
            for record in log.records():
                record_xml = record.xml()
                record_dict = xmltodict.parse(record_xml)
                
                # Extract essential fields
                event_id = record_dict['Event']['System']['EventID']['#text']
                event_time = record_dict['Event']['System']['TimeCreated']['@SystemTime']
                
                # Extracting key fields from EventData
                essential_data = {}
                if 'EventData' in record_dict['Event'] and 'Data' in record_dict['Event']['EventData']:
                    data_items = record_dict['Event']['EventData']['Data']
                    if isinstance(data_items, list):
                        for item in data_items:
                            key = item.get('@Name', 'Unknown')
                            value = item.get('#text', None)
                            if value:
                                essential_data[key] = value
                    else:
                        key = data_items.get('@Name', 'Unknown')
                        value = data_items.get('#text', None)
                        if value:
                            essential_data[key] = value

                # Output string
                event_data_str = "; ".join([f"{k}: {v}" for k, v in essential_data.items()])
                
                f.write(f"Event ID: {event_id}, Time: {event_time}\n")
                if event_data_str:
                    f.write(f"  Data: {event_data_str}\n")
                f.write("\n")  

file_path = '/path'
read_evtx(file_path)
