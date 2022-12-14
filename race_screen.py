from operator import itemgetter

from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.animation import Animation

from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

class Stopwatch(BoxLayout):
    def animate(self):
        anim = Animation(
            pos_hint={'center_x': .5},
            duration=.5)
        anim.start(self)
    
    
class RaceResults(FloatLayout):
    pass


class RaceScreen(Screen):
    dialog = None
    bug_red = ObjectProperty(None)
    bug_green = ObjectProperty(None)
    bug_blue = ObjectProperty(None)
    bug_orange = ObjectProperty(None)
    winner_bug = ObjectProperty(None)
 
    def on_enter(self):
        self.bug_red.name = "Red"
        self.bug_green.name = "Green"
        self.bug_blue.name = "Blue"
        self.bug_orange.name = "Orange"
        self.finish_line = 0.9 * self.height
        self.start_line = 0.1 * self.height
        self.event = Clock.schedule_interval(self.update, 1 / 60)
        self.game.sound_race.play()
        self.stopwatch.animate()

    def update(self, dt):
        for bug in self.bugs:
            bug.move(self.finish_line)
        for i in range(4):
            self.stopwatch.stopwatches[i].text = self.race_stopwatch(self.bugs[i])        

        if (
            self.bug_red.finished
            and self.bug_green.finished
            and self.bug_blue.finished
            and self.bug_orange.finished
        ):
            self.event.cancel()
            self.game.sound_race.stop()
            self.game.sound_race_win.play()
            self.get_winner()
            self.game.current_number_of_races += 1
            for player in self.game.players:
                player.update(self.winner_bug)
                player.get_money_won_color()
            self.game.remove_looser_players()
            self.game.gameover_check()
            
            self.show_race_results()
            self.dialog.content_cls.ids.race_winner.text = (
                f"[b][color={self.winner_bug.color}]{self.winner_bug.name}"
                f"[/color][/b] is win the race!"
            )
            for i in range(4):
                if self.game.possible_players[i].active:
                    self.dialog.content_cls.results_labels[i].text = self.race_result(self.game.possible_players[i])

    def race_stopwatch(self, bug):
        text = f"{bug.name}  {bug.stopwatch()}"
        return text
        
    def get_winner(self):
        race_results = {}
        race_results_sorted = {}
        for bug in self.bugs:
            race_results[bug.name] = bug.finish_time
        sorted_tuples = sorted(race_results.items(), key=itemgetter(1))
        race_results_sorted = {k: v for k, v in sorted_tuples}
        bug_winner_name = next(iter(race_results_sorted))
        for bug in self.bugs:
            if bug.name == bug_winner_name:
                self.winner_bug = bug
        self.winner_bug.get_color()
        
    def race_result(self, player):
        text = (
            f"{player.name}   [color={player.money_won_color}]"
            f"{player.money_won}[/color]   "
            f"${player.money}"
        )
        return text

    def show_race_results(self):
        if not self.dialog:
            self.dialog = MDDialog(
                auto_dismiss=False,
                radius=[20, 20, 20, 20],
                type="custom",
                content_cls=RaceResults(),
                buttons=[
                    MDFlatButton(
                        text="OK", on_release=lambda _: self.race_results_ok_btn()
                    ),
                ],
            )
        self.dialog.open()

    def race_results_ok_btn(self):
        for label in self.dialog.content_cls.results_labels:
            label.text = ""
        for player in self.game.possible_players:
            if player.looser:
                player.money_won = 0
        self.dialog.dismiss()
        self.game.sound_race_win.stop()
        self.game.current = "bets_screen"

    def reset(self):
        for bug in self.bugs:
            bug.y = self.start_line - bug.height
            bug.counter = 0
            bug.finished = False
            
        self.stopwatch.pos_hint = {'center_x': 1}

    def on_leave(self):
        self.reset()
