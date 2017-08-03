function O = main(varargin)
    
    % Get the current path.
    path = mfilename('fullpath');
    
    % Create parser.
    p = inputParser;

    % The base directory where to find the reference file.
    basedir = strcat(fileparts(path), '/../../PNC-data/PNC-signals/');
    % The name of the reference file.
    filename = 'REFERENCE.csv';
    % The function handle to validate the reference argument.
    checkReference = @(x) exist(x, 'file');
    % Create the reference argument.
    addOptional(p, 'Reference', strcat(basedir, filename), checkReference);
    
    % The default quota ratio.
    defaultQuota = [0.7 0.3];
    % Check if the input quota are numeric and their sum is equal to 1.
    checkQuota = @(x) isvector(x) && isnumeric(x) && sum(x) == 1;
    % Add the quota argument.
    addOptional(p, 'Quota', defaultQuota, checkQuota);
    
    % Parse the arguments.
    parse(p, varargin{:});
    
    % Load all the content from the csv file.
    content = readref(p.Results.Reference);
    % Create a new shuffle ordering for the dataset by rows.
    ordering = randperm(size(content, 1));
    % Shuffle the content.
    content = content(ordering, :);

    % Create the output vector.
    ecgs = Signal.empty(height(content),0);

    % Create the struct to map the nominal classes into integer ones.
    map = struct('N', 0, 'A', 1, 'O', 2, 'S', 3);
    
    % Compute the real quota.
    quota = round(p.Results.Quota .* size(content, 1));
    
    % Get the list of the files inside the PNC-inputs directory.
    flists = dir(strcat(fileparts(path), '../../PNC-data/PNC-inputs/*.csv'));
    % Extract the file names.
    names = regexp({flists.name}, '\d+', 'match');
    % Get the next file index.
    fi = max(str2double([names{:}])) + 1;
    
    % Open the train file.
    fid = fopen(strcat(fileparts(path), '/../../PNC-data/PNC-inputs/train-', num2str(fi), '.csv'), 'a');

    for i = 1:height(content)
        % Load the Signal data.
        signal = load(strcat(basedir, content{i,1}));
        % Load the Target data.
        target = content{i,2};
        % Save the signal into the output vector.
        ecgs(i) = Signal(signal.val, map.(char(target)), content{i,1});
        
        % Analyse the signal.
        F = patterns(ecgs(i));  
        
        % Cast the array of feature in a double matrix.
        O = compact(ecgs(i));
            
        % Check if it's time to change the output file (eval).
        if i == quota(1)
            % Close the current file.
            fclose(fid);
            % Open the eval file.
            fid = fopen(strcat(fileparts(path), '/../../PNC-data/PNC-inputs/eval-', num2str(fi), '.csv'), 'a');
        % Check if it's time to change the output file (test).
        elseif length(quota) == 3 && i == quota(1) + quota(2)
            % Close the current file.
            fclose(fid);
            % Open the test file.
            fid = fopen(strcat(fileparts(path), '/../../PNC-data/PNC-inputs/test-', num2str(fi), '.csv'), 'a');
        end
        
        % Append the data at the end of the CSV file.
        for s = 1:size(O, 1)

           % Take the i-row of the array and add commas between every
           % element.
           fprintf(fid, strcat(strjoin(O(s,:), ', '), '\n'));  
 
        end
    end
    
    % Close the file stream.
    fclose(fid);

end


