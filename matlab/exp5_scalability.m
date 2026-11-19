% EXP5_SCALABILITY  Large N with the sample-based (SAA) LP (Fig. 5). The
% community structure is fixed (4 communities, 8 popular locations) so that
% only the number of users changes. Policies are evaluated out of sample.
par = default_params(); par.C = 4; par.L = 8;
Ns = [10 15 20 30 40 50]; seeds = 1:8; r = 0.2; K = 40; Kev = 200;
sav = zeros(numel(seeds), numel(Ns), 4); tim = zeros(numel(seeds), numel(Ns), 2);
for s = seeds
    for i = 1:numel(Ns)
        par.N = Ns(i); sc = gen_scenario(par, s);
        [ae, Ge] = saa_weights(sc.theta, sc.P, Kev, 1000 + s);         % evaluation samples
        pbar = squeeze(mean(sc.P, 1)); CR = sum(pbar(:));
        tic; [aS, GS] = saa_weights(sc.theta, sc.P, K, s); x1 = central_lp(aS, GS, sc.S, r); tim(s, i, 1) = toc;
        tic; x2 = greedy_integral(aS, GS, sc.S, r); tim(s, i, 2) = toc;
        x3 = double(pbar > r);
        thc = repmat(mean(sc.theta, 2), [1 par.N 1]); [ac, Gc] = saa_weights(thc, sc.P, K, s); x4 = central_lp(ac, Gc, sc.S, r);
        X = {x1, x2, x3, x4};
        for j = 1:4, sav(s, i, j) = 1 - sum(sp_cost(X{j}, ae, Ge, sc.S, r)) / CR; end
    end
end
save(fullfile('..', 'figs', 'exp5.mat'), '-v7');
mS = squeeze(mean(sav, 1)); mT = squeeze(mean(tim, 1)); keys = {'lp', 'greedy', 'nod2d', 'crowd'};
h = figure('Position', [100 100 760 300]);
ax = subplot(1, 2, 1); hold on;
for j = 1:4, plot_method(ax, Ns, mS(:, j), keys{j}, numel(Ns)); end
xlabel('Number of users N'); ylabel('SP saving \DeltaC / C^R'); add_legend(ax, 'southeast');
title('(a) SP saving, r = 0.2'); style_axes(ax);
ax = subplot(1, 2, 2); hold on;
plot_method(ax, Ns, mT(:, 1), 'lp', numel(Ns)); plot_method(ax, Ns, mT(:, 2), 'greedy', numel(Ns));
set(ax, 'YScale', 'log'); xlabel('Number of users N'); ylabel('Run time (s)');
add_legend(ax, 'northwest'); title('(b) Computation time, M = 10'); style_axes(ax);
save_fig(h, 'fig_scalability');
fprintf('exp5 savings / time:\n'); disp([Ns' mS mT]);
