import pylab

def p5():
    a = 1.0
    b = 2.0
    c = 4.0
    yVals = []
    xVals = range(-20, 20)
    for x in xVals:
        yVals.append(a*x**2 + b*x + c)
    yVals = 2*pylab.array(yVals)
    xVals = pylab.array(xVals)
    pylab.plot(xVals, yVals,'bo')
    try:        
        a, b, c, d = pylab.polyfit(xVals, yVals, 3)
        print a, b, c, d
        estYVals = a*(xVals**3) + b*xVals**2 + c*xVals + d
        pylab.plot(xVals, estYVals, label = 'Cubic fit')
        pylab.legend(loc = 'best')
        pylab.show()
    except:
        print 'fell to here'

p5()
