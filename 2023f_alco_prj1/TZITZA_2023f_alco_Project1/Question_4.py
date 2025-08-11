import random
from collections import defaultdict
import time

class HashTable:
    def __init__(self, size=101):
        self.size = size
        self.table = [None] * size
        self.count = 0
        self.collisions = 0

    def hash_function(self, key):
        return key % self.size

    def insert(self, key):
        initial_index = self.hash_function(key)
        index = initial_index
        while self.table[index] is not None:
            if self.table[index] == key:
                # Key already exists, no need to insert
                return
            index = (index + 1) % self.size

        # Only increment the collision counter if the position was occupied
        if initial_index != index:
            self.collisions += 1

        self.table[index] = key
        self.count += 1
        print(f"Inserted key {key} at index {index} (initial index: {initial_index})")

    def find(self, key):
        index = self.hash_function(key)
        while self.table[index] is not None:
            if self.table[index] == key:
                return True
            index = (index + 1) % self.size
        return False

    def delete(self, key):
        index = self.hash_function(key)
        while self.table[index] is not None:
            if self.table[index] == key:
                self.table[index] = None
                self.count -= 1
                return True
            index = (index + 1) % self.size
        return False

# Question 1
def generate_credit_card_numbers(num_cards):
    return [random.randint(10**15, 10**16 - 1) for _ in range(num_cards)]

def generate_transactions(hash_table, credit_cards, num_transactions):
    transactions = []
    for _ in range(num_transactions):
        card = random.choice(credit_cards)
        amount = round(random.uniform(10, 1000), 2)
        transactions.append((card, amount))
        hash_table.insert(card)
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

# Create hash table
hash_table = HashTable()

# Generate credit card numbers
credit_cards = generate_credit_card_numbers(20)

# Generate transactions and count collisions
transactions = generate_transactions(hash_table, credit_cards, 100)

# Measure execution time
start_time = time.time()

# Print credit card numbers and transactions
print("Credit Card Numbers:")
print(credit_cards)

# Print collisions
print(f"\nNumber of Collisions during Insertion: {hash_table.collisions}")

# Process transactions and print results
min_total_card, max_total_card, min_count_card, max_count_card, card_totals, card_counts = process_transactions(transactions)

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