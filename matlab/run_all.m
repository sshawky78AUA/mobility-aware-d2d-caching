% RUN_ALL  Run the MATLAB part of the paper's results, then the additional
% synthetic experiments.
%   Requires the Optimization Toolbox (linprog, intlinprog). Also runs in
%   GNU Octave (glpk is used instead). Data are saved to ../figs/expN.mat,
%   figures to ../figs as EPS/PDF/PNG.
%
%   To change a setting, edit the parameter lines at the top of the
%   experiment file (each file starts with them), or edit default_params.m
%   for the synthetic experiments, and rerun that file.
%
%   The trace-driven results of Section VI-B to VI-F (Figs. 4-8) are in
%   ../trace_sim (Python); see ../README.md.

%% Results in the paper
test_core;            % checks against the analytical examples of Sections IV-V
exp0_example;         % Fig. 3: worked example with three users (Section V-E)
exp3_gap;             % Table 3: coded versus whole-copy placement, greedy (Section VI-A)

%% Additional synthetic experiments (Markov mobility model, default_params.m)
%  Not reported in the paper; useful to explore the model with small N.
exp1_two_users;       % two-user equilibria versus r'
exp2_centralized;     % SP saving versus the reward, N = 8
exp4_mobility;        % effect of how dispersed the users are
exp5_scalability;     % sample-based LP for large N
exp6_decentralized;   % equilibrium selection rules versus the optimum (MILP), N = 6
exp7_robustness;      % profiles learned from D observed periods
