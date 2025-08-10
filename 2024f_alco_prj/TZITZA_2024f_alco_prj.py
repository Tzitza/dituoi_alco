import random
import json
from datetime import datetime
import heapq
import matplotlib.pyplot as plt
import numpy as np

class SocialNetwork:
    def __init__(self):
        self.graph = {}

    def add_user(self, user_id, name=None, interests=None):
        if user_id in self.graph:
            print(f"Ο χρήστης {user_id} υπάρχει ήδη.")
            return
        self.graph[user_id] = {
            "name": name,
            "interests": interests.split(';') if interests else [],
            "connections": {}
        }
        print(f"Ο χρήστης {user_id} προστέθηκε με επιτυχία.")

    def remove_user(self, user_id):
        if user_id not in self.graph:
            print(f"Ο χρήστης {user_id} δεν υπάρχει.")
            return
        self.graph.pop(user_id)
        for user in self.graph.values():
            if user_id in user["connections"]:
                user["connections"].pop(user_id)
        print(f"Ο χρήστης {user_id} αφαιρέθηκε με επιτυχία.")

    def create_connection(self, user1_id, user2_id, weight, date=None):
        if user1_id not in self.graph or user2_id not in self.graph:
            print("Ένας ή και οι δύο χρήστες δεν υπάρχουν.")
            return
        if not (0.01 <= weight <= 1):
            print("Το βάρος πρέπει να είναι μεταξύ 0.01 και 1.")
            return
        date = date or datetime.now().strftime('%Y-%m-%d')
        self.graph[user1_id]["connections"][user2_id] = {"weight": weight, "date": date}
        self.graph[user2_id]["connections"][user1_id] = {"weight": weight, "date": date}
        print(f"Δημιουργήθηκε σύνδεση μεταξύ των χρηστών {user1_id} και {user2_id} με επιτυχία.")

    def update_connection_weight(self, user1_id, user2_id, new_weight):
        if user1_id not in self.graph or user2_id not in self.graph[user1_id]["connections"]:
            print("Η σύνδεση δεν υπάρχει.")
            return
        if not (0.01 <= new_weight <= 1):
            print("Το νέο βάρος πρέπει να είναι μεταξύ 0.01 και 1.")
            return
        self.graph[user1_id]["connections"][user2_id]["weight"] = new_weight
        self.graph[user2_id]["connections"][user1_id]["weight"] = new_weight
        print(f"Το βάρος της σύνδεσης μεταξύ των χρηστών {user1_id} και {user2_id} ενημερώθηκε με επιτυχία.")

    def find_connections(self, user_id):
        if user_id not in self.graph:
            print(f"Ο χρήστης {user_id} δεν υπάρχει.")
            return []
        return list(self.graph[user_id]["connections"].keys())

    def network_stats(self):
        num_users = len(self.graph)
        num_connections = sum(len(user["connections"]) for user in self.graph.values()) // 2
        print(f"Αριθμός χρηστών: {num_users}")
        print(f"Αριθμός συνδέσεων: {num_connections}")

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.graph, file)
        print(f"Το δίκτυο αποθηκεύτηκε στο {filename}.")

    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                self.graph = json.load(file)
            print(f"Το δίκτυο φορτώθηκε από το {filename}.")
        except FileNotFoundError:
            print(f"Το αρχείο {filename} δεν βρέθηκε.")

    def generate_random_network(self, num_users):
        self.graph = {}
        for i in range(1, num_users + 1):
            user_id = f"User{i}"
            name = f"Name{i}"
            interests = ";".join(random.sample(["Sports", "Music", "Travel", "Books", "Movies"], random.randint(1, 3)))
            self.add_user(user_id, name, interests)

        for _ in range(num_users * 2):
            user_ids = list(self.graph.keys())
            if len(user_ids) < 2:
                continue
            user1_id, user2_id = random.sample(user_ids, 2)
            weight = round(random.uniform(0.01, 1), 2)
            date = datetime.now().strftime('%Y-%m-%d')
            self.create_connection(user1_id, user2_id, weight, date)

    def dijkstra_shortest_path(self, start_user, end_user):
        if start_user not in self.graph or end_user not in self.graph:
            print("Ένας ή και οι δύο χρήστες δεν υπάρχουν.")
            return None, None

        distances = {user: float('inf') for user in self.graph}
        previous_nodes = {user: None for user in self.graph}
        distances[start_user] = 0
        priority_queue = [(0, start_user)]

        while priority_queue:
            current_distance, current_user = heapq.heappop(priority_queue)

            if current_distance > distances[current_user]:
                continue

            for neighbor, info in self.graph[current_user]["connections"].items():
                distance = current_distance + info["weight"]

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = current_user
                    heapq.heappush(priority_queue, (distance, neighbor))

        path, current_user = [], end_user
        while previous_nodes[current_user] is not None:
            path.insert(0, current_user)
            current_user = previous_nodes[current_user]

        if path:
            path.insert(0, start_user)

        return path, distances[end_user] if distances[end_user] != float('inf') else None

    def detect_communities(self, weight_threshold=0.01):
        visited = set()
        communities = []

        def dfs(user, community):
            visited.add(user)
            community.append(user)
            for neighbor, info in self.graph[user]["connections"].items():
                if neighbor not in visited and info["weight"] >= weight_threshold:
                    dfs(neighbor, community)

        for user in self.graph:
            if user not in visited:
                community = []
                dfs(user, community)
                communities.append(community)

        return communities

    def recommend_friends(self, user_id):
        if user_id not in self.graph:
            print(f"Ο χρήστης {user_id} δεν υπάρχει.")
            return []

        direct_connections = set(self.graph[user_id]["connections"].keys())
        recommendations = {}

        for connection in direct_connections:
            for friend, info in self.graph[connection]["connections"].items():
                if friend != user_id and friend not in direct_connections:
                    recommendations[friend] = recommendations.get(friend, 0) + info["weight"]

        sorted_recommendations = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)
        return [friend for friend, _ in sorted_recommendations]

    def visualize_graph(self):
        # Υλοποίηση βασικής οπτικοποίησης
        users = list(self.graph.keys())
        positions = {user: (np.cos(i * 2 * np.pi / len(users)), np.sin(i * 2 * np.pi / len(users))) for i, user in enumerate(users)}
        plt.figure(figsize=(10, 8))
        for user, connections in self.graph.items():
            x, y = positions[user]
            plt.scatter(x, y, s=100, label=user)
            for connection in connections["connections"]:
                cx, cy = positions[connection]
                plt.plot([x, cx], [y, cy], 'k-', alpha=0.5)
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
        plt.show()


    def visualize_dijkstra(self, start_user, end_user):
        # Υλοποίηση οπτικοποίησης για συντομότερη διαδρομή
        path, _ = self.dijkstra_shortest_path(start_user, end_user)
        if not path:
            print("Δεν υπάρχει διαδρομή για οπτικοποίηση.")
            return

        users = list(self.graph.keys())
        positions = {user: (np.cos(i * 2 * np.pi / len(users)), np.sin(i * 2 * np.pi / len(users))) for i, user in enumerate(users)}
        plt.figure(figsize=(10, 8))
        for user, connections in self.graph.items():
            x, y = positions[user]
            plt.scatter(x, y, s=100, label=user)
            for connection in connections["connections"]:
                cx, cy = positions[connection]
                color = 'red' if user in path and connection in path and abs(path.index(user) - path.index(connection)) == 1 else 'k'
                plt.plot([x, cx], [y, cy], color=color, alpha=0.5)
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
        plt.title(f"Συντομότερη Διαδρομή: {start_user} -> {end_user}")
        plt.show()

    def visualize_communities(self, weight_threshold=0.01):
        # Υλοποίηση οπτικοποίησης κοινοτήτων
        communities = self.detect_communities(weight_threshold)
        users = list(self.graph.keys())
        positions = {user: (np.cos(i * 2 * np.pi / len(users)), np.sin(i * 2 * np.pi / len(users))) for i, user in enumerate(users)}
        plt.figure(figsize=(10, 8))
        colors = plt.cm.rainbow(np.linspace(0, 1, len(communities)))
        for i, community in enumerate(communities):
            for user in community:
                x, y = positions[user]
                plt.scatter(x, y, s=100, color=colors[i], label=f"Community {i+1}" if user == community[0] else "")
                for connection in self.graph[user]["connections"]:
                    if connection in community:
                        cx, cy = positions[connection]
                        plt.plot([x, cx], [y, cy], color=colors[i], alpha=0.5)
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
        plt.title("Οπτικοποίηση Κοινοτήτων")
        plt.show()

# Προσθήκη επιλογών στο μενού:
if __name__ == "__main__":
    network = SocialNetwork()
    while True:
        print("\nΜενού:")
        print("1. Προσθήκη Χρήστη")
        print("2. Αφαίρεση Χρήστη")
        print("3. Δημιουργία Σύνδεσης")
        print("4. Ενημέρωση Βάρους Σύνδεσης")
        print("5. Εύρεση Συνδέσεων")
        print("6. Στατιστικά Δικτύου")
        print("7. Αποθήκευση σε Αρχείο")
        print("8. Φόρτωση από Αρχείο")
        print("9. Δημιουργία Τυχαίου Δικτύου")
        print("10. Συντομότερη Διαδρομή Dijkstra")
        print("11. Ανίχνευση Κοινοτήτων")
        print("12. Σύσταση Φίλων")
        print("13. Οπτικοποίηση Γραφήματος")
        print("14. Οπτικοποίηση Συντομότερης Διαδρομής")
        print("15. Οπτικοποίηση Κοινοτήτων")
        print("16. Έξοδος")

        choice = input("Επιλέξτε μια επιλογή: ")
        if choice == "1":
            user_id = input("Εισάγετε το ID του χρήστη: ")
            name = input("Εισάγετε το όνομα (προαιρετικά): ")
            interests = input("Εισάγετε τα ενδιαφέροντα χωρισμένα με ';' (προαιρετικά): ")
            network.add_user(user_id, name, interests)
        elif choice == "2":
            user_id = input("Εισάγετε το ID του χρήστη που θέλετε να αφαιρέσετε: ")
            network.remove_user(user_id)
        elif choice == "3":
            user1_id = input("Εισάγετε το ID του χρήστη 1: ")
            user2_id = input("Εισάγετε το ID του χρήστη 2: ")
            weight = float(input("Εισάγετε το βάρος σύνδεσης (0.01 έως 1): "))
            network.create_connection(user1_id, user2_id, weight)
        elif choice == "4":
            user1_id = input("Εισάγετε το ID του χρήστη 1: ")
            user2_id = input("Εισάγετε το ID του χρήστη 2: ")
            new_weight = float(input("Εισάγετε το νέο βάρος σύνδεσης (0.01 έως 1): "))
            network.update_connection_weight(user1_id, user2_id, new_weight)
        elif choice == "5":
            user_id = input("Εισάγετε το ID του χρήστη: ")
            connections = network.find_connections(user_id)
            print(f"Συνδέσεις για τον χρήστη {user_id}: {connections}")
        elif choice == "6":
            network.network_stats()
        elif choice == "7":
            filename = input("Εισάγετε το όνομα αρχείου για αποθήκευση του δικτύου: ")
            network.save_to_file(filename)
        elif choice == "8":
            filename = input("Εισάγετε το όνομα αρχείου για φόρτωση του δικτύου: ")
            network.load_from_file(filename)
        elif choice == "9":
            num_users = int(input("Εισάγετε τον αριθμό των χρηστών: "))
            network.generate_random_network(num_users)
        elif choice == "10":
            start_user = input("Εισάγετε το ID του χρήστη εκκίνησης: ")
            end_user = input("Εισάγετε το ID του χρήστη προορισμού: ")
            path, distance = network.dijkstra_shortest_path(start_user, end_user)
            if path:
                print(f"Η συντομότερη διαδρομή: {path} με απόσταση {distance}")
            else:
                print("Δεν βρέθηκε διαδρομή.")
        elif choice == "11":
            threshold = float(input("Εισάγετε το κατώφλι βάρους (προεπιλογή 0.01): ") or 0.01)
            communities = network.detect_communities(threshold)
            print(f"Κοινότητες: {communities}")
        elif choice == "12":
            user_id = input("Εισάγετε το ID του χρήστη: ")
            recommendations = network.recommend_friends(user_id)
            print(f"Συστάσεις φίλων για τον χρήστη {user_id}: {recommendations}")
        elif choice == "13":
            network.visualize_graph()
        elif choice == "14":
            start_user = input("Εισάγετε το ID του χρήστη εκκίνησης: ")
            end_user = input("Εισάγετε το ID του χρήστη προορισμού: ")
            network.visualize_dijkstra(start_user, end_user)
        elif choice == "15":
            threshold = float(input("Εισάγετε το κατώφλι βάρους (προεπιλογή 0.01): ") or 0.01)
            network.visualize_communities(threshold)
        elif choice == "16":
            print("Έξοδος...")
            break
        else:
            print("Μη έγκυρη επιλογή. Δοκιμάστε ξανά.")


