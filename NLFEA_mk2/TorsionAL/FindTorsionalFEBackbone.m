function FindTorsionalFEBackbone
% Get mass and stiffness matrices
dos('abaqus cae noGUI=Torsional_FE.py');
dos('abaqus cae noGUI=Torsional_FE_NoMatrices.py');
% Calculate modal forcings and increase to force shape into weakly non-linear regime 
[Phi,Lam,N,diagKs]=Get_Modal_v2_Tors;
appforce = 50;
excite = 1;
forcecalc(Phi,Lam,N,diagKs,appforce, excite);

end