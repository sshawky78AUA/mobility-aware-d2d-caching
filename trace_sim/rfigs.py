"""Figures of Section VI from results/*.npz (same style as tools/draft_figs.py)."""
import numpy as np, matplotlib, sys, os
matplotlib.use('Agg'); import matplotlib.pyplot as plt
OUT = sys.argv[1]
plt.rcParams.update({'font.size': 9, 'axes.grid': True, 'grid.alpha': .25, 'legend.fontsize': 7.2, 'font.family': 'serif', 'font.serif': ['Liberation Serif', 'DejaVu Serif'], 'pdf.fonttype': 42,
                     'mathtext.fontset': 'stix', 'axes.linewidth': .8, 'legend.framealpha': .9})
ST = {'LP': ('k', '-', 'o', 'LP (proposed)'), 'greedy': ((.47, .67, .19), '-.', '^', 'Greedy whole-copy'),
      'crowd': ((.49, .18, .56), ':', 'd', 'Crowd mobility'), 'pairwise': ((0, .45, .74), '--', 's', 'Pairwise contacts'),
      'local': ((.85, .33, .10), '-', 'v', 'Local caching'), 'nosharing': ((.6, .6, .6), '--', 'x', 'No D2D sharing'),
      'popularity': ((.75, .55, .1), ':', 'p', 'Popularity')}
def pm(ax, x, y, k, err=None, label=None, nmk=8):
    c, ls, mk, nm = ST[k]; idx = np.unique(np.round(np.linspace(0, len(x) - 1, min(nmk, len(x)))).astype(int))
    ax.plot(x, y, ls, color=c, lw=1.5, marker=mk, markevery=list(idx), ms=4.5, mfc='w', label=label or nm)
    if err is not None: ax.fill_between(x, y - err, y + err, color=c, alpha=.12, lw=0)
def se(a): return a.std(0, ddof=1) / np.sqrt(a.shape[0]) if a.shape[0] > 1 else 0 * a[0]
def done(fig, n):
    if len(fig.axes) >= 2 and fig.get_size_inches()[0] > 6:      # two-panel figures: identical panel geometry
        H = fig.get_size_inches()[1]; bot, axh = 0.444, 1.56        # same panel geometry (inches) in every figure
        fig.subplots_adjust(left=.085, right=.985, bottom=bot / H, top=(bot + axh) / H, wspace=.30)
        if n == 'fig_dec_trace': pass
    else:
        fig.tight_layout()
    fig.savefig(f'{OUT}/{n}.pdf'); plt.close(fig)
R = 'results'
if os.path.exists(f'{R}/trace.npz'):
    d = np.load(f'{R}/trace.npz'); fig, ax = plt.subplots(1, 2, figsize=(7.0, 2.29)); h = np.arange(8, 20)
    for city, c in (('NYC', 'k'), ('TKY', (.85, .33, .10))):
        ax[0].plot(h + .5, d[f'{city}_eta'], '-o', color=c, ms=3.5, mfc='w', label={'NYC': 'New York', 'TKY': 'Tokyo'}[city])
    ax[0].set(xlabel='Hour of day', ylabel=r'Activity $\eta_t$ (mean 1)', title='(a) Daily activity profile', xticks=[8, 11, 14, 17, 20]); ax[0].legend()
    w = .26; k = np.arange(8)
    for i, (N, c) in enumerate(((200, '.75'), (400, '.45'), (1000, '.1'))):
        v = d[f'NYC_others_{N}'][:8].copy(); v[-1] += d[f'NYC_others_{N}'][8:].sum()
        ax[1].bar(k + (i - 1) * w, v, w, color=c, label=f'$N={N}$')
    ax[1].set(xlabel='Other users at the requester\'s location', ylabel='Fraction of requests', title='(b) Co-located users, New York',
              xticks=k, xticklabels=[str(i) for i in range(7)] + ['7+']); ax[1].legend(); ax[1].grid(axis='x', visible=False)
    done(fig, 'fig_trace')
if os.path.exists(f'{R}/central_NYC.npz'):
    d = np.load(f'{R}/central_NYC.npz'); n = int(d['done']); x = d['rhos']
    fig, ax = plt.subplots(1, 2, figsize=(7.0, 2.66))
    for k in ('LP', 'greedy', 'crowd', 'pairwise', 'local', 'nosharing', 'popularity'):
        a = 100 * d[f'sav_{k}'][:n]; pm(ax[0], x, a.mean(0), k)
    ax[0].set(xlabel=r'Reward $\rho=rT$ (fraction of the peak price)', ylabel=r'SP saving $\Delta C/C^{\mathcal{R}}$ (%)', title='(a) SP saving', xlim=(0, 1), ylim=(0, None))
    hl, ll = ax[0].get_legend_handles_labels()
    fig.legend(hl, ll, loc='upper center', ncol=4, fontsize=7, frameon=False, bbox_to_anchor=(.53, 1.01), columnspacing=1.6, handlelength=2.4)
    base = 100 * d['sav_nosharing'][:n]
    for k in ('LP', 'greedy', 'crowd', 'local', 'pairwise'):
        g = 100 * d[f'sav_{k}'][:n] - base; pm(ax[1], x, g.mean(0), k, se(g))
    ax[1].axhline(0, color=ST['nosharing'][0], lw=1.0, ls='--')
    ax[1].set(xlabel=r'Reward $\rho=rT$', ylabel='Gain over no D2D sharing (points)', title='(b) Value of D2D and of mobility', xscale='log', xlim=(.02, 1))
    ax[0].set_xscale('log'); ax[0].set_xlim(.02, 1)
    done(fig, 'fig_central_trace')
if os.path.exists(f'{R}/density.npz'):
    d = np.load(f'{R}/density.npz'); Ns = d['Ns']; fig, ax = plt.subplots(1, 2, figsize=(7.0, 2.29))
    for city, c, mk in (('NYC', 'k', 'o'), ('TKY', (.85, .33, .10), 's')):
        if f'{city}_LP' not in d: continue
        m = (d[f'{city}_LP'] != 0).all(1)
        if not m.any(): continue
        nm = {'NYC': 'New York', 'TKY': 'Tokyo'}[city]
        g1 = 100 * (d[f'{city}_LP'] - d[f'{city}_nosharing'])[m]; g2 = 100 * (d[f'{city}_LP'] - d[f'{city}_local'])[m]
        ax[0].plot(Ns, g1.mean(0), '-', marker=mk, color=c, mfc='w', label=f'{nm}: over no D2D'); ax[0].fill_between(Ns, g1.mean(0) - se(g1), g1.mean(0) + se(g1), color=c, alpha=.12, lw=0)
        ax[0].plot(Ns, g2.mean(0), '--', marker=mk, color=c, mfc='w', label=f'{nm}: over local caching'); ax[0].fill_between(Ns, g2.mean(0) - se(g2), g2.mean(0) + se(g2), color=c, alpha=.12, lw=0)
        t = d[f'{city}_t'][m]; ax[1].plot(Ns, t.mean(0), '-', marker=mk, color=c, mfc='w', label=nm)
    import matplotlib.lines as mli
    h_city = [mli.Line2D([], [], color='k', marker='o', mfc='w', lw=1.5, label='New York'),
              mli.Line2D([], [], color=(.85, .33, .10), marker='s', mfc='w', lw=1.5, label='Tokyo')]
    h_base = [mli.Line2D([], [], color='.3', ls='-', lw=1.5, label='over no D2D sharing'),
              mli.Line2D([], [], color='.3', ls='--', lw=1.5, label='over local caching')]
    l1 = ax[0].legend(handles=h_city, loc='upper left', fontsize=7, title='City', title_fontsize=7)
    ax[0].add_artist(l1)
    ax[0].legend(handles=h_base, loc='upper left', bbox_to_anchor=(0.30, 1.0), fontsize=7, title='LP gain', title_fontsize=7)
    ax[0].set(xlabel='Participating users $N$', ylabel='Gain of the LP (points)', title=r'(a) Gain versus user density, $\rho=0.1$', ylim=(0, 14))
    ax[1].set(xlabel='Participating users $N$', ylabel='LP time for $M=1000$ items (s)', title='(b) Computation time', yscale='log'); ax[1].legend()
    done(fig, 'fig_density')
if os.path.exists(f'{R}/dec.npz'):
    d = np.load(f'{R}/dec.npz'); g = d['grid']; fig, ax = plt.subplots(1, 2, figsize=(7.0, 2.29)); cols = ['k', (.85, .33, .10), (0, .45, .74)]
    best = []
    for kap, c in zip(d['kappas'], cols):
        Pt = d[f'P_{kap}']; m = (Pt != 0).all(1); Cm = d[f'C_{kap}'][m].mean(0); Pm = Pt[m].mean(0)
        ax[0].plot(g, Cm, '-', color=c, lw=1.5, label=fr'centralized, $\kappa={kap}$')
        ax[0].plot(g, Pm, '--', color=c, lw=1.5, label=fr'decentralized, $\kappa={kap}$')
        k = int(np.argmin(Pm)); ax[0].plot(g[k], Pm[k], '*', ms=9, mfc='gold', mec='k', mew=.6, zorder=5); best.append((kap, g[k], Pm[k], Cm[k]))
    ax[0].axhline(1, color='.5', lw=.6, ls=':')
    ax[0].set(xlabel=r'Reward as a fraction of the off-peak price, $r/y_o$', ylabel=r'SP cost $C^{\mathcal{P}}/C^{\mathcal{R}}$', title='(a) SP cost versus reward', ylim=(.5, 1.15), xlim=(0, 1))
    ax[0].legend(fontsize=5.6, ncol=1, loc='lower right')
    b = np.array(best); xk = np.arange(len(b))
    ax[1].bar(xk - .18, 100 * (b[:, 2] / b[:, 3] - 1), .34, color='.35', label='gap to centralized at $r^*$ (%)')
    ax[1].bar(xk + .18, 100 * (1 - b[:, 2]), .34, color=(.85, .33, .10), label='SP saving at $r^*$ (%)')
    for i_, (kap, gs, pc, cc) in enumerate(best): ax[1].text(i_, 100 * (1 - pc) + .6, fr'$r^*={gs:.1f}\,y_o$', ha='center', fontsize=7)
    ax[1].set(xticks=xk, xticklabels=[fr'$\kappa={k}$' for k in b[:, 0]], ylabel='%', title='(b) At the best uniform reward (P2)', ylim=(0, 100 * (1 - b[:, 2]).max() + 4))
    ax[1].legend(fontsize=6.5, loc='upper right'); ax[1].grid(axis='x', visible=False)
    done(fig, 'fig_dec_trace')
if os.path.exists(f'{R}/learn.npz'):
    d = np.load(f'{R}/learn.npz'); Ds = d['Ds']; m = (d['learned'] != 0).all(1); fig, ax = plt.subplots(1, 1, figsize=(3.45, 2.6))
    if m.any():
        base = 100 * d['local'][m][:, None]
        L_ = 100 * d['learned'][m] - base; Cr = 100 * d['crowd'][m] - base; Or = 100 * (d['oracle'][m] - d['local'][m])
        pm(ax, Ds, L_.mean(0), 'LP', se(L_), label='LP, learned profiles'); pm(ax, Ds, Cr.mean(0), 'crowd', se(Cr), label='Crowd mobility, learned')
        ax.axhline(Or.mean(), color='k', ls=':', lw=1, label='LP, test-period profiles')
        ax.axhline(0, color=ST['local'][0], lw=1.2, label='Local caching')
        ax.set(xscale='log', xlabel='Training weekdays $D$', ylabel='Gain over local caching (points)', title=r'Learning from past days, $\rho=0.1$',
               xticks=list(Ds), xticklabels=[str(v) for v in Ds], ylim=(-.1, Or.mean() * 1.25)); ax.legend(fontsize=6.3, loc='lower right')
    done(fig, 'fig_learn_trace')
print('figs ok')
