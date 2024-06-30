import numpy as np

class LP(object):
    def __init__(self, A: np.array, b: np.array, c: np.array):
        self.A = A
        self.b = b
        self.c = c
        self.n, self.m = A.shape
        self.solution = None
        self.start_solution = None

        self.simplex = np.zeros(shape=(self.n + 1, self.n + self.m + 2))
        self.simplex[:-1, :self.m] = A
        self.simplex[:-1, self.m: -2] = np.identity(n=self.n)
        self.simplex[-1, :self.m] = -c
        self.simplex[-1, self.m + self.m] = 1
        self.simplex[:-1, -1] = b

        # print(self.simplex.astype('int32'))

    def get_start_solution(self):
        pass

    def simplex_method(self):
        while True:
            pivot_col = np.argmin(self.simplex[-1, :-2])
            indicator = self.simplex[-1, pivot_col]

            if indicator >= 0:
                print('Simplex table is optimized')
                break

            min_value = 10**10
            has_first = False
            pivot_row = 0

            for i in range(self.n):
                if self.simplex[i, pivot_col] > 0 and self.simplex[i, -1] / self.simplex[i, pivot_col] < min_value:
                    min_value = self.simplex[i, -1] / self.simplex[i, pivot_col]
                    pivot_row = i
                    has_first = True

            if not has_first:
                print('Maximum is not feasible')
                break
            
            self.pivot(np.array([pivot_row, pivot_col]))

    def pivot(self, pivot_indx: np.array):
        p_i, p_j = pivot_indx
        pivot_val = self.simplex[p_i, p_j]

        if pivot_val == 0:
            return

        for i in range(self.n + 1):
            cur_val = self.simplex[i, p_j]

            if p_i != i and cur_val != 0:
                self.simplex[i, :] = self.simplex[i, :] * pivot_val - self.simplex[p_i, :] * cur_val

                if self.simplex[i, -1] < 0:
                    self.simplex[i, :] *= -1

                if self.simplex[-1, -2] < 0:
                    self.simplex[-1, :] *= -1


def main():
    A = np.array([[1, 1,], [2, 3]])
    b = np.array([480, 1200])
    c = np.array([3, 4])

    P = LP(A, b, c)
    P.simplex_method()

    print(P.simplex.astype("int32"))
    
    M = np.array([[1, 0, 0], [0, 3, 0], [0, 0, 3]])
    N = np.array([240, 720, 5040])
    print(np.linalg.inv(M).dot(N)[:2].dot(c))
    # print(x.dot(c))

if __name__ == '__main__':
    main()
