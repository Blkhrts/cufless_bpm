clc;
clear all;
close all;
data=load('date6.txt');

index_start = 1500;

time = data(:,1);
ecg=data(:,2);
ppg=data(:,3);

running = 1;

% while running==1
%   test = 1;
%   for i=index_start:index_start+500
%     if (ecg(i) > 5000 || ppg(i)>10000 || ppg(i)<1000)
%       test = 0;
%     end
%   end
%   if (test==1)
%     running = 0;
%   end
%   index_start = index_start + 100
% end


index_end = 2000;

time = data(index_start:index_end,1);
ecg=data(index_start:index_end,2);
ppg=data(index_start:index_end,3);

prag_ppg = min(ppg) + 0.5 * (max(ppg)-min(ppg));
prag_ecg = max(ecg) - 0.2 * (max(ecg)-min(ecg));

ppg = sgolayfilt(ppg, 5, 53);

plot(time, ppg);


j=1;
n=length(ppg);
for i=2:n-1
    if ppg(i) < ppg(i-1) && ppg(i)<= ppg(i+1) && ppg(i)< prag_ppg
       pos_ppg(j)=i;
       if j==1
           j=j+1;
       else
           if pos_ppg(j)-pos_ppg(j-1)>40
               j=j+1;
           end
       end
     end
end



%pos_ppg = pos_ppg(2:length(pos_ppg)-1)

j=1;
n=length(ecg);
for i=2:n-1
    if ecg(i)> ecg(i-1) && ecg(i)>= ecg(i+1) && ecg(i)> prag_ecg
       pos_ecg(j)=i;
       j=j+1;
     end
end

%pos_ppg
%pos_ecg
if pos_ppg(1) < pos_ecg(1)
    pos_ppg = pos_ppg(2:length(pos_ppg))
end


my_length = min(length(pos_ppg),length(pos_ecg))


ppg_pos = pos_ppg(1:my_length)
ecg_pos = pos_ecg(1:my_length)

t1 = time(ppg_pos)
t2 = time(ecg_pos)

ptt = t1 - t2

t3 = time(ecg_pos(1:length(ecg_pos)-1));
t4 = time(ecg_pos(2:length(ecg_pos)));

60000/mean(t4-t3)




j=1
% for i=1:length(ptt)
%   if ptt(i) > 300 && ptt(i) < 400
%     ptt_final(j)=ptt(i);
%     j=j+1;
%   end
% end



ptt_final = ptt

mean(ptt_final)

std(ptt_final)
