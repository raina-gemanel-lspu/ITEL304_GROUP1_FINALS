from kivy.event import EventDispatcher
from kivy.properties import (
    StringProperty,
    NumericProperty,
    BooleanProperty,
)


class Player(EventDispatcher):
    name = StringProperty("")
    money = NumericProperty(0)
    bet = NumericProperty(1)
    money_won = NumericProperty(0)
    bug_bet = StringProperty("")
    active = BooleanProperty(False)
    looser = BooleanProperty(False)
    money_won_color = StringProperty("")

    START_MONEY = 1000

    def update(self, bug_winner):
        if self.active and not self.looser:
            if self.bug_bet == bug_winner.name:
                self.money_won = self.bet * bug_winner.odds
            else:
                self.money_won = -self.bet
            self.money += self.money_won

            if self.money <= 0:
                self.looser = True

    def get_money_won_color(self):
        if self.money_won > 0:
            self.money_won_color = "#00ad00"
        else:
            self.money_won_color = "#ff0000"
