from abaqus import *
from abaqusConstants import *
import __main__
def TorsionalBeam():
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
    from odbAccess import *
    import csv
    import sys
        ## GRAB ARGUMENTS
    mass_x_pos = float(0.096)
    density = float(7850)
    elasticity = float(210000000000)
    poisson = float(0.3)
    mesh_size = int(10)
    ## PART CREATION
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=1.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.unsetPrimaryObject()
    del mdb.models['Model-1'].sketches['__profile__']
    s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=1.0)
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.setPrimaryObject(option=STANDALONE)
    ## PART 1
    s1.rectangle(point1=(0.015, 0.001), point2=(-0.015, -0.001))
    p = mdb.models['Model-1'].Part(name='Part-1', dimensionality=THREE_D, 
        type=DEFORMABLE_BODY)
    p = mdb.models['Model-1'].parts['Part-1']
    p.BaseSolidExtrude(sketch=s1, depth=0.65)
    s1.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts['Part-1']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models['Model-1'].sketches['__profile__']
    # Partitioning Part 1
    e = p.edges
    pickedEdges = e.findAt(([0.015,0.001,0.3],))
    p.PartitionEdgeByParam(edges=pickedEdges, parameter=0.075/0.65)
    p = mdb.models['Model-1'].parts['Part-1']
    e = p.edges
    pickedEdges = e.findAt(([0,0.001,0],))
    p.PartitionEdgeByParam(edges=pickedEdges, parameter=0.5)
    p = mdb.models['Model-1'].parts['Part-1']
    p.regenerate()
    p = mdb.models['Model-1'].parts['Part-1']
    c = p.cells
    pickedCells = c
    e, v, d = p.edges, p.vertices, p.datums
    splitedge = e.findAt(([0.015,0.001,0.037],))
    splitpt = v.findAt(([0.015,0.001,0.075],))
    p.PartitionCellByPlaneNormalToEdge(edge=splitedge[0], point=splitpt[0], cells=pickedCells)
    p = mdb.models['Model-1'].parts['Part-1']
    c = p.cells
    pickedCells = c.findAt(([0,0,0.05],))
    e1, v1, d1 = p.edges, p.vertices, p.datums
    splitedge = e1.findAt(([0,0.001,0],))
    splitpt = v1.findAt(([0,0.001,0],))
    p.PartitionCellByPlaneNormalToEdge(edge=splitedge[0], point=splitpt[0], cells=pickedCells)
    ## PART 2
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=1.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.rectangle(point1=(0.2, 0.002), point2=(-0.2, -0.002))
    p = mdb.models['Model-1'].Part(name='Part-2', dimensionality=THREE_D, 
        type=DEFORMABLE_BODY)
    p = mdb.models['Model-1'].parts['Part-2']
    p.BaseSolidExtrude(sketch=s, depth=0.03)
    s.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts['Part-2']
    del mdb.models['Model-1'].sketches['__profile__']
    p = mdb.models['Model-1'].parts['Part-1']
    p = mdb.models['Model-1'].parts['Part-2']
    a = mdb.models['Model-1'].rootAssembly
    a = mdb.models['Model-1'].rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    p = mdb.models['Model-1'].parts['Part-1']
    a.Instance(name='Part-1-1', part=p, dependent=ON)
    a = mdb.models['Model-1'].rootAssembly
    p = mdb.models['Model-1'].parts['Part-2']
    a.Instance(name='Part-2-1', part=p, dependent=ON)
    ## TRANSLATE CROSS BEAM (top section is done wrong then corrected)
    a = mdb.models['Model-1'].rootAssembly
    a.translate(instanceList=('Part-2-1', ), vector=(0.0, 0.003, 0.31))
    a = mdb.models['Model-1'].rootAssembly
    a1 = mdb.models['Model-1'].rootAssembly
    f1 = a1.instances['Part-1-1'].faces
    f2 = a1.instances['Part-2-1'].faces
    a1.FaceToFace(movablePlane=f1[13], fixedPlane=f2[1], flip=ON, clearance=0.0)
        ## BOUNDARY CONDITIONS
        #face specified by user
    a = mdb.models['Model-1'].rootAssembly
    f1 = a.instances['Part-1-1'].faces
    fixed_ptx=0.01
    fixed_pty=0
    fixed_ptz=0
    fixed_pt=(fixed_ptx,fixed_pty,fixed_ptz)
    fixed_end_face = f1.findAt((fixed_pt,))
    myRegion = regionToolset.Region(faces=fixed_end_face)
    mdb.models['Model-1'].EncastreBC(name='Clamped-1', createStepName='Initial', 
        region=myRegion, localCsys=None)
    f1 = a.instances['Part-1-1'].faces
    fixed_ptx=-0.01
    fixed_pty=0
    fixed_ptz=0
    fixed_pt=(fixed_ptx,fixed_pty,fixed_ptz)
    fixed_end_face = f1.findAt((fixed_pt,))
    myRegion = regionToolset.Region(faces=fixed_end_face)
    mdb.models['Model-1'].EncastreBC(name='Clamped-2', createStepName='Initial', 
        region=myRegion, localCsys=None)
    p1 = mdb.models['Model-1'].parts['Part-2']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
        ## MATERIAL 
    mdb.models['Model-1'].Material(name='Steel')
    mdb.models['Model-1'].materials['Steel'].Density(table=((density, ), ))
    mdb.models['Model-1'].materials['Steel'].Elastic(table=((elasticity, poisson), 
        ))
    mdb.models['Model-1'].HomogeneousSolidSection(name='Section-1', 
        material='Steel', thickness=None)
    p1 = mdb.models['Model-1'].parts['Part-1']
    ## SECTION CREATION - PART 1
    p = mdb.models['Model-1'].parts['Part-1']
    c = p.cells
    region = p.Set(cells=c, name='Set-1')
    p = mdb.models['Model-1'].parts['Part-1']
    p.SectionAssignment(region=region, sectionName='Section-1', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)
    ## SECTION ASSIGNMENT - PART 2
    p1 = mdb.models['Model-1'].parts['Part-2']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    p = mdb.models['Model-1'].parts['Part-2']
    c = p.cells
    region = p.Set(cells=c, name='Set-1')
    p = mdb.models['Model-1'].parts['Part-2']
    p.SectionAssignment(region=region, sectionName='Section-1', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)
    a = mdb.models['Model-1'].rootAssembly
    a.regenerate()
    ##STEP SET UP
    mdb.models['Model-1'].FrequencyStep(name='Step-1', previous='Initial', 
        numEigen=10)
    p1 = mdb.models['Model-1'].parts['Part-2']
        ##MESHING
        #element definition
        #meshing part 2
    ##    ElemType1=mesh.ElemType(elemCode=B32)   
    p=mdb.models['Model-1'].parts['Part-2']
    ##    pickedregions=regionToolset.Region(edges=p.edges)
    ##    p.setElementType(regions=pickedregions, elemTypes=(ElemType1,))
    elemType1 = mesh.ElemType(elemCode=C3D8R, elemLibrary=STANDARD)
    elemType2 = mesh.ElemType(elemCode=C3D8R, elemLibrary=STANDARD)
    elemType3 = mesh.ElemType(elemCode=C3D8R, elemLibrary=STANDARD)
    c = p.cells
    cells = c
    pickedRegions =(cells, )
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
        elemType3))
    p = mdb.models['Model-1'].parts['Part-2']
    e = p.edges
    ## seeding long x edges
    e1 = e.findAt(([0,-0.002,0.03],))
    p.seedEdgeByNumber(edges=e1, number=20)
    e1 = e.findAt(([0,0.002,0],))
    p.seedEdgeByNumber(edges=e1, number=20)
    e1 = e.findAt(([0,-0.002,0.03],))
    p.seedEdgeByNumber(edges=e1, number=20)
    e1 = e.findAt(([0,0.002,0.03],))
    p.seedEdgeByNumber(edges=e1, number=20)
    ## seeding z edges
    e1 = e.findAt(([0.2,0.002,0.015],))
    p.seedEdgeByNumber(edges=e1, number=5)
    e1 = e.findAt(([0.2,-0.002,0.015],))
    p.seedEdgeByNumber(edges=e1, number=5)
    e1 = e.findAt(([-0.2,-0.002,0.015],))
    p.seedEdgeByNumber(edges=e1, number=5)
    e1 = e.findAt(([-0.2,0.002,0.015],))
    p.seedEdgeByNumber(edges=e1, number=5)
    ## seeding y edges
    e1 = e.findAt(([0.2,0,0],))
    p.seedEdgeByNumber(edges=e1, number=5)
    e1 = e.findAt(([0.2,0,0.03],))
    p.seedEdgeByNumber(edges=e1, number=5)
    e1 = e.findAt(([-0.2,0,0],))
    p.seedEdgeByNumber(edges=e1, number=5)
    e1 = e.findAt(([-0.2,0,0.03],))
    p.seedEdgeByNumber(edges=e1, number=5)
    p = mdb.models['Model-1'].parts['Part-2']
    p.generateMesh()
            #meshing part 1
        ## meshing
    p = mdb.models['Model-1'].parts['Part-1']
    c=p.cells
    e=p.edges
    pickedregions=(c)
    p.setMeshControls(regions=pickedregions, elemShape=QUAD)
    p.Set(cells=pickedregions, name='Set-Mesh')
    ##    p.seedPart(size=0.0075, deviationFactor=0.1, minSizeFactor=0.1)
    ##Seeding edge - short xy edges
    ##    ElemType1=mesh.ElemType(elemCode=B32)
    ##    pickedregions = a.instances['Part-1-1'].sets['Set-Mesh']
    ##    p.setElementType(regions=pickedregions, elemTypes=(ElemType1,))
    elemType1 = mesh.ElemType(elemCode=C3D8R, elemLibrary=STANDARD)
    elemType2 = mesh.ElemType(elemCode=C3D8R, elemLibrary=STANDARD)
    elemType3 = mesh.ElemType(elemCode=C3D8R, elemLibrary=STANDARD)
    c = p.cells
    cells = c
    pickedRegions =(cells, )
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
        elemType3))
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
    p = mdb.models['Model-1'].parts['Part-1']
    p.generateMesh()
    a = mdb.models['Model-1'].rootAssembly
    a.regenerate()
        ## CONNECTING FACES
    a = mdb.models['Model-1'].rootAssembly
    s1 = a.instances['Part-1-1'].faces
    fixed_ptx=0
    fixed_pty=0.001
    fixed_ptz=0.433
    fixed_pt=(fixed_ptx,fixed_pty,fixed_ptz)
    side1Faces1 = s1.findAt((fixed_pt,))
    region1=a.Surface(side1Faces=side1Faces1, name='m_Surf-3')
    a = mdb.models['Model-1'].rootAssembly
    s1 = a.instances['Part-2-1'].faces
    fixed_ptx=0
    fixed_pty=0.001
    fixed_ptz=0.325
    fixed_pt=(fixed_ptx,fixed_pty,fixed_ptz)
    side1Faces1 = s1.findAt((fixed_pt,))
    region2=a.Surface(side1Faces=side1Faces1, name='s_Surf-3')
    mdb.models['Model-1'].Tie(name='FaceTie', master=region1, slave=region2, 
        positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, 
        constraintEnforcement=SURFACE_TO_SURFACE, thickness=ON)
    ## INERTIAL ELEMENTS (POINT MASSES AND ACCELEROMETERS)
    #Point Mass
    a = mdb.models['Model-1'].rootAssembly
    pt1 = (mass_x_pos, 0.005, 0.325)
    a.ReferencePoint(point=pt1)
    r1 = a.referencePoints
    region2=a.Set(referencePoints=(r1[11],), name='Set-inertial')
    mdb.models['Model-1'].rootAssembly.engineeringFeatures.PointMassInertia(
        name='Inertia-1', region=region2, mass=0.6378, alpha=0.0, composite=0.0)
    s1 = a.instances['Part-2-1'].faces
    side1Faces1 = s1.findAt((pt1,))
    region1=a.Surface(side1Faces=side1Faces1, name='m_Surf-5')
    mdb.models['Model-1'].Tie(name='InertialTie', master=region1, slave=region2, 
        positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, 
        constraintEnforcement=NODE_TO_SURFACE, thickness=ON)
        ## CONNECTING THE TWO PARTS WITH POINT FASTENERS    
    a = mdb.models['Model-1'].rootAssembly
    Fast1=(0.0075,0.001,0.325)
    Fast2=(-0.0075,0.001,0.325)
    a.ReferencePoint(point=Fast1)
    a.ReferencePoint(point=Fast2)
    r1 = a.referencePoints
    refPoints1=(r1[14], r1[15], )
    region=a.Set(referencePoints=refPoints1, name='Set-4')
    a = mdb.models['Model-1'].rootAssembly
    tSurface1=a.surfaces['m_Surf-3']
    a = mdb.models['Model-1'].rootAssembly
    tSurface2=a.surfaces['s_Surf-3']
    targetSurface=(tSurface1, tSurface2, )
##    mdb.models['Model-1'].rootAssembly.engineeringFeatures.PointFastener(
##        name='Fasteners-1', region=region, targetSurfaces=targetSurface, 
##        physicalRadius=0.005, connectionType=BEAM_MPC, unsorted=OFF)
        ## ACCELEROMETER INERTIAS
        # End of main beam
    a = mdb.models['Model-1'].rootAssembly
    pt1 = (0,0.001,0.645)
    a.ReferencePoint(point=pt1)
    r1 = a.referencePoints
    region2=a.Set(referencePoints=(r1[17],), name='Set-Acc1')
    mdb.models['Model-1'].rootAssembly.engineeringFeatures.PointMassInertia(
        name='AccInertia-1', region=region2, mass=0.006, alpha=0.0, composite=0.0)
    s1 = a.instances['Part-1-1'].faces
    side1Faces1 = s1.findAt((pt1,))
    region1=a.Surface(side1Faces=side1Faces1, name='TopMainBeam')
    mdb.models['Model-1'].Tie(name='AccTie-1', master=region1, slave=region2, 
        positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, 
        constraintEnforcement=NODE_TO_SURFACE, thickness=ON)
        # Centre point
    a = mdb.models['Model-1'].rootAssembly
    pt1 = (0,0.005,0.335)
    a.ReferencePoint(point=pt1)
    r1 = a.referencePoints
    region2=a.Set(referencePoints=(r1[20],), name='Set-Acc2')
    mdb.models['Model-1'].rootAssembly.engineeringFeatures.PointMassInertia(
        name='AccInertia-2', region=region2, mass=0.006, alpha=0.0, composite=0.0)
    s1 = a.instances['Part-2-1'].faces
    side1Faces1 = s1.findAt((pt1,))
    region1=a.Surface(side1Faces=side1Faces1, name='TopCrossBeam')
    mdb.models['Model-1'].Tie(name='AccTie-2', master=region1, slave=region2, 
        positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, 
        constraintEnforcement=NODE_TO_SURFACE, thickness=ON)
        # End of cross beam (+ve x)
    a = mdb.models['Model-1'].rootAssembly
    pt1 = (0.195,0.005,0.335)
    a.ReferencePoint(point=pt1)
    r1 = a.referencePoints
    region2=a.Set(referencePoints=(r1[23],), name='Set-Acc3')
    mdb.models['Model-1'].rootAssembly.engineeringFeatures.PointMassInertia(
        name='AccInertia-3', region=region2, mass=0.006, alpha=0.0, composite=0.0)
    s1 = a.instances['Part-2-1'].faces
    side1Faces1 = s1.findAt((pt1,))
    region1=a.Surface(side1Faces=side1Faces1, name='TopCrossBeam')
    mdb.models['Model-1'].Tie(name='AccTie-3', master=region1, slave=region2, 
        positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, 
        constraintEnforcement=NODE_TO_SURFACE, thickness=ON)
        # Other side of cross beam
    a = mdb.models['Model-1'].rootAssembly
    pt1 = (-0.195,0.005,0.335)
    a.ReferencePoint(point=pt1)
    r1 = a.referencePoints
    region2=a.Set(referencePoints=(r1[26],), name='Set-Acc4')
    mdb.models['Model-1'].rootAssembly.engineeringFeatures.PointMassInertia(
        name='AccInertia-4', region=region2, mass=0.006, alpha=0.0, composite=0.0)
    s1 = a.instances['Part-2-1'].faces
    side1Faces1 = s1.findAt((pt1,))
    region1=a.Surface(side1Faces=side1Faces1, name='TopCrossBeam')
    mdb.models['Model-1'].Tie(name='AccTie-4', master=region1, slave=region2, 
        positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, 
        constraintEnforcement=NODE_TO_SURFACE, thickness=ON)
        ## Generate matrices
##    mdb.models['Model-1'].keywordBlock.synchVersions(storeNodesAndElements=False)
##    mdb.models['Model-1'].keywordBlock.insert(94, """
##    ** ----------------------------------------------------------------
##    **
##    * Step, name=exportmatrix
##    *matrix generate, mass, stiffness
##    *matrix output, mass, stiffness, format=coordinate
##    *end step
##    **
##    **""")
                ##JOB
    mdb.Job(name='TorsionalFreq', model='Model-1', description='Freq', type=ANALYSIS, 
        atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
        memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
        explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
        modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
        scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1, 
        numGPUs=0)
    mdb.jobs['TorsionalFreq'].submit(consistencyChecking=OFF)
    mdb.jobs['TorsionalFreq'].waitForCompletion()
    mdb.saveAs(pathName='C:/temp/TorsionalFreq_FE.cae')
##    mdb.saveAs(pathName='C:/temp/TorsionalFreq_FE.cae')
##    odb = session.openOdb('TorsionalFreq.odb')
##    NF1=odb.steps['Step-1'].frames[1].frequency
##    NF2=odb.steps['Step-1'].frames[2].frequency
##    NF3=odb.steps['Step-1'].frames[3].frequency
##    ##mass_x_pos = mdb.models['Model-1'].rootAssembly.features['RP-1'].xValue
##    with open('C:/temp/TorsionalFreqresults.csv','a') as csvfile:
##        filewriter=csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
##        filewriter.writerow([NF1, NF2, NF3])
TorsionalBeam()
