import openai

def ChatGPT(user_text, rec):
    openai.api_key = "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"

    if rec:
        messages = [
            {"role": "system", "content": "You are a friendly companion that recommends most likely popular dishes on a restaurant menu."},
            {"role": "user", "content": user_text},
        ] 
    else:
        messages = [
            {"role": "system", "content": "You are a friendly companion that generates more information about the menu and helps the user with their questions regarding the menu."},
            {"role": "user", "content": user_text},
        ]
    
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        max_tokens = 500,
        messages = messages
    )

    return response["choices"][0]["messages"]["content"]


ChatGPT("hi how are you", True)