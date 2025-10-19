
# Question 2

Given a CNN that takes an input image of size **28 × 28 × 3**, it passes through a convolutional layer with **3 filters**, each of size **2 × 2 × 3**, using **valid padding**.


**A.** How many learnable parameters does this convolutional layer have?  
**B.** How many parameters would a fully connected layer require to replicate this convolutional layer’s behavior?

---

## Solution

### A. Learnable Parameters in the Convolutional Layer

- Each filter has size:  
  \[
  2 \times 2 \times 3 = 12
  \]  
  (number of weights per filter)
  
- Each filter has one bias term, so total parameters per filter:  
  \[
  12 + 1 = 13
  \]

- Number of filters: 3

- Therefore, total learnable parameters in the convolutional layer:  
  \[
  3 \times 13 = \mathbf{39}
  \]

---

### B. Parameters in the Equivalent Fully Connected Layer

- **Output size of convolution layer (valid padding):**  
  \[
  (28 - 2 + 1) \times (28 - 2 + 1) = 27 \times 27
  \]  
  Since there are 3 filters, total output units:  
  \[
  27 \times 27 \times 3 = 2187
  \]

- **Input size to fully connected layer:**  
  \[
  28 \times 28 \times 3 = 2352
  \]

- Number of weights:  
  \[
  2352 \times 2187 = 5,143,824
  \]

- Number of biases:  
  \[
  2187
  \]

- **Total parameters:**  
  \[
  5,143,824 + 2,187 = 5,146,011
  \]

---


# Question 3 – Vanishing Gradient in Recurrent Neural Networks (RNNs)

## Mathematical Derivation

Consider a plain (Elman) RNN with hidden state:

$$
\mathbf{h}_t = f\bigl(\mathbf{W}_h\,\mathbf{h}_{t-1} + \mathbf{W}_x\,\mathbf{x}_t + \mathbf{b}\bigr),
$$

where $f$ is an element‑wise non‑linearity (e.g., **tanh** or **σ**).
Suppose the loss $\mathcal{L}$ is computed at the final step $T$.
Using the chain rule, the gradient of the loss with respect to an earlier hidden state $\mathbf{h}_t \;\; (t < T)$ is:

$$
\frac{\partial \mathcal{L}}{\partial \mathbf{h}_t} =
\frac{\partial \mathcal{L}}{\partial \mathbf{h}_T}
\prod_{k=t+1}^{T}
\underbrace{\frac{\partial \mathbf{h}_k}{\partial \mathbf{h}_{k-1}}}_{\displaystyle \mathbf{J}_k}.
$$

For a given step:

$$
\mathbf{J}_k = \mathrm{diag}\bigl(f'(\mathbf{a}_k)\bigr)\,\mathbf{W}_h,
\qquad
\mathbf{a}_k = \mathbf{W}_h\,\mathbf{h}_{k-1} + \mathbf{W}_x\,\mathbf{x}_k + \mathbf{b}.
$$

Taking norms and letting
$\rho = \lVert \mathbf{W}_h \rVert_2$ (spectral norm), and
$\gamma = \max_{z} |f'(z)|$ (for **tanh** or **σ**, $\gamma \le 1$),

$$
\left\lVert\frac{\partial \mathcal{L}}{\partial \mathbf{h}_t}\right\rVert
\le
\left\lVert\frac{\partial \mathcal{L}}{\partial \mathbf{h}_T}\right\rVert
(\gamma \rho)^{T - t}.
$$

* If $\gamma \rho < 1$: the bound **decays exponentially** with time difference $T - t$ → **vanishing gradients**.
* If $\gamma \rho > 1$: the bound **grows exponentially** → **exploding gradients**.

The root cause is the repeated multiplication of Jacobians whose singular values are typically $< 1$ (or $> 1$).

---

## Effect of Look‑Back Window Length

Let the look‑back window size be $L = T - t$.
The gradient bound becomes:

$$
\left\lVert\frac{\partial \mathcal{L}}{\partial \mathbf{h}_{T - L}}\right\rVert
\le
\left\lVert\frac{\partial \mathcal{L}}{\partial \mathbf{h}_T}\right\rVert
(\gamma \rho)^L.
$$

| Window Size $L$ | Bound on Gradient         | Practical Implication                                                                     |
| --------------: | :------------------------ | :---------------------------------------------------------------------------------------- |
|       **Small** | Close to constant         | Gradients survive; the network readily learns short‑term dependencies.                    |
|       **Large** | Exponentially small/large | Vanishing or exploding gradients dominate, hindering learning of long‑range dependencies. |

Therefore, **increasing the sequence length (look‑back window) aggravates the vanishing‑gradient problem** for standard RNNs.

Architectures such as **LSTM** and **GRU**, along with techniques like **orthogonal/identity initialization**, **gating**, **skip connections**, and **gradient clipping**, are popular remedies. These approaches help keep the effective Jacobian closer to identity, limiting exponential decay or growth.
