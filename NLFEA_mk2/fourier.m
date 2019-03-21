function [spectrum, freq] = fourier(time, voltage)

%calculate the frequency spectrum of the reflection
fft_pts = nextpow2(length(time));
spectrum = fft(voltage,2^fft_pts,1);
spectrum = spectrum(1:length(spectrum)/2) / length(time);

%build frequency axis
freq_step = 1 / (time(end)-time(1));
freq = [0 : freq_step : freq_step*length(spectrum)-1];

end