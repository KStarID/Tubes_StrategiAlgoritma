from ortools.sat.python import cp_model
import time

def read_cost_matrix_from_file(file_path):
            with open(file_path, 'r') as file:
                lines = file.readlines()
                cost_matrix = [[int(num) for num in line.strip().split()] for line in lines]
            return cost_matrix

def read_cost_matrix_from_keyboard():
    print("Masukkan ukuran matriks :")
    n = int(input())
    print("Masukkan matriks :")
    cost_matrix = []
    for _ in range(n):
        row = list(map(int, input().split()))
        cost_matrix.append(row)
    return cost_matrix

def main():
    # Data
    print("\nBonjour, Selamat datang!")
    print("\nPilih opsi input:")
    print("1. Masukkan matriks dari keyboard")
    print("2. Baca matriks dari file teks")

    choice = input("\nMasukkan pilihan (1 atau 2): ")

    if choice == '1':
        cost_matrix = read_cost_matrix_from_keyboard()
        start = time.time()
        work(cost_matrix)
        end = time.time()
        print("Waktu eksekusi   :", end - start)
    elif choice == '2':
        namafile = input("Masukkan file path teks: ")
        print("\n")
        cost_matrix = read_cost_matrix_from_file(namafile)
        start =  time.time()
        work(cost_matrix)
        end = time.time()
        print("Waktu eksekusi   :", end - start)
    else:
        print("Invalid selection. Please try again.")


def work(costs):
    num_workers = len(costs)
    num_tasks = len(costs[0])

    # Model
    model = cp_model.CpModel()

    # Variables
    x = []
    for i in range(num_workers):
        t = []
        for j in range(num_tasks):
            t.append(model.NewBoolVar(f'x[{i},{j}]'))
        x.append(t)

    # Constraints
    # Each worker is assigned to at most one task.
    for i in range(num_workers):
        model.AddAtMostOne(x[i][j] for j in range(num_tasks))

    # Each task is assigned to exactly one worker.
    for j in range(num_tasks):
        model.AddExactlyOne(x[i][j] for i in range(num_workers))

    # Objective
    objective_terms = []
    for i in range(num_workers):
        for j in range(num_tasks):
            objective_terms.append(costs[i][j] * x[i][j])
    model.Minimize(sum(objective_terms))

    # Solve
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Print solution.
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        for i in range(num_workers):
            for j in range(num_tasks):
                if solver.BooleanValue(x[i][j]):
                    print(
                        f'Worker {i} assigned to task {j} Cost = {costs[i][j]}')
        print(f'Total cost       : {solver.ObjectiveValue()}')
    else:
        print('No solution found.')


if __name__ == '__main__':
    main()