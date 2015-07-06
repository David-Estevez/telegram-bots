#################################################
### MediaPlayer
#################################################
###
### Control a MediaPlayer using dbus
###
#################################################

import dbus

__author__ = 'def'

class MediaPlayer:

    dbus_object_name = 'org.mpris.MediaPlayer2'

    def __init__(self):
        pass

        # Create objects required:
        self.connected = False
        self.bus = None
        self.root_dbus = None
        self.root_iface = None
        self.media_player = None
        self.player_iface = None
        self.tracklist_iface = None
        self.properties_iface = None

        self.connect_to_dbus()

    def connect_to_dbus(self):
        # Connect to session dbus:
        self.bus = dbus.SessionBus()
        self.root_dbus = self.bus.get_object('org.freedesktop.DBus', '/org/freedesktop/DBus')
        self.root_iface = dbus.Interface(self.root_dbus, 'org.freedesktop.DBus')

    def list_players_available(self):
        if self.root_iface:
            players = [name for name in self.root_iface.ListNames() if self.dbus_object_name in name]
        else:
            raise Exception("Not connected to dbus!!")
        return players

    def connect_to_player(self, id=None):
        available = self.list_players_available()
        selected = None
        if id:
            for player in available:
                if id in player:
                    selected = player
                    break
        else:
            selected = available[0]

        # Connect to selected player
        try:
            self.media_player = self.bus.get_object(selected, '/'+self.dbus_object_name.replace('.', '/'))
            self.player_iface = dbus.Interface(self.media_player, self.dbus_object_name+'.Player')
            self.tracklist_iface = dbus.Interface(self.media_player, self.dbus_object_name+'.TrackList')
            self.properties_iface = dbus.Interface(self.media_player, 'org.freedesktop.DBus.Properties')

            self.connected = True

        except Exception, e:
            print e
            self.connected = False

        return self.connected



    def play(self):
        if self.connected:
            self.player_iface.Play()
        else:
            raise Exception("Not connected to player!")

    def pause(self):
        if self.connected:
            self.player_iface.Pause()
        else:
            raise Exception("Not connected to player!")

    def next(self):
        if self.connected:
            self.player_iface.Next()
        else:
            raise Exception("Not connected to player!")

    def previous(self):
        if self.connected:
            self.player_iface.Previous()
        else:
            raise Exception("Not connected to player!")

    def current_song(self):
        pass


if __name__ == '__main__':
    import time as t

    player = MediaPlayer()
    if player.connect_to_player():
        player.play()
        t.sleep(5)
        player.next()
        t.sleep(5)
        player.previous()
        t.sleep(5)
        player.pause()
