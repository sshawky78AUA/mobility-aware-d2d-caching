"""Trace statistics: hourly activity and number of co-located users at request time."""
import numpy as np, sys
sys.path.insert(0, '.')
from setup import city_data
from core import sample_snapshots
out = {}
for city in ('NYC', 'TKY'):
    D = city_data(city); out[f'{city}_eta'] = D['eta']; out[f'{city}_N'] = len(D['users']); out[f'{city}_pres'] = 1 - D['th'][:, :, 0].mean()
    for N in (200, 400, 1000):
        rng = np.random.default_rng(7); idx = rng.choice(len(D['users']), min(N, len(D['users'])), replace=False)
        loc = sample_snapshots(D['th'][idx], 20, rng); K, T, n = loc.shape; h = np.zeros(12)
        for k in range(K):
            for t in range(T):
                v = loc[k, t]; occ = np.bincount(v, minlength=D['th'].shape[2]); oth = np.where(v > 0, occ[v] - 1, 0)
                h += D['eta'][t] * np.bincount(np.minimum(oth, 11), minlength=12)
        out[f'{city}_others_{N}'] = h / h.sum()
        print(city, N, 'P(no other) %.2f' % out[f'{city}_others_{N}'][0], 'mean others %.2f' % (np.arange(12) @ out[f'{city}_others_{N}']))
np.savez('results/trace.npz', **out)
