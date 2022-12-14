from kivymd.app import MDApp

from kivy.lang import Builder
from kivy.core.audio import SoundLoader
from kivy.core.text import LabelBase
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import (
    NumericProperty,
    StringProperty,
    BooleanProperty,
    ListProperty,
)

from player import Player

Builder.load_file("bug.kv")
Builder.load_file("race_screen.kv")
Builder.load_file("bets_screen.kv")
Builder.load_file("welcome_screen.kv")


class Game(ScreenManager):
    current_number_of_races = NumericProperty(0)
    total_number_of_races = NumericProperty(0)
    number_of_players = NumericProperty(0)
    winners = ListProperty()
    winner_text = StringProperty("")
    game_is_over = BooleanProperty(False)
    sound_on = BooleanProperty(True)
    sound_game_over = None

    player1 = Player()
    player2 = Player()
    player3 = Player()
    player4 = Player()

    possible_players = [player1, player2, player3, player4]
    players = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.sound_main_theme = SoundLoader.load("sounds/main.wav")
        self.sound_race = SoundLoader.load("sounds/race.wav")
        self.sound_race_win = SoundLoader.load("sounds/race_win.wav")
        self.sound_bankrupt = SoundLoader.load("sounds/bankrupt.wav")
        self.sound_game_win = SoundLoader.load("sounds/game_win.wav")
        self.sound_fail = SoundLoader.load("sounds/fail.wav")

        self.sounds = [
            self.sound_main_theme,
            self.sound_race,
            self.sound_race_win,
            self.sound_bankrupt,
            self.sound_game_win,
            self.sound_fail,
        ]

        self.sound_game_win.volume =.8
        self.sound_main_theme.volume = .5
        self.sound_main_theme.loop = True
        self.sound_main_theme.play()
        self.sound_game_over = self.sound_game_win

    def remove_looser_players(self):
        self.players = [player for player in self.players if not player.looser]

    def game_over(self):
        self.winners = []

        # all players lost money
        if len(self.players) == 0:
            self.sound_game_over = self.sound_bankrupt

            # 1-player mode
            if self.number_of_players == 1:
                self.winner_text = (
                    "[b]You[/b] lost all your money. Better luck next time!"
                )

            # multi-player mode
            else:
                self.winner_text = (
                    "[b]All players [/b] are bankrupt. There is no winner."
                )

        # one player left in multi-player mode
        elif len(self.players) == 1 and self.number_of_players > 1:
            winner = self.players[0]
            self.winner_text = (
                f"The winner is [b]{winner.name}[/b]! "
                f"He's the only player with any money."
            )

        # after a given number of races
        elif self.current_number_of_races == self.total_number_of_races:
            if self.number_of_players == 1:
                winner = self.players[0]
                self.winner_text = (
                    f"[b]You[/b] having started at ${winner.START_MONEY} "
                    f"and ending at ${winner.money}. It's a success!"
                )
            else:
                max_money = (max(*self.players, key=lambda player: player.money)).money
                self.winners = [
                    player for player in self.players if player.money == max_money
                ]

                # one winner
                if len(self.winners) == 1:
                    winner = self.winners[0]
                    self.winner_text = (
                        f"The winner is [b]{winner.name}[/b]!\n"
                        f"Having started at ${winner.START_MONEY} and winning at ${winner.money}."
                    )

                # joint winners
                else:
                    self.winner_text = "There's a tie. The joint winners are:\n\n"
                    for winner in self.winners:
                        self.winner_text += (
                            f"[b]{winner.name}[/b] having started at ${winner.START_MONEY} "
                            f"and winning at ${winner.money}.\n"
                        )

    def gameover_check(self):
        if (
            len(self.players) == 0
            or len(self.players) == 1
            and self.number_of_players > 1
            or self.current_number_of_races == self.total_number_of_races
        ):
            self.game_is_over = True

    def reset(self):
        self.game_is_over = False
        self.current_number_of_races = 0
        self.players = []
        for player in self.possible_players:
            player.name = ""
            player.active = False
            player.looser = False


class LadybugApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.primary_hue = "800"
        self.root = FloatLayout()
        self.root.add_widget(Game())
        return self.root


if __name__ == "__main__":
    LabelBase.register(
        name="Rubik",
        fn_regular="fonts/Rubik-Regular.ttf",
        fn_bold="fonts/Rubik-Bold.ttf",
        fn_italic="fonts/Komika_display.ttf",
    )
    LadybugApp().run()
