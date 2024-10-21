import requests
from datetime import datetime

def get_instagram_media(access_token, instagram_account_id, limit=5):
    """抓取 Instagram 帳號的媒體資訊。"""
    url = f"https://graph.facebook.com/v21.0/{instagram_account_id}/media"
    params = {
        "access_token": access_token,
        "fields": "id,caption,media_type,permalink,timestamp,username",
        "limit": limit  # 限制抓取的貼文數量
    }

    # 送出 GET 請求取得媒體資料
    response = requests.get(url, params=params)
    data = response.json()  # 將回應轉換為 JSON 格式
    
    if 'data' in data:  # 如果資料存在，返回媒體資料
        return data['data']
    else:  # 否則顯示錯誤訊息
        print(f"Error fetching media: {data.get('error', 'Unknown error')}")
        return []

def get_media_insights(access_token, media_id):
    """抓取單一媒體的 Insights 資訊，包含likes、shares、saved 等。"""
    url = f"https://graph.facebook.com/v21.0/{media_id}/insights"
    params = {
        "metric": "impressions,reach,likes,comments,shares,saved,total_interactions",
        "access_token": access_token
    }

    # 送出 GET 請求取得 Insights 資料
    response = requests.get(url, params=params)
    data = response.json()  # 將回應轉換為 JSON 格式
    
    if 'data' in data:  # 如果有資料，返回 Insights 資訊
        return data['data']
    elif 'error' in data:  # 如果出錯，返回錯誤訊息
        return {"error": data['error'].get('error_user_msg', 'Unknown error')}
    else:
        return []

def format_insights(media, insights):
    """格式化輸出單篇貼文的 Insights 資訊。"""
    print(f"Media ID: {media['id']} | Username: {media['username']}")
    print(f"Posted on: {media['timestamp']} | Permalink: {media['permalink']}")
    
    if isinstance(insights, dict) and 'error' in insights:  # 處理錯誤情況
        print(f"Error: {insights['error']}")
    else:
        # 格式化並輸出每個指標的資訊
        for insight in insights:
            metric_name = insight['name']
            for value in insight['values']:
                date = value.get('end_time', '')[:10] or 'N/A'  # 提取日期
                metric_value = value['value']
                if metric_value:  # 只顯示有用的數據
                    print(f"  {metric_name}: {metric_value} (Date: {date})")
    print('-' * 40)

def manage_hashtags(media_data):
    """統計標籤使用頻率。"""
    hashtags = []
    # 從每篇貼文的說明文字中提取標籤
    for media in media_data:
        caption = media.get('caption', '')
        hashtags.extend([word.lower() for word in caption.split() if word.startswith('#')])

    # 統計每個標籤出現的次數
    return {tag: hashtags.count(tag) for tag in set(hashtags)}

def display_hashtags(hashtag_stats):
    """格式化輸出標籤統計資訊。"""
    print("=== Hashtag Statistics ===")
    if not hashtag_stats:  # 如果沒有標籤
        print("No hashtags found.")
    else:
        # 顯示每個標籤的出現次數
        for hashtag, count in hashtag_stats.items():
            print(f"{hashtag}: {count} occurrences")
    print()

def format_media_data(media_data):
    """格式化輸出每篇媒體的基本資訊。"""
    print("=== Media Data ===")
    for media in media_data:
        print(f"Media ID: {media['id']}")
        print(f"Username: {media['username']}")
        print(f"Caption: {media.get('caption', 'No caption')}")
        print(f"Media Type: {media['media_type']}")
        print(f"Permalink: {media['permalink']}")
        print(f"Timestamp: {media['timestamp']}")
        print('-' * 40)
    print(f"Total posts retrieved: {len(media_data)}")
    print()

# 請使用自己的token、id
access_token = "----------------"
instagram_account_id = "----------"

# 1. 抓取媒體資訊
media_data = get_instagram_media(access_token, instagram_account_id)

if media_data:
    # 2. 顯示每篇貼文的 Insights 資訊
    print("\n=== Media Insights ===")
    for media in media_data:
        insights = get_media_insights(access_token, media['id'])
        format_insights(media, insights)

    # 3. 顯示標籤統計
    hashtag_stats = manage_hashtags(media_data)
    display_hashtags(hashtag_stats)

    # 4. 顯示每篇媒體的基本資料
    format_media_data(media_data)
else:
    print("No media data available.")  # 如果沒有抓取到媒體資料
