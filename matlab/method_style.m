function st = method_style(key)
%METHOD_STYLE  One color / line / marker per method, used in every figure.
switch key
    case {'lp', 'central'}, st = struct('c', [0 0 0],          'ls', '-',  'mk', 'o', 'name', 'LP (coded)');
    case 'whole',           st = struct('c', [0.00 0.45 0.74], 'ls', '--', 'mk', 's', 'name', 'Best whole-copy');
    case 'greedy',          st = struct('c', [0.47 0.67 0.19], 'ls', '-.', 'mk', '^', 'name', 'Greedy');
    case 'crowd',           st = struct('c', [0.49 0.18 0.56], 'ls', ':',  'mk', 'd', 'name', 'Crowd mobility');
    case 'nod2d',           st = struct('c', [0.85 0.33 0.10], 'ls', '-',  'mk', 'v', 'name', 'No D2D');
    case 'best',            st = struct('c', [0.47 0.67 0.19], 'ls', '--', 'mk', '^', 'name', 'SP-best NE');
    case 'worst',           st = struct('c', [0.85 0.33 0.10], 'ls', ':',  'mk', 'v', 'name', 'SP-worst NE');
    case 'fair',            st = struct('c', [0.00 0.45 0.74], 'ls', '-.', 'mk', 's', 'name', 'Fair NE');
    case 'pot',             st = struct('c', [0.49 0.18 0.56], 'ls', '-',  'mk', 'd', 'name', 'Potential NE');
end
if strcmp(key, 'central'), st.name = 'Centralized C^*(r)'; end
end
