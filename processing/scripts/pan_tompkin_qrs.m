function [Q_loc,R_loc,S_loc] = pan_tompkin_qrs(x1, fs, gr)

% http://archive.cnx.org/contents/611d4152-cf7f-4344-b56d-15775f92fbac@1/qrs-detection-using-pan-tompkins-algorithm

N = length(x1);
t = [0:N-1]/fs;

if gr
    figure(1)
    subplot(2,1,1)
    plot(t,x1)
    xlabel('second');ylabel('Volts');title('Input,ECG,Signal')
    subplot(2,1,2)
    plot(t(200:600),x1(200:600))
    xlabel('second');ylabel('Volts');title('Input,ECG,Signal,1-3,second')
    xlim([1, 3])
end

x1 = x1 - mean(x1);
x1 = x1 / max(abs(x1));

if gr
    figure(2)
    subplot(2,1,1)
    plot(t,x1)
    xlabel('second');ylabel('Volts');title(',ECG,Signal,after,cancellation,DC,drift,and,normalization')
    subplot(2,1,2)
    plot(t(200:600),x1(200:600))
    xlabel('second');ylabel('Volts');title(',ECG,Signal,1-3,second')
    xlim([1,3])
end

b=[1,0,0,0,0,0,-2,0,0,0,0,0,1];
a=[1,-2,1];

 
h_LP=filter(b,a,[1 zeros(1,12)]); % transfer function of LPF
 
x2 = conv (x1 ,h_LP);
%x2 = x2 (6+[1: N]); %cancle delay
x2 = x2/ max( abs(x2 )); % normalize , for convenience .
 
if gr
    figure(3)
    subplot(2,1,1)
    plot([0:length(x2)-1]/fs,x2)
    xlabel('second');ylabel('Volts');title(' ECG Signal after LPF')
    xlim([0 max(t)])
    subplot(2,1,2)
    plot(t(200:600),x2(200:600))
    xlabel('second');ylabel('Volts');title(' ECG Signal 1-3 second')
    xlim([1 3])
end

% HPF = Allpass-(Lowpass) = z^-16-[(1-z^-32)/(1-z^-1)]
b = [-1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 32 -32 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1];
a = [1 -1];
 
h_HP=filter(b,a,[1 zeros(1,32)]); % impulse response iof HPF
 
x3 = conv (x2 ,h_HP);
%x3 = x3 (16+[1: N]); %cancle delay
x3 = x3/ max( abs(x3 ));
 
if gr
    figure(4)
    subplot(2,1,1)
    plot([0:length(x3)-1]/fs,x3)
    xlabel('second');ylabel('Volts');title(' ECG Signal after HPF')
    xlim([0 max(t)])
    subplot(2,1,2)
    plot(t(200:600),x3(200:600))
    xlabel('second');ylabel('Volts');title(' ECG Signal 1-3 second')
    xlim([1 3])
end

% Make impulse response
h = [-1 -2 0 2 1]/8;
% Apply filter
x4 = conv (x3 ,h);
x4 = x4 (2+[1: N]);
x4 = x4/ max( abs(x4 ));
 
if gr
    figure(5)
    subplot(2,1,1)
    plot([0:length(x4)-1]/fs,x4)
    xlabel('second');ylabel('Volts');title(' ECG Signal after Derivative')
    subplot(2,1,2)
    plot(t(200:600),x4(200:600))
    xlabel('second');ylabel('Volts');title(' ECG Signal 1-3 second')
    xlim([1 3])
end

x5 = x4 .^2;
x5 = x5/ max( abs(x5 ));

if gr
    figure(6)
    subplot(2,1,1)
    plot([0:length(x5)-1]/fs,x5)
    xlabel('second');ylabel('Volts');title(' ECG Signal Squarting')
    subplot(2,1,2)
    plot(t(200:600),x5(200:600))
    xlabel('second');ylabel('Volts');title(' ECG Signal 1-3 second')
    xlim([1 3])
end
% Make impulse response
h = ones (1 ,31)/31;
Delay = 15; % Delay in samples
 
% Apply filter
x6 = conv (x5 ,h);
x6 = x6 (15+[1: N]);
x6 = x6/ max( abs(x6 ));
 
if gr
    figure(7)
    subplot(2,1,1)
    plot([0:length(x6)-1]/fs,x6)
    xlabel('second');ylabel('Volts');title(' ECG Signal after Averaging')
    subplot(2,1,2)
    plot(t(200:600),x6(200:600))
    xlabel('second');ylabel('Volts');title(' ECG Signal 1-3 second')
    xlim([1 3])
end 

max_h = max(x6);
thresh = mean (x6 );
poss_reg =(x6>thresh*max_h)';

 
if gr
    figure (8)
    subplot(2,1,1)
    hold on
    plot (t(200:600),x1(200:600)/max(x1))
    box on
    xlabel('second');ylabel('Integrated')
    xlim([1 3])

    subplot(2,1,2)
    plot (t(200:600),x6(200:600)/max(x6))
    xlabel('second');ylabel('Integrated')
    xlim([1 3])
end
 
left = find(diff([0; poss_reg])==1);
right = find(diff([poss_reg; 0])==-1);
 
left=left-(6+16);  % cancle delay because of LP and HP
right=right-(6+16);% cancle delay because of LP and HP

left(left <= 0) = 1;


 
for i=1:length(left)
    try
        [R_value(i) R_loc(i)] = max( x1(left(i):right(i)) );
        R_loc(i) = R_loc(i)-1+left(i); % add offset

        [Q_value(i) Q_loc(i)] = min( x1(left(i):R_loc(i)) );
        Q_loc(i) = Q_loc(i)-1+left(i); % add offset

        [S_value(i) S_loc(i)] = min( x1(left(i):right(i)) );
        S_loc(i) = S_loc(i)-1+left(i); % add offset
        
    catch ex
        oi1 = 5;
    end
end
 
% there is no selective wave
Q_loc=Q_loc(find(Q_loc~=0));
R_loc=R_loc(find(R_loc~=0));
S_loc=S_loc(find(S_loc~=0));

if gr
    figure
    subplot(2,1,1)
    title('ECG Signal with R points');
    plot (t,x1/max(x1) , t(R_loc) ,R_value , 'r^', t(S_loc) ,S_value, '*',t(Q_loc) , Q_value, 'o');
    legend('ECG','R','S','Q');
    subplot(2,1,2)
    plot (t,x1/max(x1) , t(R_loc) ,R_value , 'r^', t(S_loc) ,S_value, '*',t(Q_loc) , Q_value, 'o');
    xlim([1 3])
end

end