import webbrowser

url = 'http://www.python.org/'

chrome_path = '/usr/bin/chromium-browser %s'
webbrowser.get(chrome_path).open_new_tab(url)

# Open URL in a new tab, if a browser window is already open.
#webbrowser.open_new_tab(url + 'doc/')

