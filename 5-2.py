import random

def diceSim(numTrials):
  trialcount = 0
  for i in range(numTrials):
    c = []
    b = ['r','r','r','r','b','b','b','b']
    for a in range(3):
      ball = random.choice(b)
      b.remove(ball)
      c.append(ball)
      print c
    if c[0] == c[1] and c[0] == c[2]:
      trialcount += 1
  return float(trialcount)/numTrials
