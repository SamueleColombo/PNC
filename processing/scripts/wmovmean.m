function [M] = wmovmean(A,k,t)

    % Declare the output variable.
    M = [];

    for i = 1:length(A)

        edge = (abs(t - t(i)) < t(i) + k);
        window = A(edge);
        M(i) = wmean(window);
    end
end