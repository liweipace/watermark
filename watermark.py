'''
Author: Wei
CREATED AT: June 17, 2020
'''
import os
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.VideoClip import TextClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.fx.resize import resize
from moviepy.audio.fx.volumex import volumex
ImageClip.resize = resize

from PIL import Image, ImageDraw, ImageFont

import pandas as pd

if len(os.listdir('./video'))>999:
    print("TOO MANY VIDEOS(>999) ")
    os._exit()

# SELECT LOGO TYPE
logo_selection = input("Please SELECT A LOGO TYPE(1:Monochrome_ENG;2:Monochrome_CHN;3:Colorful_ENG;4:Colorful_CHN), type number:")
logo_dict = {'1':'watermark.png', '2':'watermark_CHN.png', '3':'watermark_colorful.png', '4':'watermark_colorful_CHN.png'}
logo_path = "./logo/"+logo_dict[str(logo_selection)]



TODAY = (pd.datetime.now()).strftime('%Y%m%d')
# MAIN
for i, filename in enumerate(os.listdir('./video')):
    series_number = (str(i+1)).zfill(3)
    series_txt = 'ML'+TODAY+'-'+series_number
    
    image = Image.new(mode='RGBA', size=(100, 100))
    im_temp = ImageDraw.Draw(im=image)
    logosize = im_temp.textsize(text=series_txt, font=ImageFont.truetype('./font/Alibaba-PuHuiTi-Regular.ttf', 20))
    image.close()
    image = Image.new(mode='RGBA', size=logosize)
    draw_table = ImageDraw.Draw(im=image)
    draw_table.text(xy=(0, 0), text=series_txt, fill='#FFFFFF', font=ImageFont.truetype('./font/Alibaba-PuHuiTi-Regular.ttf', 20))
    image.save('./logo/text_logo.png', 'PNG')
    image.close()

    video_name = filename
    video_path = './video/'+video_name
    video = VideoFileClip(video_path)
    if video.audio is None:
        video = VideoFileClip(video_path)
    else:
        newaudio = video.audio.fx(volumex,0)
        video = video.set_audio(newaudio)
    logo = (
        ImageClip(logo_path)
        .set_duration(video.duration)
        .resize(height=50)
        .set_pos(("left", "top"))
    )
    text = (
        ImageClip("./logo/text_logo.png")
        .set_duration(video.duration)
        .resize(height=20)
        .set_pos(("right", "bottom"))
    )
    #txt = TextClip(series_txt, color='white', font = './font/Alibaba-PuHuiTi-Regular.ttf', fontsize=20).set_pos(('right', 'bottom')).set_duration(video.duration)
    #final = CompositeVideoClip([video, logo, txt])
    final = CompositeVideoClip([video, logo, text])
    final.write_videofile("./video_result/{}.mp4".format(series_txt), codec="libx264", bitrate="10000000")