from typing import List

class Card:
    def __init__(self, role: str):
        self.role = role
        self.revealed = False
    
    def reveal(self):  # Encapselate setting reveal to true encase we need to trigger events based on this action.
        self.revealed = True

    def __repr__(self):
        return f"{'❌' if self.revealed else '🕶️'} {self.role}"


class Player:
    def __init__(self, name: str):
        self.name = name
        self.cards: List[Card] = []
        self.credits = 2
        self.alive = True

    def lose_card(self, role: str = None):
        unrevealed_cards = [card for card in self.cards if not card.revealed] #creates list of unrevealed cards

        if not unrevealed_cards:
            return                #Stops logic if player has no unrevealed cards

        if role:                            #is a role is spesified, it searches for that role and Reveals that card. 
            for card in unrevealed_cards:
                if card.role == role:
                    card.reveal()
                    break
        else:                                                  #if a role isn't spesified when method is called. the user is asked to choose. 
            print(f"{self.name}, choose a card to lose:")
            for i, card in enumerate(unrevealed_cards):
                print(f"{i}: {card.role}")
            choice = int(input("Enter the number of the card to reveal: "))
            unrevealed_cards[choice].reveal()

        self.check_if_alive()
    
    def has_role(self, role: str): #method to check if a player has a role that isn't already revealed 
        return any(not card.revealed and card.role == role for card in self.cards)
    
    # Commenting out becasue this is now redundent 
    
    # def reveal_role(self, role: str):
    #     for card in self.cards:
    #         if not card.revealed and card.role == role:
    #             card.reveal()
    #             return True
    #     return False

    def check_if_alive(self):
        self.alive = any(not card.revealed for card in self.cards)

    def add_card(self, card: Card):
        self.cards.append(card)

    def __repr__(self):
        return f"{self.name} ({self.credits} credits) - {self.cards}"
