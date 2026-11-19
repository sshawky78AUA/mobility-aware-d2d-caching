function [x, chain, F] = greedy_integral(a, Gm, S, r)
%GREEDY_INTEGRAL  Greedy whole-copy placement (Algorithm 1).
%   For each item, users are added one at a time by largest marginal
%   coverage F(A) = sum_{g : g meets A} W_g; the chain is stopped where
%   S*F(A_k) - r*S*k is largest.
[N, G, M] = size(a); x = zeros(N, M); chain = zeros(N, M); F = zeros(N + 1, M);
Gd = double(Gm);
for m = 1:M
    W = sum(a(:, :, m), 1)'; covered = false(G, 1); A = [];
    for k = 1:N
        gain = (W .* ~covered)' * Gd;          % marginal coverage of every user
        gain(A) = -inf; [~, bi] = max(gain);
        A = [A, bi]; covered = covered | Gm(:, bi); F(k + 1, m) = W' * covered;
    end
    chain(:, m) = A';
    [~, kbest] = max(S(m) * F(:, m) - r * S(m) * (0:N)');
    x(A(1:kbest - 1), m) = S(m);
end
end
