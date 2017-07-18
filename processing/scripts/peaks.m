function P = peaks(ecg)

    % Compute the CWT of the signal using a Daubechie 3 wavelet and 100
    % scale factors.
    cab = cwt(ecg.Values, 1:100, 'db3');
    
    % Get the index of the maximum scale factor.
    [~, a] = max(max(transpose(cab)));
    
    % Get the coefficent with maximum scale factors.
    c = cab(a,:);
    
    % Find the peaks in the `a0` waves.
    [p,l] = findpeaks(c);
    
    X = zeros(length(p), 2);
    X(:,1) = p;
    Y = pdist(X);
    Z = linkage(Y);
    T = cluster(Z, 'maxclust', 2);
    C1 = l(T == 1);
    C2 = l(T == 2);
    C3 = l(T == 3);
    C4 = l(T == 4);
    
%     plot(c);
%     hold on
%     plot(C1, c(C1), 'ro');
%     plot(C2, c(C2), 'bo');
%     plot(C3, c(C3), 'ko');
%     plot(C4, c(C4), 'go');
%     hold off
    
    % Perform the moving mean with 3s window.
    h = mean(p);
    % h = movmean(p, 900, 'SamplePoints', l);
    
    % Create the threshold mask.
    mask = abs(h) < c;
    
    % Apply the mask to the original signal.
    vm = ecg.Values .* mask;
    
    % Compute the difference between the masked signal and the original one.
    vd = ecg.Values - vm;
    
    % Get the peaks that are in the threshold.
   
    
    P = 0;

end