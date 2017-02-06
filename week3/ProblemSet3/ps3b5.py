# Problem Set 3: Simulating the Spread of Disease and Virus Population Dynamics 

import numpy
import random
import pylab

''' 
Begin helper code
'''

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''

#
# PROBLEM 2
#
class SimpleVirus(object):
    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def getMaxBirthProb(self):
        """
        Returns the max birth probability.
        """
        return self.maxBirthProb

    def getClearProb(self):
        """
        Returns the clear probability.
        """
        return self.clearProb

    def doesClear(self):
        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.getClearProb and otherwise returns
        False.
        """
        return random.random() <= self.getClearProb()
    
    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         
        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """
        reproduces = random.random() <= self.maxBirthProb * (1 - popDensity)
        if reproduces:
            return SimpleVirus(self.getMaxBirthProb(), self.getClearProb())
        else:
            raise NoChildException


class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.
        viruses: the list representing the virus population (a list of
        SimpleVirus instances)
        maxPop: the maximum virus population for this patient (an integer)
        """
        self.viruses = viruses  # list of SimpleVirus() instances
        self.maxPop = maxPop    # integer 

    def getViruses(self):
        """
        Returns the viruses in this Patient.
        """
        return self.viruses

    def getMaxPop(self):
        """
        Returns the max population.
        """
        return self.maxPop

    def getTotalPop(self):
        """
        Gets the size of the current total virus population. 
        returns: The total virus population (an integer)
        """
        return len(self.viruses)

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        
        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.                    
        returns: The total virus population at the end of the update (an
        integer)
        """
        self.viruses = [v for v in self.getViruses() if not v.doesClear()]
        popDensity = len(self.viruses) / float(self.maxPop)

        for v in self.viruses[:]: # cloned list
            try:
                self.viruses.append(v.reproduce(popDensity))
            except NoChildException:
                pass
        return self.getTotalPop()


#
# PROBLEM 3
#
def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
                          numTrials):
    """
    Run the simulation and plot the graph for problem 3 (no drugs are used,
    viruses do not have any drug resistance).    
    For each of numTrials trial, instantiates a patient, runs a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.
    numViruses: number of SimpleVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: Maximum clearance probability (a float between 0-1)
    numTrials: number of simulation runs to execute (an integer)
    Call simulationWithoutDrug(...) with the following parameters:
        -- numViruses = 100
        -- maxPop (maximum sustainable virus population) = 1000
        -- maxBirthProb (maximum reproduction probability for a virus particle) = 0.1
        -- clearProb (maximum clearance probability for a virus particle) = 0.05
    """
    trials = []
    timesteps = 300

    # run trials
    for __ in range(numTrials):
        populations = []
        # instantiate a Patient
        v = SimpleVirus(maxBirthProb, clearProb)
        viruses = [v for n in range(numViruses)]
        p = Patient(viruses, maxPop)
        # simulate virus clearance and reproduction
        for step in range(timesteps):
            populations.append(p.update())
        # add trial results
        trials.append(populations)

    # get averages per time step per trial
    step_averages = []
    for s in range(timesteps):
        this_step = []
        for t in trials:
            this_step.append(t[s])
        step_averages.append(sum(this_step) / float(numTrials))

    # plot results
    pylab.plot(step_averages, label='Total Virus Population Over Time')
    pylab.title('Simple Virus Reproduction Simulation')
    pylab.xlabel('Time Steps')
    pylab.ylabel('Average Virus Population')
    pylab.legend(loc='lower right')
    pylab.show()

#simulationWithoutDrug(100, 1000, 0.1, 0.05, 100)


#
# PROBLEM 4
#
class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """   

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.
        maxBirthProb: Maximum reproduction probability (a float between 0-1)       
        clearProb: Maximum clearance probability (a float between 0-1).
        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'srinol':False}, means that this virus
        particle is resistant to neither guttagonol nor srinol.
        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """
        SimpleVirus.__init__(self, maxBirthProb, clearProb)
        self.resistances = resistances
        self.mutProb = mutProb

    def getResistances(self):
        """
        Returns the resistances for this virus.
        """
        return self.resistances

    def getMutProb(self):
        """
        Returns the mutation probability for this virus.
        """
        return self.mutProb

    def isResistantTo(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in TreatedPatient to determine how many virus
        particles have resistance to a drug.       
        drug: The drug (a string)
        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        return self.resistances.get(drug, False)

    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the TreatedPatient class.
        A virus particle will only reproduce if it is resistant to ALL the drugs
        in the activeDrugs list. For example, if there are 2 drugs in the
        activeDrugs list, and the virus particle is resistant to 1 or no drugs,
        then it will NOT reproduce.
        Hence, if the virus is resistant to all drugs
        in activeDrugs, then the virus reproduces with probability:      
        self.maxBirthProb * (1 - popDensity).                       
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb, clearProb, and mutProb values as its parent).
        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.       
        For example, if a virus particle is resistant to guttagonol but not
        srinol, and self.mutProb is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90%
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        srinol and a 90% chance that the offspring will not be resistant to
        srinol.
        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population       
        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings).
        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """
        resistant = True
        # check resistances
        for drug in activeDrugs:
            if not self.isResistantTo(drug):
                resistant = False
                break
        if resistant:
            reproduces = random.random() <= self.maxBirthProb * (1 - popDensity)
            if reproduces:
                # mutate resistances
                resistances = {k:v if random.random() > self.mutProb else
                               not v for k, v in self.resistances.items()}
                # return offspring
                return ResistantVirus(self.getMaxBirthProb(), self.getClearProb(),
                                      resistances, self.mutProb)
        raise NoChildException


class TreatedPatient(Patient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).              
        viruses: The list representing the virus population (a list of
        virus instances)
        maxPop: The  maximum virus population for this patient (an integer)
        """
        Patient.__init__(self, viruses, maxPop)
        self.prescriptions = []

    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.
        newDrug: The name of the drug to administer to the patient (a string).
        postcondition: The list of drugs being administered to a patient is updated
        """
        if newDrug not in self.prescriptions:
            self.prescriptions.append(newDrug)

    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.
        returns: The list of drug names (strings) being administered to this
        patient.
        """
        return self.prescriptions

    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.       
        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])
        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        return len([v for v in self.viruses if all(v.isResistantTo(d) for d in drugResist)])

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:
        - Determine whether each virus particle survives and update the list of
          virus particles accordingly
        - The current population density is calculated. This population density
          value is used until the next call to update().
        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.
          The list of drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.
        - Reproduction probability:
          self.maxBirthProb * (1 - popDensity)
        returns: The total virus population at the end of the update (an
        integer)
        """
        # from Patient class:
        self.viruses = [v for v in self.getViruses() if not v.doesClear()]
        popDensity = len(self.viruses) / float(self.maxPop)

        for v in self.viruses[:]: # cloned list
            try:
                self.viruses.append(v.reproduce(popDensity, self.getPrescriptions())) # getPrescriptions only additional parameter
            except NoChildException:
                pass
        return self.getTotalPop()


#
# PROBLEM 5
#
def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb, numTrials):
    """
    Runs simulations and plots graphs for problem 5.
    For each of numTrials trials, instantiates a patient, runs a simulation for
    150 timesteps, adds guttagonol, and runs the simulation for an additional
    150 timesteps.  At the end plots the average virus population size
    (for both the total virus population and the guttagonol-resistant virus
    population) as a function of time.
    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: maximum clearance probability (a float between 0-1)
    resistances: a dictionary of drugs that each ResistantVirus is resistant to
                 (e.g., {'guttagonol': False})
    mutProb: mutation probability for each ResistantVirus particle
             (a float between 0-1). 
    numTrials: number of simulation runs to execute (an integer)
    
    """
    timesteps = 450
    treatment = 300
    totTrialPops = [] # total populations
    resTrialPops = [] # resistant populations

    for __ in range(numTrials):
        totPop = []
        resPop = []
        # instantiate a TreatedPatient
        v = ResistantVirus(maxBirthProb, clearProb, resistances, mutProb)
        viruses = [v for n in range(numViruses)]
        p = TreatedPatient(viruses, maxPop)
        # simulate virus clearance and reproduction
        for step in range(timesteps):
            if step == treatment:
                # introduce a new prescription
                p.addPrescription(random.choice([r for r in resistances.keys()]))
            p.update()
            totPop.append(p.getTotalPop())
            resPop.append(p.getResistPop([r for r in resistances.keys()]))
        totTrialPops.append(totPop)
        resTrialPops.append(resPop)

    # get total population averages per time step per trial
    tot_averages = []
    for s in range(timesteps):
        this_step = []
        for t in totTrialPops:
            this_step.append(t[s])
        tot_averages.append(sum(this_step) / float(numTrials))

    # get resistant population averages per time step per trial
    res_averages = []
    for s in range(timesteps):
        this_step = []
        for t in resTrialPops:
            this_step.append(t[s])
        res_averages.append(sum(this_step) / float(numTrials))
    
    curedcount = 0
    # percentage cured
    for x in totTrialPops:
        if len(x) <= 50:
            curedcount += 1
    #curedRatio = float(curedcount) / len(totTrialPops)
    print curedcount
    # plot results
    '''
    pylab.plot(tot_averages, label='Total Virus Pop.')
    pylab.plot(res_averages, label='Resistant Virus Pop.')
    pylab.title('Simulation of Resistant Virus in Treated Patient')
    pylab.xlabel('Time Steps')
    pylab.ylabel('Average Virus Population')
    pylab.legend(loc='upper right')
    

    pylab.hist(totTrialPops, bins = 20)
    pylab.xlabel("Total Trial Population") 
    pylab.ylabel("Number of trials")
    pylab.show()
    '''

def simulationDelayedTreatment(numTrials):
    """
    Runs simulations and make histograms for problem 1.

    Runs numTrials simulations to show the relationship between delayed
    treatment and patient outcome using a histogram.

    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).

    numTrials: number of simulation runs to execute (an integer)
    """
    results = []
    for d in delays:
        #Uncomment these to use the red module
        #\/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/
#        r = red.update(num_viruses, max_pop, max_birth_prob, clear_prob, 
#                       resistances, mut_prob, d + final_steps, 
#                       [(d, 'guttagonol')], numTrials, 4)
#        results.append(r)
        #/\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\
        #Uncomment these out to use the red module
        
        #Comment these out to use the red module
        #\/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/
        partial_result = []
        for t in range(numTrials):
            viruses = [ResistantVirus(max_birth_prob, clear_prob, 
                                      resistances, mut_prob) 
                       for _ in range(num_viruses)]
            tp = TreatedPatient(viruses, max_pop)
            for step in range(d + final_steps):
                if step == d:
                    tp.addPrescription('guttagonol')
                tp.update()
            print('Delay: ' + str(d) + '  Trial: ' + str(t))
            partial_result.append(tp.getTotalPop())
        results.append(partial_result)
        #/\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\
        #Comment these out to use the red module
    
    if len(delays) == 4:
        subplot = 221
    else:
        subplot = 111
    pylab.figure(simulationDelayedTreatment.figure)
    simulationDelayedTreatment.figure += 1
    for d, r in zip(delays, results):
        pylab.subplot(subplot)
        subplot += 1
        pylab.hist(r, bins=max_pop/remission, range=(0, max_pop))
        pylab.title(str(d) + ' Steps Delayed Treatment')
        pylab.xlabel('Final Virus Population')
        pylab.ylabel('Number of Trials')

num_viruses = 100
max_pop = 1000
max_birth_prob = 0.1
clear_prob = 0.05
resistances = {'guttagonol': False}
mut_prob = 0.005
delays = [300, 150, 75, 0]
final_steps = 150
trials = 100
remission = 50
simulationDelayedTreatment.figure = 0

#start_time = time.time()

#Q1, Q2, Q3
simulationDelayedTreatment(trials)

#Q4
#delays = [150]
#num_viruses = 10
#simulationDelayedTreatment(trials)
#num_viruses = 20
#simulationDelayedTreatment(trials)
#num_viruses = 30
#simulationDelayedTreatment(trials)
#num_viruses = 40
#simulationDelayedTreatment(trials)
#num_viruses = 100
#
#max_pop *= 2
#simulationDelayedTreatment(trials)
#max_pop /= 2
#
#max_birth_prob *= 2
#simulationDelayedTreatment(trials)
#max_birth_prob /= 2
#
#clear_prob *= 2
#simulationDelayedTreatment(trials)
#clear_prob /= 2
#
#resistances['guttagonol'] = True
#simulationDelayedTreatment(trials)
#delays = [300, 150, 75, 0]

#print(time.time() - start_time)
pylab.show()

#
# PROBLEM 2
#
def simulationTwoDrugsDelayedTreatment(numTrials):
    """
    Runs simulations and make histograms for problem 2.

    Runs numTrials simulations to show the relationship between administration
    of multiple drugs and patient outcome.

    Histograms of final total virus populations are displayed for lag times of
    300, 150, 75, 0 timesteps between adding drugs (followed by an additional
    150 timesteps of simulation).

    numTrials: number of simulation runs to execute (an integer)
    """
    results = []
    for l in lags:
        #Uncomment these to use the red module
        #\/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/
#        r = red.update(num_viruses, max_pop, max_birth_prob, clear_prob, 
#                       resistances, mut_prob, initial_steps + l + final_steps, 
#                       [(initial_steps, 'guttagonol') , 
#                        (initial_steps + l, 'grimpex')], numTrials, 4)
#        results.append(r)
        #/\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\
        #Uncomment these out to use the red module
        
        #Comment these out to use the red module
        #\/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/
        partial_result = []
        for t in range(numTrials):
            viruses = [ResistantVirus(max_birth_prob, clear_prob, 
                                      resistances, mut_prob)] * num_viruses
            tp = TreatedPatient(viruses, max_pop)
            for step in range(initial_steps + l + final_steps):
                if step == initial_steps:
                    tp.addPrescription('guttagonol')
                if step == initial_steps + l:
                    tp.addPrescription('grimpex')
                tp.update()
            print('Lag: ' + str(l) + '  Trial: ' + str(t))
            partial_result.append(tp.getTotalPop())
        results.append(partial_result)
        #/\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\
        #Comment these out to use the red module
    
    subplot = 221
    pylab.figure(simulationTwoDrugsDelayedTreatment.figure)
    simulationTwoDrugsDelayedTreatment.figure += 1
    for d, r in zip(lags, results):
        pylab.subplot(subplot)
        subplot += 1
        pylab.hist(r, bins=max_pop/remission, range=(0, max_pop))
        pylab.title(str(d) + ' Steps Delayed Treatment')
        pylab.xlabel('Final Virus Population')
        pylab.ylabel('Number of Trials')
    return results

num_viruses = 100
max_pop = 1000
max_birth_prob = 0.1
clear_prob = 0.05
resistances = {'guttagonol': False, 'grimpex': False}
mut_prob = 0.005
initial_steps = 150
lags = [300, 150, 75, 0]
final_steps = 150
remission = 50
trials = 100
simulationTwoDrugsDelayedTreatment.figure = 0

#start_time = time.time()

#Q1, Q2, Q4
simulationTwoDrugsDelayedTreatment(trials)

#Q3
#mut_prob *= 2
#simulationTwoDrugsDelayedTreatment(trials)
#mut_prob /= 2

#Q5 This won't give you the correct answer, there is a chance the 
#answer marked as correct in the Problem Set isn't in fact correct.
#results = simulationTwoDrugsDelayedTreatment(trials)
#for r in results:
#    temp = pylab.array(r)
#    print(temp.mean(), temp.var(), temp.std())

#print(time.time() - start_time)
pylab.show()
