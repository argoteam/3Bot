def show_figlet() -> str:
    figlet = r"""
       __    __              __      
     /'__`\ /\ \            /\ \__
    /\_\L\ \\ \ \____    ___\ \ ,_\
    \/_/_\_<_\ \ '__`\  / __`\ \ \/
      /\ \L\ \\ \ \L\ \/\ \L\ \ \ \_
      \ \____/ \ \_,__/\ \____/\ \__\
       \/___/   \/___/  \/___/  \/__/"""
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

BASE_COLOR = 0x2b2d31