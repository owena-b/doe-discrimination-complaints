import re
import json
import requests
import pandas as pd

url = "https://www.nba.com/players"

data = re.search(r'({"props":.*})', requests.get(url).text).group(0)
data = json.loads(data)

# uncomment to print all data:
# print(json.dumps(data, indent=4))

df = pd.DataFrame(data["props"]["pageProps"]["players"])
print(df.head().to_markdown())
