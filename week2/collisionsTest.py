# 1000 buckets, 50 insertions

insertionsNum = 50
bucketNum = 1000
collisionP = 1

for i in range(1, insertionsNum + 1):
  collisionP *= ( (bucketNum-i) / i )

collisionP = (1 - collisionP)

print collisionP
