import os
from datetime import datetime

now = datetime.now()
test = now.strftime("_%Y%M%d") 

print(test)