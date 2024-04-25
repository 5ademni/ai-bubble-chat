from poe_api_wrapper import PoeApi

tokens = {
    'b': 'YVNKZKBGPbWgKMAW1Xn17g%3D%3D',
    'lat': 'qf2oLEe0K1aw4G2NxfvwsaN9b9no9%2BsjrhlXsDWqHA%3D%3D'
}

client = PoeApi(cookie=tokens)

bot = "5ademni_bot"
message = "say hi!"

'''# streaming the response
for chunk in client.send_message(bot, message):
    print(chunk["response"], end="", flush=True)
print("\n")'''

# non-streaming response
for chunk in client.send_message(bot, message):
    pass
print(chunk["text"])
