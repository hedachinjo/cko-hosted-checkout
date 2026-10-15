#Imporating path Class from pathlib module
from pathlib import Path
import json
import urllib.request
import urllib.error

#Grabs directory containing main.py
PROJECT_DIR = Path(__file__).resolve().parent
ENVIRONMENT_FILE = PROJECT_DIR / ".env"

#Creating function to call to read API credentials in from .env
def load_environment():
    config = {} #Creating an empty dict object

    #Using for loop to split contents into individual lines and looping through
    #each line and assigning it to the variable 'line'
    #utf-8 is standard encoding for text
    for line in ENVIRONMENT_FILE.read_text(encoding="utf-8").splitlines():

        #Strips the line of whitespace from front and end
        line = line.strip()

        #Ignoring empty lines, comments, and ensuring line isn't empty
        if not line or line.startswith("#"):
            continue

        #Use "=" as delimiter, and split the line only once. Assigns first have to key, second half to value
        key, value = line.split("=", 1)

        #assigning config dict key with the key extracted earlier, and storing the value in value
        config[key] = value

    return config

def create_hosted_checkout(config):
    #Constructing the entire url/endpoint for the hosted checkout call
    entire_url = config["CKO_API_BASE_URL"] + "/hosted-payments"

    #Loading request_payload dict with representation of request body for easy reading
    request_payload = {
        "amount": 250000,
        "currency": "USD",
        "reference": "CKO-HOSTED-CHECKOUT-DEMO",
        "processing_channel_id": config["CKO_PROCESSING_CHANNEL_ID"],
        "billing":{
            "address": {
                "country": "US"
            }
        },
        "success_url": "https://example.com/success",
        "failure_url": "https://example.com/failure",
        "cancel_url": "https://example.com/cancel"
    }

    #Converting request payload dict to JSON string
    json_payload = json.dumps(request_payload).encode("utf-8")

    #Creating HTTP request object
    request = urllib.request.Request(
        url = entire_url,
        data = json_payload,
        headers = {
            "Authorization": f"Bearer {config['CKO_SECRET_KEY']}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
        method = "POST"
    )

    #Recommended format to send HTTP POST request to destination endpoint
    #Automatically closes response connection when done
    with urllib.request.urlopen(request, timeout=60) as response:

        #Loading response body into result variable and then converting the JSON
        result = json.load(response)
        print("HTTP Status Code:", response.status)
        print(json.dumps(result, indent=4))
        return result

    #print(json_payload)
    #print(entire_url)
    #print(request_payload)

#Main function to test python, and break off rust
def main():
    print("Checkout.com Hosted Checkout Demo")
    print("--------------------------------")
    print("Good to go!")

    env_file = PROJECT_DIR / ".env"

    if env_file.exists():
        print("Environment file: Found")
    else:
        print("Environment file: Missing")

    #print("This should be the entire url/endpoint for the hosted checkout call, and request payload")
    #create_hosted_checkout(load_environment())

    config = load_environment()

    try: 
        result = create_hosted_checkout(config)

        #extracting checkout URL
        #Confirms that the checkout page was successfully created
        print("Hosted Payments Page Created!")

    except urllib.error.HTTPError as e:
        #printing status code
        print("HTTP Status Code:", e.code)

        #printing error response
        print("Error Response:", e.read().decode())

    except urllib.error.URLError as e:
        #seeing if there is a network/connection error
        print("Network/Connection Error:", e.reason)
    
main()
