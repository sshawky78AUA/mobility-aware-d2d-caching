function x = best_integral(a, Gm, S, r)
%BEST_INTEGRAL  Exhaustive search over whole-copy placements (small N).
[N, G, M] = size(a); x = zeros(N, M); Gd = double(Gm);
subs = double(enum_groups(N));                      % 2^N-1 non-empty sets
for m = 1:M
    W = sum(a(:, :, m), 1)';
    cover = (Gd * subs') > 0;                       % G x (2^N-1)
    val = S(m) * (W' * cover) - r * S(m) * sum(subs, 2)';
    [bv, j] = max(val);
    if bv > 0, x(:, m) = S(m) * subs(j, :)'; end
end
end
