import pylab

principal = 1000
interestRate = 0.05
years = 20
values = []
for i in range(years + 1):
  values.append(principal)
  principal += principal * interestRate
pylab.plot(range(years + 1),values, 'ro', linewidth = 60)
pylab.title('5% Growth, compounded annually', fontsize = 24)
pylab.xlabel('yrs of compounding')
pylab.ylabel('Value of principal')
pylab.show()
