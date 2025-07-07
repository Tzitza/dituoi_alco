# Ορισμός της κλάσης Job για την αναπαράσταση μιας εργασίας
class Job:
    def __init__(self, processing_times, sequence):
        # Αρχικοποίηση χρόνων επεξεργασίας και σειράς εκτέλεσης
        self.processing_times = processing_times
        self.sequence = sequence

    def __str__(self):
        # Επιστροφή συμβολοσειράς που παρουσιάζει τα χαρακτηριστικά της εργασίας
        return f"processing times: {self.processing_times}\nsequence: {self.sequence}"

    def get_output_format(self):
        # Επιστροφή λίστας που παρουσιάζει τα αποτελέσματα σε επιθυμητή μορφή
        return [
            f"(machine {machine}, processing Time {self.processing_times[machine - 1]})"
            for machine in self.sequence
        ]

# Διάβασμα δεδομένων εισόδου από ένα αρχείο
def read_input_file(file_path):
    with open(file_path, 'r') as file:
        # Ανάγνωση αριθμού εργασιών και αριθμού μηχανών
        num_jobs = int(file.readline().strip())
        num_machines = int(file.readline().strip())

        # Ανάγνωση τρίτης γραμμής και οπτικού μέγιστου χρόνου εκτέλεσης (αν υπάρχει)
        third_line = file.readline().strip()
        optimal_makespan = int(third_line) if third_line.isdigit() else None

        # Ανάγνωση χρόνων επεξεργασίας για κάθε εργασία
        if optimal_makespan is None:
            processing_times = [list(map(int, third_line.split()))]
        else:
            processing_times = []

        processing_times.extend([list(map(int, file.readline().split())) for _ in range(num_jobs - len(processing_times))])

        # Ανάγνωση ακολουθίας εργασιών για κάθε εργασία
        job_sequences = [list(map(int, file.readline().split())) for _ in range(num_jobs)]

    # Επιστροφή δεδομένων
    return num_jobs, num_machines, optimal_makespan, processing_times, job_sequences

# Δημιουργία αντικειμένων Job από τα δεδομένα εισόδου
def create_job_objects(num_jobs, processing_times, job_sequences):
    jobs = []
    for i in range(num_jobs):
        job = Job(processing_times[i], job_sequences[i])
        jobs.append(job)
    return jobs

# Εκτύπωση των αποτελεσμάτων
def print_output(jobs):
    for i, job in enumerate(jobs, start=1):
        print(f"Job {i}: {' '.join(job.get_output_format())}")

# Κύριο μέρος του προγράμματος
if __name__ == "__main__":
    # Καθορισμός διαδρομής του αρχείου εισόδου
    file_path = "input/la01.txt"

    # Ανάγνωση δεδομένων από το αρχείο
    num_jobs, num_machines, optimal_makespan, processing_times, job_sequences = read_input_file(file_path)

    # Δημιουργία αντικειμένων Job
    jobs = create_job_objects(num_jobs, processing_times, job_sequences)

    # Εκτύπωση του οπτικού μέγιστου χρόνου εκτέλεσης (αν υπάρχει)
    if optimal_makespan is not None:
        print(f"optimal makespan: {optimal_makespan}")

    # Εκτύπωση αποτελεσμάτων
    print("\nresults:")
    print_output(jobs)
