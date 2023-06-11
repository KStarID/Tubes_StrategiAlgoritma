import time

#membuat fungsi utama
def assignment_problem(cost_matrix):
    #menyimpan ukuran matrix
    n = len(cost_matrix)
    #menyimpan solusi / cost terbaik
    min_cost = float('inf')

    #fungsi menghitung batas (bound) pada simpul-simpul yang belum dipilih
    def calculate_bound(cost_matrix, path, level):
        bound = 0
        used = [False] * n

        for i in range(level):
            bound += cost_matrix[path[i]][i]
            used[path[i]] = True

        for i in range(level, n):
            min_cost = float('inf')
            for j in range(n):
                if not used[j] and cost_matrix[j][i] < min_cost:
                    min_cost = cost_matrix[j][i]
            bound += min_cost

        return bound

    
    def branch_and_bound(cost_matrix):
        min_cost = float('inf')
        path = list(range(n))
        best_path = None

        #fungsi untuk eksplorasi pencarian
        def backtrack(cost_matrix, path, level):
            nonlocal min_cost, best_path

            #Periksa level saat ini pada var n (ukuran matriks)
            if level == n:
                cost = sum(cost_matrix[i][path[i]] for i in range(n))
                if cost < min_cost:
                    min_cost = cost
                    best_path = path.copy()
                return

            #batasan eksplorasi jika sudah melebihi nilai minimum / optimal
            bound = calculate_bound(cost_matrix, path, level)
            if bound >= min_cost:
                return

            for i in range(level, n):
                path[level], path[i] = path[i], path[level]
                backtrack(cost_matrix, path, level + 1)
                path[level], path[i] = path[i], path[level]

        backtrack(cost_matrix, path, 0)
        return min_cost, best_path
   
    #menyelesaikan masalah
    min_cost, best_path = branch_and_bound(cost_matrix)

    #menampilkan hasil
    print("Cost (Biaya)     :", min_cost)
    print("Solusi           :", [x+1 for x in best_path])  # Menampilkan indeks dimulai dari 1

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

#main program
print("\nBonjour, Selamat datang!")
print("\nPilih opsi input:")
print("1. Masukkan matriks dari keyboard")
print("2. Baca matriks dari file teks")

print(" ")
option = input("Masukkan pilihan (1 atau 2): ")

if option == "1":
    cost_matrix = read_cost_matrix_from_keyboard()
    start = time.time()
    assignment_problem(cost_matrix)
    end = time.time()
    print("Waktu Eksekusi   :", end - start)
elif option == "2":
    file_path = input("Masukkan file path teks: ")
    cost_matrix = read_cost_matrix_from_file(file_path)
    start = time.time()
    assignment_problem(cost_matrix)
    end = time.time()
    print("Waktu Eksekusi   :", end - start)
else:
    print("Pilihan tidak valid. Program berakhir.\n")
