import instaloader
from telegram import Bot
import asyncio

# إعداد البوت
telegram_bot_token = '7959850481:AAGbH_Ast2G0N6Q191BXYiCPXePTjb7yi2I'
channel_id = '@instatesytl'

bot = Bot(token=telegram_bot_token)
L = instaloader.Instaloader()


L.context.proxy = "http://192.168.1.100:8080"

# إعداد instaloader
L = instaloader.Instaloader()

L.login('mrhossam0', 'hossamshaory2003$$')

def get_latest_post(username):
    # تنزيل المنشور الأخير من الحساب
    profile = instaloader.Profile.from_username(L.context, username)
    latest_post = next(profile.get_posts())
    L.download_post(latest_post, target=profile.username)
    return latest_post

async def send_to_telegram(post):
    caption = post.caption or "No Caption"
    
    if post.typename == 'GraphImage':
        media_path = f"{post.owner_username}/{post.date_utc.strftime('%Y-%m-%d_%H-%M-%S_UTC')}.jpg"
        await bot.send_photo(chat_id=channel_id, photo=open(media_path, 'rb'), caption=caption)
    elif post.typename == 'GraphVideo':
        media_path = f"{post.owner_username}/{post.date_utc.strftime('%Y-%m-%d_%H-%M-%S_UTC')}.mp4"
        await bot.send_video(chat_id=channel_id, video=open(media_path, 'rb'), caption=caption)
    elif post.typename == 'GraphSidecar':
        # المنشور عبارة عن ألبوم
        for index, sidecar_node in enumerate(post.get_sidecar_nodes()):
            try:
                if sidecar_node.is_video:
                    media_path = f"{post.owner_username}/{post.date_utc.strftime('%Y-%m-%d_%H-%M-%S_UTC')}_{index + 1}.mp4"
                    await bot.send_video(chat_id=channel_id, video=open(media_path, 'rb'), caption=(caption if index == 0 else ""))
                else:
                    media_path = f"{post.owner_username}/{post.date_utc.strftime('%Y-%m-%d_%H-%M-%S_UTC')}_{index + 1}.jpg"
                    await bot.send_photo(chat_id=channel_id, photo=open(media_path, 'rb'), caption=(caption if index == 0 else ""))
                # تأخير لمدة 5 ثواني بين كل إرسال لتجنب الأخطاء
                await asyncio.sleep(5)
            except Exception as e:
                print(f"Error sending media {index + 1}: {e}")

async def main():
    # اسم المستخدم لحساب إنستغرام بدون @
    instagram_username = 'mrhossam0'
    last_post_shortcode = None

    while True:
        try:
            latest_post = get_latest_post(instagram_username)
            if latest_post.shortcode != last_post_shortcode:
                last_post_shortcode = latest_post.shortcode
                await send_to_telegram(latest_post)
            else:
                print("No new posts.")
        except Exception as e:
            print(f"Error: {e}")

        # انتظر 40 ثانية قبل التحقق مرة أخرى
        await asyncio.sleep(100)

# تشغيل الكود
if __name__ == "__main__":
    asyncio.run(main())
