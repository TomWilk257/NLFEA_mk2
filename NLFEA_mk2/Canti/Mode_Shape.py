from abaqus import *
from abaqusConstants import *
import __main__
# Import relevant modules 
def Mode_Shape():
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
    import csv
    # Get input data from input file 
    ##    f = open('C:/Users/tw15036/OneDrive - University of Bristol/Documents/Year 4/GIP/InputFile.txt','r')
    ##    File = f.readline()
    density = float(7850)
    elasticity = float(210000000000)
    poisson = float(0.3)
    ##    if '/n' in File:
    ##        File = File[0:-1]
    ##    # Import geometry as STEP file to create the part, change geometryFile property for other part types
    ##    filename_w_ext = os.path.basename(File)
    ##    filename, file_extension = os.path.splitext(filename_w_ext)
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
    mdb.models['Model-1'].Material(name='Steel') # Could build in prperty inputs
    mdb.models['Model-1'].materials['Steel'].Density(table=((7850, ), ))
    mdb.models['Model-1'].materials['Steel'].Elastic(table=((210000000000, 0.3), ))
    mdb.models['Model-1'].HomogeneousSolidSection(name='Section-1', 
        material='Steel', thickness=None)
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
    fixed_ptx=0
    fixed_pty=0
    fixed_ptz=0
    fixed_pt=(fixed_ptx,fixed_pty,fixed_ptz)
    fixed_end_face = f1.findAt((fixed_pt,))
    myRegion = regionToolset.Region(faces=fixed_end_face)
    mdb.models['Model-1'].EncastreBC(name='Clamped-1', createStepName='Initial', 
        region=myRegion, localCsys=None)
    session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=OFF, 
        engineeringFeatures=OFF, mesh=ON)
    session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
        meshTechnique=ON)
    ## Viewport
    p1 = mdb.models['Model-1'].parts['Beam']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    ##Meshing
    p = mdb.models['Model-1'].parts['Beam']
    c=p.cells
    e=p.edges
    pickedregions=(c)
    p.setMeshControls(regions=pickedregions, elemShape=HEX)
    elemType1 = mesh.ElemType(elemCode=C3D20R, elemLibrary=STANDARD)
    elemType2 = mesh.ElemType(elemCode=C3D15, elemLibrary=STANDARD)
    elemType3 = mesh.ElemType(elemCode=C3D10, elemLibrary=STANDARD)
    p = mdb.models['Model-1'].parts['Beam']
    c = p.cells
    cells = c[0]
    pickedRegions =(cells, )
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
        elemType3))
    ##Seeding edge - short xy edges
    ##    e1=e.findAt(([0.015,0.001,0.037],))
    ##    p.seedEdgeByNumber(edges=e1, number=4)
    ##    e1=e.findAt(([-0.015,0.001,0.037],))
    ##    p.seedEdgeByNumber(edges=e1, number=4)
    ##    e1=e.findAt(([0.015,-0.001,0.037],))
    ##    p.seedEdgeByNumber(edges=e1, number=4)
    ##    e1=e.findAt(([-0.015,-0.001,0.037],))
    ##    p.seedEdgeByNumber(edges=e1, number=4)
    ##    e1=e.findAt(([0,0.001,0.037],))
    ##    p.seedEdgeByNumber(edges=e1, number=4)
    ##    e1=e.findAt(([0,-0.001,0.037],))
    ##    p.seedEdgeByNumber(edges=e1, number=4)
        ## long z-dir sides
    e1=e.findAt(([0.015,0.001,0.37],))
    p.seedEdgeByNumber(edges=e1, number=27)
    e1=e.findAt(([-0.015,0.001,0.37],))
    p.seedEdgeByNumber(edges=e1, number=27)
    e1=e.findAt(([0.015,-0.001,0.37],))
    p.seedEdgeByNumber(edges=e1, number=27)
    e1=e.findAt(([-0.015,-0.001,0.37],))
    p.seedEdgeByNumber(edges=e1, number=27)
    ## short x-dir sides
    ##    e1=e.findAt(([0.01,0.001,0],))
    ##    p.seedEdgeByNumber(edges=e1, number=3)
    ##    e1=e.findAt(([-0.01,0.001,0],))
    ##    p.seedEdgeByNumber(edges=e1, number=3)
    ##    e1=e.findAt(([0.01,-0.001,0],))
    ##    p.seedEdgeByNumber(edges=e1, number=3)
    ##    e1=e.findAt(([-0.01,-0.001,0],))
    ##    p.seedEdgeByNumber(edges=e1, number=3)
    ##    e1=e.findAt(([0.01,0.001,0.075],))
    ##    p.seedEdgeByNumber(edges=e1, number=3)
    ##    e1=e.findAt(([-0.01,0.001,0.075],))
    ##    p.seedEdgeByNumber(edges=e1, number=3)
    ##    e1=e.findAt(([0.01,-0.001,0.075],))
    ##    p.seedEdgeByNumber(edges=e1, number=3)
    ##    e1=e.findAt(([-0.01,-0.001,0.075],))
    ##    p.seedEdgeByNumber(edges=e1, number=3)
    ## longer x-dir sides
    e1=e.findAt(([0,-0.001,0.65],))
    p.seedEdgeByNumber(edges=e1, number=5)
    e1=e.findAt(([0,-0.001,0.65],))
    p.seedEdgeByNumber(edges=e1, number=5)
    e1=e.findAt(([0,-0.001,0],))
    p.seedEdgeByNumber(edges=e1, number=5)
    e1=e.findAt(([0,-0.001,0],))
    p.seedEdgeByNumber(edges=e1, number=5)
    ## vertical edges
    e1=e.findAt(([0.015,0,0],))
    p.seedEdgeByNumber(edges=e1, number=2)
    e1=e.findAt(([-0.015,0,0],))
    p.seedEdgeByNumber(edges=e1, number=2)
    ##    e1=e.findAt(([0,0,0],))
    ##    p.seedEdgeByNumber(edges=e1, number=2)
    ##    e1=e.findAt(([-0.015,0,0.075],))
    ##    p.seedEdgeByNumber(edges=e1, number=2)
    ##    e1=e.findAt(([0.015,0,0.075],))
    ##    p.seedEdgeByNumber(edges=e1, number=2)
    ##    e1=e.findAt(([0,0,0.075],))
    ##    p.seedEdgeByNumber(edges=e1, number=2)
    e1=e.findAt(([0.015,0,0.65],))
    p.seedEdgeByNumber(edges=e1, number=2)
    e1=e.findAt(([-0.015,0,0.65],))
    p.seedEdgeByNumber(edges=e1, number=2)    
    p = mdb.models['Model-1'].parts['Beam']
    p.generateMesh()
    ##Viewport
    a = mdb.models['Model-1'].rootAssembly
    a.regenerate()
        ## ACCELEROMETER INERTIAS
        # End of main beam
    a = mdb.models['Model-1'].rootAssembly
    pt1 = (0,0.001,0.645)
    a.ReferencePoint(point=pt1)
    r1 = a.referencePoints
    region2=a.Set(referencePoints=(r1[5],), name='Set-Acc1')
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
    region2=a.Set(referencePoints=(r1[8],), name='Set-Acc2')
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
    region2=a.Set(referencePoints=(r1[11],), name='Set-Acc3')
    mdb.models['Model-1'].rootAssembly.engineeringFeatures.PointMassInertia(
        name='AccInertia-3', region=region2, mass=0.006, alpha=0.0, composite=0.0)
    s1 = a.instances['Beam-1'].faces
    side1Faces1 = s1.findAt((pt1,))
    region1=a.Surface(side1Faces=side1Faces1, name='TopCrossBeam')
    mdb.models['Model-1'].Tie(name='AccTie-3', master=region1, slave=region2, 
        positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, 
        thickness=ON)
##Apply Loading
    mdb.models['Model-1'].StaticStep(name='Step-1', previous='Initial', nlgeom=ON)
    instanceNodes = mdb.models['Model-1'].rootAssembly.instances['Beam-1'].nodes
    #Import Forces
    file=csv.reader(open('C:\\Users\\tw15036\\OneDrive - University of Bristol\\Documents\\Year 4\\GIP\\Abaqus Output Files\\myFile2.csv','r'))
    n=[]
    for row in file:
        n.append(row)
    for i in range(0,len(n)):      
        #nodeLabel = tuple(range(1,100))
        nodeLabel=[i]
        [cf11,cf22,cf33]=map(float,n[i])
        meshNodeObj = instanceNodes.sequenceFromLabels(nodeLabel)
        myRegion = regionToolset.Region(nodes=meshNodeObj)
        mdb.models['Model-1'].ConcentratedForce(name='Load-'+str(i), createStepName='Step-1', 
           region=myRegion, cf1=cf11, cf2=cf22, cf3=cf33, distributionType=UNIFORM, field='', 
           localCsys=None)
## Run job
    mdb.Job(name='Mode_Shape', model='Model-1', description='Mode Shape', 
        type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None, 
        memory=90, memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
        explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
        modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
        scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1, 
        numGPUs=0)
    mdb.jobs['Mode_Shape'].submit(consistencyChecking=OFF)
Mode_Shape()

##def Saving():
##    import section
##    import regionToolset
##    import displayGroupMdbToolset as dgm
##    import part
##    import material
##    import assembly
##    import step
##    import interaction
##    import load
##    import mesh
##    import optimization
##    import job
##    import sketch
##    import visualization
##    import xyPlot
##    import displayGroupOdbToolset as dgo
##    import connectorBehavior
##    #mdb.saveAs(pathName='C:/Users/tw15036/OneDrive - University of Bristol/Documents/Year 4/ExperimentalBeamFreq')
##    mdb.saveAs(pathName='C:/temp/ExperimentalBeamFreq')
##Saving()

##    o3 = session.openOdb(name='C:/temp/Frequency.odb')
##    session.viewports['Viewport: 1'].setValues(displayedObject=o3)
##    session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=3)
##    session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=3)
##    session.animationController.setValues(animationType=HARMONIC, viewports=(
##        'Viewport: 1', ))
##    session.animationController.play(duration=UNLIMITED)
##    session.animationController.setValues(animationType=TIME_HISTORY)
##    session.animationController.play(duration=UNLIMITED)
##    session.animationController.setValues(animationType=SCALE_FACTOR)
##    session.animationController.play(duration=UNLIMITED)
##    session.animationController.setValues(animationType=HARMONIC)
##    session.animationController.play(duration=UNLIMITED)
##    session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=3)
##    session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=3)
##    session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
##        CONTOURS_ON_DEF, ))


