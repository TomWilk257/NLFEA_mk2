# -*- coding: mbcs -*-
# Do not delete the following import lines
from abaqus import *
from abaqusConstants import *
import __main__
def TorsMerging():
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
    mass_x_pos = float(sys.argv[-1])
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
    a = mdb.models['Model-1'].rootAssembly
    a = mdb.models['Model-1'].rootAssembly
    ## Merging Part 1 and 2 to create part 3
    a.InstanceFromBooleanMerge(name='Part-3', instances=(a.instances['Part-1-1'], 
        a.instances['Part-2-1'], ), keepIntersections=ON, 
        originalInstances=SUPPRESS, domain=GEOMETRY)
    p1 = mdb.models['Model-1'].parts['Part-1']
    ## Material definition
    mdb.models['Model-1'].Material(name='Material-1')
    mdb.models['Model-1'].materials['Material-1'].Density(table=((7850.0, ), ))
    mdb.models['Model-1'].materials['Material-1'].Elastic(table=((210000000000.0, 
        0.3), ))
    mdb.models['Model-1'].HomogeneousSolidSection(name='Section-1', 
        material='Material-1', thickness=None)
    p1 = mdb.models['Model-1'].parts['Part-3']
    p = mdb.models['Model-1'].parts['Part-3']
    c = p.cells
        # Section assignment
    cells = c
    region = p.Set(cells=cells, name='Set-1')
    p = mdb.models['Model-1'].parts['Part-3']
    p.SectionAssignment(region=region, sectionName='Section-1', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)
    p = mdb.models['Model-1'].parts['Part-3']
    # Meshing 
    p.seedPart(size=0.005, deviationFactor=0.1, minSizeFactor=0.1)
    elemType1 = mesh.ElemType(elemCode=C3D20, elemLibrary=STANDARD)
    elemType2 = mesh.ElemType(elemCode=C3D15, elemLibrary=STANDARD)
    elemType3 = mesh.ElemType(elemCode=C3D10, elemLibrary=STANDARD)
    p = mdb.models['Model-1'].parts['Part-3']
    c = p.cells
    cells = c
    pickedRegions =(cells, )
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
        elemType3))
    p = mdb.models['Model-1'].parts['Part-3']
    p.generateMesh()
    a = mdb.models['Model-1'].rootAssembly
    a.regenerate()
    a = mdb.models['Model-1'].rootAssembly
    ## BCs
    a = mdb.models['Model-1'].rootAssembly
    f1 = a.instances['Part-3-1'].faces
    fixed_ptx=0.01
    fixed_pty=0
    fixed_ptz=0
    fixed_pt=(fixed_ptx,fixed_pty,fixed_ptz)
    fixed_end_face = f1.findAt((fixed_pt,))
    myRegion = regionToolset.Region(faces=fixed_end_face)
    mdb.models['Model-1'].EncastreBC(name='Clamped-1', createStepName='Initial', 
        region=myRegion, localCsys=None)
    f1 = a.instances['Part-3-1'].faces
    fixed_ptx=-0.01
    fixed_pty=0
    fixed_ptz=0
    fixed_pt=(fixed_ptx,fixed_pty,fixed_ptz)
    fixed_end_face = f1.findAt((fixed_pt,))
    myRegion = regionToolset.Region(faces=fixed_end_face)
    mdb.models['Model-1'].EncastreBC(name='Clamped-2', createStepName='Initial', 
        region=myRegion, localCsys=None)
    ## Inertial ref points
    a = mdb.models['Model-1'].rootAssembly
    a.ReferencePoint(point=(mass_x_pos, 0.005, 0.325))
    a = mdb.models['Model-1'].rootAssembly
    a.ReferencePoint(point=(0.0, 0.001, 0.645))
    a = mdb.models['Model-1'].rootAssembly
    a.ReferencePoint(point=(0.0, 0.005, 0.335))
    a = mdb.models['Model-1'].rootAssembly
    a.ReferencePoint(point=(0.195, 0.005, 0.335))
    a = mdb.models['Model-1'].rootAssembly
    a.ReferencePoint(point=(-0.195, 0.005, 0.335))
    a = mdb.models['Model-1'].rootAssembly
    r1 = a.referencePoints
        # Acc inertial bits
    refPoints1=(r1[12], r1[13], r1[14], r1[15], )
    region=a.Set(referencePoints=refPoints1, name='Set-2')
    mdb.models['Model-1'].rootAssembly.engineeringFeatures.PointMassInertia(
        name='Inertia-1', region=region, mass=0.006, alpha=0.0, composite=0.0)
    a = mdb.models['Model-1'].rootAssembly
    r1 = a.referencePoints
    ## Point mass (big)
    refPoints1=(r1[11], )
    region=a.Set(referencePoints=refPoints1, name='Set-3')
    mdb.models['Model-1'].rootAssembly.engineeringFeatures.PointMassInertia(
        name='Inertia-2', region=region, mass=0.6378, alpha=0.0, composite=0.0)
    # Tieing inertial els
    a = mdb.models['Model-1'].rootAssembly
    s1 = a.instances['Part-3-1'].faces
    side1Faces1 = s1.findAt(([0, 0.005, 0.325],))
    region1=a.Surface(side1Faces=side1Faces1, name='m_Surf-1')
    a = mdb.models['Model-1'].rootAssembly
    r1 = a.referencePoints
    refPoints1=(r1[11], r1[13], r1[14], r1[15], )
    region2=a.Set(referencePoints=refPoints1, name='s_Set-4')
    mdb.models['Model-1'].Tie(name='Constraint-1', master=region1, slave=region2, 
        positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, 
        thickness=ON)
    a = mdb.models['Model-1'].rootAssembly
    s1 = a.instances['Part-3-1'].faces
    side1Faces1 = s1.findAt(([0, 0.001, 0.625],))
    region1=a.Surface(side1Faces=side1Faces1, name='m_Surf-2')
    a = mdb.models['Model-1'].rootAssembly
    r1 = a.referencePoints
    refPoints1=(r1[12], )
    region2=a.Set(referencePoints=refPoints1, name='s_Set-5')
    mdb.models['Model-1'].Tie(name='Constraint-2', master=region1, slave=region2, 
        positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, 
        thickness=ON)
    ## Step definition
    mdb.models['Model-1'].FrequencyStep(name='Step-1', previous='Initial', 
        numEigen=10)
    mdb.models['Model-1'].steps['Step-1'].setValues(simLinearDynamics=OFF, 
        normalization=MASS, numEigen=10, vectors=18, maxIterations=30, 
        eigensolver=SUBSPACE, acousticCoupling=AC_OFF)
    ## Export matrix
##    mdb.models['Model-1'].keywordBlock.synchVersions(storeNodesAndElements=False)
##    mdb.models['Model-1'].keywordBlock.replace(51, """
##    ** ----------------------------------------------------------------
##    **
##    * Step, name=exportmatrix
##    *matrix generate, mass, stiffness
##    *matrix output, mass, stiffness, format=coordinate
##    *end step
##    **
##    **""")
    ## Job
    mdb.Job(name='Job-2', model='Model-1', description='', type=ANALYSIS, 
        atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
        memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
        explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
        modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
        scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1, 
        numGPUs=0)
    mdb.jobs['Job-2'].submit(consistencyChecking=OFF)
    mdb.jobs['Job-2'].waitForCompletion()
    odb = session.openOdb('Job-2.odb')
    NF1=odb.steps['Step-1'].frames[1].frequency
    NF2=odb.steps['Step-1'].frames[2].frequency
    NF3=odb.steps['Step-1'].frames[3].frequency
    ##mass_x_pos = mdb.models['Model-1'].rootAssembly.features['RP-1'].xValue
    with open('C:/temp/TorsVeering.csv','a') as csvfile:
        filewriter=csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow([NF1, NF2, NF3])
TorsMerging()
