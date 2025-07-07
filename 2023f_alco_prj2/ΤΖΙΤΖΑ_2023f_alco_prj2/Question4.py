import matplotlib.pyplot as plt

def plot_jssp_solution(jobs):
    # Δημιουργία λίστας για την αποθήκευση του χρόνου έναρξης κάθε εργασίας σε κάθε μηχάνημα
    start_times = [[0] * len(jobs[0].processing_times) for _ in range(len(jobs))]

    # Διάτρηση όλων των μηχανημάτων
    for machine in range(len(jobs[0].processing_times[0])):
        # Διάτρηση όλων των εργασιών
        for job in jobs:
            # Υπολογισμός χρόνου έναρξης στο συγκεκριμένο μηχάνημα
            start_times[jobs.index(job)][machine] = max(
                start_times[jobs.index(job)][machine],
                start_times[jobs.index(job) - 1][machine] if jobs.index(job) > 0 else 0
            ) + job.processing_times[machine]

    # Δημιουργία γραφήματος
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = plt.cm.viridis.colors

    # Διάτρηση όλων των μηχανημάτων
    for machine in range(len(jobs[0].processing_times[0])):
        # Διάτρηση όλων των εργασιών
        for job in jobs:
            # Σχεδίαση της εργασίας στο γράφημα
            ax.barh(jobs.index(job) + 1, job.processing_times[machine],
                    left=start_times[jobs.index(job)][machine], color=colors[machine])

    # Ορισμός ετικετών και τίτλου
    ax.set_yticks(range(1, len(jobs) + 1))
    ax.set_yticklabels([f'Job {i}' for i in range(1, len(jobs) + 1)])
    ax.set_xlabel('Χρόνος')
    ax.set_ylabel('Εργασίες')
    ax.set_title('Λύση JSSP')

    # Εμφάνιση του γραφήματος
    plt.grid(axis='x')
    plt.show()

# Κύριο μέρος του προγράμματος
if __name__ == "__main__":
    # Ανάγνωση δεδομένων από το αρχείο
    num_jobs, num_machines, optimal_makespan, processing_times, job_sequences = read_input_file(file_path)

    # Δημιουργία αντικειμένων Job
    jobs = create_job_objects(num_jobs, processing_times, job_sequences)

    # Εφαρμογή του Shortest Processing Time (SPT)
    total_processing_time_spt = apply_spt(jobs, num_machines)

    # Εκτύπωση των αποτελεσμάτων για το Shortest Processing Time (SPT)
    print("\nResults with Shortest Processing Time (SPT):")
    print_output(jobs)
    print(f"Total Processing Time per Job: {total_processing_time_spt}")

    # Απεικόνιση της λύσης JSSP
    plot_jssp_solution(jobs)
