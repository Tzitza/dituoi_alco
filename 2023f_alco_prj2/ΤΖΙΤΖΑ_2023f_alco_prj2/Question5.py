class Job:
    def __init__(self, processing_times, sequence):
        self.processing_times = processing_times
        self.sequence = sequence
        self.start_times = [0] * len(processing_times)

    def __str__(self):
        return f"processing times: {self.processing_times}\nsequence: {self.sequence}"

    def get_output_format(self):
        return [
            f"(machine {machine}, processing Time {self.processing_times[machine - 1]})"
            for machine in self.sequence
        ]


def shifting_bottleneck(jobs, num_machines):
    # Εκτελεί τη διαδικασία Shifting Bottleneck για τον υπολογισμό του προγράμματος παραγωγής
    # Επιστρέφει τον συνολικό χρόνο ολοκλήρωσης (makespan)
    total_processing_time = [0] * len(jobs)

    while any(job.sequence.count(0) > 0 for job in jobs):
        # Βρίσκει το "shifting bottleneck" (το μηχάνημα με το μεγαλύτερο συνολικό χρόνο εκτέλεσης)
        bottleneck_machine = max(range(1, num_machines + 1), key=lambda m: sum(job.processing_times[m - 1] for job in jobs))

        # Ταξινομεί τις εργασίες που δεν έχουν ολοκληρωθεί στο "shifting bottleneck" μηχάνημα
        eligible_jobs = [job for job in jobs if job.sequence[bottleneck_machine - 1] == 0]
        eligible_jobs.sort(key=lambda job: job.processing_times[bottleneck_machine - 1])

        # Επιλέγει την πρώτη εργασία και εκτελεί την εργασία στο "shifting bottleneck" μηχάνημα
        selected_job = eligible_jobs[0]
        selected_job.sequence[bottleneck_machine - 1] = bottleneck_machine
        selected_job.start_times[bottleneck_machine - 1] = max(
            total_processing_time[jobs.index(selected_job)],
            total_processing_time[jobs.index(selected_job) - 1] if jobs.index(selected_job) > 0 else 0
        )
        total_processing_time[jobs.index(selected_job)] = selected_job.start_times[bottleneck_machine - 1] + \
                                                          selected_job.processing_times[bottleneck_machine - 1]

    return max(total_processing_time)


# Κύριο μέρος του προγράμματος
if __name__ == "__main__":
    # Καθορισμός διαδρομής του αρχείου εισόδου
    file_path = "input/la01.txt"

    # Ανάγνωση δεδομένων από το αρχείο
    num_jobs, num_machines, _, processing_times, job_sequences = read_input_file(file_path)

    # Δημιουργία αντικειμένων Job
    jobs = create_job_objects(num_jobs, processing_times, job_sequences)

    # Εφαρμογή του Shifting Bottleneck
    makespan = shifting_bottleneck(jobs, num_machines)

    # Εκτύπωση του συνολικού χρόνου ολοκλήρωσης (makespan)
    print(f"Makespan using Shifting Bottleneck: {makespan}")

    # Εκτύπωση των αποτελεσμάτων
    print("\nResults after Shifting Bottleneck:")
    print_output(jobs)

    # Απεικόνιση της λύσης JSSP μετά τον Shifting Bottleneck
    plot_jssp_solution(jobs)
