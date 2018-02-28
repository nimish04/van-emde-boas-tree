import datetime

from random import randint

import math

print('Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))

class VebNonode:
        
        def __init__ (self,u):

                self.u=u     # Maximum Universe size

                self.min=None 	 # to store minimum element among the child nodes

                self.max=None 	 # to store maximum element among the child nodes

                self.summary=None 	  # to store a summary of clusters 	

                self.cluster=[None]*int(math.sqrt(u))

class VebTree:
        
        def __init__(self,u):
                
                self.root=VebNonode(u)

        def High(self,u,x):
                # Returns a key according to which cluster is to be chosen 
                return x//(int(math.sqrt(u))) 

        def Low(self,u,x):
                # Returns a value which is to be inserted in corresponding cluster
                return  x%(int(math.sqrt(u)))

        def EmptyInsert(self,universe,x):
                
                universe.min=x

                universe.max=x

        def Insert(self,universe,x):
                if universe.u<=x or x<0:
                        
                        print ("ERROR! universe size exceeded.")
                        return

                if universe.min==None:
                        # Node has no child ie. Empty node 
                        self.EmptyInsert(universe,x)
                        # Filling the min,max value
                else:
                        if universe.min>x:
                                # Line 29-32
                                universe.min,x=x,universe.min
                                # Updating the minimum or maximum 
                        elif universe.max<x:

                                universe.max,x=x,universe.max
                        
                        if x !=universe.min and x!= universe.max:

                                # For other then leaf nodes

                                high=self.High(universe.u,x)

                                low=self.Low(universe.u,x)

                                if universe.cluster[high]==None:

                                        universe.cluster[high]=VebNonode(int(math.sqrt(universe.u))) # making cluster[high] as a VebNode

                                        self.EmptyInsert(universe.cluster[high],low)

                                        if universe.summary==None:

                                                universe.summary=VebNonode(int(math.sqrt(universe.u))) # making summary as a VebNode

                                        self.Insert(universe.summary,high)

                                        # to insert summary of clusters
                                else:

                                        self.Insert(universe.cluster[high],low)   # Recursion
                                
        def search(self,universe,x):

                if universe==None or universe.min==None:

                        return False

                if x==universe.min or x==universe.max:

                        return True

                elif x<universe.min or x>universe.max: 

                        return False
                else:
                        high=self.High(universe.u,x)

                        low=self.Low(universe.u,x)

                        return self.search(universe.cluster[high],low)

        def Minimum(self,universe):

                if universe==None or universe.max==None:

                        return None

                return universe.min

        def Maximum(self,universe):

                if universe==None or universe.min==None:

                        return None

                return universe.max

        def Index(self,u,x,y):    # to returns the original No.

                return int(y*int((math.sqrt(u)))+x)

        def Successor(self,universe,x):

                if universe==None or universe.min==None:

                        return None

                if universe.min>x:

                        return universe.min

                elif x<universe.max:

                        if universe.u==2:

                                if universe.max==1 and universe.min==0:

                                        return 1
                                else:
                                        return None 

                        high=self.High(universe.u,x)

                        low=self.Low(universe.u,x)

                        maxinsubcluster=None

                        if universe.cluster[high] != None:
                                
                                # line 77-84, To find successor in its own child-cluster

                                maxinsubcluster=self.Maximum(universe.cluster[high])

                        if  maxinsubcluster!=None and maxinsubcluster>low:

                                # to check whether Successor can be present in sub-cluster(low=new x)

                                new_suc=self.Successor(universe.cluster[high],low)

                                # recursion to find successor in sub-cluster

                                if new_suc != None:

                                        return self.Index(universe.u,new_suc,high)   #  To get the original no.
                                else:
                                        return None
                        else:
                                # line 85-94, To find successor of cluster
                                
                                suc_cluster=self.Successor(universe.summary,high)

                                if suc_cluster==None:

                                        if universe.max != None and x<universe.max:

                                                return universe.max

                                        else:

                                                return None
                                else:

                                        new_suc=self.Minimum(universe.cluster[suc_cluster])

                                        return self.Index(universe.u,new_suc,suc_cluster)
                else:

                        return None

        def Predecessor(self,universe,x):

                if universe==None or x>=universe.u or universe.min==None:

                        return None

                if universe.max<x:

                        return universe.max

                elif universe.min<x:

                        high=self.High(universe.u,x)

                        low=self.Low(universe.u,x)

                        if universe.u==2:

                                if universe.max==1 and universe.min==0:

                                        return 0
                                else:
                                        return None 

                        mininsubcluster=None

                        if universe.cluster[high]!=None:
                                
                                # line 107-114 to find predecessor in sub-cluster

                                mininsubcluster=self.Minimum(universe.cluster[high])

                        if mininsubcluster!=None and low>mininsubcluster:    # to check whether predecessor can be present in sub-cluster

                                new_pred=self.Predecessor(universe.cluster[high],low)   # recursion to find predecessor in sub-cluster

                                if new_pred != None:

                                        # if  predecessors present 

                                        return self.Index(universe.u,new_pred,high)

                                # to get the original no.

                                else:

                                        return None
                        else:
                                # line 115-124 To find the Predecessor of cluster cluster

                                pred_cluster=self.Predecessor(universe.summary,high)   # to search predecessor of sub-cluster in summary 

                                if pred_cluster==None:

                                        # if predecessor not found

                                        if universe.min!=None and x>universe.min:    # *In case: only min and max are present   

                                                return universe.min
                                        else:
                                                return None

                                        # otherwise no prede.
                                else:
                                        new_pred=self.Maximum(universe.cluster[pred_cluster])    # predecessor=maximum of the predecessor of cluster

                                        return self.Index(universe.u,new_pred,pred_cluster)    # to get the original value and return it
                else:
                        return None
        
        def Delete(self,universe,x):
                
                if universe==None or universe.min==None:
                        
                        return False
                
                if x<universe.min or x>universe.max:
                        
                        return False
                
                if x==universe.min:
                        
                        if x==universe.max:
                                
                                universe.min=None
                                
                                universe.max=None
                                
                                return -1
                        
                        if universe.summary==None:
                                
                                universe.min=universe.max
                                
                                return -2
                        else:
                                y=self.Successor(universe,x)

                                high=self.High(universe.u,y)

                                low=self.Low(universe.u,y)

                                universe.min=y

                                delvalue=self.Delete(universe.cluster[high],low)

                                if delvalue==-1:

                                        if universe.cluster[high].min == None:

                                                universe.cluster[high]=None

                                        if universe.summary.min==universe.summary.max:

                                                universe.summary=None
                                        else:
                                                return self.Delete(universe.summary,high)
                elif x==universe.max:

                        if x==universe.min:

                                universe.min=None

                                universe.max=None

                                return -1

                        if universe.summary==None:

                                universe.max=universe.min

                                return -2
                        else:
                                y=self.Predecessor(universe,x)

                                high=self.High(universe.u,y)

                                low=self.Low(universe.u,y)

                                universe.max=y

                                delvalue=self.Delete(universe.cluster[high],low)

                                if delvalue==-1:

                                        if universe.cluster[high].min == None:

                                                universe.cluster[high]=None

                                        if universe.summary.min==universe.summary.max:

                                                universe.summary=None
                                        else:
                                                return self.Delete(universe.summary,high)
                else:
                        high=self.High(universe.u,x)

                        low=self.Low(universe.u,x)

                        if universe.cluster[high]==None:

                                return False
                        
                        delvalue=self.Delete(universe.cluster[high],low)

                        if delvalue==-1:

                                if universe.cluster[high].min == None:

                                        universe.cluster[high]=None

                                if universe.summary.min==universe.summary.max:

                                        universe.summary=None
                                else:
                                        return self.Delete(universe.summary,high)

def logf(x):
        
        return(int(math.log(x,2)))
                
def integerGenerator(a,b,c,d):

        a='{0:08b}'.format(a)

        b='{0:08b}'.format(b)

        c='{0:08b}'.format(c)

        d='{0:08b}'.format(d)

        a+=b

        a+=c

        a+=d

        return(int(a,2))

k=0

print("enter the universe size:")

tempSize=int(input())

if tempSize==1 or tempSize==2:

        x=0
else:

        universeSize2=logf(logf(tempSize))+1

        x=pow(2,pow(2,universeSize2))
                        
        #print(x)

vt=VebTree(x)

while(k!=1):

        print()
        print()
        print("choose options for VEB Operations")

        print("1.Insertion in tree")

        print("2.Predecessor in tree")

        print("3.Successor in tree")

        print("4.Search in tree")

        print("5.Delete in tree")

        print("6.Application of tree")

        print("7.Exit")

        choose=int(input())

        if choose==1:

                
                print("Enter the no. of elements u want to enter")

                n=int(input())

                for j in range(n):

                        print("Enter element "+str(j))

                        num=int(input())

                        vt.Insert(vt.root,num)

        elif choose==2:

                print("Enter the element to find its predecessor")

                num=int(input())

                print("Predecessor is : "+str(vt.Predecessor(vt.root,num)))

        elif choose==3:

                print("Enter the element to find its sucessor")

                num=int(input())

                print("Sucessor is : " +str(vt.Successor(vt.root,num)))

        elif choose==5:

                print("Enter the element to delete")

                num=int(input())

                if vt.Delete(vt.root,num)==False:

                        print("Delete Unsucessful")

                else:
                        print("Delete Sucessful")

        elif choose==4:

                print("Enter the element to search")

                num=int(input())

                print("Number is there: "+str(vt.search(vt.root,num)))

        elif choose==6:

                universeSize=2**32

                vt=VebTree(universeSize)

                #creating a universe of size 2^32 according to the IV04 with max size of IP address To be 2^32-1

                #creating own ranges of IP addresses their corresponding ports through with data is to be sent

                # assigning 300 ports to our router

                # so no. of ranges will be 300 in count and no ranges are overlapping

                # storing only beginning of ranges to our van emde boas tree in the van emde boas tree

                #using dictionary adt to store port numbers of various ranges

                portN={}

                i=0

                while i<300:

                        j=randint(0,universeSize-1)

                        if vt.search(vt.root,j)==False:

                                vt.Insert(vt.root,j)

                                portN[j]=i

                                i+=1

                #inputing any ip address and assigning it a port through searching its nearest range beginning

                print("Enter no. of Ip Numbers For Data Transfer")

                n=int(input())

                for i in range(n):

                        print("Enter the IP Address for data transfer") 

                        a,b,c,d=input().split('.')

                        IPinteger=integerGenerator(int(a),int(b),int(c),int(d))

                        begOfIpRange=vt.Predecessor(vt.root,IPinteger)

                        if begOfIpRange!=False and vt.Successor(vt.root,IPinteger)!=None:

                                print("Connection Established data packets transfer through port No. "+str(portN[begOfIpRange]))
                        else:
                                print("Connection Unsucessful")
        elif choose==7:

                k=1

        else:
                print("Plz Enter correct value")
                

print('Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))

