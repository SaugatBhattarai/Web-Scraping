import moviepy.editor as mp
import os
import sys

videos_path = './videos/'
video_file  = os.listdir(videos_path)
audio_path = './audio/'

for video in video_file:
    print('... video file extracting ... ', video)
    video_name_without_ext = os.path.splitext(os.path.basename(video))[0]
    video_clip = mp.VideoFileClip(videos_path+video)
    audio = video_clip.audio
    audio.write_audiofile(audio_path + video_name_without_ext+'.mp3')
    print('... audio file extracted ...')
