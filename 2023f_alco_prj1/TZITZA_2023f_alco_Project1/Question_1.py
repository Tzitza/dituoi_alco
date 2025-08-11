import random

# Αρχικοποίηση του γεννητήρα τυχαίων αριθμών (Random) με τον αριθμό μητρώου σας (σπόρο)
random.seed(12345)

# Δημιουργία 20.000 διαφορετικών μεταξύ τους τυχαίων αριθμών πιστωτικών καρτών
credit_card_numbers = random.sample(range(10**15, 10**16), 20000)

# Δημιουργία μιας λίστας με 1.000.000 χρεώσεων
charges = []

for _ in range(1000000):
    # Επιλογή τυχαίας πιστωτικής κάρτας
    credit_card_number = random.choice(credit_card_numbers)
    
    # Δημιουργία τυχαίου ποσού χρέωσης στο διάστημα από 10 μέχρι 1.000 ευρώ
    amount = round(random.uniform(10, 1000), 2)
    
    # Αποθήκευση της χρέωσης στη λίστα
    charges.append((credit_card_number, amount))