from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import AddVendors, AddProducts, ManualComboTemp
from django.db.models import Q
import random
from gridfokuzapp.decorators import Admin_only


# Create your views here.

# ---------------------------General section---------------------------

def Index(request):
    return render(request, "Index.html")

def Register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirm_password')

        if password == confirmpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already Taken")
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email Id is already Exists...")
            else:
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()
                messages.info(request, "User Successfuly created...")
                return redirect('Usrlogin')
        else:
            messages.info(request, "Both password is not matching")
            return redirect('Register')
    return render(request, 'Register.html')

def Usrlogin(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            messages.info(request, "Username or Password Is Wrong...")
            return redirect('Usrlogin')
    return render(request, 'Usrlogin.html')

def logout(request):
    auth.logout(request)
    return redirect('Usrlogin')

@Admin_only
def home(request):
    name = request.user
    product = AddProducts.objects.all()
    vendors = AddVendors.objects.all()
    price = [p.Total_GF_price for p in product]
    limit = max(price)
    return render(request, "home.html", {"name":name,
                                         "product":product,
                                         "vendors":vendors,
                                         "limit":limit})

# ---------------------------Addvendors section---------------------------

def addventors(request):
    if request.method == "POST":
        vendorname = request.POST.get("vendorname")
        vendor = AddVendors(vendorname=vendorname)
        vendor.save()
        messages.info(request, "Vendor is added successfuly...")
        return redirect("addventors")
    return render(request, "addventors.html")

# ---------------------------Product section---------------------------

def addproducts(request):
    vendor = AddVendors.objects.all()
    if request.method == "POST":
        SKU = request.POST.get("SKU")
        Vendor = request.POST.get("Vendor")
        
        vendor_name = AddVendors.objects.get(vendorname=Vendor)
        
        Category = request.POST.get("Category")
        Sub_category = request.POST.get("Sub_category")
        Product_Name = request.POST.get("Product_Name")
        MRP = request.POST.get("MRP")
        Vendor_Price = request.POST.get("Vendor_Price")
        Transport1 = request.POST.get("Transport1")
        Transport2 = request.POST.get("Transport2")
        Branding = request.POST.get("Branding")
        Packing = request.POST.get("Packing")
        Profit_in_precentage = request.POST.get("Profit_in_precentage")
        Profit_amount = request.POST.get("Profit_amount")
        GF_Price = request.POST.get("GF_Price")
        Tax_in_precentage = request.POST.get("Tax_in_precentage")
        Tax_amount = request.POST.get("Tax_amount")
        Total_GF_price = request.POST.get("Total_GF_price")
        product_image = request.FILES["product_image"]
        
        product = AddProducts(SKU=SKU,
                              Vendor=vendor_name,
                              Category=Category,
                              Sub_category=Sub_category,
                              Product_Name=Product_Name,
                              MRP=MRP,
                              Vendor_Price=Vendor_Price,
                              Transport1=Transport1,
                              Transport2=Transport2,
                              Branding=Branding,
                              Packing=Packing,
                              Profit_in_precentage=Profit_in_precentage,
                              Profit_amount=Profit_amount,
                              GF_Price=GF_Price,
                              Tax_in_precentage=Tax_in_precentage,
                              Tax_amount=Tax_amount,
                              Total_GF_price=Total_GF_price,
                              product_image=product_image)
        product.save()
        messages.info(request, "{} added successfuly...".format(Product_Name))
        return redirect("addproducts")
    return render(request, "addproducts.html",{"vendor":vendor})

def product_detail(request,id):
    product = AddProducts.objects.get(id=id)
    return render(request, "product_detail.html",{"product":product})

def update_product(request,id):
    vendor = AddVendors.objects.all()
    product = AddProducts.objects.get(id=id)
    if request.method == "POST":
        SKU = request.POST.get("SKU")
        Vendor = request.POST.get("Vendor")
        vendor_name = AddVendors.objects.get(vendorname=Vendor)
        Category = request.POST.get("Category")
        Sub_category = request.POST.get("Sub_category")
        Product_Name = request.POST.get("Product_Name")
        MRP = request.POST.get("MRP")
        Vendor_Price = request.POST.get("Vendor_Price")
        Transport1 = request.POST.get("Transport1")
        Transport2 = request.POST.get("Transport2")
        Branding = request.POST.get("Branding")
        Packing = request.POST.get("Packing")
        Profit_in_precentage = request.POST.get("Profit_in_precentage")
        Profit_amount = request.POST.get("Profit_amount")
        GF_Price = request.POST.get("GF_Price")
        Tax_in_precentage = request.POST.get("Tax_in_precentage")
        Tax_amount = request.POST.get("Tax_amount")
        Total_GF_price = request.POST.get("Total_GF_price")
        product_image = request.FILES["product_image"]
        
        product.SKU = SKU
        product.Category = Category
        product.Vendor = vendor_name
        product.Sub_category = Sub_category
        product.Product_Name = Product_Name
        product.MRP = MRP
        product.Vendor_Price = Vendor_Price
        product.Transport1 = Transport1
        product.Transport2 = Transport2
        product.Branding = Branding
        product.Packing = Packing
        product.Profit_in_precentage = Profit_in_precentage
        product.Profit_amount = Profit_amount
        product.GF_Price = GF_Price
        product.Tax_in_precentage = Tax_in_precentage
        product.Tax_amount = Tax_amount
        product.Total_GF_price = Total_GF_price
        product.product_image = product_image
        product.save()
        messages.info(request, "{} Updated Successfuly...".format(Product_Name))
        return redirect("home")
    return render(request, "update_product.html",{"product":product,
                                                  "vendor":vendor})

def delete_product(request,id):
    product = AddProducts.objects.get(id=id)
    return render(request, "delete_product.html",{"product":product})

def product_list(request):
    query = request.GET.get('search')
    name = request.user
    product = AddProducts.objects.all()
    vendors = AddVendors.objects.all()
    price = [p.Total_GF_price for p in product]
    limit = max(price)
    if query:
        product = AddProducts.objects.filter(Q(Product_Name__icontains=query))
        return render(request, "home.html",{"name":name,
                                         "product":product,
                                         "vendors":vendors,
                                         "limit":limit})
    else:
        product = AddProducts.objects.all()
        return render(request, "home.html",{"name":name,
                                         "product":product,
                                         "vendors":vendors,
                                         "limit":limit})

# ---------------------------Filtering section---------------------------

def sort_products(request):
    if request.method == "POST":
        all_product = AddProducts.objects.all()
        sorting = request.POST.get('sorting')
        selected_vendors = request.POST.getlist('vendor')
        limit = request.POST.get("limit")
        category = request.POST.getlist("category")
        sub_category = request.POST.getlist("sub_category")
        # print(selected_vendors)
        # print(category)
        # print(sub_category)
        products = []
        product = []
        cat_list = []
        final = []
        item_price_sort = []
        acending_items = []
        if selected_vendors and category and sub_category:
            for i in selected_vendors:
                vendor = AddVendors.objects.get(vendorname=i)
                pro = AddProducts.objects.filter(Vendor=vendor)
                for j in pro:
                    products.append(j)
            for lmt in products:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit):
                    product.append(item)
            for cat in product:
                item_cat = AddProducts.objects.get(id=cat.id)
                for k in category:
                    if item_cat.Category == k:
                        cat_list.append(cat)
            for sub_cat in cat_list:
                sub_item = AddProducts.objects.get(id=sub_cat.id)
                for q in sub_category:
                    if sub_item.Sub_category == q:
                        final.append(sub_item)
            if sorting != "null":
                if sorting == "acending":
                    for i in final:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort()
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "sorted_products.html",{"product":acending_items})
                elif sorting == "desending":
                    for i in final:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "sorted_products.html",{"product":acending_items})
                else:
                    return HttpResponse("Sorting Making Problem...")
            return render(request, "sorted_products.html",{"product":final})
        
        elif selected_vendors and category:
            for i in selected_vendors:
                vendor = AddVendors.objects.get(vendorname=i)
                pro = AddProducts.objects.filter(Vendor=vendor)
                for j in pro:
                    products.append(j)
            for lmt in products:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit):
                    product.append(item)
            for cat in product:
                item_cat = AddProducts.objects.get(id=cat.id)
                for i in category:
                    if item_cat.Category == i:
                        cat_list.append(cat)
            if sorting != "null":
                if sorting == "acending":
                    for i in cat_list:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort()
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "sorted_products.html",{"product":acending_items})
                elif sorting == "desending":
                    for i in cat_list:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "sorted_products.html",{"product":acending_items})
                else:
                    return HttpResponse("Sorting Making Problem...")
            return render(request, "sorted_products.html",{"product":cat_list})   
         
        elif selected_vendors and sub_category:
            for i in selected_vendors:
                vendor = AddVendors.objects.get(vendorname=i)
                pro = AddProducts.objects.filter(Vendor=vendor)
                for j in pro:
                    products.append(j)
            for lmt in products:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit):
                    product.append(item)
            for sub_cat in product:
                sub_item = AddProducts.objects.get(id=sub_cat.id)
                for i in sub_category:
                    if sub_item.Sub_category == i:
                        final.append(sub_item)
            if sorting != "null":
                if sorting == "acending":
                    for i in final:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort()
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "sorted_products.html",{"product":acending_items})
                elif sorting == "desending":
                    for i in final:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "sorted_products.html",{"product":acending_items})
                else:
                    return HttpResponse("Sorting Making Problem...")
            return render(request, "sorted_products.html",{"product":final})    
        
        elif category and sub_category:
            for lmt in all_product:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit):
                    product.append(item)
            for cat in product:
                item_cat = AddProducts.objects.get(id=cat.id)
                for k in category:
                    if item_cat.Category == k:
                        cat_list.append(cat)
            for sub_cat in cat_list:
                sub_item = AddProducts.objects.get(id=sub_cat.id)
                for q in sub_category:
                    if sub_item.Sub_category == q:
                        final.append(sub_item)
            if sorting != "null":
                if sorting == "acending":
                    for i in final:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort()
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "sorted_products.html",{"product":acending_items})
                elif sorting == "desending":
                    for i in final:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "sorted_products.html",{"product":acending_items})
                else:
                    return HttpResponse("Sorting Making Problem...")
            return render(request, "sorted_products.html",{"product":final})
        
        elif category:
            for lmt in all_product:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit):
                    product.append(item)
            for cat in product:
                item_cat = AddProducts.objects.get(id=cat.id)
                for i in category:
                    if item_cat.Category == i:
                        cat_list.append(cat)
            if sorting != "null":
                if sorting == "acending":
                    for i in cat_list:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort()
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "sorted_products.html",{"product":acending_items})
                elif sorting == "desending":
                    for i in cat_list:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "sorted_products.html",{"product":acending_items})
                else:
                    return HttpResponse("Sorting Making Problem...")
            return render(request, "sorted_products.html",{"product":cat_list})
        
        elif sub_category:
            for lmt in all_product:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit):
                    product.append(item)
            for sub_cat in product:
                sub_item = AddProducts.objects.get(id=sub_cat.id)
                for i in sub_category:
                    if sub_item.Sub_category == i:
                        final.append(sub_item)
            if sorting != "null":
                if sorting == "acending":
                    for i in final:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort()
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "sorted_products.html",{"product":acending_items})
                elif sorting == "desending":
                    for i in final:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "sorted_products.html",{"product":acending_items})
                else:
                    return HttpResponse("Sorting Making Problem...")
            return render(request, "sorted_products.html",{"product":final})
        
        elif selected_vendors:
            for i in selected_vendors:
                vendor = AddVendors.objects.get(vendorname=i)
                pro = AddProducts.objects.filter(Vendor=vendor)
                for j in pro:
                    products.append(j)
            for lmt in products:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit):
                    product.append(item)
            if sorting != "null":
                if sorting == "acending":
                    for i in product:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort()
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "sorted_products.html",{"product":acending_items})
                elif sorting == "desending":
                    for i in product:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "sorted_products.html",{"product":acending_items})
                else:
                    return HttpResponse("Sorting Making Problem...")
            return render(request, "sorted_products.html",{"product":product})
        
        elif limit:
            for lmt in all_product:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit):
                    product.append(item)
                    # print("limit pro list :",product)
            if sorting != "null":
                if sorting == "acending":
                    for i in product:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort()
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "sorted_products.html",{"product":acending_items})
                elif sorting == "desending":
                    for i in product:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "sorted_products.html",{"product":acending_items})
                else:
                    return HttpResponse("Sorting Making Problem...")
            return render(request, "sorted_products.html",{"product":product})
        else:
            messages.info(request, "Something went wrong...")
    return redirect("home")

# ---------------------------Combo section---------------------------

def Combo(request):
    name = request.user
    product = AddProducts.objects.all()
    vendors = AddVendors.objects.all()
    price = [p.Total_GF_price for p in product]
    limit = max(price)
    # combo_product = ManualComboTemp.objects.all()
    combo_product = ManualComboTemp.objects.filter(usr=request.user)
    product_price = []
    for i in combo_product:
        combo_prod = AddProducts.objects.get(id=i.product.id)
        product_price.append(combo_prod.Total_GF_price)
    combo_price = sum(product_price)
    return render(request, "ComboSection.html",{"name":name,
                                                "product":product,
                                                "vendors":vendors,
                                                "limit":limit,
                                                "combo_product":combo_product,
                                                "combo_price":combo_price})

def HomeSortedManualCombo(request):
    combo = []
    combo_price = []
    if request.method == "POST":
        manualcombolist = request.POST.getlist("manualcombolist")
        # print(manualcombolist)
        for i in manualcombolist:
            id = int(i)
            prod = AddProducts.objects.get(id=id)
            combo.append(prod)
            combo_price.append(prod.Total_GF_price)
        total_combo_price = sum(combo_price)
        return render(request, "combo.html", {"combo":combo,"total_combo_price":total_combo_price})
    return redirect("home")

def combo_sort_products(request):
    name = request.user
    if request.method == "POST":
        vendors = AddVendors.objects.all()
        all_product = AddProducts.objects.all()
        limit = request.POST.get("limit")
        product = []
        temp = []
        temp_com_price = []
        temp_combo = []
        combo = []
        count = 20
        if limit:
            for lmt in all_product:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit):
                    product.append(item) 
                    # print(product)  
            for i in product:
                com_product = AddProducts.objects.get(id=i.id)
                if float(com_product.Total_GF_price) < float(limit):
                    temp.append(com_product)
                    # print(temp)
            while count > 0:
                random.shuffle(temp)
                for j in temp:
                    com_pro = AddProducts.objects.get(id=j.id)
                    temp_combo.append(com_pro)
                    temp_com_price.append(com_pro.Total_GF_price)
                    if sum(temp_com_price) > float(limit):
                        temp_combo.pop(-1)
                        combo.append(temp_combo)
                        temp_combo = []
                        temp_com_price = []
                count = count-1
            combo.sort(key=lambda x: len(x), reverse=True)
            return render(request, "ComboSection.html", {"name":name,
                                                    "combo":combo,
                                                    "vendors":vendors})
        else:
            messages.info(request, "Something went wrong...")

    return redirect("Combo")

def ManualCombo(request):
    name = request.user
    products = AddProducts.objects.all()
    vendors = AddVendors.objects.all()
    price = [p.Total_GF_price for p in products]
    limit = max(price)
    # combo = ManualComboTemp.objects.all()
    combo = ManualComboTemp.objects.filter(usr=request.user)
    product_price = []
    for i in combo:
        combo_product = AddProducts.objects.get(id=i.product.id)
        product_price.append(combo_product.Total_GF_price)
    combo_price = sum(product_price)
    return render(request, "ManualCombo.html", {"name":name,
                                         "product":products,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "combo_price":combo_price})
    
def MakeMaualCombo(request):
    if request.method == "POST":
        manualcombolist = request.POST.getlist("manualcombolist")
        for i in manualcombolist:
            j = int(i)
            product = AddProducts.objects.get(id=j)
            if ManualComboTemp.objects.filter(product=product).exists():
                pass
            else:
                combo = ManualComboTemp(product=product,usr=request.user)
                combo.save()
        messages.info(request, "Your Combo added successfuly but need to care about Quantity anualy...")
        return redirect("Combo")
    return redirect("Combo")

def Product_Manual_Combo_Del(request,id):
    product = AddProducts.objects.get(id=id)
    com_product = ManualComboTemp.objects.filter(product=product,usr=request.user)
    com_product.delete()
    messages.info(request, "Removed Successfuly..!")
    return redirect("Combo")

def combo_product_list(request):
    query = request.GET.get('search')
    name = request.user
    product = AddProducts.objects.all()
    vendors = AddVendors.objects.all()
    price = [p.Total_GF_price for p in product]
    limit = max(price)
    combo_product = ManualComboTemp.objects.all()
    combo_product = ManualComboTemp.objects.filter(request.user)
    product_price = []
    for i in combo_product:
        combo_prod = AddProducts.objects.get(id=i.product.id)
        product_price.append(combo_prod.Total_GF_price)
    combo_price = sum(product_price)
    if query:
        product = AddProducts.objects.filter(Q(Product_Name__icontains=query))
        return render(request, "ComboSection.html",{"name":name,
                                                    "product":product,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})
    else:
        product = AddProducts.objects.all()
        return render(request, "ComboSection.html",{"name":name,
                                                    "product":product,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})
        
def SortedManualCombofinal(request):
    combo = []
    combo_price = []
    if request.method == "POST":
        manualcombolist = request.POST.getlist("manualcombolist")
        for i in manualcombolist:
            id = int(i)
            prod = AddProducts.objects.get(id=id)
            combo.append(prod)
            combo_price.append(prod.Total_GF_price)
        total_combo_price = sum(combo_price)
        return render(request, "combo.html", {"combo":combo,"total_combo_price":total_combo_price})

def AddToManualCombo(request,id):
    if ManualComboTemp.objects.filter(product=id).exists():
        messages.info(request, "Cant Select a product more than once...!")
        return redirect("Combo")
    else:
        product = AddProducts.objects.get(id=id)
        combo = ManualComboTemp(product=product,usr=request.user)
        combo.save()
        return redirect("Combo")

def DeleteCombo(request):
    # combo = ManualComboTemp.objects.all()
    combo = ManualComboTemp.objects.filter(usr=request.user)
    combo.delete()
    messages.info(request, "Combo Deleted Successfuly...")
    return redirect("Combo")

def auto_combo_submit(request):
    if request.method == "POST":
        # print('data from frontend',request.POST)
        combo_prod = request.POST.getlist("combo_prod")
        # print("selected combo",combo_prod)
        # com = ManualComboTemp.objects.all()
        com = ManualComboTemp.objects.filter(usr=request.user)
        com.delete()
        for i in combo_prod:
            j = int(i)
            product = AddProducts.objects.get(id=j)
            combo = ManualComboTemp(product=product,usr=request.user)
            combo.save()
        messages.info(request, "combo successfully added...")
        return redirect("Combo")
    return redirect("Combo")