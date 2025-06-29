def get_params_weather(api_key: str) -> dict:
    return {
        "unitGroup" : "metric",
        "key" : api_key,
        "include" : "address,resolvedAddress",
        "elements": "address,resolvedAddress",
        "content-type" : "json",
        "locationMode" : "single"
    }

def get_params_check_address(api_key: str) -> dict:
    return {
            "unitGroup" : "metric",
            "key" : api_key,
            "include" : "address,resolvedAddress",
            "elements": "address,resolvedAddress",
            "content-type" : "json",
            "locationMode" : "single"
        }