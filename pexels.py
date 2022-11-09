"""
Copyright 2022 hoangks5

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""


from pexels_api import API
import os
from dotenv import load_dotenv
load_dotenv()

PEXELS_API_KEY = os.getenv('PEXELS_API_KEY')
# Create API object
api = API(PEXELS_API_KEY)
list = []
# Search five 'kitten' photos
for i in range(1,50,1):
    api.search('kitten', page=i, results_per_page=80)
    # Get photo entries
    photos = api.get_entries()
    # Loop the five photos
    for photo in photos:
        list.append(photo.original)
string = '\n'.join(list)
with open('pexels.txt','w',encoding='utf-8') as f:
    f.write(string)
    f.close()