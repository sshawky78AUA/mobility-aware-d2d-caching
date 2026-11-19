function [a, Gm] = user_weights(theta, P, Gm)
%USER_WEIGHTS  Per-user, per-group, per-item weights (exact enumeration).
%   theta : T x N x (L+1) mobility profiles,  P : T x N x M demand profiles.
%   a(n,g,m) = (1/T) sum_t p_{n,t}^m q_{g,t}  if n in g, 0 otherwise.
[T, N, ~] = size(theta); M = size(P, 3);
if nargin < 3, Gm = enum_groups(N); end
G = size(Gm, 1);
a = zeros(N, G, M);
for t = 1:T
    q = group_probs(squeeze(theta(t, :, :)), Gm);       % G x 1
    for m = 1:M
        a(:, :, m) = a(:, :, m) + (squeeze(P(t, :, m))' * q') .* Gm' / T;
    end
end
end
