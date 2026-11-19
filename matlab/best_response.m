function v = best_response(n, x, am, Gm, S, rp)
%BEST_RESPONSE  Exact best response of user n for one item.
%   mu_n is convex piecewise linear in x_n with breakpoints at
%   S - x(B \ n); the minimum is attained at a breakpoint or an end point.
in = Gm(:, n) & am(n, :)' > 0;
y = S - (double(Gm(in, :)) * x - x(n));           % S - x(B \ n)
cand = unique([0; S; y(y > 0 & y < S)]);
w = am(n, in)';
cost = zeros(numel(cand), 1);
for c = 1:numel(cand)
    cost(c) = w' * max(0, y - cand(c)) + rp * cand(c);
end
best = min(cost);
ties = find(cost <= best + 1e-12);
[~, j] = min(abs(cand(ties) - x(n)));             % keep the current value on ties
v = cand(ties(j));
end
