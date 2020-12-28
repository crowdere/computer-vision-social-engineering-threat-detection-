import json
import logging
import requests
import msal

# load relative parameter file
config = json.load(open('parameters_prod.json'))


def update_known_people():
    # Create a preferably long-lived app instance which maintains a token cache.
    app = msal.ConfidentialClientApplication(
        config["client_id"], authority=config["authority"],
        client_credential=config["secret"],
    )
    # The pattern to acquire a token looks like this.
    result = None
    # Firstly, looks up a token from cache
    # Since we are looking for token for the current app, NOT for an end user,
    # notice we give account parameter as None.
    result = app.acquire_token_silent(config["scope"], account=None)

    if not result:
        logging.info("No suitable token exists in cache. Let's get a new one from AAD.")
        result = app.acquire_token_for_client(scopes=config["scope"])

    if "access_token" in result:
        # Calling graph using the access token
        graph_data = requests.get(  # Use token to call downstream service
            config["endpoint_base"],
            headers={'Authorization': 'Bearer ' + result['access_token']}, ).json()
        print("Updating Profiles - Graph API call result: ")

        graph_list = graph_data.get('value')
        for x in graph_list:
            if x["companyName"] == "6510":
                name = x["userPrincipalName"]
                name = name.split("@")
                photo_data = requests.get(
                    config["endpoint_base"] + x["id"] + config["endpoint_photo"],
                    headers={'Authorization': 'Bearer ' + result['access_token']}, )
                print(photo_data)
                # Write photo to directory with username as filename
                file = open("known_people/" + name[0] + ".jpg", "wb")
                file.write(photo_data.content)
                file.close()
    else:
        print(result.get("error"))
        print(result.get("error_description"))
        print(result.get("correlation_id"))  # You may need this when reporting a bug
