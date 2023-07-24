from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import AddVendors, AddProducts, ManualComboTemp, PDFtemp, Logo
from django.db.models import Q
import random
from gridfokuzapp.decorators import Admin_only
from django.contrib.auth.models import Group
from io import BytesIO
from xhtml2pdf import pisa
import pdfkit
from django.conf import settings
from django.template.loader import get_template
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.core.exceptions import PermissionDenied

# Create your views here.

# ---------------------------General section---------------------------

def Index(request):
    return render(request, "General/Index.html")

def shop(request):
    return render(request, "General/shop.html")

def ourstory(request):
    return render(request, "General/ourstory.html")

def gallery(request):
    return render(request, "General/gallery.html")

def contact(request):
    return render(request, "General/contact.html")

def user_list(request):
    users = User.objects.all()
    is_admin = False
    user_groups = request.user.groups.values_list('name', flat=True)
    admin = list(user_groups)
    # print(admin)
    if admin[0] == "Admin":
        is_admin = True
    return render(request, 'GridAdmin/user_list.html', {'users': users,"is_admin":is_admin})

def deleteuser(request,id):
    user = User.objects.get(id=id)
    user.delete()
    return redirect("user_list")


def Register(request):
    try:
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
        return render(request, 'General/Register.html')
    except PermissionDenied as e:
        return render(request, 'General/error_page.html', {'error_message': str(e)})

def Usrlogin(request):
    try:
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
        return render(request, 'General/Usrlogin.html')
    except PermissionDenied as e:
        return render(request, 'General/error_page.html', {'error_message': str(e)})

def logout(request):
    auth.logout(request)
    return redirect('Usrlogin')

# ---------------------------Add Staffs---------------------------
def addstaffs(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    is_admin = False
    user_groups = request.user.groups.values_list('name', flat=True)
    admin = list(user_groups)
    # print(admin)
    if admin[0] == "Admin":
        is_admin = True
    name = request.user
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirm_password')
        print(password,confirmpassword)
        module = request.POST.get('module')
        if password == confirmpassword:
            if User.objects.filter(username=username).exists():
                return HttpResponse("Username Already Exist")
            else:
                user = User.objects.create_user(username=username, password=password)
                group = Group.objects.get(name=module)
                user.groups.add(group)
                user.save()
                messages.info(request, f"{module} With Username {username} Created Successfuly...!")
                return render(request, 'GridAdmin/addstaffs.html', {"is_admin":is_admin})
        else:
            return HttpResponse("Password Does Not Maching")
    return render(request, "GridAdmin/addstaffs.html", {"is_admin":is_admin})

# ---------------------------Users section---------------------------

@Admin_only
def home(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    product = AddProducts.objects.all().order_by('Category')
    vendors = AddVendors.objects.all().order_by('vendorname')
    price = [p.Total_GF_price for p in product]
    limit = max(price)
    return render(request, "Customer/home.html", {"name":name,
                                         "product":product,
                                         "vendors":vendors,
                                         "limit":limit})

def GridHome(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    is_admin = False
    user_groups = request.user.groups.values_list('name', flat=True)
    admin = list(user_groups)
    # print(admin)
    if admin[0] == "Admin":
        is_admin = True
    product = AddProducts.objects.all().order_by('Category')
    vendors = AddVendors.objects.all().order_by('vendorname')
    price = [p.Total_GF_price for p in product]
    limit = max(price)
    return render(request, "GridAdmin/GridHome.html", {"name":name,
                                         "product":product,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})

def SemiAdminHome(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    product = AddProducts.objects.all().order_by('Category')
    vendors = AddVendors.objects.all().order_by('vendorname')
    price = [p.Total_GF_price for p in product]
    limit = max(price)
    return render(request, "SemiAdmin/SemiAdminHome.html", {"name":name,
                                         "product":product,
                                         "vendors":vendors,
                                         "limit":limit})

def EmployeeHome(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    product = AddProducts.objects.all().order_by('Category')
    vendors = AddVendors.objects.all().order_by('vendorname')
    price = [p.Total_GF_price for p in product]
    limit = max(price)
    return render(request, "Employee/EmployeeHome.html", {"name":name,
                                         "product":product,
                                         "vendors":vendors,
                                         "limit":limit})

# ---------------------------Vendors section---------------------------

def addventors(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    is_admin = False
    user_groups = request.user.groups.values_list('name', flat=True)
    admin = list(user_groups)
    # print(admin)
    if admin[0] == "Admin":
        is_admin = True
    if request.method == "POST":
        vendorname = request.POST.get("vendorname")
        vendorcode = request.POST.get("vendorcode")
        vendor = AddVendors(vendorname=vendorname, ventorcode=vendorcode)
        vendor.save()
        messages.info(request, "Vendor is added successfuly...")
        return redirect("addventors")
    return render(request, "GridAdmin/addventors.html", {"is_admin":is_admin})

def AdminViewAllVendors(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    vendors = AddVendors.objects.all().order_by('vendorname')
    is_admin = False
    user_groups = request.user.groups.values_list('name', flat=True)
    admin = list(user_groups)
    # print(admin)
    if admin[0] == "Admin":
        is_admin = True
    return render(request, "GridAdmin/AdminViewAllVendors.html", {"vendors":vendors, "is_admin":is_admin})

def updatevendor(request,id):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    is_admin = False
    user_groups = request.user.groups.values_list('name', flat=True)
    admin = list(user_groups)
    # print(admin)
    if admin[0] == "Admin":
        is_admin = True
    vendor = AddVendors.objects.get(id=id)
    ven_id = vendor.pk
    print(ven_id)
    ven_name = vendor.vendorname
    ven_code = vendor.ventorcode
    if request.method == "POST":
        vendorname = request.POST.get("vendorname")
        vendorcode = request.POST.get("vendorcode")
        vendor.vendorname = vendorname
        vendor.ventorcode = vendorcode
        vendor.save()
        return redirect("AdminViewAllVendors")
    return render(request, "GridAdmin/updatevendor.html",{"ven_id":ven_id, "ven_name":ven_name, "ven_code":ven_code, "is_admin":is_admin})

def deletevendor(request,id):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    default_vendor = AddVendors.objects.get(vendorname="vendorname")
    vendor = AddVendors.objects.get(id=id)
    products = AddProducts.objects.filter(Vendor=vendor)
    for product in products:
        product.Vendor = default_vendor
        product.save()
    vendor.delete()
    return redirect("AdminViewAllVendors")

# ---------------------------Product section---------------------------
def AdminViewAllProducts(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    is_admin = False
    user_groups = request.user.groups.values_list('name', flat=True)
    admin = list(user_groups)
    # print(admin)
    if admin[0] == "Admin":
        is_admin = True
    name = request.user
    product = AddProducts.objects.all().order_by('Category')
    vendors = AddVendors.objects.all().order_by('vendorname')
    price = [p.Total_GF_price for p in product]
    limit = max(price)
    return render(request, "GridAdmin/AdminViewAllProducts.html", {"name":name,
                                         "product":product,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})

def EmployeeViewAllProducts(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    product = AddProducts.objects.all().order_by('Category')
    vendors = AddVendors.objects.all().order_by('vendorname')
    price = [p.Total_GF_price for p in product]
    limit = max(price)
    return render(request, "Employee/EmployeeViewAllProducts.html", {"name":name,
                                         "product":product,
                                         "vendors":vendors,
                                         "limit":limit})

def CustomerViewAllProducts(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    product = AddProducts.objects.all().order_by('Category')
    vendors = AddVendors.objects.all().order_by('vendorname')
    price = [p.Total_GF_price for p in product]
    limit = max(price)
    return render(request, "Customer/CustomerViewAllProducts.html", {"name":name,
                                         "product":product,
                                         "vendors":vendors,
                                         "limit":limit})

def addproducts(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    vendor = AddVendors.objects.all().order_by('vendorname')
    is_admin = False
    user_groups = request.user.groups.values_list('name', flat=True)
    admin = list(user_groups)
    # print(admin)
    if admin[0] == "Admin":
        is_admin = True
    if request.method == "POST":
        SKU = request.POST.get("SKU")
        Vendor = request.POST.get("Vendor")
        vendor_name = AddVendors.objects.get(vendorname=Vendor)
        Category = request.POST.get("Category")
        Sub_category = request.POST.get("Sub_category")
        Product_Name = request.POST.get("Product_Name")
        MRP = request.POST.get("MRP")
        Vendor_Price = request.POST.get("Vendor_Price")
        # Transport1 = request.POST.get("Transport1")
        # Transport2 = request.POST.get("Transport2")
        # Branding = request.POST.get("Branding")
        # Packing = request.POST.get("Packing")
        # Profit_in_precentage = request.POST.get("Profit_in_precentage")
        # Profit_amount = request.POST.get("Profit_amount")
        # GF_Price = request.POST.get("GF_Price")
        # Tax_in_precentage = request.POST.get("Tax_in_precentage")
        # Tax_amount = request.POST.get("Tax_amount")
        Total_GF_price = request.POST.get("Total_GF_price")
        discription = request.POST.get("discription")
        product_image = request.FILES["product_image"]
        # product_image2 = request.FILES["product_image2"]
        # product_image3 = request.FILES["product_image3"]
        product = AddProducts(SKU=SKU,
                              Vendor=vendor_name,
                              Category=Category,
                              Sub_category=Sub_category,
                              Product_Name=Product_Name,
                              MRP=MRP,
                              Vendor_Price=Vendor_Price,
                            #   Transport1=Transport1,
                            #   Transport2=Transport2,
                            #   Branding=Branding,
                            #   Packing=Packing,
                            #   Profit_in_precentage=Profit_in_precentage,
                            #   Profit_amount=Profit_amount,
                            #   GF_Price=GF_Price,
                            #   Tax_in_precentage=Tax_in_precentage,
                            #   Tax_amount=Tax_amount,
                              Total_GF_price=Total_GF_price,
                              discription=discription,
                              product_image=product_image)
                            #   product_image2=product_image2,
                            #   product_image3=product_image3)
        product.save()
        messages.info(request, "{} added successfuly...".format(Product_Name))
        return redirect("addproducts")
    return render(request, "GridAdmin/addproducts.html",{"vendor":vendor, "is_admin":is_admin})

def GridAdminDeleteProduct(request,id):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    product = AddProducts.objects.get(id=id)
    product.delete()
    messages.info(request, f"{product} Deleted Successfuly...!")
    return redirect("AdminViewAllProducts")

def GridSemiAdminDeleteProduct(request,id):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    product = AddProducts.objects.get(id=id)
    product.delete()
    messages.info(request, f"{product} Deleted Successfuly...!")
    return redirect("SemiAdminHome")

def product_detail(request,id):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    is_admin = False
    user_groups = request.user.groups.values_list('name', flat=True)
    admin = list(user_groups)
    # print(admin)
    if admin[0] == "Admin":
        is_admin = True
    product = AddProducts.objects.get(id=id)
    return render(request, "GridAdmin/product_detail.html",{"product":product, "is_admin":is_admin})

def SemiAdminProductDetail(request,id):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    product = AddProducts.objects.get(id=id)
    return render(request, "SemiAdmin/SemiAdminProductDetail.html",{"product":product})

def update_product(request,id):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    is_admin = False
    user_groups = request.user.groups.values_list('name', flat=True)
    admin = list(user_groups)
    # print(admin)
    if admin[0] == "Admin":
        is_admin = True
    vendor = AddVendors.objects.all().order_by('vendorname')
    product = AddProducts.objects.get(id=id)
    if request.method == "POST":
        SKU = request.POST.get("SKU")
        Vendor = request.POST.get("Vendor")
        vendor_name = AddVendors.objects.get(vendorname=Vendor)
        Category = request.POST.get("Category")
        Sub_category = request.POST.get("Sub_category")
        Product_Name = request.POST.get("Product_Name")
        Total_GF_price = request.POST.get("Total_GF_price")
        Vendor_Price = request.POST.get("Vendor_Price")
        # Transport1 = request.POST.get("Transport1")
        # Transport2 = request.POST.get("Transport2")
        # Branding = request.POST.get("Branding")
        # Packing = request.POST.get("Packing")
        # Profit_in_precentage = request.POST.get("Profit_in_precentage")
        # Profit_amount = request.POST.get("Profit_amount")
        # GF_Price = request.POST.get("GF_Price")
        # Tax_in_precentage = request.POST.get("Tax_in_precentage")
        # Tax_amount = request.POST.get("Tax_amount")
        Total_GF_price = request.POST.get("Total_GF_price")
        try:
            product_image = request.FILES["product_image"]
            product.product_image = product_image
        except:
            pass
        product.SKU = SKU
        product.Category = Category
        product.Vendor = vendor_name
        product.Sub_category = Sub_category
        product.Product_Name = Product_Name
        product.Total_GF_price = Total_GF_price
        product.Vendor_Price = Vendor_Price
        # product.Transport1 = Transport1
        # product.Transport2 = Transport2
        # product.Branding = Branding
        # product.Packing = Packing
        # product.Profit_in_precentage = Profit_in_precentage
        # product.Profit_amount = Profit_amount
        # product.GF_Price = GF_Price
        # product.Tax_in_precentage = Tax_in_precentage
        # product.Tax_amount = Tax_amount
        product.Total_GF_price = Total_GF_price
        product.save()
        messages.info(request, "{} Updated Successfuly...".format(Product_Name))
        return redirect("AdminViewAllProducts")
    return render(request, "GridAdmin/update_product.html",{"product":product,
                                                  "vendor":vendor,
                                                  "is_admin":is_admin})

def GridSemiadminupdate_product(request,id):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    vendor = AddVendors.objects.all().order_by('vendorname')
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
        # Transport1 = request.POST.get("Transport1")
        # Transport2 = request.POST.get("Transport2")
        # Branding = request.POST.get("Branding")
        # Packing = request.POST.get("Packing")
        # Profit_in_precentage = request.POST.get("Profit_in_precentage")
        # Profit_amount = request.POST.get("Profit_amount")
        # GF_Price = request.POST.get("GF_Price")
        # Tax_in_precentage = request.POST.get("Tax_in_precentage")
        # Tax_amount = request.POST.get("Tax_amount")
        # Total_GF_price = request.POST.get("Total_GF_price")
        try:
            product_image = request.FILES["product_image"]
            product.product_image = product_image
        except:
            pass

        product.SKU = SKU
        product.Category = Category
        product.Vendor = vendor_name
        product.Sub_category = Sub_category
        product.Product_Name = Product_Name
        product.MRP = MRP
        product.Vendor_Price = Vendor_Price
        # product.Transport1 = Transport1
        # product.Transport2 = Transport2
        # product.Branding = Branding
        # product.Packing = Packing
        # product.Profit_in_precentage = Profit_in_precentage
        # product.Profit_amount = Profit_amount
        # product.GF_Price = GF_Price
        # product.Tax_in_precentage = Tax_in_precentage
        # product.Tax_amount = Tax_amount
        # product.Total_GF_price = Total_GF_price
        product.save()
        messages.info(request, "{} Updated Successfuly...".format(Product_Name))
        return redirect("SemiAdminHome")
    return render(request, "SemiAdmin/update_product.html",{"product":product,
                                                  "vendor":vendor})

def delete_product(request,id):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    product = AddProducts.objects.get(id=id)
    return render(request, "GridAdmin/delete_product.html",{"product":product})

def product_list(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    query = request.GET.get('search')
    name = request.user
    product = AddProducts.objects.all().order_by('Category')
    vendors = AddVendors.objects.all().order_by('vendorname')
    price = [p.Total_GF_price for p in product]
    limit = max(price)
    if query:
        product = AddProducts.objects.filter(Q(Product_Name__icontains=query))
        return render(request, "GridAdmin/GridHome.html",{"name":name,
                                         "product":product,
                                         "vendors":vendors,
                                         "limit":limit})
    else:
        product = AddProducts.objects.all().order_by('Category')
        return render(request, "GridAdmin/GridHome.html",{"name":name,
                                         "product":product,
                                         "vendors":vendors,
                                         "limit":limit})

def AdminViewAll_product_list(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    is_admin = False
    user_groups = request.user.groups.values_list('name', flat=True)
    admin = list(user_groups)
    # print(admin)
    if admin[0] == "Admin":
        is_admin = True
    query = request.GET.get('search')
    name = request.user
    product = AddProducts.objects.all().order_by('Category')
    vendors = AddVendors.objects.all().order_by('vendorname')
    price = [p.Total_GF_price for p in product]
    limit = max(price)
    if query:
        product = AddProducts.objects.filter(Q(Product_Name__icontains=query))
        return render(request, "GridAdmin/AdminViewAllProducts.html",{"name":name,
                                         "product":product,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})
    else:
        product = AddProducts.objects.all().order_by('Category')
        return render(request, "GridAdmin/AdminViewAllProducts.html",{"name":name,
                                         "product":product,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})

def EmployeeViewAll_product_list(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    query = request.GET.get('search')
    name = request.user
    product = AddProducts.objects.all().order_by('Category')
    vendors = AddVendors.objects.all().order_by('vendorname')
    price = [p.Total_GF_price for p in product]
    limit = max(price)
    if query:
        product = AddProducts.objects.filter(Q(Product_Name__icontains=query))
        return render(request, "Employee/EmployeeViewAllProducts.html",{"name":name,
                                         "product":product,
                                         "vendors":vendors,
                                         "limit":limit})
    else:
        product = AddProducts.objects.all().order_by('Category')
        return render(request, "Employee/EmployeeViewAllProducts.html",{"name":name,
                                         "product":product,
                                         "vendors":vendors,
                                         "limit":limit})

def CustomerViewAll_product_list(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    query = request.GET.get('search')
    name = request.user
    product = AddProducts.objects.all().order_by('Category')
    vendors = AddVendors.objects.all().order_by('vendorname')
    price = [p.Total_GF_price for p in product]
    limit = max(price)
    if query:
        product = AddProducts.objects.filter(Q(Product_Name__icontains=query))
        return render(request, "Customer/CustomerViewAllProducts.html",{"name":name,
                                         "product":product,
                                         "vendors":vendors,
                                         "limit":limit})
    else:
        product = AddProducts.objects.all().order_by('Category')
        return render(request, "Customer/CustomerViewAllProducts.html",{"name":name,
                                         "product":product,
                                         "vendors":vendors,
                                         "limit":limit})

def Employee_product_list(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    query = request.GET.get('search')
    name = request.user
    product = AddProducts.objects.all().order_by('Category')
    vendors = AddVendors.objects.all().order_by('vendorname')
    price = [p.Total_GF_price for p in product]
    limit = max(price)
    if query:
        product = AddProducts.objects.filter(Q(Product_Name__icontains=query))
        return render(request, "Employee/EmployeeHome.html",{"name":name,
                                         "product":product,
                                         "vendors":vendors,
                                         "limit":limit})
    else:
        product = AddProducts.objects.all().order_by('Category')
        return render(request, "Employee/EmployeeHome.html",{"name":name,
                                         "product":product,
                                         "vendors":vendors,
                                         "limit":limit})

def Customer_product_list(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    query = request.GET.get('search')
    name = request.user
    product = AddProducts.objects.all().order_by('Category')
    vendors = AddVendors.objects.all().order_by('vendorname')
    price = [p.Total_GF_price for p in product]
    limit = max(price)
    if query:
        product = AddProducts.objects.filter(Q(Product_Name__icontains=query))
        return render(request, "Customer/home.html",{"name":name,
                                         "product":product,
                                         "vendors":vendors,
                                         "limit":limit})
    else:
        product = AddProducts.objects.all().order_by('Category')
        return render(request, "Customer/home.html",{"name":name,
                                         "product":product,
                                         "vendors":vendors,
                                         "limit":limit})

# ---------------------------Filtering section---------------------------

def sort_products(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    is_admin = False
    user_groups = request.user.groups.values_list('name', flat=True)
    admin = list(user_groups)
    # print(admin)
    if admin[0] == "Admin":
        is_admin = True
    if request.method == "POST":
        all_product = AddProducts.objects.all().order_by('Category')
        name = request.user
        vendors = AddVendors.objects.all().order_by('vendorname')
        sorting = request.POST.get('sorting')
        print(sorting)
        selected_vendors = request.POST.getlist('vendor')
        print(selected_vendors)
        min_limit = request.POST.get("min_limit")
        print(min_limit)
        limit = request.POST.get("limit")
        print(limit)
        category = request.POST.getlist("category")
        print(category)
        sub_category = request.POST.getlist("sub_category")
        print(sub_category)
        products = []
        product = []
        cat_list = []
        final = []
        item_price_sort = []
        acending_items = []
        if selected_vendors and category and sub_category:
            print(selected_vendors)
            for i in selected_vendors:
                vendor = AddVendors.objects.get(vendorname=i)
                pro = AddProducts.objects.filter(Vendor=vendor)
                for j in pro:
                    products.append(j)
                    print(products)
            for lmt in products:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit) and float(item.Total_GF_price) >= float(min_limit):
                    product.append(item)
                    print(product)
            for cat in product:
                item_cat = AddProducts.objects.get(id=cat.id)
                for k in category:
                    if item_cat.Category == k:
                        cat_list.append(cat)
                        print(cat_list)
            for sub_cat in cat_list:
                sub_item = AddProducts.objects.get(id=sub_cat.id)
                for q in sub_category:
                    if sub_item.Sub_category == q:
                        final.append(sub_item)
                        print(final)
            if sorting != "null":
                if sorting == "acending":
                    for i in final:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort()
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    print(acending_items)
                    return render(request, "GridAdmin/sorted_products.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})
                elif sorting == "desending":
                    for i in final:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    print(acending_items)
                    return render(request, "GridAdmin/sorted_products.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})
                else:
                    return HttpResponse("Sorting Making Problem...")
            return render(request, "GridAdmin/sorted_products.html",{"name":name,
                                         "product":final,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})

        elif selected_vendors and category:
            for i in selected_vendors:
                vendor = AddVendors.objects.get(vendorname=i)
                pro = AddProducts.objects.filter(Vendor=vendor)
                for j in pro:
                    products.append(j)
            for lmt in products:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit) and float(item.Total_GF_price) >= float(min_limit):
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
                    print(product)
                    return render(request, "GridAdmin/sorted_products.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})
                elif sorting == "desending":
                    for i in cat_list:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    print(product)
                    return render(request, "GridAdmin/sorted_products.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})
                else:
                    return HttpResponse("Sorting Making Problem...")
            print(product)
            return render(request, "GridAdmin/sorted_products.html",{"name":name,
                                         "product":cat_list,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})

        elif selected_vendors and sub_category:
            for i in selected_vendors:
                vendor = AddVendors.objects.get(vendorname=i)
                pro = AddProducts.objects.filter(Vendor=vendor)
                for j in pro:
                    products.append(j)
            for lmt in products:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit) and float(item.Total_GF_price) >= float(min_limit):
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
                    print(product)
                    return render(request, "GridAdmin/sorted_products.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})
                elif sorting == "desending":
                    for i in final:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    print(product)
                    return render(request, "GridAdmin/sorted_products.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})
                else:
                    return HttpResponse("Sorting Making Problem...")
            print(product)
            return render(request, "GridAdmin/sorted_products.html",{"name":name,
                                         "product":final,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})

        elif category and sub_category:
            for lmt in all_product:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit) and float(item.Total_GF_price) >= float(min_limit):
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
                    print(product)
                    return render(request, "GridAdmin/sorted_products.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})
                elif sorting == "desending":
                    for i in final:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    print(product)
                    return render(request, "GridAdmin/sorted_products.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})
                else:
                    return HttpResponse("Sorting Making Problem...")
            print(product)
            return render(request, "GridAdmin/sorted_products.html",{"name":name,
                                         "product":final,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})

        elif category:
            for lmt in all_product:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit) and float(item.Total_GF_price) >= float(min_limit):
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
                    print(product)
                    return render(request, "GridAdmin/sorted_products.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})
                elif sorting == "desending":
                    for i in cat_list:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    print(product)
                    return render(request, "GridAdmin/sorted_products.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})
                else:
                    return HttpResponse("Sorting Making Problem...")
            print(product)
            return render(request, "GridAdmin/sorted_products.html",{"name":name,
                                         "product":cat_list,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})

        elif sub_category:
            for lmt in all_product:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit) and float(item.Total_GF_price) >= float(min_limit):
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
                    print(product)
                    return render(request, "GridAdmin/sorted_products.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})
                elif sorting == "desending":
                    for i in final:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    print(product)
                    return render(request, "GridAdmin/sorted_products.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})
                else:
                    return HttpResponse("Sorting Making Problem...")
            print(product)
            return render(request, "GridAdmin/sorted_products.html",{"name":name,
                                         "product":final,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})

        elif selected_vendors:
            for i in selected_vendors:
                vendor = AddVendors.objects.get(vendorname=i)
                pro = AddProducts.objects.filter(Vendor=vendor)
                for j in pro:
                    products.append(j)
            for lmt in products:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit) and float(item.Total_GF_price) >= float(min_limit):
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
                    print(product)
                    return render(request, "GridAdmin/sorted_products.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})
                elif sorting == "desending":
                    for i in product:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    print(product)
                    return render(request, "GridAdmin/sorted_products.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})
                else:
                    return HttpResponse("Sorting Making Problem...")
            print(product)
            return render(request, "GridAdmin/sorted_products.html",{"name":name,
                                         "product":product,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})

        elif limit:
            for lmt in all_product:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit) and float(item.Total_GF_price) >= float(min_limit):
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
                    print(product)
                    return render(request, "GridAdmin/sorted_products.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})
                elif sorting == "desending":
                    for i in product:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    print(product)
                    return render(request, "GridAdmin/sorted_products.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})
                else:
                    return HttpResponse("Sorting Making Problem...")
            print(product)
            return render(request, "GridAdmin/sorted_products.html",{"name":name,
                                         "product":product,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})
        else:
            messages.info(request, "Something went wrong...")
    return redirect("GridHome")

def AdminViewAllProduct_sort_products(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    is_admin = False
    user_groups = request.user.groups.values_list('name', flat=True)
    admin = list(user_groups)
    # print(admin)
    if admin[0] == "Admin":
        is_admin = True
    if request.method == "POST":
        all_product = AddProducts.objects.all().order_by('Category')
        name = request.user
        vendors = AddVendors.objects.all().order_by('vendorname')
        sorting = request.POST.get('sorting')
        selected_vendors = request.POST.getlist('vendor')
        min_limit = request.POST.get("min_limit")
        limit = request.POST.get("limit")
        category = request.POST.getlist("category")
        sub_category = request.POST.getlist("sub_category")
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
                if float(item.Total_GF_price) <= float(limit) and float(item.Total_GF_price) >= float(min_limit):
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
                    return render(request, "GridAdmin/AdminViewAllProducts.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})
                elif sorting == "desending":
                    for i in final:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "GridAdmin/AdminViewAllProducts.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})
                else:
                    return HttpResponse("Sorting Making Problem...")
            return render(request, "GridAdmin/AdminViewAllProducts.html",{"name":name,
                                         "product":final,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})

        elif selected_vendors and category:
            for i in selected_vendors:
                vendor = AddVendors.objects.get(vendorname=i)
                pro = AddProducts.objects.filter(Vendor=vendor)
                for j in pro:
                    products.append(j)
            for lmt in products:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit) and float(item.Total_GF_price) >= float(min_limit):
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
                    return render(request, "GridAdmin/AdminViewAllProducts.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})
                elif sorting == "desending":
                    for i in cat_list:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "GridAdmin/AdminViewAllProducts.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})
                else:
                    return HttpResponse("Sorting Making Problem...")
            return render(request, "GridAdmin/AdminViewAllProducts.html",{"name":name,
                                         "product":cat_list,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})

        elif selected_vendors and sub_category:
            for i in selected_vendors:
                vendor = AddVendors.objects.get(vendorname=i)
                pro = AddProducts.objects.filter(Vendor=vendor)
                for j in pro:
                    products.append(j)
            for lmt in products:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit) and float(item.Total_GF_price) >= float(min_limit):
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
                    return render(request, "GridAdmin/AdminViewAllProducts.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})
                elif sorting == "desending":
                    for i in final:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "GridAdmin/AdminViewAllProducts.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})
                else:
                    return HttpResponse("Sorting Making Problem...")
            return render(request, "GridAdmin/AdminViewAllProducts.html",{"name":name,
                                         "product":final,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})

        elif category and sub_category:
            for lmt in all_product:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit) and float(item.Total_GF_price) >= float(min_limit):
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
                    return render(request, "GridAdmin/AdminViewAllProducts.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})
                elif sorting == "desending":
                    for i in final:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "GridAdmin/AdminViewAllProducts.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})
                else:
                    return HttpResponse("Sorting Making Problem...")
            return render(request, "GridAdmin/AdminViewAllProducts.html",{"name":name,
                                         "product":final,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})

        elif category:
            for lmt in all_product:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit) and float(item.Total_GF_price) >= float(min_limit):
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
                    return render(request, "GridAdmin/AdminViewAllProducts.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})
                elif sorting == "desending":
                    for i in cat_list:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "GridAdmin/AdminViewAllProducts.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})
                else:
                    return HttpResponse("Sorting Making Problem...")
            return render(request, "GridAdmin/AdminViewAllProducts.html",{"name":name,
                                         "product":cat_list,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})

        elif sub_category:
            for lmt in all_product:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit) and float(item.Total_GF_price) >= float(min_limit):
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
                    return render(request, "GridAdmin/AdminViewAllProducts.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})
                elif sorting == "desending":
                    for i in final:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "GridAdmin/AdminViewAllProducts.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})
                else:
                    return HttpResponse("Sorting Making Problem...")
            return render(request, "GridAdmin/AdminViewAllProducts.html",{"name":name,
                                         "product":final,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})

        elif selected_vendors:
            for i in selected_vendors:
                vendor = AddVendors.objects.get(vendorname=i)
                pro = AddProducts.objects.filter(Vendor=vendor)
                for j in pro:
                    products.append(j)
            for lmt in products:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit) and float(item.Total_GF_price) >= float(min_limit):
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
                    return render(request, "GridAdmin/AdminViewAllProducts.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})
                elif sorting == "desending":
                    for i in product:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "GridAdmin/AdminViewAllProducts.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})
                else:
                    return HttpResponse("Sorting Making Problem...")
            return render(request, "GridAdmin/AdminViewAllProducts.html",{"name":name,
                                         "product":product,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})

        elif limit:
            for lmt in all_product:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit) and float(item.Total_GF_price) >= float(min_limit):
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
                    return render(request, "GridAdmin/AdminViewAllProducts.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})
                elif sorting == "desending":
                    for i in product:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "GridAdmin/AdminViewAllProducts.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})
                else:
                    return HttpResponse("Sorting Making Problem...")
            return render(request, "GridAdmin/AdminViewAllProducts.html",{"name":name,
                                         "product":product,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "is_admin":is_admin})
        else:
            messages.info(request, "Something went wrong...")
    return redirect("GridHome")

def EmployeeViewAllProduct_sort_products(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    if request.method == "POST":
        all_product = AddProducts.objects.all().order_by('Category')
        name = request.user
        vendors = AddVendors.objects.all()
        sorting = request.POST.get('sorting')
        selected_vendors = request.POST.getlist('vendor')
        min_limit = request.POST.get("min_limit")
        limit = request.POST.get("limit")
        category = request.POST.getlist("category")
        sub_category = request.POST.getlist("sub_category")
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
                if float(item.Total_GF_price) <= float(limit) and float(item.Total_GF_price) >= float(min_limit):
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
                    return render(request, "Employee/EmployeeViewAllProducts.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                elif sorting == "desending":
                    for i in final:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "Employee/EmployeeViewAllProducts.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                else:
                    return HttpResponse("Sorting Making Problem...")
            return render(request, "Employee/EmployeeViewAllProducts.html",{"name":name,
                                         "product":final,
                                         "vendors":vendors,
                                         "limit":limit})

        elif selected_vendors and category:
            for i in selected_vendors:
                vendor = AddVendors.objects.get(vendorname=i)
                pro = AddProducts.objects.filter(Vendor=vendor)
                for j in pro:
                    products.append(j)
            for lmt in products:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit) and float(item.Total_GF_price) >= float(min_limit):
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
                    return render(request, "Employee/EmployeeViewAllProducts.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                elif sorting == "desending":
                    for i in cat_list:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "Employee/EmployeeViewAllProducts.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                else:
                    return HttpResponse("Sorting Making Problem...")
            return render(request, "Employee/EmployeeViewAllProducts.html",{"name":name,
                                         "product":cat_list,
                                         "vendors":vendors,
                                         "limit":limit})

        elif selected_vendors and sub_category:
            for i in selected_vendors:
                vendor = AddVendors.objects.get(vendorname=i)
                pro = AddProducts.objects.filter(Vendor=vendor)
                for j in pro:
                    products.append(j)
            for lmt in products:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit) and float(item.Total_GF_price) >= float(min_limit):
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
                    return render(request, "Employee/EmployeeViewAllProducts.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                elif sorting == "desending":
                    for i in final:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "Employee/EmployeeViewAllProducts.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                else:
                    return HttpResponse("Sorting Making Problem...")
            return render(request, "Employee/EmployeeViewAllProducts.html",{"name":name,
                                         "product":final,
                                         "vendors":vendors,
                                         "limit":limit})

        elif category and sub_category:
            for lmt in all_product:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit) and float(item.Total_GF_price) >= float(min_limit):
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
                    return render(request, "Employee/EmployeeViewAllProducts.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                elif sorting == "desending":
                    for i in final:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "Employee/EmployeeViewAllProducts.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                else:
                    return HttpResponse("Sorting Making Problem...")
            return render(request, "Employee/EmployeeViewAllProducts.html",{"name":name,
                                         "product":final,
                                         "vendors":vendors,
                                         "limit":limit})

        elif category:
            for lmt in all_product:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit) and float(item.Total_GF_price) >= float(min_limit):
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
                    return render(request, "Employee/EmployeeViewAllProducts.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                elif sorting == "desending":
                    for i in cat_list:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "Employee/EmployeeViewAllProducts.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                else:
                    return HttpResponse("Sorting Making Problem...")
            return render(request, "Employee/EmployeeViewAllProducts.html",{"name":name,
                                         "product":cat_list,
                                         "vendors":vendors,
                                         "limit":limit})

        elif sub_category:
            for lmt in all_product:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit) and float(item.Total_GF_price) >= float(min_limit):
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
                    return render(request, "Employee/EmployeeViewAllProducts.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                elif sorting == "desending":
                    for i in final:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "Employee/EmployeeViewAllProducts.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                else:
                    return HttpResponse("Sorting Making Problem...")
            return render(request, "Employee/EmployeeViewAllProducts.html",{"name":name,
                                         "product":final,
                                         "vendors":vendors,
                                         "limit":limit})

        elif selected_vendors:
            for i in selected_vendors:
                vendor = AddVendors.objects.get(vendorname=i)
                pro = AddProducts.objects.filter(Vendor=vendor)
                for j in pro:
                    products.append(j)
            for lmt in products:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit) and float(item.Total_GF_price) >= float(min_limit):
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
                    return render(request, "Employee/EmployeeViewAllProducts.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                elif sorting == "desending":
                    for i in product:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "Employee/EmployeeViewAllProducts.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                else:
                    return HttpResponse("Sorting Making Problem...")
            return render(request, "Employee/EmployeeViewAllProducts.html",{"name":name,
                                         "product":product,
                                         "vendors":vendors,
                                         "limit":limit})

        elif limit:
            for lmt in all_product:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit) and float(item.Total_GF_price) >= float(min_limit):
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
                    return render(request, "Employee/EmployeeViewAllProducts.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                elif sorting == "desending":
                    for i in product:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "Employee/EmployeeViewAllProducts.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                else:
                    return HttpResponse("Sorting Making Problem...")
            return render(request, "Employee/EmployeeViewAllProducts.html",{"name":name,
                                         "product":product,
                                         "vendors":vendors,
                                         "limit":limit})
        else:
            messages.info(request, "Something went wrong...")
    return redirect("EmployeeHome")


def CustomerViewAllProduct_sort_products(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    if request.method == "POST":
        all_product = AddProducts.objects.all().order_by('Category')
        name = request.user
        vendors = AddVendors.objects.all()
        sorting = request.POST.get('sorting')
        selected_vendors = request.POST.getlist('vendor')
        min_limit = request.POST.get("min_limit")
        limit = request.POST.get("limit")
        category = request.POST.getlist("category")
        sub_category = request.POST.getlist("sub_category")
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
                if float(item.Total_GF_price) <= float(limit) and float(item.Total_GF_price) >= float(min_limit):
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
                    return render(request, "Customer/CustomerViewAllProducts.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                elif sorting == "desending":
                    for i in final:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "Customer/CustomerViewAllProducts.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                else:
                    return HttpResponse("Sorting Making Problem...")
            return render(request, "Customer/CustomerViewAllProducts.html",{"name":name,
                                         "product":final,
                                         "vendors":vendors,
                                         "limit":limit})

        elif selected_vendors and category:
            for i in selected_vendors:
                vendor = AddVendors.objects.get(vendorname=i)
                pro = AddProducts.objects.filter(Vendor=vendor)
                for j in pro:
                    products.append(j)
            for lmt in products:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit) and float(item.Total_GF_price) >= float(min_limit):
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
                    return render(request, "Customer/CustomerViewAllProducts.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                elif sorting == "desending":
                    for i in cat_list:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "Customer/CustomerViewAllProducts.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                else:
                    return HttpResponse("Sorting Making Problem...")
            return render(request, "Customer/CustomerViewAllProducts.html",{"name":name,
                                         "product":cat_list,
                                         "vendors":vendors,
                                         "limit":limit})

        elif selected_vendors and sub_category:
            for i in selected_vendors:
                vendor = AddVendors.objects.get(vendorname=i)
                pro = AddProducts.objects.filter(Vendor=vendor)
                for j in pro:
                    products.append(j)
            for lmt in products:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit) and float(item.Total_GF_price) >= float(min_limit):
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
                    return render(request, "Customer/CustomerViewAllProducts.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                elif sorting == "desending":
                    for i in final:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "Customer/CustomerViewAllProducts.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                else:
                    return HttpResponse("Sorting Making Problem...")
            return render(request, "Customer/CustomerViewAllProducts.html",{"name":name,
                                         "product":final,
                                         "vendors":vendors,
                                         "limit":limit})

        elif category and sub_category:
            for lmt in all_product:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit) and float(item.Total_GF_price) >= float(min_limit):
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
                    return render(request, "Customer/CustomerViewAllProducts.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                elif sorting == "desending":
                    for i in final:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "Customer/CustomerViewAllProducts.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                else:
                    return HttpResponse("Sorting Making Problem...")
            return render(request, "Customer/CustomerViewAllProducts.html",{"name":name,
                                         "product":final,
                                         "vendors":vendors,
                                         "limit":limit})

        elif category:
            for lmt in all_product:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit) and float(item.Total_GF_price) >= float(min_limit):
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
                    return render(request, "Customer/CustomerViewAllProducts.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                elif sorting == "desending":
                    for i in cat_list:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "Customer/CustomerViewAllProducts.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                else:
                    return HttpResponse("Sorting Making Problem...")
            return render(request, "Customer/CustomerViewAllProducts.html",{"name":name,
                                         "product":cat_list,
                                         "vendors":vendors,
                                         "limit":limit})

        elif sub_category:
            for lmt in all_product:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit) and float(item.Total_GF_price) >= float(min_limit):
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
                    return render(request, "Customer/CustomerViewAllProducts.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                elif sorting == "desending":
                    for i in final:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "Customer/CustomerViewAllProducts.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                else:
                    return HttpResponse("Sorting Making Problem...")
            return render(request, "Customer/CustomerViewAllProducts.html",{"name":name,
                                         "product":final,
                                         "vendors":vendors,
                                         "limit":limit})

        elif selected_vendors:
            for i in selected_vendors:
                vendor = AddVendors.objects.get(vendorname=i)
                pro = AddProducts.objects.filter(Vendor=vendor)
                for j in pro:
                    products.append(j)
            for lmt in products:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit) and float(item.Total_GF_price) >= float(min_limit):
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
                    return render(request, "Customer/CustomerViewAllProducts.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                elif sorting == "desending":
                    for i in product:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "Customer/CustomerViewAllProducts.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                else:
                    return HttpResponse("Sorting Making Problem...")
            return render(request, "Customer/CustomerViewAllProducts.html",{"name":name,
                                         "product":product,
                                         "vendors":vendors,
                                         "limit":limit})

        elif limit:
            for lmt in all_product:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit) and float(item.Total_GF_price) >= float(min_limit):
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
                    return render(request, "Customer/CustomerViewAllProducts.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                elif sorting == "desending":
                    for i in product:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "Customer/CustomerViewAllProducts.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                else:
                    return HttpResponse("Sorting Making Problem...")
            return render(request, "Customer/CustomerViewAllProducts.html",{"name":name,
                                         "product":product,
                                         "vendors":vendors,
                                         "limit":limit})
        else:
            messages.info(request, "Something went wrong...")
    return redirect("home")


def Employee_sort_products(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    if request.method == "POST":
        all_product = AddProducts.objects.all().order_by('Category')
        name = request.user
        vendors = AddVendors.objects.all()
        sorting = request.POST.get('sorting')
        selected_vendors = request.POST.getlist('vendor')
        min_limit = request.POST.get("min_limit")
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
                if float(item.Total_GF_price) <= float(limit) and float(item.Total_GF_price) >= float(min_limit):
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
                    return render(request, "Employee/Employee_sorted_products.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                elif sorting == "desending":
                    for i in final:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "Employee/Employee_sorted_products.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                else:
                    return HttpResponse("Sorting Making Problem...")
            return render(request, "Employee/Employee_sorted_products.html",{"name":name,
                                         "product":final,
                                         "vendors":vendors,
                                         "limit":limit})

        elif selected_vendors and category:
            for i in selected_vendors:
                vendor = AddVendors.objects.get(vendorname=i)
                pro = AddProducts.objects.filter(Vendor=vendor)
                for j in pro:
                    products.append(j)
            for lmt in products:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit) and float(item.Total_GF_price) >= float(min_limit):
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
                    return render(request, "Employee/Employee_sorted_products.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                elif sorting == "desending":
                    for i in cat_list:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "Employee/Employee_sorted_products.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                else:
                    return HttpResponse("Sorting Making Problem...")
            return render(request, "Employee/Employee_sorted_products.html",{"name":name,
                                         "product":cat_list,
                                         "vendors":vendors,
                                         "limit":limit})

        elif selected_vendors and sub_category:
            for i in selected_vendors:
                vendor = AddVendors.objects.get(vendorname=i)
                pro = AddProducts.objects.filter(Vendor=vendor)
                for j in pro:
                    products.append(j)
            for lmt in products:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit) and float(item.Total_GF_price) >= float(min_limit):
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
                    return render(request, "Employee/Employee_sorted_products.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                elif sorting == "desending":
                    for i in final:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "Employee/Employee_sorted_products.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                else:
                    return HttpResponse("Sorting Making Problem...")
            return render(request, "Employee/Employee_sorted_products.html",{"name":name,
                                         "product":final,
                                         "vendors":vendors,
                                         "limit":limit})

        elif category and sub_category:
            for lmt in all_product:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit) and float(item.Total_GF_price) >= float(min_limit):
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
                    return render(request, "Employee/Employee_sorted_products.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                elif sorting == "desending":
                    for i in final:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "Employee/Employee_sorted_products.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                else:
                    return HttpResponse("Sorting Making Problem...")
            return render(request, "Employee/Employee_sorted_products.html",{"name":name,
                                         "product":final,
                                         "vendors":vendors,
                                         "limit":limit})

        elif category:
            for lmt in all_product:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit) and float(item.Total_GF_price) >= float(min_limit):
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
                    return render(request, "Employee/Employee_sorted_products.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                elif sorting == "desending":
                    for i in cat_list:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "Employee/Employee_sorted_products.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                else:
                    return HttpResponse("Sorting Making Problem...")
            return render(request, "Employee/Employee_sorted_products.html",{"name":name,
                                         "product":cat_list,
                                         "vendors":vendors,
                                         "limit":limit})

        elif sub_category:
            for lmt in all_product:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit) and float(item.Total_GF_price) >= float(min_limit):
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
                    return render(request, "Employee/Employee_sorted_products.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                elif sorting == "desending":
                    for i in final:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "Employee/Employee_sorted_products.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                else:
                    return HttpResponse("Sorting Making Problem...")
            return render(request, "Employee/Employee_sorted_products.html",{"name":name,
                                         "product":final,
                                         "vendors":vendors,
                                         "limit":limit})

        elif selected_vendors:
            for i in selected_vendors:
                vendor = AddVendors.objects.get(vendorname=i)
                pro = AddProducts.objects.filter(Vendor=vendor)
                for j in pro:
                    products.append(j)
            for lmt in products:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit) and float(item.Total_GF_price) >= float(min_limit):
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
                    return render(request, "Employee/Employee_sorted_products.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                elif sorting == "desending":
                    for i in product:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "Employee/Employee_sorted_products.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                else:
                    return HttpResponse("Sorting Making Problem...")
            return render(request, "Employee/Employee_sorted_products.html",{"name":name,
                                         "product":product,
                                         "vendors":vendors,
                                         "limit":limit})

        elif limit:
            for lmt in all_product:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit) and float(item.Total_GF_price) >= float(min_limit):
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
                    return render(request, "Employee/Employee_sorted_products.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                elif sorting == "desending":
                    for i in product:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "Employee/Employee_sorted_products.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                else:
                    return HttpResponse("Sorting Making Problem...")
            return render(request, "Employee/Employee_sorted_products.html",{"name":name,
                                         "product":product,
                                         "vendors":vendors,
                                         "limit":limit})
        else:
            messages.info(request, "Something went wrong...")
    return redirect("EmployeeHome")

def Customer_sort_products(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    if request.method == "POST":
        all_product = AddProducts.objects.all().order_by('Category')
        name = request.user
        vendors = AddVendors.objects.all()
        sorting = request.POST.get('sorting')
        selected_vendors = request.POST.getlist('vendor')
        min_limit = request.POST.get("min_limit")
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
                if float(item.Total_GF_price) <= float(limit) and float(item.Total_GF_price) >= float(min_limit):
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
                    return render(request, "Customer/Customer_sorted_products.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                elif sorting == "desending":
                    for i in final:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "Customer/Customer_sorted_products.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                else:
                    return HttpResponse("Sorting Making Problem...")
            return render(request, "Customer/Customer_sorted_products.html",{"name":name,
                                         "product":final,
                                         "vendors":vendors,
                                         "limit":limit})

        elif selected_vendors and category:
            for i in selected_vendors:
                vendor = AddVendors.objects.get(vendorname=i)
                pro = AddProducts.objects.filter(Vendor=vendor)
                for j in pro:
                    products.append(j)
            for lmt in products:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit) and float(item.Total_GF_price) >= float(min_limit):
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
                    return render(request, "Customer/Customer_sorted_products.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                elif sorting == "desending":
                    for i in cat_list:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "Customer/Customer_sorted_products.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                else:
                    return HttpResponse("Sorting Making Problem...")
            return render(request, "Customer/Customer_sorted_products.html",{"name":name,
                                         "product":cat_list,
                                         "vendors":vendors,
                                         "limit":limit})

        elif selected_vendors and sub_category:
            for i in selected_vendors:
                vendor = AddVendors.objects.get(vendorname=i)
                pro = AddProducts.objects.filter(Vendor=vendor)
                for j in pro:
                    products.append(j)
            for lmt in products:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit) and float(item.Total_GF_price) >= float(min_limit):
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
                    return render(request, "Customer/Customer_sorted_products.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                elif sorting == "desending":
                    for i in final:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "Customer/Customer_sorted_products.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                else:
                    return HttpResponse("Sorting Making Problem...")
            return render(request, "Customer/Customer_sorted_products.html",{"name":name,
                                         "product":final,
                                         "vendors":vendors,
                                         "limit":limit})

        elif category and sub_category:
            for lmt in all_product:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit) and float(item.Total_GF_price) >= float(min_limit):
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
                    return render(request, "Customer/Customer_sorted_products.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                elif sorting == "desending":
                    for i in final:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "Customer/Customer_sorted_products.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                else:
                    return HttpResponse("Sorting Making Problem...")
            return render(request, "Customer/Customer_sorted_products.html",{"name":name,
                                         "product":final,
                                         "vendors":vendors,
                                         "limit":limit})

        elif category:
            for lmt in all_product:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit) and float(item.Total_GF_price) >= float(min_limit):
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
                    return render(request, "Customer/Customer_sorted_products.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                elif sorting == "desending":
                    for i in cat_list:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "Customer/Customer_sorted_products.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                else:
                    return HttpResponse("Sorting Making Problem...")
            return render(request, "Customer/Customer_sorted_products.html",{"name":name,
                                         "product":cat_list,
                                         "vendors":vendors,
                                         "limit":limit})

        elif sub_category:
            for lmt in all_product:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit) and float(item.Total_GF_price) >= float(min_limit):
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
                    return render(request, "Customer/Customer_sorted_products.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                elif sorting == "desending":
                    for i in final:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "Customer/Customer_sorted_products.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                else:
                    return HttpResponse("Sorting Making Problem...")
            return render(request, "Customer/Customer_sorted_products.html",{"name":name,
                                         "product":final,
                                         "vendors":vendors,
                                         "limit":limit})

        elif selected_vendors:
            for i in selected_vendors:
                vendor = AddVendors.objects.get(vendorname=i)
                pro = AddProducts.objects.filter(Vendor=vendor)
                for j in pro:
                    products.append(j)
            for lmt in products:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit) and float(item.Total_GF_price) >= float(min_limit):
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
                    return render(request, "Customer/Customer_sorted_products.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                elif sorting == "desending":
                    for i in product:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "Customer/Customer_sorted_products.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                else:
                    return HttpResponse("Sorting Making Problem...")
            return render(request, "Customer/Customer_sorted_products.html",{"name":name,
                                         "product":product,
                                         "vendors":vendors,
                                         "limit":limit})

        elif limit:
            for lmt in all_product:
                item = AddProducts.objects.get(id=lmt.id)
                if float(item.Total_GF_price) <= float(limit) and float(item.Total_GF_price) >= float(min_limit):
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
                    return render(request, "Customer/Customer_sorted_products.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                elif sorting == "desending":
                    for i in product:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    return render(request, "Customer/Customer_sorted_products.html",{"name":name,
                                         "product":acending_items,
                                         "vendors":vendors,
                                         "limit":limit})
                else:
                    return HttpResponse("Sorting Making Problem...")
            return render(request, "Customer/Customer_sorted_products.html",{"name":name,
                                         "product":product,
                                         "vendors":vendors,
                                         "limit":limit})
        else:
            messages.info(request, "Something went wrong...")

# ---------------------------Combo section---------------------------

def Combo(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    is_admin = False
    user_groups = request.user.groups.values_list('name', flat=True)
    admin = list(user_groups)
    # print(admin)
    if admin[0] == "Admin":
        is_admin = True
    name = request.user
    product = AddProducts.objects.all().order_by('Category')
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
    return render(request, "GridAdmin/ComboSection.html",{"name":name,
                                                "product":product,
                                                "vendors":vendors,
                                                "limit":limit,
                                                "combo_product":combo_product,
                                                "combo_price":combo_price,
                                                "is_admin":is_admin})

def HomeSortedManualCombo(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    combo = []
    combo_price = []
    is_admin = False
    user_groups = request.user.groups.values_list('name', flat=True)
    admin = list(user_groups)
    # print(admin)
    if admin[0] == "Admin":
        is_admin = True
    if request.method == "POST":
        manualcombolist = request.POST.getlist("manualcombolist")
        # print(manualcombolist)
        for i in manualcombolist:
            id = int(i)
            prod = AddProducts.objects.get(id=id)
            combo.append(prod)
            combo_price.append(prod.Total_GF_price)
        total_combo_price = sum(combo_price)
        return render(request, "GridAdmin/combo.html", {"combo":combo,"total_combo_price":total_combo_price, "is_admin":is_admin})
    return redirect("GridHome")

def combo_products(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    is_admin = False
    user_groups = request.user.groups.values_list('name', flat=True)
    admin = list(user_groups)
    # print(admin)
    if admin[0] == "Admin":
        is_admin = True
    name = request.user
    if request.method == "POST":
        combo_product = ManualComboTemp.objects.filter(usr=request.user)
        vendors = AddVendors.objects.all()
        prod = AddProducts.objects.all().order_by('Category')
        all_product = AddProducts.objects.all().order_by('Category')
        limit = request.POST.get("limit")
        product = []
        temp = []
        temp_com_price = []
        temp_combo = []
        combo = []
        count = 20
        product_price = []
        for i in combo_product:
            combo_prod = AddProducts.objects.get(id=i.product.id)
            product_price.append(combo_prod.Total_GF_price)
        combo_price = sum(product_price)
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
            for j in combo:
                if len(j) == 1:
                    combo.remove(j)
            combo.sort(key=lambda x: len(x), reverse=True)
            return render(request, "GridAdmin/ComboSection.html", {"name":name,"vendors":vendors,
                                                                    "combo_product":combo_product,
                                                                    "product":prod,
                                                                    "combo":combo,
                                                                    "vendors":vendors,
                                                                    "combo_price":combo_price,
                                                                    "is_admin":is_admin})
        else:
            messages.info(request, "Something went wrong...")

    return redirect("Combo")

def ManualCombo(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    is_admin = False
    user_groups = request.user.groups.values_list('name', flat=True)
    admin = list(user_groups)
    # print(admin)
    if admin[0] == "Admin":
        is_admin = True
    name = request.user
    products = AddProducts.objects.all().order_by('Category')
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
    return render(request, "GridAdmin/ManualCombo.html", {"name":name,
                                         "product":products,
                                         "vendors":vendors,
                                         "limit":limit,
                                         "combo_price":combo_price,
                                         "is_admin":is_admin})

def MakeMaualCombo(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    if request.method == "POST":
        manualcombolist = request.POST.getlist("manualcombolist")
        for i in manualcombolist:
            j = int(i)
            product = AddProducts.objects.get(id=j)
            if ManualComboTemp.objects.filter(product=product,usr=request.user).exists():
                print("inside", product)
            else:
                com = ManualComboTemp(product=product,usr=request.user)
                com.save()
        messages.info(request, "Your Combo added successfuly but need to care about Quantity manualy...")
        return redirect("Combo")
    return redirect("Combo")

def Product_Manual_Combo_Del(request,id):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    product = AddProducts.objects.get(id=id)
    com_product = ManualComboTemp.objects.filter(product=product,usr=request.user)
    com_product.delete()
    messages.info(request, "Removed Successfuly..!")
    return redirect("Combo")

def combo_product_list(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    is_admin = False
    user_groups = request.user.groups.values_list('name', flat=True)
    admin = list(user_groups)
    # print(admin)
    if admin[0] == "Admin":
        is_admin = True
    query = request.GET.get('search')
    name = request.user
    product = AddProducts.objects.all().order_by('Category')
    vendors = AddVendors.objects.all()
    price = [p.Total_GF_price for p in product]
    limit = max(price)
    combo_product = ManualComboTemp.objects.filter(usr=request.user)
    product_price = []
    for i in combo_product:
        combo_prod = AddProducts.objects.get(id=i.product.id)
        product_price.append(combo_prod.Total_GF_price)
    combo_price = sum(product_price)
    if query:
        product = AddProducts.objects.filter(Q(Product_Name__icontains=query))
        return render(request, "GridAdmin/ComboSection.html",{"name":name,
                                                    "product":product,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price,
                                                    "is_admin":is_admin})
    else:
        product = AddProducts.objects.all().order_by('Category')
        return render(request, "GridAdmin/ComboSection.html",{"name":name,
                                                    "product":product,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price,
                                                    "is_admin":is_admin})

def combo_sort_products(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    is_admin = False
    user_groups = request.user.groups.values_list('name', flat=True)
    admin = list(user_groups)
    # print(admin)
    if admin[0] == "Admin":
        is_admin = True
    name = request.user
    vendors = AddVendors.objects.all()
    prod = AddProducts.objects.all().order_by('Category')
    price = [p.Total_GF_price for p in prod]
    limit = max(price)
    combo_product = ManualComboTemp.objects.filter(usr=request.user)
    product_price = []
    for i in combo_product:
        combo_prod = AddProducts.objects.get(id=i.product.id)
        product_price.append(combo_prod.Total_GF_price)
    combo_price = sum(product_price)

    if request.method == "POST":
        all_product = AddProducts.objects.all().order_by('Category')
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
                    # return render(request, "ComboSection.html",{"product":acending_items})
                    return render(request, "GridAdmin/ComboSection.html",{"name":name,
                                                    "product":acending_items,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price,
                                                    "is_admin":is_admin})
                elif sorting == "desending":
                    for i in final:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    # return render(request, "ComboSection.html",{"product":acending_items})
                    return render(request, "GridAdmin/ComboSection.html",{"name":name,
                                                    "product":acending_items,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price,
                                                    "is_admin":is_admin})
                else:
                    return HttpResponse("Sorting Making Problem...")
            # return render(request, "ComboSection.html",{"product":final})
            return render(request, "GridAdmin/ComboSection.html",{"name":name,
                                                    "product":final,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price,
                                                    "is_admin":is_admin})

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
                    # return render(request, "ComboSection.html",{"product":acending_items})
                    return render(request, "GridAdmin/ComboSection.html",{"name":name,
                                                    "product":acending_items,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price,
                                                    "is_admin":is_admin})
                elif sorting == "desending":
                    for i in cat_list:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    # return render(request, "ComboSection.html",{"product":acending_items})
                    return render(request, "GridAdmin/ComboSection.html",{"name":name,
                                                    "product":acending_items,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price,
                                                    "is_admin":is_admin})
                else:
                    return HttpResponse("Sorting Making Problem...")
            # return render(request, "ComboSection.html",{"product":cat_list})
            return render(request, "GridAdmin/ComboSection.html",{"name":name,
                                                    "product":cat_list,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price,
                                                    "is_admin":is_admin})

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
                    # return render(request, "ComboSection.html",{"product":acending_items})
                    return render(request, "GridAdmin/ComboSection.html",{"name":name,
                                                    "product":acending_items,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price,
                                                    "is_admin":is_admin})
                elif sorting == "desending":
                    for i in final:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    # return render(request, "ComboSection.html",{"product":acending_items})
                    return render(request, "GridAdmin/ComboSection.html",{"name":name,
                                                    "product":acending_items,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price,
                                                    "is_admin":is_admin})
                else:
                    return HttpResponse("Sorting Making Problem...")
            # return render(request, "ComboSection.html",{"product":final})
            return render(request, "GridAdmin/ComboSection.html",{"name":name,
                                                    "product":final,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price,
                                                    "is_admin":is_admin})

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
                    # return render(request, "ComboSection.html",{"product":acending_items})
                    return render(request, "GridAdmin/ComboSection.html",{"name":name,
                                                    "product":acending_items,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price,
                                                    "is_admin":is_admin})
                elif sorting == "desending":
                    for i in final:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    # return render(request, "ComboSection.html",{"product":acending_items})
                    return render(request, "GridAdmin/ComboSection.html",{"name":name,
                                                    "product":acending_items,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price,
                                                    "is_admin":is_admin})
                else:
                    return HttpResponse("Sorting Making Problem...")
            # return render(request, "ComboSection.html",{"product":final})
            return render(request, "GridAdmin/ComboSection.html",{"name":name,
                                                    "product":final,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price,
                                                    "is_admin":is_admin})

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
                    # return render(request, "ComboSection.html",{"product":acending_items})
                    return render(request, "GridAdmin/ComboSection.html",{"name":name,
                                                    "product":acending_items,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price,
                                                    "is_admin":is_admin})
                elif sorting == "desending":
                    for i in cat_list:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    # return render(request, "ComboSection.html",{"product":acending_items})
                    return render(request, "GridAdmin/ComboSection.html",{"name":name,
                                                    "product":acending_items,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price,
                                                    "is_admin":is_admin})
                else:
                    return HttpResponse("Sorting Making Problem...")
            # return render(request, "ComboSection.html",{"product":cat_list})
            return render(request, "GridAdmin/ComboSection.html",{"name":name,
                                                    "product":cat_list,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price,
                                                    "is_admin":is_admin})

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
                    # return render(request, "ComboSection.html",{"product":acending_items})
                    return render(request, "GridAdmin/ComboSection.html",{"name":name,
                                                    "product":acending_items,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price,
                                                    "is_admin":is_admin})
                elif sorting == "desending":
                    for i in final:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    # return render(request, "ComboSection.html",{"product":acending_items})
                    return render(request, "GridAdmin/ComboSection.html",{"name":name,
                                                    "product":acending_items,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price,
                                                    "is_admin":is_admin})
                else:
                    return HttpResponse("Sorting Making Problem...")
            # return render(request, "ComboSection.html",{"product":final})
            return render(request, "GridAdmin/ComboSection.html",{"name":name,
                                                    "product":final,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price,
                                                    "is_admin":is_admin})

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
                    # return render(request, "ComboSection.html",{"product":acending_items})
                    return render(request, "GridAdmin/ComboSection.html",{"name":name,
                                                    "product":acending_items,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price,
                                                    "is_admin":is_admin})
                elif sorting == "desending":
                    for i in product:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    # return render(request, "ComboSection.html",{"product":acending_items})
                    return render(request, "GridAdmin/ComboSection.html",{"name":name,
                                                    "product":acending_items,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price,
                                                    "is_admin":is_admin})
                else:
                    return HttpResponse("Sorting Making Problem...")
            # return render(request, "ComboSection.html",{"product":product})
            return render(request, "GridAdmin/ComboSection.html",{"name":name,
                                                    "product":product,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price,
                                                    "is_admin":is_admin})

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
                    # return render(request, "ComboSection.html",{"product":acending_items})
                    return render(request, "GridAdmin/ComboSection.html",{"name":name,
                                                    "product":acending_items,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price,
                                                    "is_admin":is_admin})
                elif sorting == "desending":
                    for i in product:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    # return render(request, "ComboSection.html",{"product":acending_items})
                    return render(request, "GridAdmin/ComboSection.html",{"name":name,
                                                    "product":acending_items,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price,
                                                    "is_admin":is_admin})
                else:
                    return HttpResponse("Sorting Making Problem...")
            # return render(request, "ComboSection.html",{"product":product})
            return render(request, "GridAdmin/ComboSection.html",{"name":name,
                                                    "product":product,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price,
                                                    "is_admin":is_admin})
        else:
            messages.info(request, "Something went wrong...")
    return redirect("Combo")

def SortedManualCombofinal(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    is_admin = False
    user_groups = request.user.groups.values_list('name', flat=True)
    admin = list(user_groups)
    # print(admin)
    if admin[0] == "Admin":
        is_admin = True
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
        return render(request, "GridAdmin/combo.html", {"combo":combo,"total_combo_price":total_combo_price, "is_admin":is_admin})

def AddToManualCombo(request,id):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    if ManualComboTemp.objects.filter(product=id,usr=request.user).exists():
        messages.info(request, "Cant Select a product more than once...!")
        return redirect("Combo")
    else:
        product = AddProducts.objects.get(id=id)
        combo = ManualComboTemp(product=product,usr=request.user)
        combo.save()
        return redirect("Combo")

def DeleteCombo(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    # combo = ManualComboTemp.objects.all()
    combo = ManualComboTemp.objects.filter(usr=request.user)
    combo.delete()
    messages.info(request, "Combo Deleted Successfuly...")
    return redirect("Combo")

def auto_combo_submit(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    if request.method == "POST":
        combo_prod = request.POST.getlist("combo_prod")
        print(combo_prod)
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

# ---------------------------PDF section---------------------------
def IntermediatePDFsection(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    if request.method == "POST":
        productId = request.POST.getlist("productId")
        price_dis_display = request.POST.getlist("price_dis_display")
        grand_total = request.POST.getlist("grand_total")
        if PDFtemp.objects.filter(usr=request.user).exists():
            prod = PDFtemp.objects.filter(usr=request.user)
            prod.delete()
        for i,k in zip(productId, grand_total):
            j = int(i)
            product = AddProducts.objects.get(id=j)
            pdftemp = PDFtemp(product=product,grand_total=k,usr=request.user)
            pdftemp.save()
        product = PDFtemp.objects.filter(usr=request.user)
        return render(request, "General/IntermediatePDFsection.html", {"product":product})
    return render(request, "General/IntermediatePDFsection.html")


def html_to_pdf(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    is_admin = False
    user_groups = request.user.groups.values_list('name', flat=True)
    admin = list(user_groups)
    # print(admin)
    if admin[0] == "Admin":
        is_admin = True
    if request.method == "POST":
        productId = request.POST.getlist("productId")
        profit = request.POST.getlist("profit")
        profit_input = request.POST.getlist("profit_input")
        branding_cost = request.POST.getlist("branding_cost")
        branding_category = request.POST.getlist("branding_category")
        transportation_cost = request.POST.getlist("transportation_cost")
        tax = request.POST.getlist("tax")

        for i, pro_in, barn_co, bran_cat, trans_co, ta, prof in zip(productId, profit_input, branding_cost,branding_category, transportation_cost, tax, profit):
            id = int(i)
            item = AddProducts.objects.get(id=id)
            if prof == "profit_percentage":
                price_with_profit = float(item.Vendor_Price)+((float(item.Vendor_Price))*(float(pro_in)/100))
            elif prof == "profit_amount":
                price_with_profit = float(item.Vendor_Price)+float(pro_in)
            final_price = (price_with_profit+float(barn_co)+float(trans_co))+((price_with_profit+float(barn_co)+float(trans_co))*float(ta)/100)
            item.branding_category = bran_cat
            item.profit_percentage = pro_in
            item.branding_cost = barn_co
            item.transportation_cost = trans_co
            item.tax = ta
            item.final_price = final_price
            item.profit_type = prof
            item.save()

        if PDFtemp.objects.filter(usr=request.user).exists():
            prod = PDFtemp.objects.filter(usr=request.user)
            prod.delete()
        for i in productId:
            j = int(i)
            pro = AddProducts.objects.get(id=j)
            temp_prod = PDFtemp(product=pro, usr=request.user)
            temp_prod.save()
        products = PDFtemp.objects.filter(usr=request.user)
        return render(request, "GridAdmin/confirmation.html", {"products":products,"is_admin":is_admin})

def html_to_pdf_confirm(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    if request.method == "POST":
        price_display = request.POST.get("price_display")
        # print('1',price_display)
        branding_cost_dis = request.POST.get("branding_cost_dis")
        # print('2',branding_cost_dis)
        branding_cat_dis = request.POST.get("branding_cat_dis")
        # print('3',branding_cat_dis)
        transportation_cost_dis = request.POST.get("transportation_cost_dis")
        # print('4',transportation_cost_dis)
        gridfokuz_price_dis = request.POST.get("gridfokuz_price_dis")
        # print('5',gridfokuz_price_dis)
        productId = request.POST.getlist("productId")
        # print('6',productId)
        profit = request.POST.getlist("profit")
        # print('7',profit)
        profit_input = request.POST.getlist("profit_input")
        # print('8',profit_input)
        branding_cost = request.POST.getlist("branding_cost")
        # print('9',branding_cost)
        branding_category = request.POST.getlist("branding_category")
        # print('10',branding_category)
        transportation_cost = request.POST.getlist("transportation_cost")
        # print('11',transportation_cost)
        tax = request.POST.getlist("tax")
        # print('12',tax)

        for i, pro_in, barn_co, bran_cat, trans_co, ta, prof in zip(productId, profit_input, branding_cost,branding_category, transportation_cost, tax, profit):
            id = int(i)
            item = AddProducts.objects.get(id=id)
            if prof == "profit_percentage":
                price_with_profit = float(item.Vendor_Price)+((float(item.Vendor_Price))*(float(pro_in)/100))
            elif prof == "profit_amount":
                price_with_profit = float(item.Vendor_Price)+float(pro_in)
            final_price = (price_with_profit+float(barn_co)+float(trans_co))+((price_with_profit+float(barn_co)+float(trans_co))*float(ta)/100)
            item.branding_category = bran_cat
            item.profit_percentage = pro_in
            item.branding_cost = barn_co
            item.transportation_cost = trans_co
            item.tax = ta
            item.final_price = final_price
            item.profit_type = prof
            item.save()

        if PDFtemp.objects.filter(usr=request.user).exists():
            prod = PDFtemp.objects.filter(usr=request.user)
            prod.delete()
        for i in productId:
            j = int(i)
            pro = AddProducts.objects.get(id=j)
            temp_prod = PDFtemp(product=pro, usr=request.user)
            temp_prod.save()
        product = PDFtemp.objects.filter(usr=request.user)

        logo1 = Logo.objects.get(id=2)
        logo2 = Logo.objects.get(id=3)
        logo3 = Logo.objects.get(id=4)
        logo4 = Logo.objects.get(id=5)

        template_path = 'General/finalPDF.html'
        context = {'product': product,
                   'STATIC_ROOT': settings.STATIC_ROOT,
                   "price_display":price_display,
                   "branding_cost_dis":branding_cost_dis,
                   "branding_cat_dis":branding_cat_dis,
                   "transportation_cost_dis":transportation_cost_dis,
                   "gridfokuz_price_dis":gridfokuz_price_dis,
                  "logo1":logo1,
                  "logo2":logo2,
                  "logo3":logo3,
                  "logo4":logo4,
                   }
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="report.pdf"'
        template = get_template(template_path)
        html = template.render(context)
        # Create a pdf
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response

# ---------------------------Employee section---------------------------

def Employee_product_detail(request,id):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    product = AddProducts.objects.get(id=id)
    return render(request, "Employee/employee_product_detail.html",{"product":product})

def Employee_HomeSortedManualCombo(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
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
        return render(request, "Employee/Employee_combo.html", {"combo":combo,"total_combo_price":total_combo_price})
    return redirect("EmployeeHome")

def Employee_Combo(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    product = AddProducts.objects.all().order_by('Category')
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
    return render(request, "Employee/Employee_ComboSection.html",{"name":name,
                                                "product":product,
                                                "vendors":vendors,
                                                "limit":limit,
                                                "combo_product":combo_product,
                                                "combo_price":combo_price})

def Employee_AddToManualCombo(request,id):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    if ManualComboTemp.objects.filter(product=id,usr=request.user).exists():
        messages.info(request, "Cant Select a product more than once...!")
        return redirect("Employee_Combo")
    else:
        product = AddProducts.objects.get(id=id)
        combo = ManualComboTemp(product=product,usr=request.user)
        combo.save()
        return redirect("Employee_Combo")

def Employee_combo_products(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    if request.method == "POST":
        vendors = AddVendors.objects.all()
        all_product = AddProducts.objects.all().order_by('Category')
        prod = AddProducts.objects.all().order_by('Category')
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
            for j in combo:
                if len(j) == 1:
                    combo.remove(j)
            combo.sort(key=lambda x: len(x), reverse=True)
            combo_product = ManualComboTemp.objects.filter(usr=request.user)
            product_price = []
            for i in combo_product:
                combo_prod = AddProducts.objects.get(id=i.product.id)
                product_price.append(combo_prod.Total_GF_price)
            combo_price = sum(product_price)
            return render(request, "Employee/Employee_ComboSection.html", {"name":name,
                                                    "combo":combo,
                                                    "product":prod,
                                                    "vendors":vendors,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})
        else:
            messages.info(request, "Something went wrong...")

    return redirect("Employee_Combo")

def Employee_MakeMaualCombo(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    if request.method == "POST":
        manualcombolist = request.POST.getlist("manualcombolist")
        for i in manualcombolist:
            j = int(i)
            product = AddProducts.objects.get(id=j)
            if ManualComboTemp.objects.filter(product=product,usr=request.user).exists():
                print("inside", product)
            else:
                com = ManualComboTemp(product=product,usr=request.user)
                com.save()
        messages.info(request, "Your Combo added successfuly but need to care about Quantity manualy...")
        return redirect("Employee_Combo")
    return redirect("Employee_Combo")

def Employee_Product_Manual_Combo_Del(request,id):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    product = AddProducts.objects.get(id=id)
    com_product = ManualComboTemp.objects.filter(product=product,usr=request.user)
    com_product.delete()
    messages.info(request, "Removed Successfuly..!")
    return redirect("Employee_Combo")

def Employee_combo_product_list(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    query = request.GET.get('search')
    name = request.user
    product = AddProducts.objects.all().order_by('Category')
    vendors = AddVendors.objects.all()
    price = [p.Total_GF_price for p in product]
    limit = max(price)
    combo_product = ManualComboTemp.objects.filter(usr=request.user)
    product_price = []
    for i in combo_product:
        combo_prod = AddProducts.objects.get(id=i.product.id)
        product_price.append(combo_prod.Total_GF_price)
    combo_price = sum(product_price)
    if query:
        product = AddProducts.objects.filter(Q(Product_Name__icontains=query))
        return render(request, "Employee/Employee_ComboSection.html",{"name":name,
                                                    "product":product,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})

def Employee_SortedManualCombofinal(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
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
        return render(request, "Employee/Employee_combo.html", {"combo":combo,"total_combo_price":total_combo_price})

def Employee_DeleteCombo(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    # combo = ManualComboTemp.objects.all()
    combo = ManualComboTemp.objects.filter(usr=request.user)
    combo.delete()
    messages.info(request, "Combo Deleted Successfuly...")
    return redirect("Employee_Combo")

def Employee_auto_combo_submit(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    if request.method == "POST":
        combo_prod = request.POST.getlist("combo_prod")
        com = ManualComboTemp.objects.filter(usr=request.user)
        com.delete()
        for i in combo_prod:
            j = int(i)
            product = AddProducts.objects.get(id=j)
            combo = ManualComboTemp(product=product,usr=request.user)
            combo.save()
        messages.info(request, "combo successfully added...")
        return redirect("Employee_Combo")
    return redirect("Employee_Combo")

def Employee_combo_sort_products(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    vendors = AddVendors.objects.all()
    prod = AddProducts.objects.all().order_by('Category')
    price = [p.Total_GF_price for p in prod]
    limit = max(price)
    combo_product = ManualComboTemp.objects.filter(usr=request.user)
    product_price = []
    for i in combo_product:
        combo_prod = AddProducts.objects.get(id=i.product.id)
        product_price.append(combo_prod.Total_GF_price)
    combo_price = sum(product_price)

    if request.method == "POST":
        all_product = AddProducts.objects.all().order_by('Category')
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
                    # return render(request, "ComboSection.html",{"product":acending_items})
                    return render(request, "Employee/Employee_ComboSection.html",{"name":name,
                                                    "product":acending_items,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})
                elif sorting == "desending":
                    for i in final:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    # return render(request, "ComboSection.html",{"product":acending_items})
                    return render(request, "Employee/Employee_ComboSection.html",{"name":name,
                                                    "product":acending_items,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})
                else:
                    return HttpResponse("Sorting Making Problem...")
            # return render(request, "ComboSection.html",{"product":final})
            return render(request, "Employee/Employee_ComboSection.html",{"name":name,
                                                    "product":final,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})

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
                    # return render(request, "ComboSection.html",{"product":acending_items})
                    return render(request, "Employee/Employee_ComboSection.html",{"name":name,
                                                    "product":acending_items,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})
                elif sorting == "desending":
                    for i in cat_list:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    # return render(request, "ComboSection.html",{"product":acending_items})
                    return render(request, "Employee/Employee_ComboSection.html",{"name":name,
                                                    "product":acending_items,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})
                else:
                    return HttpResponse("Sorting Making Problem...")
            # return render(request, "ComboSection.html",{"product":cat_list})
            return render(request, "Employee/Employee_ComboSection.html",{"name":name,
                                                    "product":cat_list,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})

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
                    # return render(request, "ComboSection.html",{"product":acending_items})
                    return render(request, "Employee/Employee_ComboSection.html",{"name":name,
                                                    "product":acending_items,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})
                elif sorting == "desending":
                    for i in final:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    # return render(request, "ComboSection.html",{"product":acending_items})
                    return render(request, "Employee/Employee_ComboSection.html",{"name":name,
                                                    "product":acending_items,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})
                else:
                    return HttpResponse("Sorting Making Problem...")
            # return render(request, "ComboSection.html",{"product":final})
            return render(request, "Employee/Employee_ComboSection.html",{"name":name,
                                                    "product":final,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})

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
                    # return render(request, "ComboSection.html",{"product":acending_items})
                    return render(request, "Employee/Employee_ComboSection.html",{"name":name,
                                                    "product":acending_items,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})
                elif sorting == "desending":
                    for i in final:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    # return render(request, "ComboSection.html",{"product":acending_items})
                    return render(request, "Employee/Employee_ComboSection.html",{"name":name,
                                                    "product":acending_items,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})
                else:
                    return HttpResponse("Sorting Making Problem...")
            # return render(request, "ComboSection.html",{"product":final})
            return render(request, "Employee/Employee_ComboSection.html",{"name":name,
                                                    "product":final,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})

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
                    # return render(request, "ComboSection.html",{"product":acending_items})
                    return render(request, "Employee/Employee_ComboSection.html",{"name":name,
                                                    "product":acending_items,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})
                elif sorting == "desending":
                    for i in cat_list:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    # return render(request, "ComboSection.html",{"product":acending_items})
                    return render(request, "Employee/Employee_ComboSection.html",{"name":name,
                                                    "product":acending_items,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})
                else:
                    return HttpResponse("Sorting Making Problem...")
            # return render(request, "ComboSection.html",{"product":cat_list})
            return render(request, "Employee/Employee_ComboSection.html",{"name":name,
                                                    "product":cat_list,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})

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
                    # return render(request, "ComboSection.html",{"product":acending_items})
                    return render(request, "Employee/Employee_ComboSection.html",{"name":name,
                                                    "product":acending_items,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})
                elif sorting == "desending":
                    for i in final:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    # return render(request, "ComboSection.html",{"product":acending_items})
                    return render(request, "Employee/Employee_ComboSection.html",{"name":name,
                                                    "product":acending_items,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})
                else:
                    return HttpResponse("Sorting Making Problem...")
            # return render(request, "ComboSection.html",{"product":final})
            return render(request, "Employee/Employee_ComboSection.html",{"name":name,
                                                    "product":final,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})

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
                    # return render(request, "ComboSection.html",{"product":acending_items})
                    return render(request, "Employee/Employee_ComboSection.html",{"name":name,
                                                    "product":acending_items,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})
                elif sorting == "desending":
                    for i in product:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    # return render(request, "ComboSection.html",{"product":acending_items})
                    return render(request, "Employee/Employee_ComboSection.html",{"name":name,
                                                    "product":acending_items,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})
                else:
                    return HttpResponse("Sorting Making Problem...")
            # return render(request, "ComboSection.html",{"product":product})
            return render(request, "Employee/Employee_ComboSection.html",{"name":name,
                                                    "product":product,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})

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
                    # return render(request, "ComboSection.html",{"product":acending_items})
                    return render(request, "Employee/Employee_ComboSection.html",{"name":name,
                                                    "product":acending_items,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})
                elif sorting == "desending":
                    for i in product:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    # return render(request, "ComboSection.html",{"product":acending_items})
                    return render(request, "Employee/Employee_ComboSection.html",{"name":name,
                                                    "product":acending_items,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})
                else:
                    return HttpResponse("Sorting Making Problem...")
            # return render(request, "ComboSection.html",{"product":product})
            return render(request, "Employee/Employee_ComboSection.html",{"name":name,
                                                    "product":product,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})
        else:
            messages.info(request, "Something went wrong...")
    return redirect("Employee_Combo")

# ---------------------------Customer section---------------------------

def Customer_product_detail(request,id):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    product = AddProducts.objects.get(id=id)
    return render(request, "Customer/Customer_product_detail.html",{"product":product})

def Customer_HomeSortedManualCombo(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
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
        return render(request, "Customer/Customer_combo.html", {"combo":combo,"total_combo_price":total_combo_price})
    return redirect("home")

def Customer_Combo(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    product = AddProducts.objects.all().order_by('Category')
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
    return render(request, "Customer/Customer_ComboSection.html",{"name":name,
                                                "product":product,
                                                "vendors":vendors,
                                                "limit":limit,
                                                "combo_product":combo_product,
                                                "combo_price":combo_price})

def Customer_AddToManualCombo(request,id):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    if ManualComboTemp.objects.filter(product=id,usr=request.user).exists():
        messages.info(request, "Cant Select a product more than once...!")
        return redirect("Customer_Combo")
    else:
        product = AddProducts.objects.get(id=id)
        combo = ManualComboTemp(product=product,usr=request.user)
        combo.save()
        return redirect("Customer_Combo")

def Customer_combo_products(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    name = request.user
    if request.method == "POST":
        vendors = AddVendors.objects.all()
        all_product = AddProducts.objects.all().order_by('Category')
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
            for j in combo:
                if len(j) == 1:
                    combo.remove(j)
            combo.sort(key=lambda x: len(x), reverse=True)
            return render(request, "Customer/Customer_ComboSection.html", {"name":name,
                                                    "combo":combo,
                                                    "vendors":vendors})
        else:
            messages.info(request, "Something went wrong...")

    return redirect("Customer_Combo")

def Customer_MakeMaualCombo(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    if request.method == "POST":
        manualcombolist = request.POST.getlist("manualcombolist")
        for i in manualcombolist:
            j = int(i)
            product = AddProducts.objects.get(id=j)
            if ManualComboTemp.objects.filter(product=product,usr=request.user).exists():
                print("inside", product)
            else:
                com = ManualComboTemp(product=product,usr=request.user)
                com.save()
        messages.info(request, "Your Combo added successfuly but need to care about Quantity manualy...")
        return redirect("Customer_Combo")
    return redirect("Customer_Combo")

def Customer_Product_Manual_Combo_Del(request,id):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    product = AddProducts.objects.get(id=id)
    com_product = ManualComboTemp.objects.filter(product=product,usr=request.user)
    com_product.delete()
    messages.info(request, "Removed Successfuly..!")
    return redirect("Customer_Combo")

def Customer_combo_product_list(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    query = request.GET.get('search')
    name = request.user
    product = AddProducts.objects.all().order_by('Category')
    vendors = AddVendors.objects.all()
    price = [p.Total_GF_price for p in product]
    limit = max(price)
    combo_product = ManualComboTemp.objects.filter(usr=request.user)
    product_price = []
    for i in combo_product:
        combo_prod = AddProducts.objects.get(id=i.product.id)
        product_price.append(combo_prod.Total_GF_price)
    combo_price = sum(product_price)
    if query:
        product = AddProducts.objects.filter(Q(Product_Name__icontains=query))
        return render(request, "Customer/Customer_ComboSection.html",{"name":name,
                                                    "product":product,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})

def Customer_SortedManualCombofinal(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
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
        return render(request, "Customer/Customer_combo.html", {"combo":combo,"total_combo_price":total_combo_price})

def Customer_DeleteCombo(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    # combo = ManualComboTemp.objects.all()
    combo = ManualComboTemp.objects.filter(usr=request.user)
    combo.delete()
    messages.info(request, "Combo Deleted Successfuly...")
    return redirect("Customer_Combo")

def Customer_auto_combo_submit(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    if request.method == "POST":
        combo_prod = request.POST.getlist("combo_prod")
        com = ManualComboTemp.objects.filter(usr=request.user)
        com.delete()
        for i in combo_prod:
            j = int(i)
            product = AddProducts.objects.get(id=j)
            combo = ManualComboTemp(product=product,usr=request.user)
            combo.save()
        messages.info(request, "combo successfully added...")
        return redirect("Customer_Combo")
    return redirect("Customer_Combo")

def Customer_combo_sort_products(request):
    if not request.user.is_authenticated:
        return redirect('Usrlogin')
    name = request.user
    vendors = AddVendors.objects.all()
    prod = AddProducts.objects.all().order_by('Category')
    price = [p.Total_GF_price for p in prod]
    limit = max(price)
    combo_product = ManualComboTemp.objects.filter(usr=request.user)
    product_price = []
    for i in combo_product:
        combo_prod = AddProducts.objects.get(id=i.product.id)
        product_price.append(combo_prod.Total_GF_price)
    combo_price = sum(product_price)

    if request.method == "POST":
        all_product = AddProducts.objects.all().order_by('Category')
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
                    # return render(request, "ComboSection.html",{"product":acending_items})
                    return render(request, "Customer/Customer_ComboSection.html",{"name":name,
                                                    "product":acending_items,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})
                elif sorting == "desending":
                    for i in final:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    # return render(request, "ComboSection.html",{"product":acending_items})
                    return render(request, "Customer/Customer_ComboSection.html",{"name":name,
                                                    "product":acending_items,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})
                else:
                    return HttpResponse("Sorting Making Problem...")
            # return render(request, "ComboSection.html",{"product":final})
            return render(request, "Customer/Customer_ComboSection.html",{"name":name,
                                                    "product":final,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})

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
                    # return render(request, "ComboSection.html",{"product":acending_items})
                    return render(request, "Customer/Customer_ComboSection.html",{"name":name,
                                                    "product":acending_items,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})
                elif sorting == "desending":
                    for i in cat_list:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    # return render(request, "ComboSection.html",{"product":acending_items})
                    return render(request, "Customer/Customer_ComboSection.html",{"name":name,
                                                    "product":acending_items,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})
                else:
                    return HttpResponse("Sorting Making Problem...")
            # return render(request, "ComboSection.html",{"product":cat_list})
            return render(request, "Customer/Customer_ComboSection.html",{"name":name,
                                                    "product":cat_list,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})

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
                    # return render(request, "ComboSection.html",{"product":acending_items})
                    return render(request, "Customer/Customer_ComboSection.html",{"name":name,
                                                    "product":acending_items,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})
                elif sorting == "desending":
                    for i in final:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    # return render(request, "ComboSection.html",{"product":acending_items})
                    return render(request, "Customer/Customer_ComboSection.html",{"name":name,
                                                    "product":acending_items,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})
                else:
                    return HttpResponse("Sorting Making Problem...")
            # return render(request, "ComboSection.html",{"product":final})
            return render(request, "Customer/Customer_ComboSection.html",{"name":name,
                                                    "product":final,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})

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
                    # return render(request, "ComboSection.html",{"product":acending_items})
                    return render(request, "Customer/Customer_ComboSection.html",{"name":name,
                                                    "product":acending_items,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})
                elif sorting == "desending":
                    for i in final:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    # return render(request, "ComboSection.html",{"product":acending_items})
                    return render(request, "Customer/Customer_ComboSection.html",{"name":name,
                                                    "product":acending_items,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})
                else:
                    return HttpResponse("Sorting Making Problem...")
            # return render(request, "ComboSection.html",{"product":final})
            return render(request, "Customer/Customer_ComboSection.html",{"name":name,
                                                    "product":final,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})

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
                    # return render(request, "ComboSection.html",{"product":acending_items})
                    return render(request, "Customer/Customer_ComboSection.html",{"name":name,
                                                    "product":acending_items,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})
                elif sorting == "desending":
                    for i in cat_list:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    # return render(request, "ComboSection.html",{"product":acending_items})
                    return render(request, "Customer/Customer_ComboSection.html",{"name":name,
                                                    "product":acending_items,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})
                else:
                    return HttpResponse("Sorting Making Problem...")
            # return render(request, "ComboSection.html",{"product":cat_list})
            return render(request, "Customer/Customer_ComboSection.html",{"name":name,
                                                    "product":cat_list,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})

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
                    # return render(request, "ComboSection.html",{"product":acending_items})
                    return render(request, "Customer/Customer_ComboSection.html",{"name":name,
                                                    "product":acending_items,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})
                elif sorting == "desending":
                    for i in final:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    # return render(request, "ComboSection.html",{"product":acending_items})
                    return render(request, "Customer/Customer_ComboSection.html",{"name":name,
                                                    "product":acending_items,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})
                else:
                    return HttpResponse("Sorting Making Problem...")
            # return render(request, "ComboSection.html",{"product":final})
            return render(request, "Customer/Customer_ComboSection.html",{"name":name,
                                                    "product":final,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})

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
                    # return render(request, "ComboSection.html",{"product":acending_items})
                    return render(request, "Customer/Customer_ComboSection.html",{"name":name,
                                                    "product":acending_items,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})
                elif sorting == "desending":
                    for i in product:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    # return render(request, "ComboSection.html",{"product":acending_items})
                    return render(request, "Customer/Customer_ComboSection.html",{"name":name,
                                                    "product":acending_items,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})
                else:
                    return HttpResponse("Sorting Making Problem...")
            # return render(request, "ComboSection.html",{"product":product})
            return render(request, "Customer/Customer_ComboSection.html",{"name":name,
                                                    "product":product,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})

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
                    # return render(request, "ComboSection.html",{"product":acending_items})
                    return render(request, "Customer/Customer_ComboSection.html",{"name":name,
                                                    "product":acending_items,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})
                elif sorting == "desending":
                    for i in product:
                        items = AddProducts.objects.get(id=i.id)
                        item_price_sort.append(items.Total_GF_price)
                    item_price_sort.sort(reverse=True)
                    for j in item_price_sort:
                        acend_items = AddProducts.objects.get(Total_GF_price=j)
                        acending_items.append(acend_items)
                    # return render(request, "ComboSection.html",{"product":acending_items})
                    return render(request, "Customer/Customer_ComboSection.html",{"name":name,
                                                    "product":acending_items,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})
                else:
                    return HttpResponse("Sorting Making Problem...")
            # return render(request, "ComboSection.html",{"product":product})
            return render(request, "Customer/Customer_ComboSection.html",{"name":name,
                                                    "product":product,
                                                    "vendors":vendors,
                                                    "limit":limit,
                                                    "combo_product":combo_product,
                                                    "combo_price":combo_price})
        else:
            messages.info(request, "Something went wrong...")
    return redirect("Customer_Combo")