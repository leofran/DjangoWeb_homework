from utils import NumBox, PersonPlayer, ComputerPlayer
from time import sleep


class Game:

    def __init__(self):
        self.box = NumBox()
        self.players =[]

    def choose_players(self):
        self.computers = self.call_players("computer")
        self.persons = self.call_players("person")

    def call_players(self, kind_of_players):
        players_in_game = input(f"How many {kind_of_players}s are playing the game: ")
        players_in_game = int(players_in_game) if players_in_game.isdigit() else 0
        new_players = []
        if players_in_game:
            name_players = input(f"It is {players_in_game} {kind_of_players}(s) in game. You can give them names (Y - I will, empty - default names): ")
            name_players = name_players in ("Y", "y", "Yes", "yes")
            for x in range(players_in_game):
                counter = len(self.players) + 1
                player_name = f"Player_{kind_of_players}_{counter}"
                if name_players:
                    input_name = input(f"Write name for playing {kind_of_players} number_{counter} (empty - default name): ")
                    if input_name.strip():
                        player_name = input_name
                card_obj = ComputerPlayer if kind_of_players == "computer" else PersonPlayer
                player = card_obj(player_name)
                self.players.append(player)
                new_players.append(player)

        return new_players

    def person_choice(self, person, num):
        choice = input(f"\n{person.name} -> Is there {num} in your card (y - yes, empty - no): ")
        return choice in ("Y", "y", "Yes", "yes")

    def run(self):
        print("\n*** NEW GAME ***\n")
        self.box.shuffle()

        while True:
            self.choose_players()
            if len(self.players) > 0:
                break
            print("\nThere are no players in the game. Try once more :)")
            sleep(1)

        print("\nLet's begin :)")

        counter = 0
        winners =[]
        while not winners :
            counter += 1
            num = self.box.num_out()
            persons_alive = [person for person in self.persons if person.alive]
            players_alive = self.computers + persons_alive
            if len(persons_alive) != 0: sleep(1)
            print(f"\n--- Step {counter} ---\nNew number from box: {num} (It's {len(self.box)} nums left in box now)\n")
            if len(persons_alive) != 0: sleep(1)
            for player in players_alive:
                player.print_card()
            for person in persons_alive:
                if self.person_choice(person, num) == person.num_in_card(num):
                    print("Pass on!")
                else:
                    print("Game over for you (((")
                    person.alive = False
            persons_alive = [person for person in self.persons if person.alive]
            players_alive = self.computers + persons_alive
            for computer in self.computers:
                computer.num_in_card(num)
            for player in players_alive:
                if player.no_num_in_card() or (len(players_alive) == 1 and len(persons_alive) == 0):
                    winners.append(player.name)

        print("\nWe have winners!!!\nHere they are:", ", ".join(winners))


if __name__ == "__main__":
    while True:
        game = Game()
        game.run()
        play = input("\nOnce more game (y - yes, empty - no)?: ")
        if not play in ("Y", "y", "Yes", "yes"):
            break


