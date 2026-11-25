"""Fig. 5: centralized placement versus the reward, compared with the baselines.
Saves <out>/central_<city>.npz.  Run with --help for all parameters.

The reward is given as rho = r*T, the reward per item-day relative to one off-peak unit (Section VI-B)."""
import numpy as np, time, os
from params import get_params
from setup import city_data, demand
from core import *
p = get_params(dict(N=400, seeds=4, seed0=100,
                    rhos=[0.02, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0],
                    methods=['LP', 'greedy', 'pairwise', 'crowd', 'popularity', 'local', 'nosharing']),
               'Centralized placement versus reward (Fig. 5)')
city = p.city; N0 = p.N; M = p.M; seeds = range(p.seeds); T = p.T
rhos = np.array(p.rhos, float); meth = list(p.methods)
D = city_data(city, p); out = {k: np.zeros((len(seeds), len(rhos))) for k in meth}; d2d = {k: np.zeros_like(out[meth[0]]) for k in meth}
copies = {k: np.zeros_like(out[meth[0]]) for k in meth}; tlp = np.zeros_like(out[meth[0]])
for si, sd in enumerate(seeds):
    rng = np.random.default_rng(p.seed0 + sd)
    idx = rng.choice(len(D['users']), N0, replace=False); th = D['th'][idx]; eta = D['eta']; N = N0
    P = demand(N, M, rng, p=p)
    A, f = groups_from(sample_snapshots(th, p.K_plan, rng), eta); Ae, fe = groups_from(sample_snapshots(th, p.K_eval, rng), eta)
    W = weights(A, f, P)
    thc = np.repeat(th.mean(0, keepdims=True), N, 0); Ac, fc = groups_from(sample_snapshots(thc, p.K_plan, rng), eta); Wc = weights(Ac, fc, P)
    alpha = pairwise_alpha(th, eta)
    for ri, rho in enumerate(rhos):
        r = rho / T; X = {}
        if 'LP' in meth:
            t0 = time.time(); X['LP'] = central(A, W, r); tlp[si, ri] = time.time() - t0
        if 'greedy' in meth:
            Xg = np.zeros((N, M))
            for m in range(M):
                if (A.T @ W[:, m]).max() > r: Xg[:, m] = greedy_item(A, W[:, m], r)
            X['greedy'] = Xg
        if 'pairwise' in meth:
            X['pairwise'] = np.column_stack([pairwise_item(alpha, P[:, m], r) for m in range(M)])
        if 'crowd' in meth:
            X['crowd'] = central(Ac, Wc, r)
        if 'popularity' in meth:
            X['popularity'] = np.tile((P.mean(0) > r).astype(float), (N, 1))
        if 'local' in meth or 'nosharing' in meth:
            X['local'] = (P > r).astype(float); X['nosharing'] = X['local']
        for k in meth:
            e = no_sharing(X[k], Ae, fe, P, r) if k == 'nosharing' else evaluate(X[k], Ae, fe, P, r)
            out[k][si, ri] = 1 - e['cost'] / e['total']; d2d[k][si, ri] = e['d2d'] / e['total']; copies[k][si, ri] = X[k].sum() / M
        print(city, sd, rho, {k: round(float(out[k][si, ri]), 4) for k in meth}, 'tLP %.1f' % tlp[si, ri], flush=True)
    np.savez(os.path.join(p.out, f'central_{city}.npz'), rhos=rhos, meth=meth, tlp=tlp, **{f'sav_{k}': out[k] for k in meth},
             **{f'd2d_{k}': d2d[k] for k in meth}, **{f'cop_{k}': copies[k] for k in meth}, done=si + 1)
