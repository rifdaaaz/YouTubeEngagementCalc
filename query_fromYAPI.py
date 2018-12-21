import urllib.request
import json, math

def channel_query(channelID):
    #mengambil info ttg channel dari youtube data API
    api_key = 'AIzaSyCHPstZ_0VoIvpAL5n49piska5DF17zBgw'
    url = 'https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&fields=items(id,snippet,statistics)&key=' + api_key
    final_url = url + '&id=' + channelID

    chl_obj = urllib.request.urlopen(final_url)

    data = json.load(chl_obj)


    return data['items'][0]

def video_search(channelID,pageToken):
    #mengambil list video dari sebuah channel

    api_key = 'AIzaSyCHPstZ_0VoIvpAL5n49piska5DF17zBgw'
    url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=50&type=video&key=' + api_key
    final_url = url + '&channelId=' + channelID +'&pageToken=' +pageToken

    chl_obj = urllib.request.urlopen(final_url)

    data = json.load(chl_obj)
    return data

# print(video_search('UCeXBXzelo7MvLkMr3dAKODQ'))

def count_like_comment(channelID):
    #menghitung total like dan comment dari sebuah channel, iterate semua videonya

    sum_like=0
    sum_comment=0

    #searchvideo
    temp = video_search(channelID,'')
    for i in range(len(temp['items'])):
        # print("hitung"+str(i))
        sum_like += like_video(temp['items'][i]['id']['videoId'])
        sum_comment += comment_video(temp['items'][i]['id']['videoId'])
    for x in range(math.floor(((temp['pageInfo']['totalResults'])-1)/50)):
        temp = video_search(channelID,temp['nextPageToken'])
        # print("page " + str(x) + " is loading")
        for i in range(len(temp['items'])):
            sum_like+= like_video(temp['items'][i]['id']['videoId'])
            sum_comment += comment_video(temp['items'][i]['id']['videoId'])

    #iterate for every video
        #call function keluarin jumlah likeperview
        #ditambahin
    #return jumlah like
    return sum_like,sum_comment

# def count_comment(channelID):
#     sum_comment=0
#     #searchvideo
#     temp = video_search(channelID,'')
#     for i in range(len(temp['items'])):
#         sum_comment += comment_video(temp['items'][i]['id']['videoId'])
#         print("video : "+temp['items'][i]['id']['videoId'] )
#         print("comen"+str(sum_comment))
#         print("next video : "+temp['items'][i+1]['id']['videoId'] )
#
#     for x in range(int(((temp['pageInfo']['totalResults'])-1)/50)):
#         temp = video_search(channelID,temp['nextPageToken'])
#         print("page " + str(x) + " is loading")
#         for i in range(len(temp['items'])):
#             sum_comment += comment_video(temp['items'][i]['id']['videoId'])
#         print("comment: " + str(sum_comment))
#
#     #iterate for every video
#         #call function keluarin jumlah likeperview
#         #ditambahin
#     #return jumlah like
#     return sum_comment

def like_video(video_id):
    #mengambil jumlah like dari suatu video

        api_key = 'AIzaSyCHPstZ_0VoIvpAL5n49piska5DF17zBgw'
        url = 'https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&fields=items(id,snippet(channelId,title),statistics)&part=snippet,statistics&key=' + api_key
        final_url = url + '&id=' + video_id

        chl_obj = urllib.request.urlopen(final_url)

        data = json.load(chl_obj)

        return int(data['items'][0]['statistics']['likeCount'])

def comment_video(video_id):
        api_key = 'AIzaSyCHPstZ_0VoIvpAL5n49piska5DF17zBgw'
        url = 'https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&fields=items(id,snippet(channelId,title),statistics)&part=snippet,statistics&key=' + api_key
        final_url = url + '&id=' + video_id

        chl_obj = urllib.request.urlopen(final_url)

        data = json.load(chl_obj)
        try:
            return int(data['items'][0]['statistics']['commentCount'])
        except:
            return 0

#print(comment_video("xyx6hrb7LTs"))

# print(count_comment("UCgTbspgOb47SKEsOxYHlwPA")) #sti

# print(count_comment("UCIecZQpkLmj1HdBR6iV9rlQ"))
