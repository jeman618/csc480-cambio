import random

class Card:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"{self.value}"

class Deck:
    def __init__(self):
        # 1, 11, 12, 13 are A, J, Q, K
        self.cards = (
            [Card("A")] + 
            [Card(v) for v in range(2, 11)] +
            [Card("J"), Card("Q"), Card("K")]
            ) * 4
        print(self.cards)
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()
    
# contains actions player can make
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = [None] * 4
        self.known = [None] * 4

    def set_hand(self, cards):
        self.hand = cards

    def choose_draw(self):
        pass

    def stick(self):
        pass

    def choose_action(self):
        pass

    def choose_discard(self):
        pass

    def call_cambio(self):
        return False

class CambioGame:
    def __init__(self, players):
        self.deck = Deck()
        self.discard = []
        self.players = players
        self.current_player = 0
        self.cambio_called = False
        self.final_round = 0

    # initializes the deck and gives 4 cards to each player
    def deal(self):
        for p in self.players:
            p.set_hand([self.deck.draw() for _ in range(4)])

        for p in self.players:
            p.known[0] = p.hand[0]
            p.known[1] = p.hand[1]

    # switch cards between players
    def swap(self, p1, p2, i1, i2):
        tmp = p1.hand[i1]
        p1.hand[i1] = p2.hand[i2]
        p2.hand[i2] = tmp

    # currently peek your own cards
    def peek(self, player, index):

        if index < 0 or index >= len(player.hand):
            raise ValueError("Invalid peek index")
        
        player.known[index] = player.hand[index]

    def check_cambio(self, player):
        known_sum = sum(c.value for c in player.known if c)
        return known_sum
    
    def calculate_score(self, player):

        result = 0
        for c in player.hand:
            if c.value == "A":
                c.value = 1
            elif c.value == "J":
                c.value = 0
            elif c.value == "K" or c.value == "Q":
                c.value = 10

            result += c.value

        return result
    
    # tallies final score
    def score_game(self):
        w_score = 1000
        w_name = ""

        for p in self.players:
            current = self.calculate_score(p)
            if current < w_score:
                w_score = current
                w_name = p.name

        return f"\"{w_name}\" wins with a score of {w_score}!"
    
    # "it is the next player's turn now"
    def advance_turn(self):
        pass

    def game_over(self):
        return self.final_round is False

    def play_turn(self):
        player = self.players[self.current_player]
        self.advance_turn()
    
    def play(self):
        i = 1
        while not self.game_over():
            print("Round {i}")
            self.play_turn()
            i += 1
        return self.score_game()

# tests some functions
def test():
    p1, p2 = Player("JIM"), Player("BOB")
    game = CambioGame([p1, p2])
    game.deal()
    print(p1.hand)
    print(p2.hand)
    game.swap(p1, p2, 0, 2)
    print(p1.hand)
    print(p2.hand)
    
    game.peek(p1, 2)
    
    print(game.score_game())
    assert len(p1.hand) == 4

if __name__ == "__main__":
    test()
    p1, p2 = Player("A"), Player("B")
    print("test successful!")
