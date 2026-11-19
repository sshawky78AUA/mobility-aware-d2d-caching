function mu = user_payment(x, a, Gm, S, rp)
%USER_PAYMENT  Expected payment of every user (N x M), price 1 per peak byte
%   from the BS and rp = 1 - r per cached byte.
[N, M] = size(x); mu = zeros(N, M);
for m = 1:M
    deficit = max(0, S(m) - double(Gm) * x(:, m));   % G x 1
    mu(:, m) = a(:, :, m) * deficit + rp * x(:, m);
end
end
