import os
import platform

if platform.system() == 'Windows':
    import win32gui
    import win32api
elif platform.system() == 'Linux':
    import dbus

###Virtual-KeyCodes###
Media_Next = 0xB0
Media_Previous = 0xB1
Media_Pause = 0xB3  # Play/Pause
Media_Mute = 0xAD


class Spotify(object):

    @staticmethod
    def linux_status():
        try:
            session_bus = dbus.SessionBus()
            spotify_bus = session_bus.get_object("org.mpris.MediaPlayer2.spotify",
                                                 "/org/mpris/MediaPlayer2")
            spotify_properties = dbus.Interface(spotify_bus,
                                                "org.freedesktop.DBus.Properties")
            status = spotify_properties.Get("org.mpris.MediaPlayer2.Player",
                                            "PlaybackStatus")
            return status
        except:
            return "Paused"

    @staticmethod
    def song_info_linux():
        if Spotify.linux_status() == "Playing":
            session_bus = dbus.SessionBus()
            spotify_bus = session_bus.get_object("org.mpris.MediaPlayer2.spotify",
                                                 "/org/mpris/MediaPlayer2")
            spotify_properties = dbus.Interface(spotify_bus,
                                                "org.freedesktop.DBus.Properties")
            metadata = spotify_properties.Get(
                "org.mpris.MediaPlayer2.Player", "Metadata")
            song_info = metadata['xesam:title']
            return song_info
        else:
            return "There is nothing playing at this moment"

    @staticmethod
    def artist_info_linux():
        if Spotify.linux_status() == "Playing":
            session_bus = dbus.SessionBus()
            spotify_bus = session_bus.get_object("org.mpris.MediaPlayer2.spotify",
                                                 "/org/mpris/MediaPlayer2")
            spotify_properties = dbus.Interface(spotify_bus,
                                                "org.freedesktop.DBus.Properties")
            metadata = spotify_properties.Get(
                "org.mpris.MediaPlayer2.Player", "Metadata")
            artist_info = metadata['xesam:artist'][0]
            return artist_info
        else:
            return "There is nothing playing at this moment"

    @staticmethod
    def getwindow(Title="SpotifyMainWindow"):
        window_id = win32gui.FindWindow(Title, None)
        return window_id

    @staticmethod
    def song_info():
        try:
            song_info = win32gui.GetWindowText(Spotify.getwindow())
        except:
            pass
        return song_info

    @staticmethod
    def artist():
        if platform.system() == 'Windows':
            try:
                temp = Spotify.song_info()
                artist, song = temp.split("-", 1)
                artist = artist.strip()
                return artist
            except:
                return "There is nothing playing at this moment"
        elif platform.system() == 'Linux':
            try:
                return Spotify.artist_info_linux()
            except:
                return "There is nothing playing at this moment"

    @staticmethod
    def song():
        if platform.system() == 'Windows':
            try:
                temp = Spotify.song_info()
                artist, song = temp.split("-", 1)
                song = song.strip()
                return song
            except:
                return "There is nothing playing at this moment"
        elif platform.system() == 'Linux':
            try:
                return Spotify.song_info_linux()
            except:
                return "There is nothing playing at this moment"

    ###SpotifyBlock###

    @staticmethod
    def createfolder(folder_path=r"C:\SpotiBlock"):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        else:
            pass

    @staticmethod
    def createfile(file_path=r"C:\SpotiBlock\Block.txt"):
        if not os.path.exists(file_path):
            file = open(file_path, "a")
            file.write("ThisFirstLineWillBeIgnoredButIsNecessaryForUse")

    @staticmethod
    def blocklist(file_path=r"C:\SpotiBlock\Block.txt"):
        block_list = []
        for line in open(file_path, "r"):
            if not line == "":
                block_list.append(line.strip())
        return block_list

    @staticmethod
    def add_to_blocklist(file_path=r"C:\SpotiBlock\Block.txt"):
        with open(file_path, 'a') as text_file:
            text_file.write("\n" + Spotify.song_info())

    @staticmethod
    def reset_blocklist(file_path=r"C:\SpotiBlock\Block.txt"):
        with open(file_path, 'w') as text_file:
            text_file.write("ThisFirstLineWillBeIgnored")
            pass

    @staticmethod
    ###Media Controls###
    def hwcode(Media):
        hwcode = win32api.MapVirtualKey(Media, 0)
        return hwcode

    @staticmethod
    def next():
        if platform.system() == 'Linux':
            bus = dbus.SessionBus()
            proxy = bus.get_object(
                'org.mpris.MediaPlayer2.spotify', '/org/mpris/MediaPlayer2')
            interface = dbus.Interface(
                proxy, dbus_interface='org.mpris.MediaPlayer2.Player')
            interface.Next()
        elif platform.system() == 'Windows':
            win32api.keybd_event(Media_Next, Spotify.hwcode(Media_Next))

    @staticmethod
    def previous():
        if platform.system() == 'Linux':
            bus = dbus.SessionBus()
            proxy = bus.get_object(
                'org.mpris.MediaPlayer2.spotify', '/org/mpris/MediaPlayer2')
            interface = dbus.Interface(
                proxy, dbus_interface='org.mpris.MediaPlayer2.Player')
            interface.Previous()
        elif platform.system() == 'Windows':
            win32api.keybd_event(Media_Previous, Spotify.hwcode(Media_Previous))

    @staticmethod
    def pause():
        if platform.system() == 'Linux':
            bus = dbus.SessionBus()
            proxy = bus.get_object(
                'org.mpris.MediaPlayer2.spotify', '/org/mpris/MediaPlayer2')
            interface = dbus.Interface(
                proxy, dbus_interface='org.mpris.MediaPlayer2.Player')
            interface.PlayPause()
        elif platform.system() == 'Windows':
            win32api.keybd_event(Media_Pause, Spotify.hwcode(Media_Pause))

    @staticmethod
    def play():
        if platform.system() == 'Linux':
            bus = dbus.SessionBus()
            proxy = bus.get_object(
                'org.mpris.MediaPlayer2.spotify', '/org/mpris/MediaPlayer2')
            interface = dbus.Interface(
                proxy, dbus_interface='org.mpris.MediaPlayer2.Player')
            interface.PlayPause()
        elif platform.system() == 'Windows':
            win32api.keybd_event(Media_Pause, Spotify.hwcode(Media_Pause))

    @staticmethod
    def mute():
        win32api.keybd_event(Media_Mute, Spotify.hwcode(Media_Mute))
