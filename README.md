# Minimal-Universal-MultiQudit-Gate-Sets
The code repository alligns with the research paper titled "Practically Implementable Minimal Universal Gate Sets for Multi-Qudit Systems with Cryptographic Validation".

## 1. Introduction

This repository provides a practical implementation and validation framework for a minimal universal gate set for multi-qudit systems. 
It aligns with the paper titled "Practically Implementable Minimal Universal Gate Sets for Multi-Qudit Systems with Cryptographic Validation". 
Unlike generic qubit circuits, qudit circuits leverage higher-dimensional Hilbert spaces. 
Here we validate two cryptographically significant algorithms: **Grover's search** and **Quantum Key Distribution (QKD)**. 
Both implementations are constructed with traditional gates and with decomposed gates synthesized entirely from the universal set `PHASE1 ∪ T_elements`. 
The aim is to confirm functional equivalence and assess performance trade-offs, thereby demonstrating that qudit-based circuits can be realistically deployed for cryptographic applications.

## 2. Repository Structure

```
.
├── __init__.py
├── grover_utils.py
├── grover_circuits.py
├── qkd_utils.py
├── qkd_circuits.py
├── Grover_Measurements/ Grovers Circuit with Traditional Gates.png (histograms generated during execution)
├── Grover_Measurements/ Grovers Circuit with Universal Gates.png (histograms generated during execution)
├── QKD_Measurements/ QKD Basis Choice Distribution.png (distribution plot generated during execution)
├── QKD_Measurements/ QKD Simulation Outcomes.txt (simulation log generated during execution)
```

- **`__init__.py`** → Entry point to run Grover’s Algorithm and QKD simulations.  
- **`grover_utils.py`** → Core utilities for Grover’s algorithm (Hadamard, oracle, diffusion, decomposition).  
- **`grover_circuits.py`** → Builders for Grover circuits (traditional and universal).  
- **`qkd_utils.py`** → Qutrit swap gates, Hadamard generalizations, decomposition utilities.  
- **`qkd_circuits.py`** → QKD simulation circuits for Alice and Bob.  
- **Output folders** store histograms, logs, and distribution plots.  

## 3. Technical Flow

- Execution begins with **`__init__.py`**.  
- For **Grover’s algorithm**: two 4-dimensional qudits are initialized.  
  - Traditional circuit → Generalized Hadamard, Uf, U0, measurement.  
  - Decomposed circuit → Reck’s decomposition of Hadamard-like gates into 2×2 rotations + PHASE1 gates.  
- For **QKD**:  
  - Alice encodes states in rectilinear/diagonal basis.  
  - Bob randomly selects measurement basis.  
  - Both traditional and universal gates are used.  
  - Keys are extracted where bases match.  
- Outputs include:  
  - Histograms of Grover amplified states.  
  - Basis choice distribution plots.  
  - Logs with per-round QKD results.  

## 4. Grover’s Algorithm Validation

### Traditional Circuit

Constructed with generalized qudit gates:  

```python
circuit = cirq.Circuit([
    QuditHGate(d=4)(q0),
    QuditHGate(d=4)(q1),
    UfGate()(q0,q1),
    QuditHGate(d=4)(q0),
    QuditHGate(d=4)(q1),
    U0Gate()(q0,q1),
    QuditHGate(d=4)(q0),
    QuditHGate(d=4)(q1),
    cirq.measure(q0, q1)
])
```

### Universal Circuit

Constructed using Reck’s decomposition:  

```python
H_unitary = QuditHGate(d=4)._unitary_()
R_matrices, Phi = reckon_decompose_unitary(H_unitary)
ops = [ArbitraryGate(d=4, matrix=Phi)(q0), ArbitraryGate(d=4, matrix=Phi)(q1)]
for M in R_matrices[::-1]:
    ops += [ArbitraryGate(d=4, matrix=M)(q0), ArbitraryGate(d=4, matrix=M)(q1)]
```

### Results

- **Traditional Histogram**  
  ![Grover Traditional](./Grover_Measurements/Grovers%20Circuit%20with%20Traditional%20Gates.png)  

- **Universal Histogram**  
  ![Grover Universal](./Grover_Measurements/Grovers%20Circuit%20with%20Universal%20Gates.png)  

**Interpretation:** Both amplify the same marked state, confirming equivalence.  
The universal version has greater depth but functional correctness is preserved.  

## 5. Quantum Key Distribution (QKD) Validation

- Alice chooses random trit (0/1/2) and basis (rectilinear/diagonal).  
- Bob chooses random basis (rectilinear/diagonal).  
- Keys established when bases align.  

### Basis Choice Distribution  

![QKD Basis](./QKD_Measurements/QKD%20Basis%20Choice%20Distribution.png)  

### Example Logs  

```
--- QKD Round 29/100 ---
Alice: Preparing bit 2 in basis 'diagonal'.
Bob: Choosing basis 'diagonal'.
0(d=3): --- Qutrit_0swap2_Gate --- Qu3H --- Qu3H --- M('diagonal_measurement')
0(d=3): --- Qu3M x3 --- Qu3M x5 --- Qu3M x5 --- M('diagonal_measurement')
Bob: Measured bit 2 in basis 'diagonal'.
Bob: Measured bit 2 in basis 'diagonal'.
Alice and Bob used the same basis.
Key established for this round: 2
```

In Round 29 of the QKD simulation, within the traditional setup, Alice randomly selected
the trit “2” and the diagonal basis, while Bob independently chose the same diagonal
basis. On Alice’s side, this resulted in a circuit beginning with the 0swap2 gate
to encode the symbol, followed by a Hadamard gate to realize the diagonal basis. Bob,
matching the basis choice, appended a Hadamard gate before measurement. In case of
universal decomposed gates, all the gates are decomposed into unitary matrices of the
proposed forms and then appended subsequently replacing the traditional gates. The
0swap2 gate has been replaced with one Ri j, one Φbalance and one Φ matrices, while
the Hadamard gate has been replaced with three Ri j, one Φbalance and one Φ matrices.
Both measurements yielded the value “2”, and since the bases aligned, a key bit was
successfully established, exactly as predicted by the principles of QKD.


```
--- QKD Round 67/100 ---
Alice: Preparing bit 0 in basis 'rectilinear'.
Bob: Choosing basis 'diagonal'.
20 Anonymous Submission
0(d=3): --- Qu3H --- M('rectilinear_measurement')
0(d=3): --- Qu3M --- Qu3M --- Qu3M --- Qu3M --- Qu3M --- M('diagonal_measurement')
Bob: Measured bit 1 in basis 'diagonal'.
Bob: Measured bit 2 in basis 'diagonal'.
Alice and Bob used different bases or measurement result invalid.
No key bit established for this round.
```

In Round 67 of the QKD simulation, within the traditional setup, Alice randomly selected
the trit “0” and the rectilinear basis, while Bob independently chose the diagonal
basis. Because of Alice’s choices, this resulted in a circuit that keeps the state unaltered.
Bob, matching the basis choice, appended a Hadamard gate before measurement.
In case of universal decomposed gates, the only Hadamard gate in the circuit has been
replaced with three Ri j, one Φbalance and one Φ matrices. We see both measurements
yielded different values of measured bit, although the choice of bases being different,
this round will anyway not yield any shared key bit.

### Summary  

- 100 rounds simulated.  
- ~52 shared key bits established.  
- Both traditional and universal gates produced identical outcomes.  

## 6. Implementation Details

- **Reck’s decomposition** expresses arbitrary unitaries as products of 2×2 rotations and a diagonal phase.  
- Custom Cirq gates (`QuditHGate`, `Qutrit_0swap1`, `Qutrit_0swap2`) are decomposed into `ArbitraryGate` instances.  
- Circuits use `cirq.LineQid` with dimension=3 (QKD) or 4 (Grover).  
- Outputs:  
  - Histograms (`Matplotlib`)  
  - Logs (plain text)  

## 7. Results & Outputs

### Sample Grover JSON Output  

```json
{
  "Grovers Circuit with Traditional Gates": {
    "measurement_outcomes": "State 10 amplified",
    "states_with_most_probability": "10 - 2741, 11 - 1121, 00 - 1023"
  },
  "Grovers Circuit with Universal Gates": {
    "measurement_outcomes": "State 10 amplified",
    "states_with_most_probability": "10 - 2698, 11 - 1102, 00 - 1031"
  }
}
```

### Sample QKD JSON Output  

```json
{
  "QKD Simulation Response": {
    "Total Rounds Simulated": 100,
    "Number of Key Bits Established": 52,
    "Shared Secret Key": "101001101...",
    "Impression": "Bases matched 52 times; both universal and traditional circuits aligned in 52 cases."
  }
}
```

## 8. Cryptographic Relevance

- Grover’s algorithm validates **attack feasibility** in qudit cryptanalysis.  
- QKD demonstrates **defensive protocol correctness** under decomposition.  
- Equivalence testing confirms minimal gate sets can support cryptography securely.  

## 9. How to Run

### Requirements  

- Python 3.9+  
- Cirq  
- NumPy  
- Matplotlib  

### Installation  

```bash
pip install -r requirements.txt
```

### Run Simulation  

```bash
python __init__.py
```

Outputs will be in `Grover_Measurements/` and `QKD_Measurements/`.  

---

## ✅ Conclusion
This repository validates the practicality of the minimal universal gate set (`PHASE1 ∪ T_elements`) by demonstrating end-to-end cryptographic protocols in a reproducible Python framework.  
Both **Grover** and **QKD** confirm **functional equivalence** between traditional and decomposed implementations, ensuring security and scalability in cryptographic contexts.
