"""
Constants that are probably useful.
"""

# base endpoint for package analytics
# BASE_ENDPOINT = "http://10.102.11.96:8080/fa/api/v1"
BASE_ENDPOINT = "http://127.0.0.1:8080/fa/api/v1"

# endpoint used for barcode search
# API_ENDPOINT = "http://10.102.11.96:8080/search/execute?offset=0&size=10&locale=en-US"
API_ENDPOINT = BASE_ENDPOINT + "/search/execute?offset=0&size=10&locale=en-US"

# endpoint used for images
PIC_API_ENDPOINT = BASE_ENDPOINT + "/facility/1/system/"
# PIC_API_ENDPOINT = "http://127.0.0.1:8080/system/"
# "http://10.102.11.96:8080/system/3/object/{id}/device/{results[""0""].devices[""0""].deviceNumber}/media/img-sm?objectScanTime={objectScanTime}&mode=&locale=en-US"
# ^ the full url format for reference

# endpoint used for system configuration
SYSTEM_CONFIG_API_ENDPOINT = BASE_ENDPOINT + "/config/facility/1/system?locale=en-US"

# time window for how far in the past we should search for a barcode
SEARCH_DAYS = 7

# threshold for tamper detection
tamper_threshold = 0.05
