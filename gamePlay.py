import pydealer
from os import system, name
import time


def find_list(deck, rank):
    list_of_cards = []
    # print(deck)
    for card in deck:
        type(card)
        if card.value.lower() == rank.lower():
            list_of_cards.append(card)
    return list_of_cards

def get_list(deck, rank):
    list_of_cards = []
    card_indexes = []
    # print(len(deck))
    for i in range(0,len(deck)):
        if deck[i].value.lower() == rank.lower():
            card_indexes.append(i)
    card_indexes.reverse()
    for i in card_indexes:
        list_of_cards.append(deck.get(i)[0])

    return list_of_cards

class Player:
    def __init__(self, name, deck, n_players):
        n_cards = 5 if n_players > 3 else 7
        self.hand = deck.deal(n_cards)
        self.name = name
        self.n_fours = 0

    def see_hand(self):

        print(self.name + "'s deck:")
        print("[")
        print(self.hand)
        print("]")
        print("Current number of fours : " + str(self.n_fours))

    def give_cards(self, rank):
        return get_list(self.hand, rank)

    def add_cards(self, cards):
        self.hand.add(cards)
        # print("ADDED CARDS")
        # print(self.hand)
        self.store_away()

    def store_away(self):
        RANKS = pydealer.POKER_RANKS["values"].keys()
        for r in RANKS:
            if len(find_list(self.hand,r)) == 4:
                get_list(self.hand,r)
                self.n_fours += 1
                print(self.name + " now has 4 " + r + " cards!")


    def draw_from_deck(self, deck, n_cards):
        if n_cards > len(deck):
            n_cards = len(deck)
        new_cards = deck.deal(n_cards)
        self.hand.add(new_cards)
        print("Cards(s) added to " + self.name + "'s deck: ")
        for nc in new_cards:
            print(nc)
        self.store_away()

    def hide_deck(self):
        print("Hiding your deck so next player's turn can begin...")
        for i in range(5,0,-1):
            time.sleep(1)
            print(str(i) + "..." )
        system('cls' if name == 'nt' else 'clear')
        print(self.name + "'s deck is now hidden")

    def hasRank(self,rank):
        if len(find_list(self.hand,rank)) > 0:
            return True
        else:
            return False

class goFish:
    def __init__(self, list_of_players):
        self.deck = pydealer.Deck()
        self.deck.shuffle()
        self.players = {}
        self.list_of_players = list_of_players
        self.n_players = len(list_of_players)
        for player_name in list_of_players:
            self.players[player_name.lower()] = Player(player_name.lower(), self.deck, self.n_players)

    def ask_cards(self, asker_name, askee_name, rank):
        asker = self.players[asker_name]
        askee = self.players[askee_name]
        askee_rank_cards = askee.give_cards(rank)
        if len(askee_rank_cards) > 0:
            print(askee_name + " gave you their" + str(askee_rank_cards) + " cards. ")
            asker.add_cards(askee_rank_cards)
            return True
        else:
            print("Go Fish!")
            asker.draw_from_deck(self.deck, 1)
            return False

    def play(self):
        i = 0
        while(len(self.deck) > 0 or self.players_have_cards()):
            player = self.players[self.list_of_players[i % self.n_players]]
            print(player.name + "'s TURN!")
            if len(player.hand)==0:
                print("Hand is empty so will draw cards.")
                player.draw_from_deck(self.deck, 5)
            player.see_hand()
            print("Type in the player and the suit you want to ask from them")
            print("Example format: Meg Queen")
            print("Example format: Vicky 10")
            user_input = input().split(" ")
            while(len(user_input) != 2):
                print("Invalid input. Please follow the format given.")
                user_input = input().split(" ")
            other_player_name, rank = user_input
            while(other_player_name not in self.list_of_players or player.hasRank(rank)==False):
                if other_player_name not in self.list_of_players:
                    print("Player not in game, try again")
                elif player.hasRank(rank)==False:
                    print("You can't ask for a rank you don't have, try again")
                other_player_name, rank = input().split(" ")
            if self.ask_cards(player.name, other_player_name, rank):
                print(player.name + " gets to go again!")
            else:
                i += 1
                player.hide_deck()

        most_fours = 0
        for p in self.players.keys():
            if self.players[p].n_fours > most_fours:
                most_fours = self.players[p].n_fours
        winners = []
        for p in self.players.keys():
            if self.players[p].n_fours == most_fours:
                winners.append(p)
        print("Winner(s):")
        print(winners)

    def players_have_cards(self):
        for p in self.list_of_players:
            if len(self.players[p].hand) > 0:
                return True
        return False


def main():
    print("Name all players in one line:")
    print("Example format: Meg Vicky")
    list_of_players = input().split(" ")
    while (len(list_of_players) < 2):
        print("There needs to be more than 1 player!")
        list_of_players = input().split(" ")
    g = goFish(list_of_players)
    g.play()

print("Name all players in one line:")
print("Example format: Meg Vicky")
list_of_players = input().split(" ")
while(len(list_of_players) < 2):
    print("There needs to be more than 1 player!")
    list_of_players = input().split(" ")
g = goFish(list_of_players)
g.play()
