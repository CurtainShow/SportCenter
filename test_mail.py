import win32com.client

# 1) Launch Outlook
outlook = win32com.client.Dispatch("Outlook.Application")

# 2) Create a new mail item
mail = outlook.CreateItem(0)  # 0 = olMailItem

# 3) Fill in fields
mail.To      = "allan.barbot@manutan.fr"
mail.CC      = ""
mail.Subject = "Test via COM automation"
mail.Body    = "Hello!\n\nThis was sent by Python controlling Outlook."

# 4) (Optional) Add an attachment
# mail.Attachments.Add(r"C:\path\to\file.pdf")

# 5) Send or display for review
mail.Send()
# mail.Display()  # if you want to inspect before sending

print("Mail dispatched via Outlook client.")