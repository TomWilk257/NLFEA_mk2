function [t,q] = modalAnalysis_Canti

[Phi,Lam,N,diagKs]=Get_Modal_v2;
% Import file
results = csvread('Canti-AllTimeDisps3.csv');

% Get time column out
t = results(:, 1);
% work out no. of nodes from time value repetition
nodes = find(t~=t(1), 1) - 1;
% Remove duplicates from time vector
t = t(1:nodes:end);

% Reshape into 1 col per time step
results = reshape(results(:,2:4)', [], length(t));
% Remove fixed nodes
I = find(results(:,1) == 0);
results(I,:) = [];
% Remove accelerometers
results(1:9,:) = [];
q = [];

for i = 1 : size(results,2)
    q_i = inv(Phi)*results(:, i);
    q = [q, q_i];
end


end