from kivy.properties import NumericProperty, StringProperty
from kivy.animation import Animation

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog


class BetWidget(MDBoxLayout):
    player_name = StringProperty("")
    player_money = NumericProperty(0)
    bet_value = NumericProperty(0)
    max_bet_value = NumericProperty(0)
    bet_bug = StringProperty("")
    player_group = StringProperty("")
    start_pos = NumericProperty(0)

    def update_player_bet(self, player):
        player.bet = self.bet_value

    def update_player_bug(self, player):
        player.bug_bet = self.bet_bug

    def animate(self):
        anim = Animation(
            pos_hint={'center_x': .5},
            duration=1)
        anim.start(self)
        
class GameResults(MDBoxLayout):
    pass


class AlertDialog(MDBoxLayout):
    pass


class BetsScreen(MDScreen):
    dialog = None
    alert_dialog = None

    def clear_bets(self):
        for bet in self.bets:
            for checkbox in bet.checkboxes:
                if checkbox.active:
                    checkbox.active = False
            bet.animate()

    def on_enter(self):
        self.clear_bets()
        if self.game.game_is_over:
            self.game.game_over()
            self.show_game_results()
            self.game.sound_main_theme.stop()
            self.game.sound_game_over.play()
            self.dialog.content_cls.ids.winner.text = f"{self.game.winner_text}"

    def show_alert_dialog(self):
        if not self.alert_dialog:
            self.alert_dialog = MDDialog(
                radius=[20, 20, 20, 20],
                type="custom",
                content_cls=AlertDialog(),
                auto_dismiss=False,
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_release=lambda _: self.alert_dialog.dismiss(),
                    ),
                ],
            )
        self.alert_dialog.open()

    def go_race_btn(self):
        players_with_bugs = [
            player for player in self.game.players if player.bug_bet != ""
        ]
        if len(players_with_bugs) == len(self.game.players):
            self.game.current = "race_screen"
        else:
            self.show_alert_dialog()
            self.game.sound_fail.play()

    def show_game_results(self):
        if not self.dialog:
            self.dialog = MDDialog(
                auto_dismiss=False,
                type="custom",
                content_cls=GameResults(),
                radius=[20, 20, 20, 20],
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_release=lambda _: self.game_results_ok_btn(),
                    ),
                ],
            )
        self.dialog.open()

    def game_results_ok_btn(self):
        self.game.reset()
        self.dialog.dismiss()
        self.game.sound_game_over.stop()
        self.game.sound_game_over = self.game.sound_game_win
        self.game.sound_main_theme.play()
        self.game.current = "welcome_screen"

    def on_leave(self):
        for bet in self.bets:
            bet.pos_hint = {'center_x': bet.start_pos}