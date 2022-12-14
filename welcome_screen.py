from kivy.uix.screenmanager import Screen

from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout


class PlayersNames(MDBoxLayout):
    pass


class WelcomeScreen(Screen):
    dialog = None

    def show_playersnames_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                radius=[20, 20, 20, 20],
                type="custom",
                auto_dismiss=False,
                content_cls=PlayersNames(),
                buttons=[
                    MDFlatButton(
                        text="OK", on_release=lambda _: self.show_bets_screen()
                    ),
                ],
            )
        self.dialog.open()

    def show_bets_screen(self):
        if self.dialog.content_cls.ids.player1_name.text != "":
            self.game.player1.active = True
            self.game.player1.name = self.dialog.content_cls.ids.player1_name.text
            self.game.player1.money = self.game.player1.START_MONEY
            self.game.players.append(self.game.player1)
            if self.dialog.content_cls.ids.player2_name.text != "":
                self.game.player2.active = True
                self.game.player2.name = self.dialog.content_cls.ids.player2_name.text
                self.game.player2.money = self.game.player2.START_MONEY
                self.game.players.append(self.game.player2)
            if self.dialog.content_cls.ids.player3_name.text != "":
                self.game.player3.active = True
                self.game.player3.name = self.dialog.content_cls.ids.player3_name.text
                self.game.player3.money = self.game.player3.START_MONEY
                self.game.players.append(self.game.player3)
            if self.dialog.content_cls.ids.player4_name.text != "":
                self.game.player4.active = True
                self.game.player4.name = self.dialog.content_cls.ids.player4_name.text
                self.game.player4.money = self.game.player4.START_MONEY
                self.game.players.append(self.game.player4)
            self.game.number_of_players = len(self.game.players)
            self.game.total_number_of_races = (
                self.dialog.content_cls.ids.game_slider.value
            )
            self.dialog.dismiss()
            self.game.current = "bets_screen"

    def mute_unmute(self):
        if self.game.sound_on:
            self.game.sound_on = False
            self.ids.sound_btn.icon = "volume-off"
            for sound in self.game.sounds:
                sound.default_volume = sound.volume
                sound.volume = 0
        else:
            self.game.sound_on = True
            self.ids.sound_btn.icon = "volume-high"
            for sound in self.game.sounds:
                sound.volume = sound.default_volume
