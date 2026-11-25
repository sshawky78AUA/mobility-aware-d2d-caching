function par = default_params()
% DEFAULT_PARAMS  Settings of the synthetic scenario used by exp1-exp7
% (gen_scenario.m). Edit the values here to change every synthetic experiment.
%   N     number of users            M     number of items
%   L     number of popular locations C    number of communities
%   T     slots per period           phase daily phase of each slot (1 home, 2 work, 3 leisure)
%   psi   demand level of each slot  rho  mobility rate: weight of the move toward the slot's target distribution (Eq. 3)
%   disp  dispersion of users away from their community (0 = together, 1 = independent)
%   zipf  Zipf exponent of item popularity
%   het   lognormal spread of user request rates
%   lam   mean requests per user per slot
par.N = 8; par.M = 10; par.L = 6; par.C = 2;
par.T = 12;                                   % two-hour slots
par.phase = [1 1 2 2 2 2 3 2 3 3 1 1];        % home / work / leisure
par.psi = [0.3 0.6 0.8 0.8 1.0 1.0 1.2 1.0 1.3 1.6 1.4 0.8];
par.rho = 0.9; par.disp = 0.1;
par.zipf = 0.8; par.het = 0.5; par.lam = 1;
end
