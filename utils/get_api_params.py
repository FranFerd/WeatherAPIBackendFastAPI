def get_params_weather(api_key: str) -> dict:
    return {
        "unitGroup" : "metric",
        "key" : api_key,
        "include" : "hours,resolvedAddress",
        "elements": "address,datetime,temp,feelslike,conditions,preciptype,icon,windspeed,uvindex,sunrise,sunset",
        "contentType" : "json",
        "locationMode" : "single"
    }

def get_params_check_address(api_key: str) -> dict:
    return {
        "unitGroup" : "metric",
        "key" : api_key,
        "include" : "address,resolvedAddress",
        "elements": "address,resolvedAddress",
        "contentType" : "json",
        "locationMode" : "single"
        }