function FindFEBackbone
% Get mass and stiffness matrices
dos('abaqus cae noGUI=Freq_Analysis.py');
dos('abaqus cae noGUI=Freq_Analysis_FE.py');
% Calculate modal forcings and increase to force shape into weakly non-linear regime 
[Phi,Lam,N,diagKs]=Get_Modal_v2;
appforce = 100;
excite = 2;
forcecalc(Phi,Lam,N,diagKs,appforce, excite);
% Apply first modal forcing 
dos('abaqus cae noGUI=BackboneDef.py');
% read results from csv file 
results = csvread('Canti-BackboneNF2.csv');
% find backbone curve using RDM from Simon Nield's paper 
time = results(:,1);
signal = results(:,3);

[amp, freq] = RDM(time, signal)

end