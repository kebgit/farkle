import random
import matplotlib.pyplot as plt
import numpy as np



dice_left = 6
bank = 0
hand = []
four_of_a_kind_points = 1000
five_of_a_kind_points = 2000
six_of_a_kind_points = 3000
straight_points = 1500
three_pairs_points = 1500
two_triples_points = 2500

def reset_hand():
  global hand
  hand = []

count = {
  1:0,
  2:0,
  3:0,
  4:0,
  5:0,
  6:0
}


def roll():
  return random.choice([1,2,3,4,5,6])

def roll_hand():
  reset_hand()
  global hand
  global bank
  for i in range(dice_left):
    hand.append(roll())
  print(hand)

# def collect_points():
  # run all checks
  # logic to pass on 5s if you already have a 1: e.g. bank needed = 1, if there is a 1 then bank needed=0 to skip 5s, etc
  # can have risk aversion / strategy parameter to take 5s or not, and when to take the 5s

# checks needed
  # PLAYER INFO AKA INPUTS:
  # 1s, how many 1s there are - x
  # 5s, how many 5s there are x
  # double values --> if there's 3 doubles x
  # triple values and if there are 2 triples x
  # four, five, and six of a kind x
  # straights
  # current score
  # opponents scores
  # current bank
  # dice left
  # 
  # this creates data for the strategies to play off of. i.e. if there are 5s, but there is a 1, do not take the 5s. 
  # can Create strategy then run MC on different parameters and strategies
  # can also create ML: there are only certain decisions to make after each roll, therefore it can take data of what 


# potential strategies:
  # take all the points you can get all the time
  # do not take 5s
  # only roll with 1,2,3,4,5 dice remaining
  # combination of taking 5s or not, and when to stop rolling, and what score threshold to stop rolling
  # never backing out before 1 or 2 or 3 hot dice resets

# check for basic scores: 1s, and multiples
def check():
  global bank
  bank = 0
  for i in range(6):
    count[i] = hand.count(i)

  for n in count.keys():
    if count[n] < 3:
      if n == 1:
        bank += count[n]*100
      if n == 5:
        bank += count[n]*50
    elif count[n] == 3:
      if n == 1:
        bank += 300
      else:
        bank += n*100
    elif count[n] == 4:
      bank += four_of_a_kind_points
    elif count[n] == 5:
      bank += five_of_a_kind_points
    else:
      bank += six_of_a_kind_points

  # check for three pairs
  if list(count.values()).count(2) == 3:
    bank += three_pairs_points
  
  # check for two triples
  if list(count.values()).count(3) == 2:
    bank += two_triples_points

  # check for straights
  if list(count.values()).count(1) == 6:
    bank += straight_points

  return(bank)

score_outcomes = {
  0:0,
  99:0,
  199:0,
  299:0,
  399:0,
  499:0,
  749:0,
  999:0,
  1499:0,
  1999:0,
  2499:0,
  2999:0
}

N = 1000000
for i in range(N):
  roll_hand()
  score = check()
  print(score)
  for n in score_outcomes.keys():
    if score>n:
      score_outcomes[n]+= (1/N)*100
      # value in %

print(score_outcomes)

xvalues = score_outcomes.keys()
yvalues = score_outcomes.values()

plt.plot(xvalues,yvalues)
plt.xlabel('Score Reached')
plt.ylabel('% of rolls')
plt.title(f'First Roll Raw Scores: N = {N}')
plt.xlim(left=0)
plt.ylim(bottom=0)
plt.show()

# roll_hand()
# check()
# print(bank)


