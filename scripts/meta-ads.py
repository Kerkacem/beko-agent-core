import requests
import json


def get_meta_ads_data():
    # Meta Ads API endpoint
    url = "https://api.meta.com/ads"
    # TRC Protocol API endpoint
    trc_url = "https://api.trc.com/protocol"
    # Send request to Meta Ads API
    response = requests.get(url)
    # Send request to TRC Protocol API
    trc_response = requests.get(trc_url)
    # Parse JSON response
    data = json.loads(response.text)
    trc_data = json.loads(trc_response.text)
    # Return the combined data
    return {**data, **trc_data}
