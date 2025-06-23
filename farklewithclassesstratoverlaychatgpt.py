import random
import numpy as np
import matplotlib.pyplot as plt

STRATEGY = 3

class Farkle:
  def __init__(self, cashout_threshold=300, score_target=10000, strategy=1):
    self.cashout_threshold = cashout_threshold
    self.score_target = score_target
    self.bank = 0
    self.total_score = 0
    self.turns = 0
    self.dice_left = 6
    self.cashout_status = 0
    self.busted = 0
    self.hand = []

    self.strategies = {
      1:"Take-All",
      2:"Minimum Fives",
      3:"Minimum Fives and Ones"
    }

    self.strategy = strategy


    # Points
    self.four_of_a_kind_points = 1000
    self.five_of_a_kind_points = 2000
    self.six_of_a_kind_points = 3000
    self.straight_points = 1500
    self.three_pairs_points = 1500
    self.two_triples_points = 2500

  def reset_game(self):
      self.total_score = 0
      self.turns = 0
      self.busted = False
      self.dice_left = 6
      self.bank = 0
      self.cashout_status = 0

  def roll_die(self):
    return random.choice([1,2,3,4,5,6])

  def roll_hand(self):
    self.hand = [self.roll_die() for i in range(self.dice_left)]

  def count_hand(self):
    counts = {i: self.hand.count(i) for i in range(1,7)}
    return counts

  def check_roll_take_all(self):
    counts = self.count_hand()
    roll_score = 0
    dice_used = 0

    # straight
    if list(counts.values()).count(1) == 6:
      roll_score += (self.straight_points)
      dice_used = 6
    # six of a kind
    elif list(counts.values()).count(6) == 1:
      roll_score += (self.six_of_a_kind_points)
      dice_used = 6
    # 3 pairs
    elif list(counts.values()).count(2) == 3:
      roll_score += (self.three_pairs_points)
      dice_used = 6
    # 2 triples
    elif list(counts.values()).count(3) == 2:
      roll_score += (self.two_triples_points)
      dice_used = 6
    else:
      for n in counts:
        c = counts[n]
        if c < 3:
          if n == 1:
            roll_score += c*100
            dice_used += c
          elif n == 5:
            roll_score += c*50
            dice_used += c
        elif c == 3:
          if n == 1:
            roll_score += 300
            dice_used += c
          else:
            roll_score += n*100
            dice_used += c
        elif c==4:
            roll_score += self.four_of_a_kind_points
            dice_used += c
        elif c==5:
            roll_score += self.five_of_a_kind_points
            dice_used += c

    if roll_score == 0:
      self.busted = True
      self.bank = 0
      return

    self.dice_left -= dice_used

    if self.dice_left == 0:
      self.dice_left = 6

    self.bank += roll_score

    if self.bank >= self.cashout_threshold or self.total_score + self.bank >= self.score_target:
      self.cashout_status = 1

  def check_roll_no_fives(self):
    counts = self.count_hand()
    roll_score = 0
    dice_used = 0
    points_taken = False

    # straight
    if list(counts.values()).count(1) == 6:
      roll_score += (self.straight_points)
      dice_used = 6
      points_taken = True
    # six of a kind
    elif list(counts.values()).count(6) == 1:
      roll_score += (self.six_of_a_kind_points)
      dice_used = 6
      points_taken = True
    # 3 pairs
    elif list(counts.values()).count(2) == 3:
      roll_score += (self.three_pairs_points)
      dice_used = 6
      points_taken = True
    # 2 triples
    elif list(counts.values()).count(3) == 2:
      roll_score += (self.two_triples_points)
      dice_used = 6
      points_taken = True
    else:
      for n in counts:
        c = counts[n]
        if c == 3:
          if n == 1:
            roll_score += 300
            dice_used += c
            points_taken = True
          else:
            roll_score += n*100
            dice_used += c
            points_taken = True
        elif c==4:
            roll_score += self.four_of_a_kind_points
            dice_used += c
            points_taken = True
        elif c==5:
            roll_score += self.five_of_a_kind_points
            dice_used += c
            points_taken = True
        elif c < 3 and c > 0:
          if n == 1:
            roll_score += c*100
            dice_used += c
            points_taken = True
        
      if points_taken == False:
        if counts[5] > 0:
          roll_score += 50
          dice_used += 1

    if roll_score == 0:
      self.busted = True
      self.bank = 0
      return

    self.dice_left -= dice_used

    if self.dice_left == 0:
      self.dice_left = 6

    self.bank += roll_score

    if self.bank >= self.cashout_threshold or self.total_score + self.bank >= self.score_target:
      self.cashout_status = 1

  def check_roll_no_fives_min_ones(self):
    counts = self.count_hand()
    roll_score = 0
    dice_used = 0
    points_taken = False

    # straight
    if list(counts.values()).count(1) == 6:
      roll_score += (self.straight_points)
      dice_used = 6
      points_taken = True
    # six of a kind
    elif list(counts.values()).count(6) == 1:
      roll_score += (self.six_of_a_kind_points)
      dice_used = 6
      points_taken = True
    # 3 pairs
    elif list(counts.values()).count(2) == 3:
      roll_score += (self.three_pairs_points)
      dice_used = 6
      points_taken = True
    # 2 triples
    elif list(counts.values()).count(3) == 2:
      roll_score += (self.two_triples_points)
      dice_used = 6
      points_taken = True
    else:
      for n in counts:
        c = counts[n]
        if c == 3:
          if n == 1:
            roll_score += 100
            dice_used += 1
            points_taken = True
          else:
            roll_score += n*100
            dice_used += c
            points_taken = True
        elif c==4:
            roll_score += self.four_of_a_kind_points
            dice_used += c
            points_taken = True
        elif c==5:
            roll_score += self.five_of_a_kind_points
            dice_used += c
            points_taken = True
        elif c < 3 and c > 0:
          if n == 1:
            roll_score += 100
            dice_used += 1
            points_taken = True
        
      if points_taken == False:
        if counts[5] > 0:
          roll_score += 50
          dice_used += 1

    if roll_score == 0:
      self.busted = True
      self.bank = 0
      return

    self.dice_left -= dice_used

    if self.dice_left == 0:
      self.dice_left = 6

    self.bank += roll_score

    if self.bank >= self.cashout_threshold or self.total_score + self.bank >= self.score_target:
      self.cashout_status = 1



  def play_round(self):
      self.bank = 0
      self.dice_left = 6
      self.busted = False
      self.cashout_status = 0

      while not self.busted and not self.cashout_status:
          self.roll_hand()
          if self.strategy == 1:
            self.check_roll_take_all()
          elif self.strategy == 2:
            self.check_roll_no_fives()
          elif self.strategy == 3:
            self.check_roll_no_fives_min_ones()

      if not self.busted:
          self.total_score += self.bank
      self.turns += 1    

  def play_game(self):
      self.reset_game()
      while self.total_score < self.score_target:
          self.play_round()
      return self.turns, self.total_score


# Mainly written by ChatGPT V

strategies = [1, 2, 3]
strategy_labels = {1: "Take-All", 2: "Min Fives, Max Ones", 3: "Min Fives, Min Ones"}
thresholds = range(100, 1050, 50)
num_games = 10000

results_by_strategy = {}

for strategy in strategies:
    avg_turns_list = []
    for threshold in thresholds:
        turns_list = []
        for _ in range(num_games):
            game = Farkle(cashout_threshold=threshold, strategy=strategy)
            turns, score = game.play_game()
            turns_list.append(turns)
        avg_turns = np.mean(turns_list)
        avg_turns_list.append(avg_turns)
        print(f"Strategy {strategy_labels[strategy]}, Threshold {threshold}: Avg Turns = {avg_turns:.2f}")
    results_by_strategy[strategy] = avg_turns_list

# Plotting all strategies
plt.figure(figsize=(10, 6))
for strategy in strategies:
    plt.plot(thresholds, results_by_strategy[strategy], marker='o', label=strategy_labels[strategy])

plt.xlabel('Bank Threshold')
plt.ylabel(f'Average Turns to Reach {game.score_target} Points')
plt.title(f'Farkle Strategy Comparison (N={num_games})')
plt.legend()
plt.grid(True)
plt.tight_layout()

# Personal Labels

plt.annotate("Chicken Valley",
              xy=(275, 24), 
              xytext=(210, 31), 
              arrowprops=dict(arrowstyle='->'),
              fontsize=12,
              color='black')
plt.annotate("Mt. Bust",
              xy=(700, 34), 
              xytext=(410, 35), 
              arrowprops=dict(arrowstyle='->'),
              fontsize=12,
              color='black')

plt.show()