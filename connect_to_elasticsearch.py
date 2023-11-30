# Assuming local ngrok Client is started
ngrok_host_id = "007b-92-186-122-170"

# Create an Elasticsearch client
es = Elasticsearch(
    hosts=[{
        'host': ngrok_host_id + '.ngrok-free.app',
        'port': 443,
        'scheme': 'https',
    }],
    basic_auth=('jakob', 'entwickler'),
    request_timeout=300 # Set the timeout to 30 seconds
)

# Check if the connection is successful
if es.ping():
    print("Connected to Elasticsearch")
else:
    print("Connection to Elasticsearch failed")