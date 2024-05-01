import requests
import json

url="https://script.google.com/macros/s/AKfycbxM7EAGb1CgZIs8s5XNm04TEDiHTbVowzzsbzU7zGBwen31r0GkaTJzUpK5gs42Ipui/exec"
def test():
    print("just test")
    
# class Reply:
#     def __init__(self, message_temp="just fuck off!"):
#         self.content = message_temp
#         self.status = 0  # 預設狀態為 0


def dealer(func,input):
    print("entering dealer")
    input = input.split()
    reply = genernal_request(func,input)
    return reply



def genernal_request(func="roll_call",data=["周西瓜","1","1","被電神電暈了"]):#data:string=>a list of parameters
    print("entering genernal request")
    # print(type(data))
    # data = data.split(" ")
    data_dictize ={"data":",".join(data) , "func":func}
    # solve "don't match the signature for spreadsheet.appendRow":
    # beacuse get can't directly pass parameters of type of list
    # change list to string by ",".join(data) and then data.split(",") in the server
    # https://stackoverflow.com/questions/35851315/how-to-send-a-list-in-python-requests-get
    print(data_dictize)
    response = requests.get(url, params=data_dictize) # Use json=data for JSON data(X )
                                                    #Use params=data in get and Use data=data in post
    print("response was gotten")
    try:
        print(json.loads(response.text))
    except Exception as e:
        print(response.text)
    response_dealed = json.loads(response.text) # this change json-like string to json(dictionary)
    # response = response.json()
    # print(response['data'])
    # Check for successful response
    if response.status_code == 200:
        try:
            print("dealing data")
            # Assuming JSON response: Parse as JSON and access data
            data = response_dealed['data']
            print(data)
            if response_dealed['status'] == 1:  # Check for API-specific status code
                print("Request successful!")
                status = 1
            else:
                print(f"Error: API returned status {response_dealed['status']}")
                status = -1
        except (json.JSONDecodeError, KeyError):
            # Handle potential errors if response is not JSON or 'status' key is missing
            print("Error: Could not parse response data.")
            status = -1
    else:
        print(f"Error: HTTP status code {response.status_code}")
        status = -1

    return {"status":status,"content":response_dealed['reply']}


# print(roll_call(0).content)
# print(genernal_request())