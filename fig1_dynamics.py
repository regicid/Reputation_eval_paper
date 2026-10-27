# Fig. 1: reputation dynamics r_{t+1} = (1 - lam(1 - beta)) r_t + lam g for beta = 0, 0.8, 1.2.
# Run from the repository root: python3 figures/fig1_dynamics.py
# Set FONT to whatever Garamond you have installed (e.g. "EB Garamond", "Garamond", "Adobe Garamond Pro").
import os
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

FONT = "EB Garamond"
family = FONT if any(f.name == FONT for f in matplotlib.font_manager.fontManager.ttflist) else "serif"
here = os.path.dirname(os.path.abspath(__file__))
plt.rcParams.update({
    "font.family": family, "font.size": 10,
    "mathtext.fontset": "custom", "mathtext.rm": family, "mathtext.it": f"{family}:italic", "mathtext.bf": f"{family}:bold", "mathtext.cal": family,
    "axes.spines.top": False, "axes.spines.right": False,
})

lam, T = 0.3, 60
betas = [0.0, 0.8, 1.1]
titles = [r"$\beta=0$: accurate", r"$\beta=0.8$: amplified, still coupled", r"$\beta=1.1$: decoupled"]
t = np.arange(1, T + 1)

def traj(r1, g, beta):
    a = 1 - lam * (1 - beta)
    r = np.empty(T); r[0] = r1
    for k in range(1, T):
        r[k] = a * r[k - 1] + lam * g
    return r

gs = {-0.2: "#D55E00", 0.2: "#0072B2"}     # colour = true generosity
r1s = {-2.0: "--", 2.0: "-"}               # linestyle = initial reputation

fig, axes = plt.subplots(1, 3, figsize=(9, 3.3))
axes[1].sharey(axes[0])                     # panels 1-2 share a linear scale; panel 3 is free
for ax, beta, title in zip(axes, betas, titles):
    ax.axhline(0, color="gray", lw=0.6)
    for g, c in gs.items():
        ax.axhline(g, color=c, lw=0.9, ls=":", alpha=0.9)   # true generosity
        for r1, ls in r1s.items():
            ax.plot(t, traj(r1, g, beta), color=c, ls=ls, lw=1.6)
    ax.set_title(title); ax.set_xlabel("round")
    if beta > 1:
        ax.set_yscale("symlog", linthresh=2)
axes[0].set_ylabel("reputation $r_t$"); axes[0].set_ylim(-2.6, 2.6)
axes[1].tick_params(labelleft=False)

handles = [Line2D([], [], color=c, lw=1.6, label= f"$g={g:+}$") for g, c in gs.items()] + \
          [Line2D([], [], color="gray", ls=ls, lw=1.6, label= f"$r_0={r1:+g}$") for r1, ls in r1s.items()] + \
          [Line2D([], [], color="gray", ls=":", lw=0.9, label="true generosity $g$")]
fig.legend(handles=handles, frameon=False, fontsize=9, ncol=5, loc="lower center", bbox_to_anchor=(0.5, 0.0))
fig.tight_layout(rect=(0, 0.08, 1, 1))
fig.savefig(os.path.join(here, "fig1_dynamics.png"), dpi=300)
