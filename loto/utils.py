import random


class NumBox:
    num_range = 90

    def __init__(self):
        self.numbers = [x for x in range(1, self.num_range + 1)]
        self.shuffle()

    def __len__(self) -> int:
        return len(self.numbers) - self.pointer

    def shuffle(self):
        random.shuffle(self.numbers)
        self.pointer = 0

    def num_out(self) -> int:
        self.pointer += 1

        try:
            return self.numbers[self.pointer - 1]
        except ValueError:
            return 0


class NumCard:
    rows_number = min(3, NumBox.num_range - 1)
    cells_filled_in_row = min(5, NumBox.num_range // rows_number)
    cells_in_row = max(9, cells_filled_in_row * 2 - 1)

    def __init__(self):
        self.matrix = self.new_card()
        self.nums_left = NumCard.rows_number * NumCard.cells_filled_in_row

    def new_card(self):
        nums = random.sample(range(1, NumBox.num_range + 1), NumCard.rows_number * NumCard.cells_filled_in_row)
        card = [["" for c in range(NumCard.cells_in_row)] for r in range(NumCard.rows_number)]

        for row in range(NumCard.rows_number):
            tmp_nums = sorted(nums[row * NumCard.cells_filled_in_row:(row + 1) * NumCard.cells_filled_in_row])
            next_num = tmp_nums.pop()

            for cell in reversed(range(self.cells_in_row)):
                if len(tmp_nums)  == cell or random.randint(0, 1):
                    card[row][cell] = next_num
                    if tmp_nums:
                        next_num = tmp_nums.pop()
                    else:
                        break

        return card

    def print_card(self):
        print(f"{(" " + self.name + " "):-^{3 * NumCard.cells_in_row}}")

        for row in range(self.rows_number):
            for cell in range(self.cells_in_row):
                print(f"{self.matrix[row][cell]:^3}", end="")
            print()

        print("-" * NumCard.cells_in_row * 3)

    def num_in_card(self, num):
        for row in self.matrix:
            try:
                cell = row.index(num)
            except ValueError:
                continue

            row[cell] = "-"
            self.nums_left -= 1
            return True

        return False

    def num_choice(self, num):
        choice = input(f"\n{self} -> Is there {num} in your card (y - yes, empty - no): ")
        return choice in ("Y", "y", "Yes", "yes")


class PersonPlayer(NumCard):

    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.alive = True

    def __str__(self):
        return f"{self.name} (person)"


class ComputerPlayer(NumCard):

    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def __str__(self):
        return f"{self.name} (computer)"
