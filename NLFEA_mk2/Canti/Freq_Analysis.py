# -*- coding: mbcs -*-
# Do not delete the following import lines
from abaqus import *
from abaqusConstants import *
import __main__
# Import relevant modules 
def FreqAnalysis():
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    import os
    step = mdb.openStep(
        'C:/Users/tw15036/OneDrive - University of Bristol/Documents/Year 4/GIP/BeamGeom.stp', 
        scaleFromFile=OFF)
    mdb.models['Model-1'].PartFromGeometryFile(name='BeamGeom', geometryFile=step, 
        combine=False, dimensionality=THREE_D, type=DEFORMABLE_BODY, 
        scale=0.001)
    #Then change part name to Beam
    ##    if filename!='Beam':
    mdb.models['Model-1'].parts.changeKey(fromName='BeamGeom', toName='Beam') # To fit with the pre-written variable names  
    p = mdb.models['Model-1'].parts['Beam']
    ## material properties and name
    mdb.models['Model-1'].Material(name='Steel') # Could build in property inputs
    mdb.models['Model-1'].materials['Steel'].Density(table=((7850, ), ))
    mdb.models['Model-1'].materials['Steel'].Elastic(table=((210000000000, 0.3), ))
##    mdb.models['Model-1'].materials['Steel'].Damping(composite=0.05)       
    mdb.models['Model-1'].HomogeneousSolidSection(name='Section-1', 
        material='Steel', thickness=None)
    ## partioning cell
    e = p.edges
    pickedEdges = e.findAt(([0.015,0.001,0.3],))
    p.PartitionEdgeByParam(edges=pickedEdges, parameter=0.075/0.65)
    p = mdb.models['Model-1'].parts['Beam']
    e = p.edges
    pickedEdges = e.findAt(([0,0.001,0],))
    p.PartitionEdgeByParam(edges=pickedEdges, parameter=0.5)
    p = mdb.models['Model-1'].parts['Beam']
    p.regenerate()
    p = mdb.models['Model-1'].parts['Beam']
    c = p.cells
    pickedCells = c
    e, v, d = p.edges, p.vertices, p.datums
    splitedge = e.findAt(([0.015,0.001,0.037],))
    splitpt = v.findAt(([0.015,0.001,0.075],))
    p.PartitionCellByPlaneNormalToEdge(edge=splitedge[0], point=splitpt[0], cells=pickedCells)
    p = mdb.models['Model-1'].parts['Beam']
    c = p.cells
    pickedCells = c.findAt(([0,0,0.05],))
    e1, v1, d1 = p.edges, p.vertices, p.datums
    splitedge = e1.findAt(([0,0.001,0],))
    splitpt = v1.findAt(([0,0.001,0],))
    p.PartitionCellByPlaneNormalToEdge(edge=splitedge[0], point=splitpt[0], cells=pickedCells)
    ## applying it to the model
    p = mdb.models['Model-1'].parts['Beam']
    c = p.cells
    region = (c,)
    p = mdb.models['Model-1'].parts['Beam']
    p.SectionAssignment(region=region, sectionName='Section-1', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)
    a = mdb.models['Model-1'].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(
        optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
    a = mdb.models['Model-1'].rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    p = mdb.models['Model-1'].parts['Beam']
    a.Instance(name='Beam-1', part=p, dependent=ON)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(
        adaptiveMeshConstraints=ON)
    ## create frequency analysis step
    mdb.models['Model-1'].FrequencyStep(name='Frequency', previous='Initial', 
        limitSavedEigenvectorRegion=None, numEigen=10) # numEigen = no of modes analysed
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Frequency')
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
        predefinedFields=ON, connectors=ON, adaptiveMeshConstraints=OFF)
    ## Clamped boundary conditions
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Initial')
    a = mdb.models['Model-1'].rootAssembly
    f1 = a.instances['Beam-1'].faces
    fixed_ptx=0.01
    fixed_pty=0
    fixed_ptz=0
    fixed_pt=(fixed_ptx,fixed_pty,fixed_ptz)
    fixed_end_face = f1.findAt((fixed_pt,))
    myRegion = regionToolset.Region(faces=fixed_end_face)
    mdb.models['Model-1'].EncastreBC(name='Clamped-1', createStepName='Initial', 
        region=myRegion, localCsys=None)
    a = mdb.models['Model-1'].rootAssembly
    f1 = a.instances['Beam-1'].faces
    fixed_ptx=-0.01
    fixed_pty=0
    fixed_ptz=0
    fixed_pt=(fixed_ptx,fixed_pty,fixed_ptz)
    fixed_end_face = f1.findAt((fixed_pt,))
    myRegion = regionToolset.Region(faces=fixed_end_face)
    mdb.models['Model-1'].EncastreBC(name='Clamped-2', createStepName='Initial', 
        region=myRegion, localCsys=None)
##    session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=OFF, 
##        engineeringFeatures=OFF, mesh=ON)
##    session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
##        meshTechnique=ON)
    ## Viewport
    p1 = mdb.models['Model-1'].parts['Beam']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    ##Meshing
    p = mdb.models['Model-1'].parts['Beam']
    c=p.cells
    e=p.edges
    pickedregions=(c)
    p.setMeshControls(regions=pickedregions, elemShape=QUAD)
    elemType1 = mesh.ElemType(elemCode=C3D8R, elemLibrary=EXPLICIT)
    elemType2 = mesh.ElemType(elemCode=C3D8R, elemLibrary=EXPLICIT)
    elemType3 = mesh.ElemType(elemCode=C3D8R, elemLibrary=EXPLICIT)
    p = mdb.models['Model-1'].parts['Beam']
    c = p.cells
    cells = c[0]
    pickedRegions =(cells, )
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
        elemType3))
    ##Seeding edge - short xy edges
    e1=e.findAt(([0.015,0.001,0.037],))
    p.seedEdgeByNumber(edges=e1, number=4)
    e1=e.findAt(([-0.015,0.001,0.037],))
    p.seedEdgeByNumber(edges=e1, number=4)
    e1=e.findAt(([0.015,-0.001,0.037],))
    p.seedEdgeByNumber(edges=e1, number=4)
    e1=e.findAt(([-0.015,-0.001,0.037],))
    p.seedEdgeByNumber(edges=e1, number=4)
    e1=e.findAt(([0,0.001,0.037],))
    p.seedEdgeByNumber(edges=e1, number=4)
    e1=e.findAt(([0,-0.001,0.037],))
    p.seedEdgeByNumber(edges=e1, number=4)
    ## Longer xy sides
    e1=e.findAt(([0.015,0.001,0.37],))
    p.seedEdgeByNumber(edges=e1, number=24)
    e1=e.findAt(([-0.015,0.001,0.37],))
    p.seedEdgeByNumber(edges=e1, number=24)
    e1=e.findAt(([0.015,-0.001,0.37],))
    p.seedEdgeByNumber(edges=e1, number=24)
    e1=e.findAt(([-0.015,-0.001,0.37],))
    p.seedEdgeByNumber(edges=e1, number=24)
    ## short yz sides
    e1=e.findAt(([0.01,0.001,0],))
    p.seedEdgeByNumber(edges=e1, number=2)
    e1=e.findAt(([-0.01,0.001,0],))
    p.seedEdgeByNumber(edges=e1, number=2)
    e1=e.findAt(([0.01,-0.001,0],))
    p.seedEdgeByNumber(edges=e1, number=2)
    e1=e.findAt(([-0.01,-0.001,0],))
    p.seedEdgeByNumber(edges=e1, number=2)
    e1=e.findAt(([0.01,0.001,0.075],))
    p.seedEdgeByNumber(edges=e1, number=2)
    e1=e.findAt(([-0.01,0.001,0.075],))
    p.seedEdgeByNumber(edges=e1, number=2)
    e1=e.findAt(([0.01,-0.001,0.075],))
    p.seedEdgeByNumber(edges=e1, number=2)
    e1=e.findAt(([-0.01,-0.001,0.075],))
    p.seedEdgeByNumber(edges=e1, number=2)
    ## longer yz sides
    e1=e.findAt(([0,-0.001,0.65],))
    p.seedEdgeByNumber(edges=e1, number=4)
    e1=e.findAt(([0,-0.001,0.65],))
    p.seedEdgeByNumber(edges=e1, number=4)
    ## vertical edges
    e1=e.findAt(([0.015,0,0],))
    p.seedEdgeByNumber(edges=e1, number=2)
    e1=e.findAt(([-0.015,0,0],))
    p.seedEdgeByNumber(edges=e1, number=2)
    e1=e.findAt(([0,0,0],))
    p.seedEdgeByNumber(edges=e1, number=2)
    e1=e.findAt(([-0.015,0,0.075],))
    p.seedEdgeByNumber(edges=e1, number=2)
    e1=e.findAt(([0.015,0,0.075],))
    p.seedEdgeByNumber(edges=e1, number=2)
    e1=e.findAt(([0,0,0.075],))
    p.seedEdgeByNumber(edges=e1, number=2)
    e1=e.findAt(([0.015,0,0.65],))
    p.seedEdgeByNumber(edges=e1, number=2)
    e1=e.findAt(([-0.015,0,0.65],))
    p.seedEdgeByNumber(edges=e1, number=2)    
    p = mdb.models['Model-1'].parts['Beam']
    p.generateMesh()
    a = mdb.models['Model-1'].rootAssembly
    a.regenerate()
    ##Viewport
    a = mdb.models['Model-1'].rootAssembly
    a.regenerate()
        ## ACCELEROMETER INERTIAS
        # End of main beam
    a = mdb.models['Model-1'].rootAssembly
    pt1 = (0,0.001,0.645)
    a.ReferencePoint(point=pt1)
    r1 = a.referencePoints
    region2=a.Set(referencePoints=(r1[6],), name='Set-Acc1')
    mdb.models['Model-1'].rootAssembly.engineeringFeatures.PointMassInertia(
        name='AccInertia-1', region=region2, mass=0.006, alpha=0.0, composite=0.0)
    s1 = a.instances['Beam-1'].faces
    side1Faces1 = s1.findAt((pt1,))
    region1=a.Surface(side1Faces=side1Faces1, name='TopMainBeam')
    mdb.models['Model-1'].Tie(name='AccTie-1', master=region1, slave=region2, 
        positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, 
        thickness=ON)
        # 2/3 along beam
    a = mdb.models['Model-1'].rootAssembly
    pt1 = (0,0.001,0.433)
    a.ReferencePoint(point=pt1)
    r1 = a.referencePoints
    region2=a.Set(referencePoints=(r1[9],), name='Set-Acc2')
    mdb.models['Model-1'].rootAssembly.engineeringFeatures.PointMassInertia(
        name='AccInertia-2', region=region2, mass=0.006, alpha=0.0, composite=0.0)
    s1 = a.instances['Beam-1'].faces
    side1Faces1 = s1.findAt((pt1,))
    region1=a.Surface(side1Faces=side1Faces1, name='TopCrossBeam')
    mdb.models['Model-1'].Tie(name='AccTie-2', master=region1, slave=region2, 
        positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, 
        thickness=ON)
        # 1/3 along beam
    a = mdb.models['Model-1'].rootAssembly
    pt1 = (0,0.001,0.217)
    a.ReferencePoint(point=pt1)
    r1 = a.referencePoints
    region2=a.Set(referencePoints=(r1[12],), name='Set-Acc3')
    mdb.models['Model-1'].rootAssembly.engineeringFeatures.PointMassInertia(
        name='AccInertia-3', region=region2, mass=0.006, alpha=0.0, composite=0.0)
    s1 = a.instances['Beam-1'].faces
    side1Faces1 = s1.findAt((pt1,))
    region1=a.Surface(side1Faces=side1Faces1, name='TopCrossBeam')
    mdb.models['Model-1'].Tie(name='AccTie-3', master=region1, slave=region2, 
        positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, 
        thickness=ON)
    ## Generate matrices
    mdb.models['Model-1'].keywordBlock.synchVersions(storeNodesAndElements=False)
    mdb.models['Model-1'].keywordBlock.insert(55, """
    ** ----------------------------------------------------------------
    **
    * Step, name=exportmatrix
    *matrix generate, mass, stiffness
    *matrix output, mass, stiffness, format=coordinate
    *end step
    **
    **""")
    ## Run job
    mdb.Job(name='Frequency', model='Model-1', description='Frequency Analysis', 
        type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None, 
        memory=90, memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
        explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
        modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
        scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1, 
        numGPUs=0)
    mdb.jobs['Frequency'].submit(consistencyChecking=OFF)
    session.mdbData.summary()
    mdb.jobs['Frequency'].waitForCompletion
FreqAnalysis()

def Saving():
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    #mdb.saveAs(pathName='C:/Users/tw15036/OneDrive - University of Bristol/Documents/Year 4/ExperimentalBeamFreq')
    mdb.saveAs(pathName='C:/temp/FreqAnalysis.cae')
Saving()




