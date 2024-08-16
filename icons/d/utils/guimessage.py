def GuiMessagesConverter(AssistantName:str,NickName:str,messages:list[dict[str,str]]):
    temp = []
    Assistantname = AssistantName
    Username = NickName

    for message in messages:
        if message["role"] == "assistant":
            temp.append(f'''<span class = "Assistant">{Assistantname}</span> : {message['content']}''')
            temp.append("[*end*]")
        elif message["role"] == "user":
            temp.append(f"""<span class = "User">{Username}</span> : {message['content']}""")
        else:
            temp.append(f"""<span class = "User">{Username}</span> : {message['content']}""")
    return temp
