import random
import matplotlib.pyplot as plt
import numpy as np

# === CONFIGURABLE SETTINGS ===
end_game_score = 10000
games_per_threshold = 1000
threshold_range = range(100, 2001, 100)  # Test from 100 to 2000 in steps of 100

# === POINTS FOR SPECIAL COMBOS ===
four_of_a_kind_points = 1000
five_of_a_kind_points = 2000
six_of_a_kind_points = 3000
straight_points = 1500
three_pairs_points = 1500
two_triples_points = 2500

# === GLOBAL STATE ===
score_bins = np.linspace(-1, 10000, 50)
hand = []
count = {i: 0 for i in range(1, 7)}
dice_rolled = []
dice_left_on_bust = []

# === PLAYER STATE ===
busted = False
dice_left = 6
bank = 0
cashout_threshold = 500
cashout_status = 0
total_score = 0
turns = 0
scores_all_in = []

# === HELPER FUNCTIONS ===
def reset_hand():
    global hand
    hand = []

def roll():
    return random.choice([1, 2, 3, 4, 5, 6])

def roll_hand():
    global hand, dice_left
    reset_hand()
    for _ in range(dice_left):
        hand.append(roll())

def skip_fives():
    global bank
    global dice_left
    global busted
    global dice_left_on_bust
    global dice_rolled
    global total_score
    global cashout_status

    dice_rolled.append(dice_left)

    roll_score = 0
    for i in range(1, 7):
        count[i] = hand.count(i)

    dice_used = 0
    fives_to_score = 0
    scoring_dice_found = False

    # First check for combinations
    if list(count.values()).count(2) == 3:
        roll_score += three_pairs_points
        dice_used += 6
        scoring_dice_found = True
        if count[1] == 2:
            roll_score -= 200

    if list(count.values()).count(3) == 2:
        roll_score += two_triples_points
        dice_used += 6
        scoring_dice_found = True
        if count[1] == 3:
            roll_score -= 300

    if list(count.values()).count(1) == 6:
        roll_score += (straight_points - 100 - 50)
        dice_used += 6
        scoring_dice_found = True

    for n in count.keys():
        if count[n] == 6:
            roll_score += six_of_a_kind_points
            dice_used += 6
            scoring_dice_found = True
        elif count[n] == 5:
            roll_score += five_of_a_kind_points
            dice_used += 5
            scoring_dice_found = True
        elif count[n] == 4:
            roll_score += four_of_a_kind_points
            dice_used += 4
            scoring_dice_found = True
        elif count[n] == 3:
            if n == 1:
                roll_score += 300
            else:
                roll_score += n * 100
            dice_used += 3
            scoring_dice_found = True
        elif count[n] < 3:
            if n == 1:
                roll_score += count[n] * 100
                dice_used += count[n]
                scoring_dice_found = True
            elif n == 5:
                fives_to_score = count[n]  # Don't score 5s yet

    # Only score 5s if no other scoring dice were used
    if not scoring_dice_found and fives_to_score > 0:
        roll_score += 50
        dice_used += 1

    if roll_score == 0:
        print("\nBUST")
        busted = True
        bank = 0
        dice_left_on_bust.append(dice_left)

    if dice_used == dice_left:
        print("Hot dice!")
        dice_left = 6
    else:
        dice_left -= dice_used

    bank += roll_score
    if not busted:
        print(f'Bank: {bank}')
        print(f'Dice left: {dice_left}')

    if bank >= cashout_threshold:
        cashout_status = 1
        print("\nCashed Out")


def check_take_all():
    global bank, dice_left, busted, dice_left_on_bust
    global total_score, cashout_status, count, hand

    dice_rolled.append(dice_left)
    roll_score = 0
    count = {i: hand.count(i) for i in range(1, 7)}

    for n in count:
        if count[n] < 3:
            if n == 1:
                roll_score += count[n] * 100
                dice_left -= count[n]
            elif n == 5:
                roll_score += count[n] * 50
                dice_left -= count[n]
        elif count[n] == 3:
            roll_score += 300 if n == 1 else n * 100
            dice_left -= 3
        elif count[n] == 4:
            roll_score += four_of_a_kind_points
            dice_left -= 4
        elif count[n] == 5:
            roll_score += five_of_a_kind_points
            dice_left -= 5
        elif count[n] >= 6:
            roll_score += six_of_a_kind_points
            dice_left -= 6

    # Special combo: three pairs
    if list(count.values()).count(2) == 3:
        roll_score += three_pairs_points
        if count[1] == 2:
            roll_score -= 200  # remove the duplicate 1s value

    # Special combo: two triples
    if list(count.values()).count(3) == 2:
        roll_score += two_triples_points
        if count[1] == 3:
            roll_score -= 300

    # Special combo: straight
    if list(count.values()).count(1) == 6:
        roll_score += (straight_points - 100 - 50)

    # BUST
    if roll_score == 0:
        busted = True
        bank = 0
        dice_left_on_bust.append(dice_left)
        return

    # HOT DICE RESET
    if dice_left == 0:
        dice_left = 6

    bank += roll_score

    if bank >= cashout_threshold:
        cashout_status = 1

def play_round():
    global busted, cashout_status, scores_all_in
    while not busted and cashout_status == 0:
        roll_hand()
        # check_take_all()
        skip_fives()
    scores_all_in.append(bank)

def reset_round():
    global busted, dice_left, bank, hand, cashout_status
    global total_score, turns

    if busted or cashout_status == 1:
        total_score += bank
        turns += 1

    busted = False
    dice_left = 6
    bank = 0
    hand = []
    cashout_status = 0

def simulate_games(threshold, games=100, end_score=10000):
    global busted, dice_left, bank, hand, cashout_status
    global total_score, turns, scores_all_in, dice_rolled, dice_left_on_bust
    global cashout_threshold

    cashout_threshold = threshold
    rounds_needed_acc = []

    for _ in range(games):
        total_score = 0
        turns = 0
        scores_all_in = []
        dice_rolled = []
        dice_left_on_bust = []

        while total_score < end_score:
            play_round()
            reset_round()

        rounds_needed_acc.append(turns)

    return np.mean(rounds_needed_acc)

# === RUN MONTE CARLO EXPERIMENT ===
results = {}

print("Running Monte Carlo simulation...\n")
for threshold in threshold_range:
    avg_turns = simulate_games(threshold, games=games_per_threshold)
    results[threshold] = avg_turns
    print(f"Threshold {threshold}: Avg Turns = {avg_turns:.2f}")

# === PLOT THE RESULTS ===
plt.plot(list(results.keys()), list(results.values()), marker='o')
plt.xlabel("Cash-Out Threshold")
plt.ylabel("Average Turns to Reach 10,000 Points")
plt.ylim(bottom=0)
plt.title("Monte Carlo: Best Cash-Out Threshold (Skip 5s Strategy)")
plt.grid(True)
plt.xticks(threshold_range)
plt.show()
