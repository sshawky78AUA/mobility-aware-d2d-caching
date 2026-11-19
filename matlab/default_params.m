function par = default_params()
par.N = 8; par.M = 10; par.L = 6; par.C = 2;
par.T = 12;                                   % two-hour slots
par.phase = [1 1 2 2 2 2 3 2 3 3 1 1];        % home / work / leisure
par.psi = [0.3 0.6 0.8 0.8 1.0 1.0 1.2 1.0 1.3 1.6 1.4 0.8];
par.rho = 0.9; par.disp = 0.1;
par.zipf = 0.8; par.het = 0.5; par.lam = 1;
end
