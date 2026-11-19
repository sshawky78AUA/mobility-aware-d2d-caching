"""R2: centralized placement versus the reward on the NYC trace. Saves results/central_NYC.npz"""
import numpy as np, time, sys
sys.path.insert(0, '.')
from setup import city_data, demand
from core import *
city = sys.argv[1] if len(sys.argv) > 1 else 'NYC'; N0 = 400; M = 1000; seeds = range(4); T = 12
rhos = np.array([0.02, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0])
meth = ['LP', 'greedy', 'pairwise', 'crowd', 'popularity', 'local', 'nosharing']
D = city_data(city); out = {k: np.zeros((len(seeds), len(rhos))) for k in meth}; d2d = {k: np.zeros_like(out['LP']) for k in meth}
copies = {k: np.zeros_like(out['LP']) for k in meth}; tlp = np.zeros_like(out['LP'])
for si, sd in enumerate(seeds):
    rng = np.random.default_rng(100 + sd)
    idx = rng.choice(len(D['users']), N0, replace=False); th = D['th'][idx]; eta = D['eta']; N = N0
    P = demand(N, M, rng)
    A, f = groups_from(sample_snapshots(th, 5, rng), eta); Ae, fe = groups_from(sample_snapshots(th, 20, rng), eta)
    W = weights(A, f, P)
    thc = np.repeat(th.mean(0, keepdims=True), N, 0); Ac, fc = groups_from(sample_snapshots(thc, 5, rng), eta); Wc = weights(Ac, fc, P)
    alpha = pairwise_alpha(th, eta)
    for ri, rho in enumerate(rhos):
        r = rho / T; t0 = time.time()
        X = {'LP': central(A, W, r)}; tlp[si, ri] = time.time() - t0
        Xg = np.zeros((N, M))
        for m in range(M):
            if (A.T @ W[:, m]).max() > r: Xg[:, m] = greedy_item(A, W[:, m], r)
        X['greedy'] = Xg
        X['pairwise'] = np.column_stack([pairwise_item(alpha, P[:, m], r) for m in range(M)])
        X['crowd'] = central(Ac, Wc, r)
        X['popularity'] = np.tile((P.mean(0) > r).astype(float), (N, 1))
        X['local'] = (P > r).astype(float); X['nosharing'] = X['local']
        for k in meth:
            e = no_sharing(X[k], Ae, fe, P, r) if k == 'nosharing' else evaluate(X[k], Ae, fe, P, r)
            out[k][si, ri] = 1 - e['cost'] / e['total']; d2d[k][si, ri] = e['d2d'] / e['total']; copies[k][si, ri] = X[k].sum() / M
        print(city, sd, rho, {k: round(out[k][si, ri], 4) for k in meth}, 'tLP %.1f' % tlp[si, ri], flush=True)
    np.savez(f'results/central_{city}.npz', rhos=rhos, meth=meth, tlp=tlp, **{f'sav_{k}': out[k] for k in meth},
             **{f'd2d_{k}': d2d[k] for k in meth}, **{f'cop_{k}': copies[k] for k in meth}, done=si + 1)
