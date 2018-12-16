import urllib.request
import json

def channel_query(query):
    api_key = 'AIzaSyCHPstZ_0VoIvpAL5n49piska5DF17zBgw'
    url = 'https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&fields=items(id,snippet,statistics)&key=' + api_key
    final_url = url + '&id=' + query

    chl_obj = urllib.request.urlopen(final_url)

    data = json.load(chl_obj)

    # print(data['items'][0])

    # for item in (data['items']):
    #     print ('Channel : '+ str(item['snippet']['title']))
    #     print ('Views : '+ str(item['statistics']['viewCount']))

    #     print ('Subscriber : '+ str(item['statistics']['subscriberCount']))

    return data['items'][0]

def video_search(channelID):
    api_key = 'AIzaSyCHPstZ_0VoIvpAL5n49piska5DF17zBgw'
    url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&key=' + api_key
    final_url = url + '&id=' + channelID

    chl_obj = urllib.request.urlopen(final_url)

    data = json.load(chl_obj)
    return data['items']

# print(video_search('UCeXBXzelo7MvLkMr3dAKODQ'))

def count_like(video_list):

    #searchvideo
    #iterate for every video
        #call function keluarin jumlah likeperview
        #ditambahin
    #return jumlah like
    return sum_like;

def like_video(video_id):
        api_key = 'AIzaSyCHPstZ_0VoIvpAL5n49piska5DF17zBgw'
        url = 'https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&fields=items(id,snippet(channelId,title),statistics)&part=snippet,statistics&key=' + api_key
        final_url = url + '&id=' + video_id

        chl_obj = urllib.request.urlopen(final_url)

        data = json.load(chl_obj)

        return data['items'][0]['statistics']['likeCount']

#print(like_video("xyx6hrb7LTs"))
