import random
import matplotlib.pyplot as plt
import numpy as np

score_bins = np.linspace(-1, 10000, 50)

dice_left = 6
bank = 0
hand = []
busted = False

four_of_a_kind_points = 1000
five_of_a_kind_points = 2000
six_of_a_kind_points = 3000
straight_points = 1500
three_pairs_points = 1500
two_triples_points = 2500

dice_left_on_bust = []
dice_rolled = []


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
  # print(hand)

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

def check_take_all():
  global bank
  global dice_left
  global busted
  global dice_left_on_bust
  global dice_rolled

  dice_rolled.append(dice_left)

  roll_score = 0
  for i in range(6):
    count[i] = hand.count(i)

  for n in count.keys():
    if count[n] < 3:
      if n == 1:
        roll_score += count[n]*100
        dice_left -= count[n]
      if n == 5:
        roll_score += count[n]*50
        dice_left -= count[n]
    elif count[n] == 3:
      if n == 1:
        roll_score += 300
      else:
        roll_score += n*100
      dice_left -= count[n]
    elif count[n] == 4:
      roll_score += four_of_a_kind_points
      dice_left -= count[n]
    elif count[n] == 5:
      roll_score += five_of_a_kind_points
      dice_left -= count[n]
    else:
      roll_score += six_of_a_kind_points

  # check for three pairs
  if list(count.values()).count(2) == 3:
    roll_score += three_pairs_points
  
  # check for two triples
  if list(count.values()).count(3) == 2:
    roll_score += two_triples_points

  # check for straights
  if list(count.values()).count(1) == 6:
    roll_score += straight_points

  if roll_score == 0:
    # print("YOU BUSTED!!!!")
    busted = True
    dice_left_on_bust.append(dice_left)

  if dice_left == 0:
    # print("Hot dice!")
    dice_left = 6

  bank = bank+roll_score
  # print(f'Bank: {bank}')
  # print(f'Dice left: {dice_left}')
  



# def check_take_min: reorganize to check for 5s last, have a "need points" boolean that turns off if any other condition has been met
# if not then the

scores_all_in = []


def play_round():
  global scores_all_in
  global bank
  while busted == False:
    roll_hand()
    check_take_all()
  scores_all_in.append(bank)

def reset_round():
    global busted
    global dice_left
    global bank
    global hand
    busted = False
    dice_left = 6
    bank = 0
    hand = []


N = 1000000
for i in range(N):
  play_round()
  reset_round()

# print(scores_all_in)
print(max(scores_all_in))

# print(dice_left_on_bust)

plt.hist(dice_rolled)
plt.xlabel('Dice Rolled')
plt.ylabel('Occurances')
plt.title(f'"Take-All Strategy" (N = {N})')
plt.xlim(left=0)
plt.show()

plt.hist(dice_left_on_bust)
plt.xlabel('Dice Left on Bust')
plt.ylabel('Occurances')
plt.title(f'"Take-All Strategy" (N = {N})')
plt.xlim(left=0)
plt.show()

plt.hist(scores_all_in, bins = score_bins)
plt.xlabel('Bust Score')
plt.ylabel('Occurances')
plt.title(f'"Take-All Strategy" (N = {N})')
plt.xlim(left=0)
plt.show()



 


# old
# N = 10
# for i in range(N):
#   roll_hand()
#   score = check_take_all()
#   print(score)
#   for n in score_outcomes.keys():
#     if score>n:
#       score_outcomes[n]+= (1/N)*100
#       # value in %

# print(score_outcomes)



# PLOT OUTCOMES

# xvalues = score_outcomes.keys()
# yvalues = score_outcomes.values()

# plt.plot(xvalues,yvalues)
# plt.xlabel('Score Reached')
# plt.ylabel('% of rolls')
# plt.title(f'First Roll Raw Scores: N = {N}')
# plt.xlim(left=0)
# plt.ylim(bottom=0)
# plt.show()



# roll_hand()
# check()
# print(bank)


