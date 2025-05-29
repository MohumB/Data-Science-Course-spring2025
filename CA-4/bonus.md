# Question 3 – Vanishing Gradient in Recurrent Neural Networks (RNNs)

## Mathematical derivation

Consider a plain (Elman) RNN with hidden state  

\[
\mathbf{h}_t = f\bigl(\mathbf{W}_h\,\mathbf{h}_{t-1} + \mathbf{W}_x\,\mathbf{x}_t + \mathbf{b}\bigr),
\]

where *f* is an element‑wise non‑linearity (e.g. **tanh** or **σ**).  
Suppose the loss \(\mathcal L\) is computed at the final step \(T\).
Using the chain rule, the gradient of the loss with respect to an
earlier hidden state \(\mathbf{h}_t\;(t < T)\) is

\[
\frac{\partial \mathcal L}{\partial \mathbf{h}_t} =
    \frac{\partial \mathcal L}{\partial \mathbf{h}_T}
    \prod_{k=t+1}^{T}
    \underbrace{\frac{\partial \mathbf{h}_k}{\partial \mathbf{h}_{k-1}}}_{\displaystyle \mathbf{J}_k}.
\]

For a given step  

\[
\mathbf{J}_k = \mathrm{diag}\bigl(f'(\mathbf{a}_k)\bigr)\;\mathbf{W}_h,
\qquad
\mathbf{a}_k = \mathbf{W}_h\,\mathbf{h}_{k-1} + \mathbf{W}_x\,\mathbf{x}_k + \mathbf{b}.
\]

Taking norms and letting  
\(\rho = \lVert \mathbf{W}_h \rVert_2\) (spectral norm) and  
\(\gamma = \max_{z}|f'(z)|\) (for **tanh** or **σ**, \(\gamma \le 1\)),

\[
\Bigl\lVert\frac{\partial \mathcal L}{\partial \mathbf{h}_t}\Bigr\rVert
\le
\Bigl\lVert\frac{\partial \mathcal L}{\partial \mathbf{h}_T}\Bigr\rVert
(\gamma\,\rho)^{\,T-t}.
\]

* If \(\gamma\,\rho < 1\), the bound **decays exponentially** with the temporal
  distance \((T-t)\) – **vanishing gradients**.
* If \(\gamma\,\rho > 1\), it **grows exponentially** – **exploding gradients**.

The root cause is the repeated multiplication of Jacobians whose
singular values are typically < 1 (or > 1).

## Effect of look‑back window length

Let the look‑back window size be \(L = T - t\).  
The gradient bound becomes  

\[
\Bigl\lVert\frac{\partial \mathcal L}{\partial \mathbf{h}_{T-L}}\Bigr\rVert
\le
\Bigl\lVert\frac{\partial \mathcal L}{\partial \mathbf{h}_T}\Bigr\rVert
(\gamma\,\rho)^{L}.
\]

| Window size \(L\) | Bound on gradient | Practical implication |
|-------------------:|:------------------|:----------------------|
| **Small**          | Close to constant | Gradients survive; the network readily learns short‑term dependencies. |
| **Large**          | Exponentially small (or large) | Vanishing/exploding gradients dominate, hindering learning of long‑range dependencies. |

Therefore, **increasing the sequence length (look‑back window) aggravates
the vanishing‑gradient problem** for standard RNNs.  
Architectures such as **LSTM** and **GRU**, orthogonal/identity initialization,
gating, skip connections, and gradient clipping are popular remedies
because they keep the effective Jacobian closer to identity, limiting the
exponential decay or growth.

---
