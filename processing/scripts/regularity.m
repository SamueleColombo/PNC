function [O] = regularity(S)

    % Check if is a Signal.
    if isa(S, 'Signal')
        % Check if the signal S already contains the R-peaks.
        if ~isequal(S.Points, Point.empty()) && isempty(S.Filter('Peak','R'))
            % Get the list of the Point annotated with R-peak.
            R = S.Filter('Peak','R');
            % Save the x coordinates of the points.
            x = [R.X]';
            % Save the y coordinates of the points.
            y = [R.Y]';
        else
            % Find the R-peaks with the PT algorithm with 300Hz sampling.
            [x, y] = pan_tompkin(S.Values, 300, false);
        end
        % Copy the data.
        T = S.Values;
        
    % Check if is an array of numbers.
    elseif isnumeric(S)
        % Find the R-peaks with the PT algorithm with 300Hz sampling.
        [~, y, ~] = pan_tompkin_qrs(S, 300, false);
        % Copy the data.
        T = S;
    end
    
    
    % TODO: Check if the |y| > 2.
    
    % Padding the y positions.
    y = [1 y length(T)];
    
    % Initialize the D array.
    D = zeros(length(y)-1);
    DC = zeros(length(y)-1);
    DT = zeros(length(y)-1);
    
    % Initialize the R cell array.
    C = {};
    
    % Iterate all over the chunks except the edge ones.
    for i = 1:length(y)-1
        
        % Chunk i.
        c1 = T(y(i):y(i+1));
        
        for j = 1:length(y)-1

            % Chunk i + 1.
            c2 = T(y(j):y(j+1));
            % Perform the cross-correlation between the two chunks.
            xc = xcorr(c1, c2);          
            % Perform the cosine similarity.
            % DC(i,j) = cosine(c1, c2);
            % Perform the Tanimoto similarity.
            % DT(i,j) = tanimoto(c1, c2);
            % How much is the dispersion of the cross-correlation data?
            D(i,j) = std(xc);
            % TODO: Plot the D matrix to understand what happens.
        end
        
        % Save the current chunk.
        C{i} = c1;
    end
    
    % Perform the mean of all the cross-correlation between each chunk.
    threshold_mean = mean(mean(D));
    % Perform the std of all the cross-correlation between each chunk
    threshold_std = std(mean(D));
    % Filter the chunk using the thresholds performed.
    mask = abs(mean(D) - threshold_mean) < threshold_std;
    % Filter the array.
    C = C(mask);
    
    % Append all the right chunks.
    O = [C{:}];
    
    % Check if the input argument is a Signal.
    if isa(S, 'Signal')
       % Save the copied data into the Values property.
       S.Values = T;
    end
    
end

function C = cosine(P, Q)

    % Calculate the different between the length of the two arrays.
    l = length(P) - length(Q);
    
    % Check if |D1| > |D2|.
    if l > 0
        % Extend D2.
        Q = interp1(linspace(1,10,length(Q)), Q, linspace(1,10,length(P)));
    % Check if |D2| > |D1|.
    elseif l < 0
        % Extend D1.
        P = interp1(linspace(1,10,length(P)), P, linspace(1,10,length(Q)));
    end
    
    % Now D1 e D2 have the same length.
    
    C = (P * Q') / (norm(P) * norm(Q));
end

function T = tanimoto(P, Q)

    % Calculate the different between the length of the two arrays.
    l = length(P) - length(Q);
    
    % Check if |D1| > |D2|.
    if l > 0
        % Extend D2.
        Q = interp1(linspace(1,10,length(Q)), Q, linspace(1,10,length(P)));
    % Check if |D2| > |D1|.
    elseif l < 0
        % Extend D1.
        P = interp1(linspace(1,10,length(P)), P, linspace(1,10,length(Q)));
    end
    
    T = (P * Q') /(norm(Q)^2 + norm(P)^2 - (P * Q'));

end