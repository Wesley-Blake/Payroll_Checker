import sys
import win32com.client as win32

def email(cc: str, bcc: list[str], pay_period: str, body: str) -> None:
    try:
        outlook = win32.Dispatch("outlook.application")
    except Exception as e:
        sys.exit(f"Failed to create Outlook application: {e}")

    mail = outlook.CreateItem(0)
    mail.CC = cc
    mail.BCC = "; ".join(bcc)
    mail.Subject = f"Pay Period: BW{pay_period}"
    mail.Body = \
f"""\
Hi,

Error: {body}

If you are receiving this email, it means that {len(bcc)} of your employees have some issue related to their timesheet: {pay_period}.
They are BCC'd on this email, so there is no action needed on your part.
"""
    mail.Send()
    #mail.Display()
