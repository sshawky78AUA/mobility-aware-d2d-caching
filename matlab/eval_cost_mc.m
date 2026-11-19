function [C, Lo] = eval_cost_mc(x, theta, P, S, r, K, seed)
%EVAL_COST_MC  Out-of-sample SP cost by Monte Carlo over locations (large N).
[a, Gm] = saa_weights(theta, P, K, seed);
[C, Lo] = sp_cost(x, a, Gm, S, r);
end
