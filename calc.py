import query_fromYAPI

def calculate_all(userID):
    data = query_fromYAPI.channel_query(userID)
    cname = data['snippet']['title']
    vc = int(data['statistics']['viewCount'])
    cc = int(query_fromYAPI.count_like(userID)[1])
    mv = int(data['statistics']['videoCount'])
    sc = int(data['statistics']['subscriberCount'])
    lc = int(query_fromYAPI.count_like(userID)[0])
    subsrate = round(float(sc/(vc/sc)*100),2)
    commentrate = round(float(cc/vc*100),2)
    likerate = round(float(lc/vc*100),2)

    return cname,lc,vc,cc,sc,likerate,commentrate,subsrate
