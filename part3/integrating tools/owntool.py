from langchain.tools import tool


@tool ## decorator for creating tool

def get_greeting(name: str) -> str: # type hints
    '''
    Generate a greeting message for a user
    '''
    
    return f"Hello {name}, Welcome to the AI World"

result = get_greeting.invoke({"name":"Roshan"})

print(result)

print(get_greeting.name)
print(get_greeting.description)
print(get_greeting.args)