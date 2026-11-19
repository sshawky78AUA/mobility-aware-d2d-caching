function [a, Gm] = saa_weights(theta, P, K, seed)
%SAA_WEIGHTS  Sample-based weights, Eq. (25).
%   Draws K joint location snapshots per slot (users independent,
%   Assumption 2) and records the group of every user. Returns
%   a(n,g,m) = (1/(K T)) sum_{k,t} p_{n,t}^m 1{G_{n,t}^k = g} and the
%   G x N logical matrix Gm of the groups that occurred.
%   To use observed co-location traces instead, replace the sampling of
%   'loc' by the recorded locations.
rng(seed);
[T, N, L1] = size(theta); M = size(P, 3);
maxRows = K * T * N; rows = false(maxRows, N); slot = zeros(maxRows, 1); nr = 0;
for t = 1:T
    cdf = cumsum(squeeze(theta(t, :, :)), 2);
    for k = 1:K
        loc = sum(repmat(rand(N, 1), 1, L1) > cdf, 2);      % 0 = private state
        for n = find(loc == 0)'                              % singletons
            nr = nr + 1; rows(nr, n) = true; slot(nr) = t;
        end
        for l = unique(loc(loc > 0))'
            nr = nr + 1; rows(nr, loc == l) = true; slot(nr) = t;
        end
    end
end
rows = rows(1:nr, :); slot = slot(1:nr);
[Gm, ~, idx] = unique(rows, 'rows');
G = size(Gm, 1);
cnt = accumarray([idx(:), slot(:)], 1, [G, T]) / (K * T);   % G x T
a = zeros(N, G, M);
for m = 1:M
    a(:, :, m) = ((cnt * P(:, :, m)) .* Gm)';                % N x G
end
end
