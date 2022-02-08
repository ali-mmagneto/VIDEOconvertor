#Tg:ChauhanMahesh/Dronebots
#Github.com/vasusen-code

import os
import time
import asyncio
from .. import Drone, LOG_CHANNEL, FORCESUB_UN, MONGODB_URI, ACCESS_CHANNEL
from telethon import events, Button
from telethon.tl.types import DocumentAttributeVideo
from main.plugins.rename import media_rename
from main.plugins.compressor import compress
from main.plugins.trimmer import trim
from main.plugins.convertor import mp3, flac, wav, mp4, mkv, webm, file, video
from main.Database.database import Database
from LOCAL.localisation import source_text, SUPPORT_LINK
from main.plugins.actions import force_sub
from ethon.telefunc import fast_download
from ethon.pyfunc import video_metadata

#Don't be a MF by stealing someone's hardwork.
forcesubtext = f"Beni Kullanmak İçin @{FORCESUB_UN} Katılmalısın.\n\nDestek @trbotlistesidestek."

@Drone.on(events.NewMessage(incoming=True,func=lambda e: e.is_private))
async def compin(event):
    db = Database(MONGODB_URI, 'videoconvertor')
    if event.is_private:
        media = event.media
        if media:
            yy = await force_sub(event.sender_id)
            if yy is True:
                return await event.reply(forcesubtext)
            banned = await db.is_banned(event.sender_id)
            if banned is True:
                return await event.reply(f'Yasaklandın!\n\nİletişim [Grup]({SUPPORT_LINK})', link_preview=False)
            video = event.file.mime_type
            if 'video' in video:
                await event.reply("📽",
                            buttons=[
                                [Button.inline("Sıkıştır", data="compress"),
                                 Button.inline("Dönüştür", data="convert")],
                                [Button.inline("Yeniden Adlandır", data="rename"),
                                 Button.inline("Kırp", data="trim")]
                            ])
            elif 'png' in video:
                return
            elif 'jpeg' in video:
                return
            elif 'jpg' in video:
                return    
            else:
                await event.reply('📦',
                            buttons=[  
                                [Button.inline("Yeniden Adlandır", data="rename")]])
    await event.forward_to(int(ACCESS_CHANNEL))

@Drone.on(events.callbackquery.CallbackQuery(data="convert"))
async def convert(event):
    button = await event.get_message()
    msg = await button.get_reply_message()  
    await event.edit("🔃**Dönüştür:**",
                    buttons=[
                        [Button.inline("MP3", data="mp3"),
                         Button.inline("FLAC", data="flac"),
                         Button.inline("WAV", data="wav")],
                        [Button.inline("MP4", data="mp4"),
                         Button.inline("WEBM", data="webm"),
                         Button.inline("MKV", data="mkv")],
                        [Button.inline("FILE", data="file"),
                         Button.inline("VIDEO", data="video")],
                        [Button.inline("BACK", data="back")]])
                        
@Drone.on(events.callbackquery.CallbackQuery(data="back"))
async def back(event):
    await event.edit("📽",
                    buttons=[
                        [Button.inline("Sıkıştır", data="compress"),
                         Button.inline("Dönüştür", data="convert")],
                        [Button.inline("Yeniden Adlandır", data="rename"),
                         Button.inline("Kırp", data="trim")]])
                            
#-----------------------------------------------------------------------------------------

process1 = []
timer = []

@Drone.on(events.callbackquery.CallbackQuery(data="mp3"))
async def vtmp3(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    button = await event.get_message()
    msg = await button.get_reply_message() 
    if not os.path.isdir("audioconvert"):
        await event.delete()
        os.mkdir("audioconvert")
        await mp3(event, msg)
        os.rmdir("audioconvert")
    else:
        await event.edit("Devam Eden Başka Bir İşlem Var! Sonra Tekrar Dene!")
        
@Drone.on(events.callbackquery.CallbackQuery(data="flac"))
async def vtflac(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    button = await event.get_message()
    msg = await button.get_reply_message()  
    if not os.path.isdir("audioconvert"):
        await event.delete()
        os.mkdir("audioconvert")
        await flac(event, msg)
        os.rmdir("audioconvert")
    else:
        await event.edit("Devam Eden Başka Bir İşlem Var! Sonra Tekrar Dene!")
        
@Drone.on(events.callbackquery.CallbackQuery(data="wav"))
async def vtwav(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    button = await event.get_message()
    msg = await button.get_reply_message() 
    if not os.path.isdir("audioconvert"):
        await event.delete()
        os.mkdir("audioconvert")
        await wav(event, msg)
        os.rmdir("audioconvert")
    else:
        await event.edit("Devam Eden Başka Bir İşlem Var! Sonra Tekrar Dene!")
        
@Drone.on(events.callbackquery.CallbackQuery(data="mp4"))
async def vtmp4(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    button = await event.get_message()
    msg = await button.get_reply_message() 
    await event.delete()
    await mp4(event, msg)
    
@Drone.on(events.callbackquery.CallbackQuery(data="mkv"))
async def vtmkv(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    button = await event.get_message()
    msg = await button.get_reply_message() 
    await event.delete()
    await mkv(event, msg)  
    
@Drone.on(events.callbackquery.CallbackQuery(data="webm"))
async def vtwebm(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    button = await event.get_message()
    msg = await button.get_reply_message() 
    await event.delete()
    await webm(event, msg)  
    
@Drone.on(events.callbackquery.CallbackQuery(data="file"))
async def vtfile(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    button = await event.get_message()
    msg = await button.get_reply_message() 
    await event.delete()
    await file(event, msg)    

@Drone.on(events.callbackquery.CallbackQuery(data="video"))
async def ftvideo(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    button = await event.get_message()
    msg = await button.get_reply_message() 
    await event.delete()
    await video(event, msg)
    
@Drone.on(events.callbackquery.CallbackQuery(data="rename"))
async def rename(event):    
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    button = await event.get_message()
    msg = await button.get_reply_message()  
    await event.delete()
    async with Drone.conversation(event.chat_id) as conv: 
        cm = await conv.send_message("Bu Mesaja 'Yanıt' Olarak Dosya İçin Bana Yeni Bir Ad Gönder.\n\n**NOT:** Uzantıya Gerek Yok.")                              
        try:
            m = await conv.get_reply()
            new_name = m.text
            await cm.delete()                    
            if not m:                
                return await cm.edit("Yanıt Bulunamadı.")
        except Exception as e: 
            print(e)
            return await cm.edit("Yanıt Beklenirken Bir Hata Oluştu.")
    await media_rename(event, msg, new_name)                     
                   
@Drone.on(events.callbackquery.CallbackQuery(data="compress"))
async def compresss(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    if f'{event.sender_id}' in process1:
        index = process1.index(f'{event.sender_id}')
        last = timer[int(index)]
        present = time.time()
        return await event.answer(f"Yeni Bir İşlem Başlatmak İçin {300-round(present-float(last))} Saniye Beklemelisin!", alert=True)
    button = await event.get_message()
    msg = await button.get_reply_message()
    if not os.path.isdir("compressmedia"):
        await event.delete()
        os.mkdir("compressmedia")
        await compress(event, msg)
        os.rmdir("compressmedia")
        now = time.time()
        timer.append(f'{now}')
        process1.append(f'{event.sender_id}')
        await event.client.send_message(event.chat_id, '5 Dakika Sonra Tekrar Yeni Bir İşleme Başlayabilirsiniz.')
        await asyncio.sleep(300)
        timer.pop(int(timer.index(f'{now}')))
        process1.pop(int(process1.index(f'{event.sender_id}')))
    else:
        await event.edit(f"Devam Eden Başka Bir İşlem Var!\n\n**[Bilgi Kanalı](https://t.me/{LOG_CHANNEL})**", link_preview=False)
    
@Drone.on(events.callbackquery.CallbackQuery(data="trim"))
async def vtrim(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    button = await event.get_message()
    msg = await button.get_reply_message()  
    await event.delete()
    async with Drone.conversation(event.chat_id) as conv: 
        try:
            xx = await conv.send_message("Buna Cevap Olarak Kırpmak İstediğin Videonun Başlangıç Saatini Bana Gönder. \n\n**Format** saat:dakika:saniye , Örnek: `01:20:69` ")
            x = await conv.get_reply()
            st = x.text
            await xx.delete()                    
            if not st:               
                return await xx.edit("Yanıt Bulunamadı.")
        except Exception as e: 
            print(e)
            return await xx.edit("Yanıt Beklenirken Bir Hata Oluştu.")
        try:
            xy = await conv.send_message("Buna Cevap Olarak Kırpmak İstediğin Videonun Bitiş Saatini Bana Gönder.  \n\n**Format** : saat:dakika:saniye , Örnek: `01:20:69` ")  
            y = await conv.get_reply()
            et = y.text
            await xy.delete()                    
            if not et:                
                return await xy.edit("Yanıt Bulunamadı.")
        except Exception as e: 
            print(e)
            return await xy.edit("Yanıt Beklenirken Bir Hata Oluştu.")
        await trim(event, msg, st, et)
            
