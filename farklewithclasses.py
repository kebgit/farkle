import random
import numpy as np
import matplotlib.pyplot as plt

class Farkle:
  def __init__(self, cashout_threshold=300, score_target=10000):
    self.cashout_threshold = cashout_threshold
    self.score_target = score_target
    self.bank = 0
    self.total_score = 0
    self.turns = 0
    self.dice_left = 6
    self.cashout_status = 0
    self.busted = 0
    self.hand = []
    self.strategy = ""

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
    self.strategy = "Take-All"
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

  def play_round(self):
      self.bank = 0
      self.dice_left = 6
      self.busted = False
      self.cashout_status = 0

      while not self.busted and not self.cashout_status:
          self.roll_hand()
          self.check_roll_take_all()

      if not self.busted:
          self.total_score += self.bank
      self.turns += 1    

  def play_game(self):
      self.reset_game()
      while self.total_score < self.score_target:
          self.play_round()
      return self.turns, self.total_score

# game = Farkle()
# turns,score = game.play_game()

# print(f'Turns: {turns}')
# print(f'Score: {score}')


thresholds = range(100, 1000, 50)  # example thresholds from 100 to 1800 by 200
num_games = 10000  # number of simulated games per threshold

results = []

for threshold in thresholds:
    turns_list = []
    for _ in range(num_games):
        game = Farkle(cashout_threshold=threshold)
        turns, score = game.play_game()
        turns_list.append(turns)
    avg_turns = np.mean(turns_list)
    results.append((threshold, avg_turns))
    print(f"Threshold {threshold}: Average turns to reach {game.score_target} = {avg_turns:.2f}")

# Plot results
thresholds, avg_turns = zip(*results)
plt.plot(thresholds, avg_turns, marker='o')
plt.xlabel('Bank Threshold')
plt.ylabel(f'Average Turns to Reach {game.score_target} Points')
plt.title(f'Risk Threshold Effects on {game.strategy} Strategy - (N={num_games})')
plt.annotate("No-Balls Valley",
              xy=(275, 23.5), 
              xytext=(200, 28), 
              arrowprops=dict(arrowstyle='->'),
              fontsize=12,
              color='black')

plt.show()