% TEST_CORE  Sanity checks of the MATLAB implementation against known cases.
% (1) symmetric three-user example: half copies are optimal
th = zeros(1, 3, 3); th(1, :, 2:3) = 0.5;             % no private state, L = 2
P = 0.4 * ones(1, 3, 1);
[a, Gm] = user_weights(th, P);
[x, C] = central_lp(a, Gm, 1, 0.2);
fprintf('sym example: x = [%s], C = %.4f (expect 0.5s, 0.45)\n', num2str(x', 3), C);
xb = best_integral(a, Gm, 1, 0.2); fprintf('best integral C = %.4f (expect 0.50)\n', sp_cost(xb, a, Gm, 1, 0.2));
% (2) N = 2 example of [old Fig. 12]: p = (0.8, 0.6), meeting prob 0.5
th = zeros(1, 2, 3); th(1, :, 2:3) = 0.5; P = reshape([0.8 0.6], [1 2 1]);
[a, Gm] = user_weights(th, P); am = a(:, :, 1);
for rp = [0.35 0.5 0.7]
    xbst = ne_milp(am, Gm, 1, rp, 1 - rp, 'best'); xw = ne_milp(am, Gm, 1, rp, 1 - rp, 'worst');
    xf = ne_milp(am, Gm, 1, rp, 1 - rp, 'fair'); xp = potential_ne(am, Gm, 1, rp);
    xbr = br_dynamics(am, Gm, 1, rp, [0.5; 0.5]);
    fprintf('rp=%.2f best=[%s] worst=[%s] fair=[%s] pot=[%s] br=[%s] NEchk=%d%d%d%d\n', rp, ...
        num2str(xbst', 3), num2str(xw', 3), num2str(xf', 3), num2str(xp', 3), num2str(xbr', 3), ...
        ne_check(xbst, am, Gm, 1, rp), ne_check(xf, am, Gm, 1, rp), ne_check(xp, am, Gm, 1, rp), ne_check(xbr, am, Gm, 1, rp));
end
% (3) old proportional rule fails, fair NE in the symmetric example
th = zeros(1, 3, 3); th(1, :, 2:3) = 0.5; P = 0.3 * ones(1, 3, 1);
[a, Gm] = user_weights(th, P); am = a(:, :, 1);
fprintf('proportional (1/3,1/3,1/3) is NE? %d\n', ne_check([1;1;1] / 3, am, Gm, 1, 0.2));
xf = ne_milp(am, Gm, 1, 0.2, 0.8, 'fair'); fprintf('fair NE = [%s]\n', num2str(xf', 3));
% (4) random scenario: every selection is an equilibrium
par = default_params(); par.N = 6; par.M = 3; sc = gen_scenario(par, 1);
[a, Gm] = user_weights(sc.theta, sc.P);
bad = 0;
for m = 1:3
    for rp = 0.05:0.1:0.65
        am = a(:, :, m);
        for mode = {'best', 'worst', 'fair'}
            xx = ne_milp(am, Gm, 1, rp, 1 - rp, mode{1}); bad = bad + ~ne_check(xx, am, Gm, 1, rp, 1e-4);
        end
        bad = bad + ~ne_check(potential_ne(am, Gm, 1, rp), am, Gm, 1, rp, 1e-6);
        bad = bad + ~ne_check(br_dynamics(am, Gm, 1, rp, zeros(6, 1)), am, Gm, 1, rp, 1e-6);
    end
end
fprintf('random N=6: selections failing NE check = %d\n', bad);
