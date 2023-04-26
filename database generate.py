import os
import re
import json
from tkinter import Tk
from tkinter.filedialog import askdirectory

def analyze_lua_files():
    root = Tk()
    root.withdraw()
    folder_path = askdirectory(title='Select Folder')
    if not folder_path:
        return
    result = []
    sLines = set()
    for filename in os.listdir(folder_path):
        if filename.endswith('.lua'):
            with open(os.path.join(folder_path, filename), 'r') as f:
                content = f.read()
                title_search = re.search(r'function\s+(\w+)\(', content)
                if title_search:
                    title = title_search.group(1)
                    dLine = {}
                    sLine = {}
                    for i, line in enumerate(content.split('\n')):
                        if title in line:
                            dLine[str(i+1)] = line.strip()
                            if line.strip() not in sLines:
                                if 'local' not in line and 'function' not in line and '=' in line:
                                    sLine[str(len(sLine)+1)] = line.strip()
                                    sLines.add(line.strip())
                                elif 'callbacks.Register' in line or 'callbacks.Unregister' in line:
                                    sLine[str(len(sLine)+1)] = line.strip()
                                    sLines.add(line.strip())
                                elif '=' in line or 'Get' in line or 'Set' in line or '()' in line:
                                  sLine[str(len(sLine)+1)] = line.strip()
                                  sLines.add(line.strip())
                                else:
                                    function_call_search = re.search(r'(\w+)\(', line)
                                    if function_call_search:
                                        function_name = function_call_search.group(1)
                                        function_search = re.search(r'function\s+' + function_name + r'\s*\((.*?)\)([\s\S]*?)end', content)
                                        if function_search:
                                            function_code = function_search.group(0)
                                            sLine[str(len(sLine)+1)] = function_code
                                            sLines.add(function_code)
                    subTitle = ''
                    if dLine:
                        subTitle = list(dLine.values())[0][:20]
                    if not title:
                        title = 'No Title'
                    if not dLine:
                        dLine['1'] = 'No dLine'
                    if not sLine:
                        sLine['1'] = 'No SLine'
                    result.append({
                        'Title': title,
                        'subTitle': subTitle,
                        'dLine': dLine,
                        'SLine': sLine
                    })
    result.sort(key=lambda x: x['Title'])
    return result

json_data = {"tables": analyze_lua_files()}

# Write JSON data to file
with open("database.json", "w") as f:
    json.dump(json_data, f, indent=4)