classdef Feature < dynamicprops
    
    properties
       Key      % The name of the feature.
       Value    % The valure of the feature (integer, real, array).
    end
    
    methods
        function obj = Feature(k, v)
           
            % Create an input parser.
            parameter = inputParser;
            
            % Create the Key parser.
            addRequired(parameter, 'key', @ischar);
            
            % Create the Value parser.
            addRequired(parameter, 'value');
            
            % Parse the varagin arguments.
            parse(parameter, k, v);
            
            % Save the data into the object.
            obj.Key = k;
            obj.Value = v;            
        end
        
%         function S = size(obj)
%            
%             % Calculate the size of each feature inside this container.
%             S = cellfun(@(x) length(x), {obj.Value});
%             
%         end
    end
    
end