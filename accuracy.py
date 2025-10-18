
import pandas as pd
from utils.tools import *


def randomMatrixDecompRecons(n):
    matrix = generate_random_unitary_matrix(n)
    R_matrices, Phi = reckon_decompose_unitary(matrix)
    reconstructed = Phi
    if R_matrices:
        # The R_matrices are stored in the order they are multiplied from left
        # M = R_matrices[0] @ R_matrices[1] @ ... @ R_matrices[-1] @ Phi
        if len(R_matrices)>1: reconstructed = np.linalg.multi_dot(R_matrices) @ Phi
        else: reconstructed = R_matrices @ Phi
    return(matrix, reconstructed)


def decomposition_accuracy(trials = 10):

    table = pd.DataFrame(
        columns = [
            'n-Value', 
            'Trials', 
            'Operator fidelity', 
            'Trace similarity', 
            'Frobenius error', 
            'Spectral norm error', 
            'Eigenphase minimal arc'
            ]
        )

    arr = generate_sorted_random_numbers()
    for n in arr:
        fidelity_score_cumulated = 0
        trace_similarity_score_cumulated = 0
        frobenius_error_cumulated = 0
        spectral_norm_error_cumulated = 0
        eigenphase_spread_cumulated = 0
        
        for a in range(trials):
            matrix, reconstructed = randomMatrixDecompRecons(n)

            fidelity_score  = operator_fidelity(matrix, reconstructed)
            trace_similarity_score  = trace_similarity(matrix, reconstructed)
            frobenius_error_value = frobenius_error(matrix, reconstructed)
            spectral_norm_error_value = spectral_norm_error(matrix, reconstructed)
            eigenphase_spread_value = unitary_eigenphase_spread(matrix, reconstructed)   # radians, in [0, 2π]
            gate_fidelity_score = average_gate_fidelity(matrix, reconstructed)
            gate_fidelity_normalized_score = hilbert_schmidt_inner(matrix, reconstructed, normalized=True)
            diamond_norm_estimate = diamond_norm_unitary_estimate(matrix, reconstructed)          # in [0, 2]
            
            fidelity_score_cumulated += fidelity_score 
            trace_similarity_score_cumulated += trace_similarity_score 
            frobenius_error_cumulated += frobenius_error_value 
            spectral_norm_error_cumulated += spectral_norm_error_value 
            eigenphase_spread_cumulated += eigenphase_spread_value 
            
        table.loc[len(table)] = [
            n, 
            trials, 
            fidelity_score_cumulated/trials, 
            trace_similarity_score_cumulated/trials, 
            frobenius_error_cumulated/trials, 
            spectral_norm_error_cumulated/trials, 
            eigenphase_spread_cumulated/trials
        ]

    return table


if __name__ == "__main__":

    # Grover's Algorithm with Universal Decomposition
    print(" ---- ---- Validation of Decomposition Accuracy ---- ---- ")
    response_table = decomposition_accuracy()
    response_table['n-Value'] = response_table['n-Value'].astype(int)
    print(response_table)

