from hand import Hand

class Player:
    """Describes each player object in the game."""

    def __init__(self, name = None):
        """Initialize chips and cards for a player.
        'first_turn' indicates whether it is the first turn of a round."""
        # Other things might need to be initialized.
        self.name = name
        self.chips = 500
        self.hands = []
        self.first_turn = True
        self.turn_over = False
        self.actions = {
            'double': self.double_down, 
            'hit': self.hit, 
            'stand': self.stand, 
            'split': self.split, 
            'surrender': self.surrender
        # Track whether or not player has acted in a way that ends their turn.
        }

    def __str__(self):
        """Return the name of a player, or Player X if not set."""
        if self.name == None:
            return "Human player"
        return self.name

    def show_card(self, card):
        """A function designed to be overridden by clever AI player script. Each card shown to the player (ie. dealt cards to any player) can be recorded. This data can be used for making good decisions."""
        pass

    def get_allowed_actions(self):
        """Return the actions currently available to the player. If it is the
        first turn of a round, there are more actions available."""
        if self.first_turn:
            return ['double', 'hit', 'stand', 'split', 'surrender']
        else:
            return ['hit', 'stand', 'surrender']

    # NOTE: This function is to be deprecated for a more dynamic funciton that
    # allows for a specific hand to be given a new card, not just a player.
    def assign_new_card(self, new_card, hand = None):
        """Deal a player a new card. If he has no hands, create one."""
        # If player has no hands, create one.
        if len(self.hands) == 0:
            self.hands.append(Hand([new_card]))
        # If player has exactly one hand, use it.
        elif len(self.hands) == 1:
            self.hands[0].add_card(new_card)
        else:
            # if no hand is specified and player has >1 hands, return False.
            # This assumes hands is a non-negative integer.
            if hand == None:
                return False
            hand.add_card(new_card)
        return True

    def assign_hand(self, hand):
        """Deal a new hand to the player."""
        self.hands.append(hand)

    def purge_hands(self):
        """Remove all hands for this player. Return their hands for disposal."""
        hands = self.hands[:]
        del self.hands[:]
        return hands

    def purge_hand(self, hand):
        """Remove the specific hand. Return the hand for disposal."""
        self.hands.remove(hand)
        return hand

    def get_action(self, game, hand):
        """Get input from the player to determine their next action.
        Takes as input the entire game object because the player needs more
        information to make decisions.
        Also set the player's first_turn property to False!
        Therefore, ALL player actions must go through this function."""
        # @TODO Utilize a separate UI module for this input

        action = self.get_user_input(game, hand, str(self) + ", type an action: ",
            self.get_allowed_actions())
        self.first_turn = False
        return action

    def fold_hand(self, hand):
        """Remove a hand from play."""
        hand.fold()

    def perform_action(self, action):
        """Take in an action and act on it."""
        return self.actions[action]()

# FUNCTIONS FOR ACTIONS A PLAYER CAN TAKE
    def double_down(self):
        """Double wager, take a single card and finish."""
        print self.name, 'DOUBLE DOWN' # Test output
        self.set_turn_over()

    def hit(self):
        """Ie. take a card."""
        print self.name, 'HIT' # Test output
        pass

    def stand(self):
        """Ie. end their turn (and wait)."""
        self.set_turn_over()
        print self.name, 'STAND' # Test output
        pass

    def split(self):
        """If the two initial cards have the same value, separate them to make two hands."""
        print self.name, 'SPLIT' # Test output
        pass

    def surrender(self):
        """Give up a half-bet and retire from the game."""
        print self.name, 'SURRENDER' # Test output
        self.turn_over = True

    def place_bet(self, value, hand = None):
        """Makes a player place a bet on a specific hand that belongs to them.
        If no hand is provided, it defaults to their first hand.
        Returns False if player does not have enough chips."""
        if self.chips - value < 0:
            return False
        # Default to first player hand.
        if hand == None:
            hand = self.hands[0]
        hand.place_bet(value, self)
        self.remove_chips(value)

        return True

    def get_user_input(self, game, hand, message, allowed_actions):
        """Gets command-line user input given a message."""
        user_input = raw_input(message)
        while user_input not in allowed_actions:
            print "Not an allowed action!"
            user_input = raw_input(message)

        return user_input

    def get_user_integer_input(self, game, hand, message, default, minimum, maximum):
        """Gets command-line user INTEGER input given a message, a default
        value, and a min and max value."""
        user_input = raw_input(message)
        try:
            user_input = int(user_input)
        except ValueError:
            if user_input == "" or user_input == "\n":
                user_input = default
        while type(user_input) != int or user_input < minimum or user_input > maximum:
            print "Not an allowed number!"
            print "Enter a number between {} and {}.".format(minimum, maximum)
            try:
                user_input = int(raw_input(message))
            except ValueError:
                continue

        return user_input

    def set_new_turn(self):
        """Set a player's properties to reflect that it is a new turn."""
        self.first_turn = True
        self.turn_over = False

    def set_turn_over(self):
        """Sets a turn to be True or False (True by default)."""
        self.turn_over = True

    def add_chips(self, value = 0):
        """Increase the chips by the value given (or decrease by the negative
        value)."""
        self.chips += value

    def remove_chips(self, value = 0):
        """Reduce the chips by the value given. Wraps self.add_chips(). Do not
        allow negative values!"""
        if value < 0:
            return False
        else:
            self.add_chips(-value)
            return True

    def has_enough_chips(self, min_bet):
        """Determine whether or not a player has enough chips to play. Return
        True is so, False otherwise."""
        if self.chips >= min_bet:
            return True
        return False