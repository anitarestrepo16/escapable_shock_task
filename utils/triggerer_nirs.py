from pylsl import StreamInfo, StreamOutlet


class NIRS_Triggerer:
    '''
    Attributes:
    - stream_name: name of the LSL trigger stream
    - source_id: unique identifier for the LSL stream source
    - outlet: LSL outlet used to send trigger markers from PsychoPy to Aurora or NIRStar
    - trigger_codes: dictionary pairing trigger names with trigger codes

    Methods:
    - __init__: initializes the LSL trigger stream with settings appropriate for discrete event markers
    - set_trigger_codes: takes a dictionary pairing trigger names with trigger codes and sets the trigger_codes attribute
    - send: takes a trigger code and sends it as a single LSL marker sample
    - send_named: takes a trigger name, looks up its trigger code, and sends it as an LSL marker
    '''

    def __init__(self, stream_name="Trigger", source_id="nirs_trigger_stream"):
        """
        Initializes an LSL outlet (self.outlet) for sending triggers to fNIRS recording.

        Input:
            - stream_name (str): name of the LSL stream. "Trigger" is the default stream name
              expected by Aurora. If you are using NIRStar, change this to "TriggerStream".
            - source_id (str): optional unique identifier for the stream source

        LSL stream settings:
            - type = "Markers": because the stream is being used to send event markers
            - channel_count = 1: because one trigger value is sent per event/timepoint
            - nominal_srate = 0: because trigger events occur irregularly rather than at a fixed sampling rate
            - channel_format = "string": because trigger codes are sent as string markers

        Output: none
        """
        self.stream_name = stream_name
        self.source_id = source_id
        self.trigger_codes = {}

        info = StreamInfo(
            # names the stream
            name = stream_name,  # "Trigger" is the default name for the stream in Aurora. If you are using NIRStar, change this to "TriggerStream"
            # sets the content of the stream
            type = "Markers",
            # sets the number of channels per sample (timepoint)
            channel_count = 1,
            # sets a fixed sampling rate
            nominal_srate = 0,
            # sets channel type
            channel_format = "string",
            source_id = source_id
        )
        self.outlet = StreamOutlet(info)

    def set_trigger_codes(self, trigger_codes):
        '''
        Takes a dictionary pairing trigger names with trigger codes and sets the trigger_codes attribute.

        Input:
            - trigger_codes (dict): dictionary with trigger names (str) as keys and trigger codes (int or str) as values

        Output: none
        '''
        self.trigger_codes = trigger_codes

    def send(self, code):
        '''
        Takes a trigger code and sends it as a single LSL marker sample.

        Input:
            - code (int or str): trigger code to send

        Output: none
        '''
        self.outlet.push_sample([str(code)])

    def send_named(self, trigger_name):
        '''
        Takes a trigger name, looks up its corresponding trigger code in the trigger_codes
        attribute, and sends that code as an LSL marker.

        Input:
            - trigger_name (str): name of the trigger to send

        Output: none
        '''
        code = self.trigger_codes[trigger_name]
        self.send(code)
