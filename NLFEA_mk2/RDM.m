function [amp, freq] = RDM(time, signal)
%% Import csv file 
% res = csvread('Canti-BackboneNF2.csv');
% time = res(:,1);
% signal = res(:,3);
% figure;
% plot(time, signal)
% 
% % Filtering to get 2nd mode
% 
% [spectrum, frequency] = fourier(time, signal);
% [~, locs] = findpeaks(abs(spectrum(1:length(frequency))), frequency, 'NPeaks', 2, 'SortStr', 'descend');
% window = fn_gaussian(length(spectrum), locs(2)/ max(frequency), 40/max(frequency));
% filt_spec = window.*spectrum;
% signal = real(ifft(filt_spec, length(time)));
% signal = signal(1:2000);
% time = time(1:2000);

%% Finding the instantaneous frequency
% Adjust the signal to be about its median
signal = signal - mean(signal);

% Find zero crossing points
crossingpts = [];
for i = 2:length(signal)
    if sign(signal(i)) ~= sign(signal(i-1))
        crossingpts = [crossingpts, time(i)];
    end
end

% Evaluate frequency at each crossing point

freq = [];
amp = [];
for i = 2 : length(crossingpts) - 1
    instfreq = (crossingpts(i+1) - crossingpts(i-1))^(-1);
    ind_lo = find(time == crossingpts(i-1));
    ind_hi = find(time == crossingpts(i+1));
    instamp = max(abs(signal(ind_lo : ind_hi)));
    freq = [freq, instfreq];
    amp = [amp, instamp];
end

% MA_freq = smooth(freq, 5);

%% Finding the instantaneous amplitude 
% % Find the peaks of the sinusoidal signal 
% 
% [pks, locs] = findpeaks(signal, time);
% 
% % fit a polynomial through the points
% P_amp = polyfit(locs, pks', 7);
% %Evaluate the polynomial at the crossing pts to get values at same time as
% %instantaneous frequencies
% amp = polyval(P_amp, crossingpts(2 : end-1));



%% Fit Backbone curve

% P_BB = polyfit(amp, freq, 7);
% freq_space = linspace(min(amp), max(amp), 100);
% BB = polyval(P_BB, freq_space);

%% Plot results 

figure
%Time domain plots
subplot(2,1,1)
plot(time, signal, 'k')
hold on
% amp_time = polyval(P_amp, time);
% plot(time, amp_time, 'r')
hold off
xlabel('Time (s)')
ylabel('Amplitude (m)')

% Frequency domain plots
subplot(2,1,2)
scatter(freq, amp, 'r*')
hold on
% scatter(MA_freq, amp, 'bo')
% plot(BB, freq_space, 'r--')
xlabel('Frequency (Hz)')
ylabel('Amplitude (m)')
axis([0, inf, 0, inf])


end