from win32com_email import email

with open("secret.txt", "r") as file:
    for i in file.readlines():
        if '@' in i:
            cc = i
        else:
            cc = "Fuck"

email(cc,[],2,"testing",True)