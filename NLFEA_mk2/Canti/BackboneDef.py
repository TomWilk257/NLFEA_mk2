# -*- coding: mbcs -*-
# Do not delete the following import lines
from abaqus import *
from abaqusConstants import *
import __main__
def BackboneDef():
    ##    from abaqus import *
    ##    from abaqusConstants import *
    ##    import __main__    
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
    import time
    ##    import numpy
    ##    ## Get inputs
    ##    freq = float(sys.argv[-1])
    ##    forcing = float(sys.argv[-2])
    freq=2*pi*20.734
    ## import geometry file
    openMdb('C:/temp/BeamFreq_FE.cae')
    del mdb.jobs['Frequency']
    del mdb.models['Model-1'].steps['Frequency']
    mdb.models['Model-1'].materials['Steel'].Damping(composite=0.05)  
    ## creating dynamic explicit step
    mdb.models['Model-1'].ExplicitDynamicsStep(name='Step-1', previous='Initial', 
        timePeriod=0.05, improvedDtMethod=ON)
    ##    session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
    ## setting disp as field output request
    mdb.models['Model-1'].FieldOutputRequest(name='F-Output-2', 
        createStepName='Step-1', variables=('U', ), numIntervals=int(100*freq/pi))
    ## creating amplitude - freq is circular freq
##    mdb.models['Model-1'].PeriodicAmplitude(name='Amp-1', timeSpan=STEP, 
##        frequency=freq, start=0.0, a_0=0.0, data=((0, 1.0), )) # apply freq here
        ## Free response step  
    mdb.models['Model-1'].ExplicitDynamicsStep(name='Step-2', previous='Step-1', 
        timePeriod=25*2*pi/freq, improvedDtMethod=ON)  
    #Import Forces
    instanceNodes = mdb.models['Model-1'].rootAssembly.instances['Beam-1'].nodes
    file=csv.reader(open('C:\\Users\\tw15036\\OneDrive - University of Bristol\\Documents\\Year 4\\GIP\\myFile2.csv','r'))
    n=[]
    for row in file:
        n.append(row)    
    for i in range(1,len(n)+1):      
        #nodeLabel = tuple(range(1,100))
        nodeLabel=[i]
        [cf11,cf22,cf33]=map(float,n[i-1])
        meshNodeObj = instanceNodes.sequenceFromLabels(nodeLabel)
        myRegion = regionToolset.Region(nodes=meshNodeObj)
        mdb.models['Model-1'].ConcentratedForce(name='Load-'+str(i), createStepName='Step-1', 
           region=myRegion, cf1=cf11, cf2=cf22, cf3=cf33, distributionType=UNIFORM, field='', 
           localCsys=None)
        mdb.models['Model-1'].loads['Load-'+str(i)].deactivate('Step-2')  
         ## run job
    mdb.Job(name='Job-Backbone', model='Model-1', description='', type=ANALYSIS, 
        atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
        memoryUnits=PERCENTAGE, explicitPrecision=DOUBLE, 
        nodalOutputPrecision=SINGLE, echoPrint=OFF, modelPrint=OFF, 
        contactPrint=OFF, historyPrint=OFF, userSubroutine='', scratch='', 
        resultsFormat=ODB, parallelizationMethodExplicit=DOMAIN, numDomains=1, 
        activateLoadBalancing=False, multiprocessingMode=DEFAULT, numCpus=1)
    mdb.jobs['Job-Backbone'].submit(consistencyChecking=OFF)
    session.mdbData.summary()
    ## Get tip displacement for
##    msg = mdb.jobs['Job-Time'].messages[-2].data
##    while mdb.jobs['Job-Time'].status == RUNNING:
##        if mdb.jobs['Job-Time'].messages[-2] != msg:
##            msg = mdb.jobs['Job-Time'].messages[-2]
##            print(msg)
BackboneDef()


