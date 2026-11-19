function [theta_h, P_h] = estimate_profiles(sc, D, seed)
%ESTIMATE_PROFILES  Profiles learned from D observed periods (Section V-E).
%   Location frequencies with add-1/2 smoothing; demand from request counts
%   using the separable form p = pbar_n^m * psi_t (psi estimated from the
%   aggregate request volume of each slot).
rng(seed);
[T, N, L1] = size(sc.theta); M = size(sc.P, 3);
cnt = zeros(T, N, L1); req = zeros(T, N, M);
for d = 1:D
    for t = 1:T
        cdf = cumsum(squeeze(sc.theta(t, :, :)), 2);
        loc = sum(repmat(rand(N, 1), 1, L1) > cdf, 2) + 1;
        for n = 1:N, cnt(t, n, loc(n)) = cnt(t, n, loc(n)) + 1; end
        req(t, :, :) = req(t, :, :) + (rand(1, N, M) < sc.P(t, :, :));
    end
end
theta_h = (cnt + 0.5) / (D + 0.5 * L1);
tot = squeeze(sum(sum(req, 2), 3)) + 1e-9; psi_h = tot / mean(tot);       % T x 1
pbar = squeeze(sum(req, 1)) / (D * T);                                     % N x M
P_h = zeros(T, N, M);
for t = 1:T, P_h(t, :, :) = reshape(min(1, pbar * psi_h(t)), [1, N, M]); end
end
