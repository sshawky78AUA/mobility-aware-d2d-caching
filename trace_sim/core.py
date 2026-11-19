"""Trace-driven evaluation of mobility-aware D2D caching (Section VI).
All LPs are solved with HiGHS (the solver behind MATLAB linprog)."""
import numpy as np, scipy.sparse as sp, time
from scipy.optimize import linprog

# ---------------------------------------------------------------- snapshots and groups
def sample_snapshots(th, K, rng):
    """th: N x T x (L+1). Returns loc[K, T, N] drawn independently per user (Assumption 2)."""
    N, T, L1 = th.shape
    cum = np.cumsum(th, axis=2); u = rng.random((K, T, N))
    loc = (u[..., None] > cum.transpose(1, 0, 2)[None]).sum(-1)
    return np.minimum(loc, L1 - 1)

def groups_from(loc, eta):
    """Unique co-location groups and their time-weighted frequencies.
    Returns A (G x N incidence, csr) and f (G,) with f_g = (1/(K T)) sum_{(k,t): g occurs} eta_t."""
    K, T, N = loc.shape; key = {}; rows = []; f = []
    for k in range(K):
        for t in range(T):
            v = loc[k, t]
            for l in np.unique(v):
                mem = np.flatnonzero(v == l)
                if l == 0 or len(mem) == 1:
                    for n in mem:                               # singleton (private or alone)
                        g = key.setdefault((int(n),), len(key))
                        if g == len(f): f.append(0.0); rows.append((int(n),))
                        f[g] += eta[t]
                else:
                    tup = tuple(mem.tolist()); g = key.setdefault(tup, len(key))
                    if g == len(f): f.append(0.0); rows.append(tup)
                    f[g] += eta[t]
    G = len(rows); r_i = np.repeat(np.arange(G), [len(r) for r in rows]); c_i = np.concatenate([np.array(r) for r in rows])
    A = sp.csr_matrix((np.ones(len(c_i)), (r_i, c_i)), shape=(G, N))
    return A, np.array(f) / (K * T)

def weights(A, f, P):
    """Group weights W[g, m] = f_g * sum_{n in g} phat-scale P[n, m] (P[n,m] = a_n pi_n^m, i.e. p_{n,t}^m / eta_t)."""
    return (A @ P) * f[:, None]

# ---------------------------------------------------------------- centralized placement
def lp_item(A, Wm, r, S=1.0):
    """min r sum x + sum_g W_g (S - x(g))^+  (Theorem 1), after the per-user reduction:
    a user with tau_n >= r caches the whole item and a user with s_n <= r caches nothing in some
    optimal solution (Corollary of Theorem 2), so the LP is solved only over the remaining users."""
    G, N = A.shape; keep = Wm > 1e-15; Ak = A[keep].tocsr(); Wk = Wm[keep]
    s = Ak.T @ Wk                                               # level-1 scores s_n
    x = np.zeros(N)
    if r >= s.max(): return x                                   # Theorem 2(2)
    size = np.diff(Ak.indptr); single = size == 1
    tau = np.zeros(N); np.add.at(tau, Ak.indices[Ak.indptr[:-1][single]], Wk[single])
    full = tau >= r; zero = (s <= r) & ~full; free = ~(full | zero)
    x[full] = S
    if not free.any(): return x
    # groups already holding a full copy are satisfied; fixed users drop out of the others
    sat = (Ak @ full.astype(float)) > 0
    Ar = Ak[~sat][:, free]; Wr = Wk[~sat]
    nz = np.diff(Ar.indptr) > 0; Ar = Ar[nz]; Wr = Wr[nz]; Gr, Nf = Ar.shape
    c = np.r_[np.full(Nf, r), Wr]
    Aub = sp.hstack([-Ar, -sp.identity(Gr)], format='csr')
    res = linprog(c, A_ub=Aub, b_ub=-S * np.ones(Gr), bounds=[(0, S)] * Nf + [(0, None)] * Gr, method='highs')
    x[free] = np.clip(res.x[:Nf], 0, S)
    return x

def central(A, W, r, S=1.0, items=None):
    N = A.shape[1]; M = W.shape[1]; X = np.zeros((N, M))
    for m in (range(M) if items is None else items): X[:, m] = lp_item(A, W[:, m], r, S)
    return X

def greedy_item(A, Wm, r, S=1.0):
    """Algorithm 1: greedy whole copies on the coverage function."""
    G, N = A.shape; Ac = A.tocsc(); covered = np.zeros(G, bool); chosen = []; best = (0.0, 0); gain_tot = 0.0
    s = Ac.T @ Wm
    if r >= s.max(): return np.zeros(N)
    for k in range(1, N + 1):
        marg = Ac.T @ (Wm * ~covered); marg[chosen] = -1
        n = int(np.argmax(marg))
        if marg[n] <= 0: break
        chosen.append(n); covered[Ac[:, n].indices] = True; gain_tot += marg[n]
        if gain_tot - r * k > best[0]: best = (gain_tot - r * k, k)
        if marg[n] < r and k > best[1] + 5: break               # marginal gains only decrease (submodularity)
    x = np.zeros(N); x[chosen[:best[1]]] = S
    return x

# ---------------------------------------------------------------- evaluation
def evaluate(X, A, f, P, r, S=1.0):
    """Expected SP cost terms on an evaluation sample. Returns dict of per-period averages."""
    W = weights(A, f, P)                                         # G x M
    load = A @ X                                                 # G x M, x^m(g)
    deficit = np.maximum(S - load, 0)
    bs = (W * deficit).sum()
    # bytes from own cache vs D2D, for each requester in each group
    own = 0.0; tot = (W.sum()) * S
    # own cache share: sum_g f_g sum_{n in g} P[n,m] min(x_n, S)
    Ac = A.tocoo()
    own = (f[Ac.row][:, None] * P[Ac.col] * np.minimum(X[Ac.col], S)).sum()
    return dict(bs=bs, own=own, d2d=tot - bs - own, total=tot, reward=r * X.sum(), cost=bs + r * X.sum())

def no_sharing(X, A, f, P, r, S=1.0):
    """Cost when devices serve only their own requests (no D2D)."""
    e = evaluate(X, A, f, P, r, S); bs = e['total'] - e['own']
    return dict(e, bs=bs, d2d=0.0, cost=bs + e['reward'])

def pairwise_alpha(th, eta):
    """alpha[n, j] = P(j at n's popular location when n requests), eta-weighted over slots (pairwise model)."""
    N, T, L1 = th.shape; a = np.zeros((N, N))
    for t in range(T):
        Q = th[:, t, 1:]; a += eta[t] * (Q @ Q.T)
    a /= eta.sum(); np.fill_diagonal(a, 0); return a

def pairwise_item(alpha, Pm, r, S=1.0):
    """Pairwise-contact placement: deficit of n approximated by (S - x_n - sum_j alpha_nj x_j)^+."""
    N = len(Pm); reach = Pm + alpha.T @ Pm
    if r >= reach.max(): return np.zeros(N)
    Ad = np.eye(N) + alpha
    c = np.r_[np.full(N, r), Pm]
    Aub = sp.hstack([-sp.csr_matrix(Ad), -sp.identity(N)], format='csr')
    res = linprog(c, A_ub=Aub, b_ub=-S * np.ones(N), bounds=[(0, S)] * N + [(0, None)] * N, method='highs')
    return np.clip(res.x[:N], 0, S)

# ---------------------------------------------------------------- decentralized: potential equilibrium (Theorem 5)
def pot_item(A, f, Pm, rp, S=1.0):
    """Potential-minimizing NE for one item: min sum_g f_g (S - x(g))^+ + rp * sum_n x_n / phat_n,
    with phat_n = Pm[n] (separable weights, c_g = f_g). Users with rp < ptilde_n hold S, users with rp > phat_n hold 0."""
    G, N = A.shape; x = np.zeros(N); act = Pm > 1e-15
    if not act.any(): return x
    Ak = A.tocsr(); size = np.diff(Ak.indptr); single = size == 1
    ptil = np.zeros(N); np.add.at(ptil, Ak.indices[Ak.indptr[:-1][single]], f[single]); ptil *= Pm
    full = act & (rp < ptil); zero = ~act | (rp > Pm); free = ~(full | zero); x[full] = S
    if not free.any(): return x
    sat = (Ak @ full.astype(float)) > 0
    Ar = Ak[~sat][:, free]; fr = f[~sat]; nz = np.diff(Ar.indptr) > 0; Ar = Ar[nz]; fr = fr[nz]; Gr, Nf = Ar.shape
    c = np.r_[rp / Pm[free], fr]
    Aub = sp.hstack([-Ar, -sp.identity(Gr)], format='csr')
    res = linprog(c, A_ub=Aub, b_ub=-S * np.ones(Gr), bounds=[(0, S)] * Nf + [(0, None)] * Gr, method='highs')
    x[free] = np.clip(res.x[:Nf], 0, S); return x
