# Gra w karty wojna
# Od 1 do 7 graczy współzawodniczy między sobą

import karty, gry

class W_Card(karty.Card):
    """Karta do gry w wojnę"""

    @property
    def value(self):
        v = W_Card.RANKS.index(self.rank) + 1
        if v > 10:
            v = 10
        return v

class W_Deck(karty.Deck):
    """Talia kart do gry w wojnę"""

    def __str__(self):
        return "Liczba kart pozostałych w talii: " + str(self.cards_in_deck)

    def populate(self):
        for suit in W_Card.SUITS: 
            for rank in W_Card.RANKS: 
                self.cards.append(W_Card(rank, suit))

    @property
    def cards_in_deck(self):
        #ile pozostało kart w talii
        cards_in_deck = len(self.cards)
        return cards_in_deck

class W_Hand(karty.Hand):
    """Wyłożone karty w wojnie"""
    def __init__(self, name):
        super(W_Hand, self).__init__()
        self.name = name

    def __str__(self):
        rep = self.name + ":\t" + super(W_Hand, self).__str__()  
        if self.cards:
            rep += "(" + str(self.cards[-1].value) + ")"        
        return rep

    
class W_Player(W_Hand):
    """Gracz w wojnie"""
    def is_continuing(self):
        response = gry.ask_yes_no("\n" + self.name + ", chcesz grać dalej? (T/N): ")
        return response == "t"

##    @property
##    def is_looser(self):
##        max_value =  W_Game.max_value()
##        print(max_value)
##        return self.cards[-1].value < max_value
    
    def lose(self):
        print(self.name, "przegrywa.")
       

    def win(self):
        print(self.name, "wygrywa.")

    def push(self):
        print(self.name, "remisuje.")


class W_Game(object):
    """gra w wojnę"""
    def __init__(self, names):      
        self.players = []
        for name in names:
            player = W_Player(name)
            self.players.append(player)

        self.deck = W_Deck()
        self.deck.populate()
        self.deck.shuffle()

    def is_continuing(self):
        response = gry.ask_yes_no("\nGramy dalej? (T/N): ")
        return response == "t"

   
        
    def current_max_value(self, players):
            values = []
            for player in players:
                if player.cards:
                    values.append(player.cards[-1].value)

            values.sort()
            
            if values:
                return values[-1]
            else:
                return None

    def currently_still_playing(self, players, max_value):
        sp = []
        for player in players:
            if player.cards:
                if player.cards[-1].value == max_value:
                    sp.append(player)        
        if sp:
            return sp
        else:
            return None
        
    @property
    def max_value(self):
        values = []
        for player in self.players:
            values.append(player.cards[-1].value)

        values.sort()
        return values[-1]
    
    @property
    def still_playing(self):
        sp = []
        for player in self.players:
            if player.cards[-1].value == self.max_value:
                    sp.append(player)
        return sp


    def __additional_cards(self, player, deck):
        if deck.cards_in_deck:
            if player in self.still_playing:
                self.deck.deal([player])
                print(player)
        else:
            
            for player in self.players:
                player.clear()
            return None 
                
                    
    def play(self):
        #sprawdź, czy w talii jest co najmniej tyle kart, żeby rozdać każdemu z graczy
        print("\nNOWA GRA")
        print("\nLiczba kart w talii: " + str(self.deck.cards_in_deck)+"\n")
        if self.deck.cards_in_deck < len(self.players):
            print("za mało kart do dalszej gry, muszę przetasować\n")

            self.deck.clear()
            self.deck.populate()
            self.deck.shuffle()
            print("Liczba kart w talii po przetasowaniu: " + str(self.deck.cards_in_deck))

        # rozdaj każdemu graczowi początkową kartę
        self.deck.deal(self.players)
        for player in self.players:
            print(player)
            
        # jeśli jest jeden zwycięzca, wskaż go
        if len(self.still_playing) == 1:
            winner = self.still_playing[0]
            winner.win()

            for player in self.players:
                if player not in self.still_playing:
                    player.lose()

        # jeśli jest remis, wyświetl remisujących i przegranych
        else:
            for player in self.still_playing:
                player.push()

            #utwórz listę graczy, którzy zremisowali
            push_players = self.still_playing

            #utwórz listę graczy, którzy przegrali
            loosers = set(self.players).difference(set(self.still_playing))
            for player in loosers:
                player.lose()
            
            #dogrywka, rozdaj dodatkowe karty  
            winners = push_players       
            while len(winners) > 1 and self.is_continuing(): # jeśli gra ma być kontynuowana
                for player in winners:
                   self.__additional_cards(player, self.deck)

                
                if not self.deck.cards_in_deck:
                    print("Zabrakło dodatkowych kart dla graczy - kończymy grę")
                    return None
                
                current_max_value = self.current_max_value(winners)
                winners = self.currently_still_playing(winners, current_max_value)
                loosers = set(push_players).difference(set(winners))

                # jeśli jest jeden zwycięzca, wskaż go
                if len(winners) == 1:
                    winners[0].win()
                else:
                    push_players = winners
                    for player in winners:
                        player.push()
                        
                        
                    
                #wskaż graczy, którzy po remisie przegrali
                for player in loosers:
                    player.lose()

        # na koniec usuń karty wszystkich graczy
        for player in self.players:
            player.clear()
                
            

def main():

    print("\t\tWitaj w grze 'Wojna'!\n")
    
    names = []
    number = gry.ask_number("Podaj liczbę graczy (1 - 7): ", low = 1, high = 8)
    for i in range(number):
        name = input("Wprowadź nazwę gracza: ")
        names.append(name)
    print()
        
    game = W_Game(names)

    again = None
    while again != "n":
        game.play()
        again = gry.ask_yes_no("\nCzy chcesz zagrać ponownie?: ")

main()
input("\n\nAby zakończyć program, naciśnij klawisz Enter.")
