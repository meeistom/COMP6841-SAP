import vlc
from time import sleep
from urllib.parse import quote

def play_rtsp_stream(rtsp_url):
    # Create an instance of the VLC player
    instance = vlc.Instance()
    
    # Create a new media player
    player = instance.media_player_new()

    # Create a media object for the RTSP stream
    media = instance.media_new(rtsp_url)

    # Set the media for the player
    player.set_media(media)

    # Start playing the RTSP stream
    player.play()

    # Keep the script running to allow the player to keep playing
    while True:
        state = player.get_state()
        if state == vlc.State.Ended:
            print("Stream has ended.")
            break
        elif state == vlc.State.Error:
            print("Error occurred.")
            break
        # Give some time for the media to load
        sleep(1)

if __name__ == "__main__":
    # Replace this with your RTSP URL

    username = quote('admin')
    password = quote('123456')

    rtsp_url = f"rtsp://{username}:{password}@192.168.0.129:554/ch01/0"
    
    # Start playing the stream
    play_rtsp_stream(rtsp_url)
