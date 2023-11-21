import telebot
from PIL import Image, ImageDraw, ImageFont, ImageOps
from config import bot_token, CHATS
import io
import textwrap

bot = telebot.TeleBot(bot_token)

CHATS = CHATS

AVATAR_HEIGHT = 100
AVATAR_WIGHT = 100
STICKER_HEIGHT = 512
STICKER_WIGHT = 512
FONT_HEIGHT_TEXT = 24
FONT_HEIGHT_NAME = 30
WIGHT_TEXT_MAX = 23 #26 для montserrat-regular
WIGHT_NAME_MAX = 19 #20 для montserrat-regular
INDENT = 20
LINE_HEIGHT_NAME = 30
LINE_HEIGHT_TEXT = 27

#bot.create_new_sticker_set(user_id=549883953, name='Quotes_by_Quote_stick_bot', title='Цитаты великих', emojis=['\U00002712'], png_sticker='CAACAgIAAxkBAAEBlPBlNsNj6thvlbFK6wL3cLdf3ggivwACPzEAAreicUlop3VNAid-FTAE')

@bot.message_handler(commands = ['q'])
def send_sticker(message):
    #print(message)
    if message.reply_to_message and hasattr(message.reply_to_message, 'forward_from') and message.reply_to_message.forward_from:
        profile_photos = bot.get_user_profile_photos(message.reply_to_message.forward_from.id, limit=1)
    elif message.reply_to_message and hasattr(message.reply_to_message, 'forward_sender_name') and message.reply_to_message.forward_sender_name:
        profile_photos = None
    #elif message.reply_to_message and message.reply_to_message.from_user: #and hasattr(message.reply_to_message.forward_from, 'None') and hasattr(message.reply_to_message.forward_sender_name, 'None')
    elif message.reply_to_message and message.reply_to_message.from_user:
        profile_photos = bot.get_user_profile_photos(message.reply_to_message.from_user.id, limit=1)
    else:
        profile_photos = None
    if profile_photos and len(profile_photos.photos) > 0:
        profile_photo = profile_photos.photos[0][-1]
        file_id = profile_photo.file_id
        file_info = bot.get_file(file_id)
        file_path = file_info.file_path
        data = bot.download_file(file_path)
        avatar = Image.open(io.BytesIO(data))
        avatar = avatar.resize((AVATAR_HEIGHT, AVATAR_WIGHT))
        mask = Image.new('L', (101, 101), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + (AVATAR_HEIGHT, AVATAR_WIGHT), fill=255)
        avatar = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
        avatar.putalpha(mask)
        avatar.save('avatar.png')
    else:
        avatar = None
    if message.reply_to_message and hasattr(message.reply_to_message, 'forward_from') and message.reply_to_message.forward_from:
        wrapped_name_fill = textwrap.fill(message.reply_to_message.forward_from.first_name, width=WIGHT_NAME_MAX)
        wrapped_text_fill = textwrap.fill(message.reply_to_message.text, width=WIGHT_TEXT_MAX)
        wrapped_name_wrap = textwrap.wrap(message.reply_to_message.forward_from.first_name, width=WIGHT_NAME_MAX)
        wrapped_text_wrap = textwrap.wrap(message.reply_to_message.text, width=WIGHT_TEXT_MAX)
    elif message.reply_to_message and hasattr(message.reply_to_message, 'forward_sender_name') and message.reply_to_message.forward_sender_name:
        wrapped_name_fill = textwrap.fill(message.reply_to_message.forward_sender_name, width=WIGHT_NAME_MAX)
        wrapped_text_fill = textwrap.fill(message.reply_to_message.text, width=WIGHT_TEXT_MAX)
        wrapped_name_wrap = textwrap.wrap(message.reply_to_message.forward_sender_name, width=WIGHT_NAME_MAX)
        wrapped_text_wrap = textwrap.wrap(message.reply_to_message.text, width=WIGHT_TEXT_MAX)
    elif message.reply_to_message and message.reply_to_message.from_user:
        wrapped_name_fill = textwrap.fill(message.reply_to_message.from_user.first_name, width=WIGHT_NAME_MAX)
        wrapped_text_fill = textwrap.fill(message.reply_to_message.text, width=WIGHT_TEXT_MAX)
        wrapped_name_wrap = textwrap.wrap(message.reply_to_message.from_user.first_name, width=WIGHT_NAME_MAX)
        wrapped_text_wrap = textwrap.wrap(message.reply_to_message.text, width=WIGHT_TEXT_MAX)
    else:
        print('Не удалось достать данные')
        return
    height_rr_name = LINE_HEIGHT_NAME * len(wrapped_name_wrap) + INDENT
    height_rr_text = LINE_HEIGHT_TEXT * len(wrapped_text_wrap) + height_rr_name + INDENT
    image = Image.new('RGBA', (STICKER_WIGHT, height_rr_name+height_rr_text)) #color=(255, 140, 0)
    draw = ImageDraw.Draw(image)
    font_name = ImageFont.truetype('montserrat-alternates-medium.ttf', size=FONT_HEIGHT_NAME)
    font_text = ImageFont.truetype('montserrat-alternates-medium.ttf', size=FONT_HEIGHT_TEXT)
    if avatar is not None:
        image.paste(avatar, (0, 0))
    elif avatar is None:
        draw.ellipse((0, 0, (AVATAR_HEIGHT, AVATAR_WIGHT)), fill="#170F1F", width=1)
    draw.rounded_rectangle((AVATAR_WIGHT + INDENT, 0, STICKER_HEIGHT, height_rr_text), radius=20, fill='#002137', width=1) #363636-серый, 1E1429-фиолетовый, 191731-синий, 121212-черный, 191919-темно-серый, 262626, 002F55, 343E40, 423C63, 26203C, 003841, 002137
    draw.rounded_rectangle((AVATAR_WIGHT + INDENT, 0, STICKER_HEIGHT, height_rr_name), radius=20, fill='#001B2E', corners=(20, 20, 0, 0), width=1) #302f2f, 191122, 141226, 000000, 121212, 121212, 0E294B, 23282B, 373252, 1A162A, 003038, 001B2E
    draw.text((AVATAR_WIGHT + INDENT * 2, 60), wrapped_text_fill, fill="#E0FFFF", font=font_text)
    draw.text((AVATAR_WIGHT + INDENT * 2, 10), wrapped_name_fill, fill="#AFEEEE", font=font_name)
    image.save('sticker.png')
    if message.reply_to_message:
        with open('sticker.png', 'rb') as sticker:
            bot.send_sticker(message.chat.id, sticker)
            #bot.register_next_step_handler(sticker, save_sticker)

#@bot.message_handler(commands = ['add'])
#def save_sticker(message, sticker):
    #bot.add_sticker_to_set(user_id=message.from_user.id, name='Quotes_by_Quote_stick_bot', emojis=['\U00002712'], png_sticker=sticker)

if __name__ == '__main__':
     bot.infinity_polling()