function O = default(varargin)
    
    % Create parser.
    p = inputParser;

    % The base directory where to find the reference file.
    basedir = 'C:\Users\Samuele\Documents\PyCharmProjects\PNC2\PNC-data\raw\training\';
    % The name of the reference file.
    filename = 'REFERENCE.csv';
    % The function handle to validate the reference argument.
    checkReference = @(x) exist(x, 'file');
    % Create the reference argument.
    addOptional(p, 'Reference', strcat(basedir, filename), checkReference);
    
    % Parse the arguments.
    parse(p, varargin{:});
    
    % Load all the content from the csv file.
    content = readref(p.Results.Reference);

    % Create the output vector.
    ecgs = Signal.empty(height(content),0);

    % Create the struct to map the nominal classes into integer ones.
    map = struct('N', 0, 'A', 1, 'O', 2, 'S', 3);

    for i = 1:height(content)
        % Load the Signal data.
        signal = load(strcat(basedir, content{i,1}));
        % Load the Target data.
        target = content{i,2};
        % Save the signal into the output vector.
        ecgs(i) = Signal(signal.val, map.(char(target)), content{i,1});
    end

    % Start the analysis.
    F = patterns(ecgs);
    
    % Get the current path.
    path = mfilename('fullpath');
    
    % Save the features in a checkpoint directory.
    save(strcat(fileparts(path), '/../../test/PNC-features/F'), 'ecgs');
    
    % Compact the Features into readable matrix.
    O = compact(ecgs);
end


