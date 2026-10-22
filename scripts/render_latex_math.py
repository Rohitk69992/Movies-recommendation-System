"""
Render mathematical equations as high-resolution transparent PNG images using Matplotlib.
Uses native mathtext formatting to produce bold, sharp, publication-grade mathematical equations.
"""

import os
import matplotlib.pyplot as plt

os.makedirs("reports/figures/math", exist_ok=True)


def render_math(latex_math, filename, fontsize=16, figsize=(7.5, 1.0)):
    fig = plt.figure(figsize=figsize, dpi=300)
    fig.patch.set_alpha(0.0)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.patch.set_alpha(0.0)
    ax.axis('off')
    ax.text(0.5, 0.5, f"${latex_math}$", fontsize=fontsize, ha='center', va='center',
            color='#0f172a', math_fontfamily='dejavusans')
    out_path = os.path.join("reports/figures/math", filename)
    plt.savefig(out_path, dpi=300, bbox_inches='tight', transparent=True, pad_inches=0.08)
    plt.close()
    print(f"Generated: {out_path}")


def render_all_equations():
    equations = [
        (r"R(m_q, K) = \mathrm{argmax}_{S \subseteq \mathcal{X} \setminus \{m_q\},\, |S|=K} \sum_{v \in S} \cos(\mathbf{u}_q, \mathbf{v}) \qquad (3.1)", "eq_3_1.png", 16, (8.0, 1.1)),
        (r"\cos(\mathbf{u}, \mathbf{v}) = \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\|_2 \, \|\mathbf{v}\|_2} = \frac{\sum_{k=1}^V u_k v_k}{\sqrt{\sum_{k=1}^V u_k^2} \sqrt{\sum_{k=1}^V v_k^2}} \qquad (3.2)", "eq_3_2.png", 16, (8.0, 1.1)),
        (r"\mathrm{TF}(t, d) = f_{t, d} \qquad (5.1)", "eq_5_1.png", 16, (5.0, 0.9)),
        (r"\mathbf{u} = \left[ \mathrm{TF}(t_1, d),\, \mathrm{TF}(t_2, d),\, \dots,\, \mathrm{TF}(t_V, d) \right]^T \in \mathbb{R}^V \qquad (5.2)", "eq_5_2.png", 16, (8.0, 1.1)),
        (r"\cos(\mathbf{u}, \mathbf{v}) = \frac{\mathbf{u}^T \mathbf{v}}{\|\mathbf{u}\|_2 \, \|\mathbf{v}\|_2} = \frac{\sum_{k=1}^V u_k v_k}{\sqrt{\sum_{k=1}^V u_k^2} \sqrt{\sum_{k=1}^V v_k^2}} \qquad (5.3)", "eq_5_3.png", 16, (8.0, 1.1)),
        (r"\cos(\mathbf{u}, \mathbf{v}) = \left\langle \frac{\mathbf{u}}{\|\mathbf{u}\|_2},\, \frac{\mathbf{v}}{\|\mathbf{v}\|_2} \right\rangle = \mathbf{\hat{u}}^T \mathbf{\hat{v}} \qquad (6.1)", "eq_6_1.png", 16, (8.0, 1.1)),
        (r"\mathbf{s} = \mathbf{A} \, \mathbf{\hat{u}}_q, \quad \mathbf{A} \in \mathbb{R}^{N \times V}, \; \mathbf{\hat{u}}_q \in \mathbb{R}^V, \; \mathbf{s} \in [0, 1]^N \qquad (6.2)", "eq_6_2.png", 16, (8.0, 1.1)),
        (r"\mathrm{MMR} = \mathrm{argmax}_{d \in \mathcal{C} \setminus S} \left[ \lambda \cos(\mathbf{u}_q, \mathbf{v}_d) - (1 - \lambda) \max_{d_j \in S} \cos(\mathbf{v}_d, \mathbf{v}_{d_j}) \right] \qquad (11.1)", "eq_11_1.png", 16, (8.0, 1.1)),
    ]
    for latex_math, filename, fontsize, figsize in equations:
        render_math(latex_math, filename, fontsize=fontsize, figsize=figsize)


if __name__ == "__main__":
    render_all_equations()
