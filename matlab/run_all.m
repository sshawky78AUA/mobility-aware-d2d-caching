% RUN_ALL  Reproduce every numerical result of the paper.
%   Requires the Optimization Toolbox (linprog, intlinprog). Figures are
%   written to ../figs as EPS, PDF and PNG; the data as expN.mat.
%   Approximate run times on a laptop: exp6 (MILPs) is the longest.
test_core;            % sanity checks against the analytical examples
exp0_example;      % Fig. 3: worked example (three users)
exp1_two_users;       % Fig. 2  (two-user equilibria)
exp2_centralized;     % Fig. 3  (saving vs reward)
exp3_gap;             % Table III (coded vs whole-copy, greedy)
exp4_mobility;        % Fig. 4  (impact of mobility)
exp5_scalability;     % Fig. 5  (sample-based LP, large N)
exp6_decentralized;   % Fig. 6  (equilibria, Stackelberg reward)
exp7_robustness;      % Fig. 7  (learned profiles)
