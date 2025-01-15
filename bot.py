from telegram import Bot
import asyncio

telegram_bot_token = '7959850481:AAGbH_Ast2G0N6Q191BXYiCPXePTjb7yi2I'
channel_id = '@instatesytl'

bot = Bot(token=telegram_bot_token)

async def send_to_telegram(post):
    caption = post.caption or "No Caption"
    
    # تحقق من نوع المنشور وأرسل الوسائط المناسبة
    if post.typename == 'GraphImage':
        media_path = f"{post.owner_username}/{post.date_utc.strftime('%Y-%m-%d_%H-%M-%S_UTC')}.jpg"
        await bot.send_photo(chat_id=channel_id, photo=open(media_path, 'rb'), caption=caption)
        await asyncio.sleep(5)
    elif post.typename == 'GraphVideo':
        media_path = f"{post.owner_username}/{post.date_utc.strftime('%Y-%m-%d_%H-%M-%S_UTC')}.mp4"
        await bot.send_video(chat_id=channel_id, video=open(media_path, 'rb'), caption=caption)
        await asyncio.sleep(5)
    elif post.typename == 'GraphSidecar':
        for index, sidecar_node in enumerate(post.get_sidecar_nodes()):
            try:
                if sidecar_node.is_video:
                    media_path = f"{post.owner_username}/{post.date_utc.strftime('%Y-%m-%d_%H-%M-%S_UTC')}_{index + 1}.mp4"
                    await bot.send_video(chat_id=channel_id, video=open(media_path, 'rb'), caption=(caption if index == 0 else ""))
                else:
                    media_path = f"{post.owner_username}/{post.date_utc.strftime('%Y-%m-%d_%H-%M-%S_UTC')}_{index + 1}.jpg"
                    await bot.send_photo(chat_id=channel_id, photo=open(media_path, 'rb'), caption=(caption if index == 0 else ""))
                await asyncio.sleep(5)
            except Exception as e:
                print(f"Error sending media {index + 1}: {e}")
