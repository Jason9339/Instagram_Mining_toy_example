import instaloader
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

# 初始化 Instaloader
L = instaloader.Instaloader()

# 設定公開的 IG 帳號 (例如，'foodblogger_account')
account_name = 'foodiee_diaryy'

# 下載帳號貼文
posts = instaloader.Profile.from_username(L.context, account_name).get_posts()

# 記錄貼文數據的資料結構
data = []
max_posts = 200  # 設定最多分析的貼文數量

for post in posts:
    if len(data) >= max_posts:
        break
    data.append({
        "likes": post.likes,
        "comments": post.comments,
        "date": post.date,  # 貼文發布時間
    })

# 將數據轉換成 DataFrame 以便分析
df = pd.DataFrame(data)

# 將發布時間分成小時，以便觀察時間趨勢
df['hour'] = df['date'].dt.hour

# 計算各小時的平均按讚數
hourly_likes = df.groupby('hour')['likes'].mean()
hourly_comments = df.groupby('hour')['comments'].mean()

# 畫出按讚和留言的平均數據圖表
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
hourly_likes.plot(kind='bar', color='skyblue')
plt.title("Average Likes by Hour of Post")
plt.xlabel("Hour of Day (24h)")
plt.ylabel("Average Likes")
plt.xticks(rotation=0)

plt.subplot(1, 2, 2)
hourly_comments.plot(kind='bar', color='lightcoral')
plt.title("Average Comments by Hour of Post")
plt.xlabel("Hour of Day (24h)")
plt.ylabel("Average Comments")
plt.xticks(rotation=0)

plt.tight_layout()
plt.show()