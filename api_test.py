from poe_api_wrapper import PoeApi

client = PoeApi("CmpguqkTtuqLZh5w1XeRGw%3D%3D")

bot = "travel_assitance"
message = "say hi!"

'''# streaming the response
for chunk in client.send_message(bot, message):
    print(chunk["response"], end="", flush=True)
print("\n")'''

# non-streaming response
for chunk in client.send_message(bot, message):
    pass
print(chunk["text"])
