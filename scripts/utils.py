def show_figlet() -> str:
    figlet = r"""
     _                             _                   _           _   
    | |                           | |                 | |         | |  
    | | _____  _ __  _ __ __ _  __| | ___   ___ ______| |__   ___ | |_ 
    | |/ / _ \| '_ \| '__/ _` |/ _` |/ _ \ / _ \______| '_ \ / _ \| __|
    |   < (_) | | | | | | (_| | (_| | (_) | (_) |     | |_) | (_) | |_ 
    |_|\_\___/|_| |_|_|  \__,_|\__,_|\___/ \___/      |_.__/ \___/ \__|"""
    return figlet

def table(*tuples, center_leng) -> str:
    middle = center_leng - 2
    res = ""
    for name, second in tuples:
        res += f"{' '*(middle-len(name))}{name} : {second}\n"
        
    return res

def clean_code(string) -> str:
    if string.startswith("```") and string.endwith("```"):
        return string[3:-3]
    
    if string.startswith("`") and string.endswith("`"):
        return string[1:-1]
    
    return string