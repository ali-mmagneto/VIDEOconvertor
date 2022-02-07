#tg:ChauhanMahesh/DroneBots
#github.com/vasusen-code

from .. import Drone, ACCESS_CHANNEL, AUTH_USERS
from telethon import events, Button
from LOCAL.localisation import START_TEXT as st
from LOCAL.localisation import JPG0 as file
from LOCAL.localisation import JPG4
from LOCAL.localisation import info_text, spam_notice, help_text, DEV, source_text, SUPPORT_LINK
from ethon.teleutils import mention
from main.plugins.actions import set_thumbnail, rem_thumbnail, heroku_restart

@Drone.on(events.NewMessage(incoming=True, pattern="/start"))
async def start(event):
    await event.reply(f'{st}', 
                      buttons=[
                              [Button.inline("Menü", data="menu")]
                              ])
    tag = f'[{event.sender.first_name}](tg://user?id={event.sender_id})'
    await Drone.send_message(int(ACCESS_CHANNEL), f'{tag} Botu Başlattı!')
    
@Drone.on(events.callbackquery.CallbackQuery(data="menu"))
async def menu(event):
    await event.client.send_file(event.chat_id, caption="**📑MENÜ**", file=file,
                    buttons=[[
                         Button.inline("Bilgi", data="info"),
                         Button.inline("Kod", data="source")],
                         [
                         Button.inline("Not", data="notice"),
                         Button.inline("Yardım/Ayarlar", data="help")],
                         [
                         Button.url("Geliştirici", url=f"{DEV}")]])
    await event.delete()
    
@Drone.on(events.callbackquery.CallbackQuery(data="menu2"))
async def menu2(event):
    await event.edit("**📑MENÜ**",
                    buttons=[[
                         Button.inline("Bilgi", data="info"),
                         Button.inline("Kod", data="source")],
                         [
                         Button.inline("Not", data="notice"),
                         Button.inline("Yardım/Ayarlar", data="help")],
                         [
                         Button.url("Geliştirici", url=f"{DEV}")]])
       
@Drone.on(events.callbackquery.CallbackQuery(data="info"))
async def info(event):
    await event.edit(f'**Bilgi:**\n\n{info_text}',
                    buttons=[[
                         Button.inline("Menü", data="menu2")]])
    
@Drone.on(events.callbackquery.CallbackQuery(data="notice"))
async def notice(event):
    await event.answer(f'{spam_notice}', alert=True)
    
@Drone.on(events.callbackquery.CallbackQuery(data="source"))
async def source(event):
    await event.edit(source_text,
                    buttons=[[
                         Button.url("Kişisei", url="https://github.com/vasusen-code/videoconvertor/tree/main"),
                         Button.url("Halk", url="https://github.com/vasusen-code/videoconvertor/tree/public")]])
                         
                    
@Drone.on(events.callbackquery.CallbackQuery(data="help"))
async def help(event):
    await event.edit('**Yardım ve Ayarlar**',
                    buttons=[[
                         Button.inline("Thumbnail Ayarla", data="sett"),
                         Button.inline("Thumbnail Kaldır", data='remt')],
                         [
                         Button.inline("Eklentiler", data="plugins"),
                         Button.inline("Yeniden Başlat", data="restart"),
                         Button.url("Destek", url=f"{SUPPORT_LINK}")],
                         [
                         Button.inline("Menü", data="menu2")]])
    
@Drone.on(events.callbackquery.CallbackQuery(data="plugins"))
async def plugins(event):
    await event.edit(f'{help_text}',
                    buttons=[[Button.inline("Menü", data="menu2")]])
                   
 #-----------------------------------------------------------------------------------------------                            
    
@Drone.on(events.callbackquery.CallbackQuery(data="sett"))
async def sett(event):    
    button = await event.get_message()
    msg = await button.get_reply_message() 
    await event.delete()
    async with Drone.conversation(event.chat_id) as conv: 
        xx = await conv.send_message("Bu Mesaja 'Yanıt' Olarak Küçük Resim İçin Bana Herhangi Bir Resim Gönder.")
        x = await conv.get_reply()
        if not x.media:
            xx.edit("Medya Bulunamadı.")
        mime = x.file.mime_type
        if not 'png' in mime:
            if not 'jpg' in mime:
                if not 'jpeg' in mime:
                    return await xx.edit("Resim Bulunamadı.")
        await set_thumbnail(event, x.media)
        await xx.delete()
        
@Drone.on(events.callbackquery.CallbackQuery(data="remt"))
async def remt(event):  
    await event.delete()
    await rem_thumbnail(event)
    
@Drone.on(events.callbackquery.CallbackQuery(data="restart"))
async def res(event):
    if not f'{event.sender_id}' == f'{int(AUTH_USERS)}':
        return await event.edit("Yalnızca Yetkili Kullanıcı Yeniden Başlatabilir!")
    result = await heroku_restart()
    if result is None:
        await event.edit("You have not filled `HEROKU_API` and `HEROKU_APP_NAME` vars.")
    elif result is False:
        await event.edit("Bir Hata Oluştu!")
    elif result is True:
        await event.edit("Uygulama Yeniden Başlatılıyor, Bir Dakika Bekleyin.")
