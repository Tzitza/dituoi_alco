import random
from collections import defaultdict
import time

# Question 1
def generate_credit_card_numbers(num_cards):
    return [''.join(str(random.randint(0, 9)) for _ in range(16)) for _ in range(num_cards)]

def generate_transactions(credit_cards, num_transactions):
    transactions = []
    for _ in range(num_transactions):
        card = random.choice(credit_cards)
        amount = round(random.uniform(10, 1000), 2)
        transactions.append((card, amount))
    return transactions

# Question 2
def process_transactions(transactions):
    card_totals = defaultdict(float)
    card_counts = defaultdict(int)

    for card, amount in transactions:
        card_totals[card] += amount
        card_counts[card] += 1

    min_total_card = min(card_totals, key=card_totals.get)
    max_total_card = max(card_totals, key=card_totals.get)
    min_count_card = min(card_counts, key=card_counts.get)
    max_count_card = max(card_counts, key=card_counts.get)

    return min_total_card, max_total_card, min_count_card, max_count_card, card_totals, card_counts

# Generate credit card numbers
credit_cards = generate_credit_card_numbers(20.000)

# Generate transactions
transactions = generate_transactions(credit_cards, 1000000)

# Measure execution time
start_time = time.time()

# Process transactions and print results
min_total_card, max_total_card, min_count_card, max_count_card, card_totals, card_counts = process_transactions(transactions)

# Print credit card numbers and transactions
print("Credit Card Numbers:")
print(credit_cards)

print("\nTransactions:")
for card, amount in transactions:
    print(f"Card: {card}, Amount: {amount} euros")

# Print results
print("\nResults:")
print(f"Minimum Total Amount Card: {min_total_card}, Total Amount: {round(card_totals[min_total_card], 2)} euros")
print(f"Maximum Total Amount Card: {max_total_card}, Total Amount: {round(card_totals[max_total_card], 2)} euros")
print(f"Minimum Number of Transactions Card: {min_count_card}, Number of Transactions: {card_counts[min_count_card]}")
print(f"Maximum Number of Transactions Card: {max_count_card}, Number of Transactions: {card_counts[max_count_card]}")

# Print execution time
end_time = time.time()
execution_time = (end_time - start_time) * 1000.0  # Convert to milliseconds
print(f"\nExecution Time: {execution_time:.4f} milliseconds")