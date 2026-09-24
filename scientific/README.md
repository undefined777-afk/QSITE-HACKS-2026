[README (1).md](https://github.com/user-attachments/files/32579711/README.1.md)

# Quantum Phase Detection and Noise Sensitivity in the 1D ANNNI Model

**QSITE 2026 Scientific Track Challenge** | *PennyLane Implementation*

---

## 💡 The Big Picture (Plain English Summary)

Imagine a row of **8 tiny magnets** placed side-by-side. This project explores how those magnets arrange themselves when **three competing physical forces** pull on them at the exact same time:

1. **Neighbor Alignment Force:** Encourages adjacent magnets to point in the same direction ($\uparrow\uparrow$).
2. **Frustration Force ($\kappa$):** Encourages magnets two spots apart to point in opposite directions ($\uparrow \dots \downarrow$).
3. **External Magnetic Field ($h$):** Pulls *all* magnets to point sideways ($\rightarrow\rightarrow$).

Depending on which force wins, the magnets organize into **three distinct magnetic patterns (phases)**:
- 🔴 **Ferromagnetic Phase:** All magnets align in one direction ($\uparrow\uparrow\uparrow\uparrow$).
- 🟣 **Antiphase:** Magnets form a repeating 4-step pattern ($\uparrow\uparrow\downarrow\downarrow$) due to high frustration.
- 🔵 **Paramagnetic Phase:** The magnetic field wins and pulls all magnets sideways ($\rightarrow\rightarrow\rightarrow\rightarrow$).

Using **PennyLane** and **Exact Diagonalization (ED)** in Python, we mapped out where these three phases exist across a $15 \times 15$ grid of conditions ($\kappa$ vs $h$). Then, we introduced **simulated quantum computer noise** ($p = 0.0, 0.01, 0.05$) to measure how quickly real-world gate errors break down these delicate magnetic arrangements.

---

## 🧲 Physical Model & The ANNNI Hamiltonian

The system is mathematically described by the 1D **Axial Next-Nearest-Neighbor Ising (ANNNI)** spin model with periodic boundary conditions (forming a closed ring of 8 spins):

$$\hat{H} = -J_1 \sum_{i=1}^{N} \hat{Z}_i \hat{Z}_{i+1} + J_1 \kappa \sum_{i=1}^{N} \hat{Z}_i \hat{Z}_{i+2} - h \sum_{i=1}^{N} \hat{X}_i$$

### Parameter Breakdown
| Parameter | Symbol | What It Controls physically |
| :--- | :---: | :--- |
| **Coupling Constant** | $J_1 = 1.0$ | Sets the base energy scale for neighboring spin interactions. |
| **Frustration Strength** | $\kappa$ | Controls the next-nearest-neighbor penalty. Higher $\kappa$ drives the system into the **Antiphase**. |
| **Transverse Field** | $h$ | Controls the external magnetic field strength along $X$. Higher $h$ drives the system into the **Paramagnetic Phase**. |

---

## 🔍 How We Detect the Phases (Order Parameters)

Instead of training complex neural networks, we calculate the lowest-energy state (ground state) using exact matrix math (`scipy.linalg.eigh`) and measure two simple physical correlation parameters:

1. **Nearest-Neighbor Correlation ($C_1$):** Measures if adjacent spins point the same way.
   $$C_1 = \frac{1}{N} \sum_{i=1}^{N} \langle \hat{Z}_i \hat{Z}_{i+1} \rangle$$
   - $C_1 \approx +1.0$ $\rightarrow$ **Ferromagnetic Phase**
   - $C_1 \approx 0.0$ $\rightarrow$ **Antiphase or Paramagnetic Phase**

2. **Next-Nearest-Neighbor Correlation ($C_2$):** Measures alignment between spins separated by two spots.
   $$C_2 = \frac{1}{N} \sum_{i=1}^{N} \langle \hat{Z}_i \hat{Z}_{i+2} \rangle$$
   - $C_2 \approx +1.0$ $\rightarrow$ **Ferromagnetic Phase**
   - $C_2 \approx -1.0$ $\rightarrow$ **Antiphase** ($\uparrow\uparrow\downarrow\downarrow$)
   - $C_2 \approx 0.0$ $\rightarrow$ **Paramagnetic Phase**



---

## 🗺️ Visualizing the Phase Diagrams

### 1. Clean Reference Phase Diagram ($p = 0.0$)

The clean heatmap (`clean_phase_diagram.png`) shows sharp transitions between all three phases on a $15 \times 15$ grid. The theoretical boundary equations are overlaid in white:

- **Ising Transition Line ($h_I$):** Theoretical boundary separating Ferromagnetic and Paramagnetic phases.
- **KT Line ($h_{KT}$):** Theoretical boundary separating Antiphase and Paramagnetic phases.
- **BKT Line ($h_{BKT}$):** Bounds the narrow floating phase region.

![Clean Phase Diagram]
<img width="4200" height="1800" alt="clean_phase_diagram" src="https://github.com/user-attachments/assets/a1b521e0-41da-4e25-8a8e-2b3dbac66b6d" />


### 2. Noisy Comparison Diagram ($p = 0.0, 0.01, 0.05$)

To simulate real quantum hardware errors, we applied depolarizing noise (`qml.DepolarizingChannel`) after CNOT gate interactions on PennyLane's `default.mixed` simulator across three noise probability levels:

![Noisy Phase Diagrams Comparison]
<img width="3600" height="4200" alt="noisy_phase_diagrams_comparison" src="https://github.com/user-attachments/assets/29e7bb35-451c-4a17-ac32-47f210f5ab43" />


---

## 🔑 Key Physical Insights

1. **Depolarizing Noise Dampens Correlation:** As noise increases from $p=0.0 \rightarrow 0.01 \rightarrow 0.05$, the bright colors fade toward neutral zero ($0.0$). Quantum errors scramble ordered spin arrangements into a disordered mixed state.
2. **The Antiphase is Fragile:** The period-4 pattern ($\uparrow\uparrow\downarrow\downarrow$) in the Antiphase relies on delicate next-nearest-neighbor correlations ($C_2 \approx -1.0$). CNOT gate errors easily destroy this pattern, causing the dark purple region to shrink rapidly under noise.
3. **The Ferromagnetic Phase is Resilient:** Simple uniform alignment ($\uparrow\uparrow\uparrow\uparrow$) retains its strong correlation ($C_1 \approx +1.0$) much better at low noise levels ($p = 0.01$) compared to the Antiphase.
4. **Boundary Smearing:** Noise broadens the sharp white theoretical boundaries into fuzzy transition zones.

---


```

