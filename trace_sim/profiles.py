"""Hour-of-day location profiles theta[n, t, l] (l = 0 private, 1..L popular cells) from check-ins,
with Bayesian smoothing toward the user's all-day distribution and the population distribution."""
import numpy as np, pandas as pd
def load(path, h0=8, T=12):
    df = pd.read_csv(path)
    ts = pd.to_datetime(df['utcTimestamp'], format='%a %b %d %H:%M:%S +0000 %Y') + pd.to_timedelta(df['timezoneOffset'], unit='m')
    df['date'] = ts.dt.normalize(); df['hour'] = ts.dt.hour; df['wd'] = ts.dt.weekday
    w = df[(df.wd < 5) & (df.hour >= h0) & (df.hour < h0 + T)].copy(); w['t'] = w.hour - h0
    return w
def cells(w, cell=500, L=40):
    lat0 = w.latitude.mean(); mx = 111320 * np.cos(np.radians(lat0)); my = 110540
    gx = np.floor((w.longitude - w.longitude.min()) * mx / cell).astype(int); gy = np.floor((w.latitude - w.latitude.min()) * my / cell).astype(int)
    c = gx * 100000 + gy; top = c.value_counts().index[:L]; cid = {v: i + 1 for i, v in enumerate(top)}
    return c.map(cid).fillna(0).astype(int).values
def theta(w, users, L, T=12, k_user=4.0, k_pop=4.0):
    uid = {u: i for i, u in enumerate(users)}; N = len(users)
    sub = w[w.userId.isin(uid)]; n = sub.userId.map(uid).values
    C = np.zeros((N, T, L + 1)); np.add.at(C, (n, sub.t.values, sub.l.values), 1)
    pop = C.sum((0, 1)) + 1; pop /= pop.sum()                       # population location distribution
    U = C.sum(1); U = (U + k_pop * pop) / (U.sum(1, keepdims=True) + k_pop)   # user all-day distribution
    th = (C + k_user * U[:, None, :]) / (C.sum(2, keepdims=True) + k_user)
    return th, C
