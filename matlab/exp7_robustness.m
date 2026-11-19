% EXP7_ROBUSTNESS  Profiles learned from D observed periods (Fig. 7). The SP
% solves the LP with estimated profiles; placements are evaluated with the
% true profiles.
par = default_params(); Ds = [1 2 3 5 10 20 50 100]; seeds = 1:10; reps = 5; r = 0.2;
sav = zeros(numel(seeds), numel(Ds), 3); opt = zeros(numel(seeds), 1); nod = opt;
for s = seeds
    sc = gen_scenario(par, s); [a, Gm] = user_weights(sc.theta, sc.P);
    pbar = squeeze(sum(a, 2)); CR = sum(pbar(:));
    opt(s) = 1 - sum(sp_cost(central_lp(a, Gm, sc.S, r), a, Gm, sc.S, r)) / CR;
    nod(s) = 1 - sum(sp_cost(double(pbar > r), a, Gm, sc.S, r)) / CR;
    for i = 1:numel(Ds)
        acc = zeros(1, 3);
        for q = 1:reps
            [thh, Ph] = estimate_profiles(sc, Ds(i), 100 * s + q);
            ah = user_weights(thh, Ph, Gm); pbh = squeeze(sum(ah, 2));
            thc = repmat(mean(thh, 2), [1 par.N 1]);
            X = {central_lp(ah, Gm, sc.S, r), double(pbh > r), central_lp(user_weights(thc, Ph, Gm), Gm, sc.S, r)};
            for j = 1:3, acc(j) = acc(j) + (1 - sum(sp_cost(X{j}, a, Gm, sc.S, r)) / CR) / reps; end
        end
        sav(s, i, :) = acc;
    end
end
save(fullfile('..', 'figs', 'exp7.mat'), '-v7');
mS = squeeze(mean(sav, 1)); keys = {'lp', 'nod2d', 'crowd'};
h = figure('Position', [100 100 760 300]);
ax = subplot(1, 2, 1); hold on;
for j = [1 3 2], plot_method(ax, Ds, mS(:, j), keys{j}, numel(Ds)); end
plot(ax, Ds, mean(opt) * ones(size(Ds)), 'k--', 'DisplayName', 'LP, true profiles');
plot(ax, Ds, mean(nod) * ones(size(Ds)), '--', 'Color', [0.85 0.33 0.10], 'DisplayName', 'No D2D, true profiles');
set(ax, 'XScale', 'log'); xlabel('Observed periods D'); ylabel('SP saving \DeltaC / C^R');
title('(a) SP saving, r = 0.2'); add_legend(ax, 'southeast'); style_axes(ax);
ax = subplot(1, 2, 2); hold on;
loss = 100 * (repmat(opt, [1 numel(Ds) 3]) - sav) ./ repmat(opt, [1 numel(Ds) 3]);   % % of full-information saving lost
for j = [1 3 2], plot_method(ax, Ds, mean(loss(:, :, j), 1), keys{j}, numel(Ds)); end
set(ax, 'XScale', 'log'); xlabel('Observed periods D'); ylabel('Loss vs. full information (%)');
title('(b) Cost of learning'); add_legend(ax, 'northeast'); style_axes(ax);
save_fig(h, 'fig_robustness');
fprintf('exp7: opt %.4f nod %.4f\n', mean(opt), mean(nod)); disp([Ds' mS]);
