
import pandas as pd
from utils.tools import *

def count_reck(matrix):
    R_matrices, Phi = reckon_decompose_unitary(matrix)
    return(len(R_matrices)+1)

def count_cnott(matrix, N):
    n = 1
    M = N**n
    Q, _ = np.linalg.qr(matrix)
    gates = li_roberts_yin_decompose(Q)
    return(len(gates))

def gate_comparison():

    comparison_table = pd.DataFrame(columns=[
        'Qudit States', 'Trials Count', 'Li-Robert-Yin Method - Avg Gate Count', 'Recks Method - Avg Gate Count'
        ]
    )
    
    trial = 10
    arr = generate_sorted_random_numbers()
    for N in arr:
        reck_decomposition_count = 0
        li_robert_yin_decomposition_count = 0
        for t in range(trial):
            matrix = generate_random_unitary_matrix(N)
            reck_decomposition_count += count_reck(matrix)
            li_robert_yin_decomposition_count += count_cnott(matrix, N)
        comparison_table.loc[len(comparison_table)] = [N, trial, li_robert_yin_decomposition_count/trial, reck_decomposition_count/trial]

    comparison_table['Qudit States'] = comparison_table['Qudit States'].astype(int)
    comparison_table['Trials Count'] = comparison_table['Trials Count'].astype(int)
    # pd.set_option('display.float_format', lambda x: f'{x:.16f}')

    return comparison_table


if __name__ == "__main__":

    # Average Gate Comparison between Reck's Decomposition and Li-Robert-Yin's Decomposition
    print(" ---- ---- Average Gate Comparison between Reck's Decomposition and Li-Robert-Yin's Decomposition ---- ---- ")
    response_table = gate_comparison()
    print(response_table)

