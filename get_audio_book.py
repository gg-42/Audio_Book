
import yt #https://github.com/1/python-youtube-library
import os
import subprocess
import logging
import argparse
logging.basicConfig(format='%(asctime)s %(message)s')

'''
Useful references
https://github.com/1/python-youtube-library
https://developers.google.com/youtube/2.0/developers_guide_protocol_playlists#Retrieving_playlists
https://wiki.videolan.org/How_to_Batch_Encode/
https://wiki.videolan.org/Transcode/
'''

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--gui', help='Show VLC gui when transcoding files')
    parser.add_argument('playlist_id',   help='Playlist ID')
    parser.add_argument('--title', nargs=1, help='Alternative Title for the Playlist')
    
    playlist = get_playlist(args.playlist_id)
    download_playlist(playlist, args.title, args.gui)

    #test_suite()
    

def download_playlist(playlist, title=None, gui_enabled=False, audio_format='ogg'):
    ''' Download entire youtube playlist. 
    playlist - Youtube playlist object.See yt library

    title - an optional title can be given, if no title is given then title of the 
    playlist is used. The title is used in each individual video and a number is 
    appended to the end.

    gui_enabled - enables the VLC gui. This is turned off by default
    
    audio_format - currently only ogg can be accepted. This switch is for future use
    '''

    if title == None:
        title = playlist.title.replace(' ', '_')
    dst_dir = setup_output_dir(title)
    
    #Video Sequence
    i = 1

    for video in playlist.videos:
        #Setup audio file name
        video.title = dst_dir + '/' + title + '_' + str(i) + '.' + audio_format
        print video.title + '\t' + video.id 

        #Download video and transcode
        youtube_URL = getURL(video)
        download_audio(youtube_URL, gui_enabled, video.title)
        
        i = i + 1

def download_audio(src_stream, gui_enabled, dst_file='out.mp3'):
    ''' 
    Takes the stream input and extracts the audio and creates an mp3 file using VLC
    '''
    #require quotations due to spaces    
    vlc_path = '"C:\Program Files (x86)\VideoLAN\VLC\VLC.exe"' 
    
    if gui_enabled = True:
        gui_screen = ''
    else:
        gui_screen = '-I dummy'

    # Transcode to MP3. Will quit VLC on completion
    vlc_options = transcode_ogg(src_stream, dst_file)
    cmd = vlc_path  + ' ' + gui_screen + ' ' + src_stream + ' ' + vlc_options  +  'vlc://quit'

    try:
        subprocess.call(cmd)
    except CalledProcessError:
        logging.error('Unable to execute VLC command. VLC command:\n\t' + cmd)
        print "Unable to find or execute VLC"


def transcode_ogg(src_stream, dst_file='out.ogg'):
    '''
    VLC options for transcoding to ogg format
    See https://wiki.videolan.org/Transcode/ for more information
    '''
    ogg_encoded = ' -vvv --no-video --sout "#transcode{vcodec=none,acodec=vorb,ab=128,channels=2,samplerate=44100}:std{access=file,mux=ogg,dst="' + dst_file + '"}"  '
    return ogg_encoded 


def transcode_mp3(src_stream, dst_file='out.ogg'):
    '''
    VLC options for transcoding to mp3 format.
    NOTE: currently mp3 causes vlc to crash randomly due to an unhandled exception(16/08/2014).
    
    See https://wiki.videolan.org/Transcode/ for more information
    '''
    mp3_encoded = ' -vvv --no-video --sout "#transcode{vcodec=none,acodec=mp3,ab=128,channels=2,samplerate=44100}:std{access=file,mux=dummy,dst="' + dst_file + '"}"  '
    return mp3_encoded


def get_playlist(playlist_id):
    playlist = yt.Playlist(playlist_id)
    return playlist


def setup_output_dir(dir_name):
    try:
        os.mkdir(dir_name)
    except OSError:
        logging.warning("Output directory already exists, files may be overwritten:\n\t " +
                        "Directory: " + os.getcwd() + '/' + dir_name)
    os.chdir(dir_name)
    new_dir_path = os.getcwd()
    os.chdir("../")
    return new_dir_path



def getURL(video, secure=True):
    protocol = 'https'
    
    if secure == False:
        protocol = 'http'

    youtube_base_URL = protocol + '://www.youtube.com/watch?v='

    youtube_URL = youtube_base_URL + video.id
    return youtube_URL


#################### TESTS #########################

# Testing Transcoding using VLC
def test1():
    link = "test.mp3"
    download_audio(link)

def test2():
    link = "test.mp3"
    download_audio(link, "testing.mp3")


#Testing download and transcoding of audio book
def test3():
    link = "http://www.youtube.com/watch?v=QqLHtThwPrc&list=PLF117E70FAE81AF65"
    dst_file = 'test2.ogg'
    download_audio(link, dst_file)


# Testing playlist library
def test4():
    playlist_id = 'PLF117E70FAE81AF65'
    playlist = get_playlist(playlist_id)
    download_playlist(playlist)


#Testing Downloading and transcoding of Playlist
def test5():
    playlist_id = 'PLF117E70FAE81AF65'

    dst_dir = setup_output_dir("Test")
    print dst_dir

def test_suite():
#    test1()
#    test2()
   # test3()
    test4()
   # test5()

main()






