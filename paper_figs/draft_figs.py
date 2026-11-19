"""Draft figures for the PDF from the .mat files written by the MATLAB
experiment scripts. Same data and the same style as method_style.m."""
import sys, numpy as np, scipy.io as sio, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
F = sys.argv[1]
plt.rcParams.update({'font.size': 9, 'axes.grid': True, 'grid.alpha': .25, 'legend.fontsize': 7.5,
                     'font.family': 'serif', 'font.serif': ['Liberation Serif', 'DejaVu Serif'], 'pdf.fonttype': 42, 'mathtext.fontset': 'stix', 'axes.linewidth': .8,
                     'legend.framealpha': .9})
ST = {  # color, linestyle, marker, label  (mirrors method_style.m)
    'lp':      ((0, 0, 0),          '-',  'o', 'LP (coded)'),
    'central': ((0, 0, 0),          '-',  'o', r'Centralized $C^*(r)$'),
    'whole':   ((0, .45, .74),      '--', 's', 'Best whole-copy'),
    'greedy':  ((.47, .67, .19),    '-.', '^', 'Greedy'),
    'crowd':   ((.49, .18, .56),    ':',  'd', 'Crowd mobility'),
    'nod2d':   ((.85, .33, .10),    '-',  'v', 'No D2D'),
    'best':    ((.47, .67, .19),    '--', '^', 'SP-best NE'),
    'worst':   ((.85, .33, .10),    ':',  'v', 'SP-worst NE'),
    'fair':    ((0, .45, .74),      '-.', 's', 'Fair NE'),
    'pot':     ((.49, .18, .56),    '-',  'd', 'Potential NE')}
def pm(ax, x, y, key, nmk=8, label=None):
    c, ls, mk, nm = ST[key]; x = np.asarray(x, float); y = np.asarray(y, float)
    idx = np.unique(np.round(np.linspace(0, len(x) - 1, min(nmk, len(x)))).astype(int))
    ax.plot(x, y, ls, color=c, lw=1.5, marker=mk, markevery=list(idx), ms=4.5, mfc='w', label=label or nm)
def L(n): return sio.loadmat(f'{F}/{n}.mat')
def two(): return plt.subplots(1, 2, figsize=(7.0, 2.6))
def done(fig, n): fig.tight_layout(); fig.savefig(f'{F}/{n}.pdf'); plt.close(fig)

# Worked example (three users, one item): both schemes on the same reward axis (y_o = 1)
d = L('exp0'); cu = ['#4C72B0', '#DD8452', '#55A868']; yo = float(np.ravel(d['yo'])[0])
tau = d['tau'].ravel(); sn = d['sn'].ravel(); ph = d['phat'].ravel()
rg = np.round(np.arange(0, 1.0001, .005), 4)
def on_grid(x, X, xq):           # step-wise lookup of X(:,x) at xq (zero outside the data range)
    out = np.zeros((X.shape[0], len(xq)))
    for k, v in enumerate(xq):
        idx = np.where(x <= v + 1e-9)[0]
        if len(idx) and v <= x[-1] + 1e-9: out[:, k] = X[:, idx[-1]]
    return out
Xc = on_grid(d['rs'].ravel(), d['Xc'], rg)
rpx = d['rps'].ravel()                                    # users' cost r' = y_o - r
Xd = np.zeros((3, len(rg))); multi = np.zeros(len(rg), bool); fail = np.zeros(len(rg), bool)
for k, r in enumerate(rg):
    v = yo - r; idx = np.where(rpx <= v + 1e-9)[0]
    if v <= rpx[-1] + 1e-9 and len(idx):
        Xd[:, k] = d['Xf'][:, idx[-1]]; multi[k] = d['multi'].ravel()[idx[-1]]; fail[k] = not d['propOK'].ravel()[idx[-1]]
fig, ax = plt.subplots(1, 3, figsize=(7.16, 2.65))
def stack(a_, x, X, lbl=True):
    base = np.zeros_like(x, float)
    for n in range(3):
        top = base + X[n]
        a_.fill_between(x, base, top, step='post', color=cu[n], alpha=.85, lw=0, label=f'user {n+1}' if lbl else None)
        base = top
    a_.step(x, base, where='post', color='k', lw=1.0)
    a_.grid(False); a_.yaxis.grid(True, alpha=.25)
def spans(a_, x, mask, y0, y1, **kw):
    m = np.r_[False, mask, False].astype(int); st = np.where(np.diff(m) == 1)[0]; en = np.where(np.diff(m) == -1)[0] - 1
    for i0, i1 in zip(st, en):
        if i1 > i0: a_.fill_between([x[i0], x[min(i1 + 1, len(x) - 1)]], y0, y1, **kw)
# (a) centralized
stack(ax[0], rg, Xc)
for xm, t in [(.075, '3'), (.2, '2'), (.315, '1.5'), (.56, '1'), (.87, '0')]:
    ax[0].text(xm, 3.12, t, ha='center', fontsize=7.5, color='.25')
for v in (tau.min(), sn.max()): ax[0].axvline(v, color='.3', ls=(0, (2, 2)), lw=.8)
ax[0].set(xlabel='Reward $r$', ylabel=r'Copies cached, $\Sigma_n x_n/S$', title='(a) Centralized', xlim=(0, 1), ylim=(0, 3.4), yticks=np.arange(0, 3.01, .5),
          xticks=[0, tau.min(), .5, sn.max(), 1], xticklabels=['0', '$r_1$', '0.5', '$r_N$', '1'])
ax[0].legend(loc='upper right', fontsize=6.5, bbox_to_anchor=(1, .9))
# (b) decentralized, fair equilibrium
stack(ax[1], rg, Xd, lbl=False)
spans(ax[1], rg, multi, 3.12, 3.24, color='.6', lw=0)
spans(ax[1], rg, fail, 3.27, 3.39, color='#C44E52', lw=0)
for v in (yo - ph.max(), yo - tau.min()): ax[1].axvline(v, color='.3', ls=(0, (2, 2)), lw=.8)
import matplotlib.patches as mpa
ax[1].legend(handles=[mpa.Patch(color='.6', label='multiple NE'), mpa.Patch(color='#C44E52', label='proportional rule fails')],
             loc='upper left', fontsize=6.5, bbox_to_anchor=(0, .9))
ax[1].set(xlabel=r"Reward $r$ (users pay $r'=1-r$)", ylabel=r'Copies cached, $\Sigma_n x_n/S$', title='(b) Decentralized (fair NE)', xlim=(0, 1), ylim=(0, 3.4), yticks=np.arange(0, 3.01, .5),
          xticks=[0, yo - ph.max(), yo - tau.min()], xticklabels=['0', r'$1-\hat{p}_1$', r'$1-\tilde{p}_3$'])
# (c) SP cost: three regimes, gap shaded, solution of (P2) marked
rr = d['rr'].ravel(); CP = d['CP']
r_lo = yo - ph.max(); gap = CP[1] - CP[0]
r_hi = rr[np.where((rr > r_lo) & (CP[1] > 1 + 1e-6))[0][0]]           # users over-cache: SP pays more than with no caching
for x0, x1, t, y in [(0, r_lo, 'users do\nnot cache', 2.42), (r_lo, r_hi, 'near\noptimal', 2.42), (r_hi, 1, 'users\nover-cache', .62)]:
    ax[2].text((x0 + x1) / 2, y, t, ha='center', va='top', fontsize=6.3, color='.3', linespacing=.95)
for v in (r_lo, r_hi): ax[2].axvline(v, color='.3', ls=(0, (2, 2)), lw=.8)
ax[2].fill_between(rr, CP[0], CP[1], where=gap > 1e-9, color='#C44E52', alpha=.18, lw=0, label='cost of decentralization')
ax[2].plot(rr, CP[0], '-', color='k', lw=1.6, label='centralized')
ax[2].plot(rr, CP[1], '-', color='#4C72B0', lw=1.6, label='decentralized (fair NE)')
k = np.argmin(CP[1]); ax[2].plot(rr[k], CP[1, k], '*', ms=10, mfc='gold', mec='k', mew=.6, zorder=5, label='best reward, (P2)')
ax[2].axhline(1, color='.5', lw=.6, ls=':')
ax[2].set(xlabel='Reward $r$', ylabel=r'SP cost $C^{\mathcal{P}}/C^{\mathcal{R}}$', title='(c) SP cost', ylim=(0, 2.6), xlim=(0, 1),
          xticks=[0, .5, 1])
ax[2].legend(loc='upper left', fontsize=6, bbox_to_anchor=(0, .8), framealpha=.95)
for a_ in ax:
    a_.spines[['top', 'right']].set_visible(False); a_.title.set_fontsize(9); a_.title.set_fontweight('normal'); a_.set_title(a_.get_title(), pad=7)
fig.tight_layout(w_pad=1.0); fig.savefig(f'{F}/fig_example.pdf'); plt.close(fig)

# Fig. 2: two users (steps drawn as steps)
d = L('exp1'); r = d['rps'].ravel(); xf, xp, muf, mup = d['xf'], d['xp'], d['muf'], d['mup']
multi = d['multi'].ravel().astype(bool); cl = [(.85, .33, .10), (0, .45, .74)]
fig, ax = two(); i = np.where(multi)[0]
ax[0].axvspan(r[i[0]], r[i[-1]], color='0.9', label='multiple NE')
for n in range(2):
    ax[0].step(r, xf[n], '-', where='post', color=cl[n], lw=1.6, label=f'$x_{n+1}$, fair')
    ax[0].step(r, xp[n], '--', where='post', color=cl[n], lw=1.2, label=f'$x_{n+1}$, potential')
ax[0].set(xlabel="Caching cost $r'$", ylabel='$x_n^m/S_m$', title='(a) Equilibrium placement', ylim=(-.05, 1.08)); ax[0].legend(loc='center right')
def brk(x, y, tol=.02):
    x = np.asarray(x, float).copy(); y = np.asarray(y, float).copy(); j = np.where(np.abs(np.diff(y)) > tol)[0] + 1
    return np.insert(x, j, np.nan), np.insert(y, j, np.nan)
for n in range(2):
    ax[1].plot(*brk(r, muf[n]), '-', color=cl[n], lw=1.6, label=rf'$\mu_{n+1}^{{\mathcal{{P}}}}$, fair')
    ax[1].plot(*brk(r, mup[n]), '--', color=cl[n], lw=1.2, label=rf'$\mu_{n+1}^{{\mathcal{{P}}}}$, potential')
ax[1].axvspan(r[i[0]], r[i[-1]], color='0.9', zorder=0)
ax[1].set(xlabel="Caching cost $r'$", ylabel=r'Expected payment $\mu_n^{\mathcal{P}}$', title='(b) User payments', ylim=(-.03, .9)); ax[1].legend(loc='upper left')
done(fig, 'fig_two_users')

# Fig. 3: centralized vs reward
d = L('exp2'); r = d['rs'].ravel(); C = 1 - d['Cn'].mean(0); X = d['Xc'].mean(0)
fig, ax = two()
for j, k in enumerate(['lp', 'whole', 'greedy', 'crowd', 'nod2d']): pm(ax[0], r, C[:, j], k, 9)
ax[0].set(xlabel='Reward $r$', ylabel=r'SP saving $\Delta C/C^{\mathcal{R}}$', title='(a) SP saving', ylim=(0, 1.02), xlim=(0, .6)); ax[0].legend()
for j, k in enumerate(['lp', 'crowd', 'nod2d']): pm(ax[1], r, np.maximum(X[:, j], 1e-3), k, 9)
ax[1].set(xlabel='Reward $r$', ylabel='Copies per item', title='(b) Total placement $X^*(r)/M$', yscale='log', ylim=(1e-2, 10), xlim=(0, .6)); ax[1].legend()
done(fig, 'fig_central_r')

# Fig. 4: mobility (dispersion on the x-axis)
d = L('exp4'); S = d['sav'].mean(0); ds = d['ds'].ravel()
fig, ax = two()
for j, k in enumerate(['lp', 'nod2d', 'crowd']): pm(ax[0], ds, S[:, j], k, 11)
ax[0].set(xlabel=r'Dispersion $\delta$', ylabel=r'SP saving $\Delta C/C^{\mathcal{R}}$', title='(a) SP saving, $r=0.2$'); ax[0].legend()
g = d['sav'][:, :, [0, 2]] - d['sav'][:, :, [1]]
for j, k in enumerate(['lp', 'crowd']):
    m = g[:, :, j].mean(0); sd = g[:, :, j].std(0) / np.sqrt(g.shape[0])
    pm(ax[1], ds, 100 * m, k, 11); ax[1].fill_between(ds, 100 * (m - sd), 100 * (m + sd), color=ST[k][0], alpha=.12, lw=0)
ax[1].set(xlabel=r'Dispersion $\delta$', ylabel='Gain over No D2D (points of %)', title='(b) Value of mobility information'); ax[1].legend()
done(fig, 'fig_mobility')

# Fig. 5: scalability
try:
    d = L('exp5'); Ns = d['Ns'].ravel(); S = d['sav'].mean(0); T = d['tim'].mean(0)
    fig, ax = two()
    for j, k in enumerate(['lp', 'greedy', 'nod2d', 'crowd']): pm(ax[0], Ns, S[:, j], k, len(Ns), label={'lp': 'SAA LP (coded)'}.get(k))
    ax[0].set(xlabel='Number of users $N$', ylabel=r'SP saving $\Delta C/C^{\mathcal{R}}$', title='(a) SP saving, $r=0.2$'); ax[0].legend(loc='upper left')
    pm(ax[1], Ns, T[:, 0], 'lp', len(Ns), 'SAA LP'); pm(ax[1], Ns, T[:, 1], 'greedy', len(Ns))
    ax[1].set(xlabel='Number of users $N$', ylabel='Run time (s)', title='(b) Computation time, $M=10$', yscale='log'); ax[1].legend()
    done(fig, 'fig_scalability')
except FileNotFoundError: print('exp5 missing')

# Fig. 6: decentralized. The four selection rules differ by <1%, so the
# SP-best/SP-worst range is drawn as a band, with the fair and potential NE.
d = L('exp6'); r = d['rs'].ravel(); J = d['J'].mean(0); U = d['U'].mean(0)
fig, ax = two()
for a_, Y, ttl, yl in [(ax[0], J, '(a) SP cost', r'SP cost $C^{\mathcal{P}}/C^{\mathcal{R}}$'),
                       (ax[1], U, '(b) User payments', r'Total user payment $/C^{\mathcal{R}}$')]:
    lo = np.minimum(Y[:, 1], Y[:, 2]); hi = np.maximum(Y[:, 1], Y[:, 2])
    a_.fill_between(r, lo, hi, color=ST['worst'][0], alpha=.25, lw=0, label='SP-best to SP-worst NE')
    pm(a_, r, Y[:, 0], 'central', 9); pm(a_, r, Y[:, 3], 'fair', 9); pm(a_, r, Y[:, 4], 'pot', 9)
    a_.set(xlabel="Reward $r=1-r'$", ylabel=yl, title=ttl)
kk = np.argmin(J[:, 4]); ax[0].plot(r[kk], J[kk, 4], '*', ms=11, mfc='gold', mec='k', label="solution of (P2)", zorder=5)
ax[0].set(xlim=(0, 1), ylim=(0, 2.2)); ax[0].legend(loc='upper left', fontsize=7)
ax[1].axhline(0, color='.5', lw=.6); ax[1].set(xlim=(0, 1), ylim=(-0.3, 1.1)); ax[1].legend(loc='lower left', bbox_to_anchor=(0.36, 0.0), fontsize=7)
done(fig, 'fig_decentralized')

# Fig. 7: learned profiles
d = L('exp7'); D = d['Ds'].ravel(); sv = d['sav']; S = sv.mean(0); opt = d['opt'].ravel()
fig, ax = two()
pm(ax[0], D, S[:, 0], 'lp', len(D), 'LP, learned'); pm(ax[0], D, S[:, 2], 'crowd', len(D), 'Crowd, learned'); pm(ax[0], D, S[:, 1], 'nod2d', len(D), 'No D2D, learned')
ax[0].axhline(opt.mean(), color='k', ls='--', lw=1, label='LP, true profiles')
ax[0].axhline(d['nod'].mean(), color=ST['nod2d'][0], ls='--', lw=1, label='No D2D, true profiles')
ax[0].set(xscale='log', xlabel='Observed periods $D$', ylabel=r'SP saving $\Delta C/C^{\mathcal{R}}$', title='(a) SP saving, $r=0.2$', ylim=(0.075, 0.195)); ax[0].legend(loc='lower right', ncol=2, fontsize=7)
for j, k, nm in [(0, 'lp', 'LP, learned'), (2, 'crowd', 'Crowd, learned'), (1, 'nod2d', 'No D2D, learned')]:
    loss = 100 * (opt[:, None] - sv[:, :, j]) / opt[:, None]; m = loss.mean(0); sd = loss.std(0) / np.sqrt(loss.shape[0])
    pm(ax[1], D, m, k, len(D), nm); ax[1].fill_between(D, m - sd, m + sd, color=ST[k][0], alpha=.12, lw=0)
ax[1].set(xscale='log', xlabel='Observed periods $D$', ylabel='Loss vs. full information (%)', title='(b) Cost of learning', ylim=(0, None)); ax[1].legend(loc='upper right')
done(fig, 'fig_robustness')
print('ok')
