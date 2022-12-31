import queue

# okx config
apikey = "30fe390f-ac39-464c-a81d-a52cadd5cc30"
secretkey = "32849050203B4F658031ECEEA8BB4116"
OkxPublicTopic = "wss://ws.okx.com:8443/ws/v5/public"
OkxPrivateTopic = "wss://ws.okx.com:8443/ws/v5/public"

# data queue
data_Q = queue.Queue()


# data config
resample_map = {
    'Open': 'first',
    'High': 'max',
    'Low': 'min',
    'Close': 'last',
    'Volume': 'last'
}

resample_period = '1T'
