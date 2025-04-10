import sys
import xbmcplugin
import xbmcgui
import xbmcaddon
import requests

addon = xbmcaddon.Addon()
addon_handle = int(sys.argv[1])
base_url = "https://archive.org/advancedsearch.php"

xbmcplugin.setContent(addon_handle, 'videos')

def build_url(query):
    return f"{sys.argv[0]}?{query}"

def list_movies():
    # Search for public domain movies on Archive.org
    query = {
        'q': 'mediatype:(movies)',
        'fl[]': 'identifier,title',
        'rows': '10',
        'page': '1',
        'output': 'json'
    }
    response = requests.get(base_url, params=query)
    if response.status_code == 200:
        results = response.json()['response']['docs']
        for movie in results:
            title = movie.get('title', 'Unknown Title')
            identifier = movie.get('identifier')
            url = f"https://archive.org/download/{identifier}/{identifier}.mp4"
            li = xbmcgui.ListItem(title)
            li.setInfo('video', {'title': title})
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False)
    xbmcplugin.endOfDirectory(addon_handle)

if __name__ == '__main__':
    list_movies()