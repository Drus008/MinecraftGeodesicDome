from colocarBloques import creacionDomo
import time

# 4 50 5 7 10

for d in range(4):
    t = time.time()
    print(str(d) +": " + str(time.time()))
    for r in range(1,50):
        print("  " + str(r)+": "+str(time.time()))
        for c in range(5):
            print("    "+str(c))
            for a in range(7):
                print("      "+str(a))
                for e in range(10):
                    creacionDomo(d,r,c,a,e, False)
                    print("        "+str(e))
    print(t-time.time())