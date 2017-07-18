classdef Features < dynamicprops
   
    properties
       Values  % The Feature object array. 
    end
    
    methods
        function obj = Features(varargin)
            
            if nargin >= 1
                % TODO: Check if varargin contains only Feature object.
                
                % Copy the Feature inside the Values array.
                obj.Values = [varargin{:}];
            end   
            
        end
    end
    
end