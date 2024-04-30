def test():
    print("just test")
    
class Reply:
    def __init__(self, message_temp="just fuck off!"):#warning:can't use message as a argument name as it has already be initialized in the app.py?
        self.content = message_temp
        self.status = 0  # 預設狀態為 0


def roll_call(input):#名字 課程ID 是否會遲到(0/1) 備註(選填)

    reply = Reply()
    reply.status=1
    reply.content="just fuck off!"
    return reply

# print(roll_call(0).content)