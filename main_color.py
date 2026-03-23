from colorama import Fore, Style, init

init(autoreset=True)

def menu():
    print(Fore.CYAN + "\n=== Microsoft Graph IAM Automation Toolkit ===")
    print(Fore.YELLOW + "1." + Fore.WHITE + " Export all Groups")
    print(Fore.YELLOW + "2." + Fore.WHITE + " Export Group Membership")
    print(Fore.YELLOW + "3." + Fore.WHITE + " Export User Access")
    print(Fore.YELLOW + "4." + Fore.WHITE + " Add User to Group")
    print(Fore.YELLOW + "5." + Fore.WHITE + " List Group Members")
    print(Fore.YELLOW + "6." + Fore.WHITE + " Remove User from Group")
    print(Fore.YELLOW + "7." + Fore.WHITE + " Delete User")
    print(Fore.YELLOW + "8." + Fore.WHITE + " Disable User")
    print(Fore.YELLOW + "9." + Fore.WHITE + " Force User Sign-Out")
    print(Fore.YELLOW + "10." + Fore.WHITE + " Update User Display Name")
    print(Fore.YELLOW + "0." + Fore.WHITE + " Exit")
    print(Fore.CYAN + "===============================================")


