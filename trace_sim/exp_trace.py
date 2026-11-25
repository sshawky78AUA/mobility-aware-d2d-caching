"""Fig. 4: trace statistics. Hourly activity profile and the number of other users co-located with a
requesting user. Saves <out>/trace.npz.  Run with --help for all parameters."""
import numpy as np, os
from params import get_params
from setup import city_data
from core import sample_snapshots
p = get_params(dict(cities=['NYC', 'TKY'], Ns=[200, 400, 1000], seed=7, max_others=11),
               'Trace statistics (Fig. 4)')
out = {}
B = p.max_others + 1
for city in p.cities:
    D = city_data(city, p); out[f'{city}_eta'] = D['eta']; out[f'{city}_N'] = len(D['users']); out[f'{city}_pres'] = 1 - D['th'][:, :, 0].mean()
    for N in p.Ns:
        rng = np.random.default_rng(p.seed); idx = rng.choice(len(D['users']), min(N, len(D['users'])), replace=False)
        loc = sample_snapshots(D['th'][idx], p.K_eval, rng); K, T, n = loc.shape; h = np.zeros(B)
        for k in range(K):
            for t in range(T):
                v = loc[k, t]; occ = np.bincount(v, minlength=D['th'].shape[2]); oth = np.where(v > 0, occ[v] - 1, 0)
                h += D['eta'][t] * np.bincount(np.minimum(oth, p.max_others), minlength=B)
        out[f'{city}_others_{N}'] = h / h.sum()
        print(city, N, 'P(no other) %.2f' % out[f'{city}_others_{N}'][0], 'mean others %.2f' % (np.arange(B) @ out[f'{city}_others_{N}']))
np.savez(os.path.join(p.out, 'trace.npz'), h0=p.h0, **out)
