import requests
import json
import logging

url="https://script.google.com/macros/s/AKfycbxM7EAGb1CgZIs8s5XNm04TEDiHTbVowzzsbzU7zGBwen31r0GkaTJzUpK5gs42Ipui/exec"
def test():
    print("just test")
    
# class Reply:
#     def __init__(self, message_temp="just fuck off!"):
#         self.content = message_temp
#         self.status = 0  # 預設狀態為 0


def dealer(app,func,input):
    app.logger.info("entering dealer")
    input = input.split()
    reply = genernal_request(app,func,input)
    return reply



def genernal_request(app,func="roll_call",data=["周西瓜","1","1","被電神電暈了"]):#data:string=>a list of parameters
    app.logger.info("entering genernal request")
    # print(type(data))
    # data = data.split(" ")
    data_dictize ={"data":",".join(data) , "func":func}
    # solve "don't match the signature for spreadsheet.appendRow":
    # beacuse get can't directly pass parameters of type of list
    # change list to string by ",".join(data) and then data.split(",") in the server
    # https://stackoverflow.com/questions/35851315/how-to-send-a-list-in-python-requests-get
    app.logger.info(data_dictize)
    response = requests.get(url, params=data_dictize) # Use json=data for JSON data(X )
                                                    #Use params=data in get and Use data=data in post
    app.logger.info("response was gotten")
    try:
        app.logger.info(json.loads(response.text))
    except Exception as e:
        app.logger.info(response.text)
    response_dealed = json.loads(response.text) # this change json-like string to json(dictionary)
    # response = response.json()
    # app.logger.info(response['data'])
    # Check for successful response
    if response.status_code == 200:
        try:
            app.logger.info("dealing data")
            # Assuming JSON response: Parse as JSON and access data
            # data = response_dealed['data']
            # app.logger.info(data)
            if response_dealed['status'] == 1:  # Check for API-specific status code
                app.logger.info("Request successful!")
                status = 1
            else:
                app.logger.info(f"Error: API returned status {response_dealed['status']}")
                status = -1
        except (json.JSONDecodeError, KeyError):
            # Handle potential errors if response is not JSON or 'status' key is missing
            app.logger.info("Error: Could not parse response data.")
            response_dealed['reply'] = "出問題囉:Error: Could not parse response data."
            status = -1
    else:
        app.logger.info(f"Error: HTTP status code {response.status_code}")
        response_dealed['reply'] = f"出問題囉:Error: HTTP status code {response.status_code}"
        status = -1

    return {"status":status,"content":response_dealed['reply']}


# app.logger.info(roll_call(0).content)
# print(genernal_request()['status'])
# print(dealer("roll_call","1 1 1 1"))