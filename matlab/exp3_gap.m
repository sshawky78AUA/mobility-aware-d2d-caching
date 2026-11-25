% EXP3_GAP  Coded versus whole-copy placement on random instances (Table 3).
% ---- Parameters (edit here) ----  (r is drawn in [0, rmax], L in [Lmin, Lmax])
Ns = 3:8; trials = 500; rmax = 0.8; Lmin = 2; Lmax = 5;
% ----------------------------------
frac = zeros(size(Ns)); avgGap = frac; maxGap = frac; gre = frac;
rng(5);
for i = 1:numel(Ns)
    N = Ns(i); gaps = zeros(trials, 1); gg = gaps;
    for k = 1:trials
        L = randi([Lmin Lmax]); th = zeros(1, N, L + 1);
        for n = 1:N, v = -log(rand(1, L + 1)); v(1) = v(1) * rand; th(1, n, :) = v / sum(v); end
        P = reshape(rand(1, N), [1 N 1]); r = rand * rmax;
        [a, Gm] = user_weights(th, P);
        [~, C1] = central_lp(a, Gm, 1, r);
        C2 = sp_cost(best_integral(a, Gm, 1, r), a, Gm, 1, r);
        C3 = sp_cost(greedy_integral(a, Gm, 1, r), a, Gm, 1, r);
        gaps(k) = (C2 - C1) / C2; gg(k) = (C3 - C2) / C2;
    end
    frac(i) = mean(gaps > 1e-6); avgGap(i) = mean(gaps(gaps > 1e-6)); maxGap(i) = max(gaps); gre(i) = max(gg);
end
save(fullfile('..', 'figs', 'exp3.mat'), '-v7');
fprintf('N   frac>0   meanGap   maxGap   greedyMaxGap\n');
for i = 1:numel(Ns), fprintf('%d   %.3f    %.4f    %.4f   %.4f\n', Ns(i), frac(i), avgGap(i), maxGap(i), gre(i)); end
