function [x, it, conv] = br_dynamics(am, Gm, S, rp, x0, maxit)
%BR_DYNAMICS  Round-robin best-response dynamics for one item.
if nargin < 6, maxit = 500; end
x = x0(:); N = numel(x); conv = false;
for it = 1:maxit
    xold = x;
    for n = 1:N, x(n) = best_response(n, x, am, Gm, S, rp); end
    if max(abs(x - xold)) < 1e-10, conv = true; break; end
end
end
