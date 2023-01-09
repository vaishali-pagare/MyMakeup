from django.shortcuts import render,redirect
from Admin.models import Category,Product,UserInfo,PaymentMaster
from User.models import MyCart,OrderMaster,Address,MyOrder
from datetime import datetime


# Create your views here.

def homepage(request):
    #Fetch all records from Category table
    cats = Category.objects.all()
    prdts = Product.objects.all()
    return render(request,"homepage.html",{"cats":cats,"prdts":prdts})

def ViewDetails(request,id):
    cats = Category.objects.all()
    prdt = Product.objects.get(id=id)
    return render(request,"ViewDetails.html",{"prdt":prdt,"cats":cats})

def login(request):
    cats = Category.objects.all()
    return render(request,"login.html",{"cats":cats})
    
def register(request):
    if(request.method=="POST"):
        uname = request.POST["uname"]
        password = request.POST["password"]
        email = request.POST["email"]
        user = UserInfo()
        user.uname=uname
        user.password=password
        user.email=email
        user.save()
        return redirect(homepage)
        
def verify(request):
    if(request.method=="POST"):
        uname = request.POST["uname"]
        password = request.POST["password"]
        try:
            user = UserInfo.objects.get(uname=uname,password=password)
        except:
            return redirect(login)
        else:
                #Create the session
            request.session["uname"]=uname
            if("uname" in request.session):
                request.session["email"] = user.email
                return redirect(homepage)

def signout(request):
    request.session.clear()
    return redirect(homepage)

def ShowPrdt(request,id):
    #get method returns single object
    id = Category.objects.get(id=id)
    #filter method returns multiple object
    prdts = Product.objects.filter(cat = id)
    cats = Category.objects.all()
    return render(request,"homepage.html",{"cats":cats,"prdts":prdts})

def addToCart(request):
    if(request.method == "POST"):
        if("uname" in request.session):
            #Add to cart
            #User and Product
            prdtid = request.POST["prdtid"]
            user = request.session["uname"]
            qty = request.POST["qty"]
            prdt = Product.objects.get(id=prdtid)
            user = UserInfo.objects.get(uname = user)
            #check for duplicate entry
            try:
                cart = MyCart.objects.get(prdt=prdt,user=user)
            except:
                cart = MyCart()
                cart.user = user
                cart.prdt = prdt
                cart.qty = qty
                cart.save()
            else:
                pass
            return redirect(ShowAllCartItems)
        else:
            return redirect(login)

def ShowAllCartItems(request):
    uname = request.session["uname"]
    user = UserInfo.objects.get(uname = uname)
    cats = Category.objects.all()
    if(request.method == "GET"):       
        cartitems = MyCart.objects.filter(user=user)
        total = 0
        for item in cartitems:
            total += item.qty*item.prdt.price
        request.session["total"] = total
        return render(request,"ShowAllCartItems.html",{"items":cartitems,"cats":cats})
    else:
        id = request.POST["prdtid"]
        prdt = Product.objects.get(id=id)
        item = MyCart.objects.get(user=user,prdt=prdt)           
        qty = request.POST["qty"]
        item.qty = qty
        item.save() #Update
        return redirect(ShowAllCartItems)

def RemoveItem(request):
    uname = request.session["uname"]
    user = UserInfo.objects.get(uname = uname)
    id = request.POST["prdtid"]
    prdt = Product.objects.get(id=id)
    item = MyCart.objects.get(user=user,prdt=prdt)   
    item.delete()
    return redirect(ShowAllCartItems)

def addr(request):
    cats = Category.objects.all()
    if(request.method == "GET"):
        return render(request,"address.html",{"cats":cats})
    else:
        address = request.POST["address"]
        landmark = request.POST["landmark"]
        state = request.POST["state"]
        pin = request.POST["pin"]
        add = Address()
        add.address = address
        add.landmark = landmark
        add.state = state
        add.pin = pin
        add.save()
        return redirect(MakePayment)

def MakePayment(request):
    cats = Category.objects.all()
    if(request.method == "GET"):
        return render(request,"MakePayment.html",{"cats":cats})
    else:
        cardno = request.POST["cardno"]
        cvv = request.POST["cvv"]
        expiry = request.POST["expiry"]
        try:
            buyer = PaymentMaster.objects.get(cardno=cardno,cvv=cvv,expiry=expiry)
        except:
            return redirect(MakePayment)
        else:
            #Its a match
            owner = PaymentMaster.objects.get(cardno='111',cvv='111',expiry='12/2025')
            owner.balance += request.session["total"]
            buyer.balance -= request.session["total"]
            owner.save()
            buyer.save()
            #Delete all items from cart
            uname = request.session["uname"]
            user = UserInfo.objects.get(uname = uname)
            #order.dateOfOrder = datetime.now
            #Fetch all cart items for that user   
            items = MyCart.objects.filter(user=user)
            order = MyOrder()
            for item in items:
                uname =item.user.email
                pname = item.prdt.pname
                price = item.prdt.price
                description = item.prdt.description
                quantity = item.prdt.quantity
                order.pname=pname
                order.price=price
                order.description=description
                order.user=uname
                order.quantity=quantity       
                order.save()
                item.delete()
                return redirect(myorder)

def myorder(request):
    uname = request.session["uname"]
    user = UserInfo.objects.get(uname = uname)
    email = MyOrder.objects.filter(user=user.email)
    print(email)
    return render(request,"MyOrders.html",{"order":email})

