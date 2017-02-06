import pylab


pylab.figure(1)
pylab.plot([1,2,3,4],[1,2,3,4])
pylab.figure(2)
pylab.plot([1,2,3,4],[5,6,7,8])
pylab.savefig('Figure-Eric')
pylab.figure(1)
pylab.plot([5,6,10,3])
pylab.savefig('Figure-Grimson')
