function [C, Lo, X] = sp_cost(x, a, Gm, S, r)
%SP_COST  SP cost per item: expected peak load + r * cached amount.
%   x : N x M caching decisions, a : N x G x M weights, S : 1 x M sizes.
M = size(x, 2); Lo = zeros(1, M); X = sum(x, 1);
for m = 1:M
    W = sum(a(:, :, m), 1)';                 % G x 1 group weights
    deficit = max(0, S(m) - double(Gm) * x(:, m));
    Lo(m) = W' * deficit;
end
C = Lo + r * X;
end
