from datetime import datetime
text="08.08.202"
datetime_object = datetime.strptime(text, "%d.%m.%Y")
text = datetime_object.strftime("%Y-%m-%d")

# ValueError