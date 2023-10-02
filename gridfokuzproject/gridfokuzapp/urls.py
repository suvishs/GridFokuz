from django.urls import path
from . import views

urlpatterns = [
    # -------------------General Section-------------------
    path("", views.Index, name="index"),
    path("Index", views.Index, name="index"),
    path("shop", views.shop, name="shop"),
    path("ourstory", views.ourstory, name="ourstory"),
    path("gallery", views.gallery, name="gallery"),
    path("contact", views.contact, name="contact"),
    path("Usrlogin", views.Usrlogin, name="Usrlogin"),
    path("Register", views.Register, name="Register"),
    path("home", views.home, name="home"),
    path("GridHome", views.GridHome, name="GridHome"),
    path("SemiAdminHome", views.SemiAdminHome, name="SemiAdminHome"),
    path("EmployeeHome", views.EmployeeHome, name="EmployeeHome"),
    path("logout", views.logout, name="logout"),
    path('users', views.user_list, name='user_list'),
    path('deleteuser/<int:id>', views.deleteuser, name="deleteuser"),
    path('sort_products_shop', views.sort_products_shop, name="sort_products_shop"),

    # -------------------Vendor Section-------------------
    path("addventors", views.addventors, name="addventors"),
    path("AdminViewAllVendors", views.AdminViewAllVendors, name="AdminViewAllVendors"),
    path("updatevendor/<int:id>", views.updatevendor, name="updatevendor"),
    path("deletevendor/<int:id>", views.deletevendor, name="deletevendor"),

    # -------------------Vendor Section-------------------
    path("addstaffs", views.addstaffs, name="addstaffs"),

    # -------------------Product Section-------------------
    path("addproducts", views.addproducts, name="addproducts"),
    path("product_detail/<int:id>", views.product_detail, name="product_detail"),
    path("Employee_product_detail/<int:id>", views.Employee_product_detail, name="Employee_product_detail"),
    path("Customer_product_detail/<int:id>", views.Customer_product_detail, name="Customer_product_detail"),
    path("SemiAdminProductDetail/<int:id>", views.SemiAdminProductDetail, name="SemiAdminProductDetail"),
    path("GridAdminDeleteProduct/<int:id>", views.GridAdminDeleteProduct, name="GridAdminDeleteProduct"),
    path("GridSemiAdminDeleteProduct/<int:id>", views.GridSemiAdminDeleteProduct, name="GridSemiAdminDeleteProduct"),
    path("GridSemiadminupdate_product/<int:id>", views.GridSemiadminupdate_product, name="GridSemiadminupdate_product"),
    path("update_product/<int:id>", views.update_product, name="update_product"),
    path("delete_product/<int:id>", views.delete_product, name="delete_product"),
    path("AdminViewAllProducts", views.AdminViewAllProducts, name="AdminViewAllProducts"),
    path("EmployeeViewAllProducts", views.EmployeeViewAllProducts, name="EmployeeViewAllProducts"),
    path("CustomerViewAllProducts", views.CustomerViewAllProducts, name="CustomerViewAllProducts"),
    path("productlist", views.productlist, name="productlist"),
    path("GridAdminDeleteProduct_list/<int:id>", views.GridAdminDeleteProduct_list, name="GridAdminDeleteProduct_list"),
    path("Admindeleteproductlist", views.Admindeleteproductlist, name="Admindeleteproductlist"),
    path("update_product_list/<int:id>", views.update_product_list, name="update_product_list"),


    # -------------------Filtering Section-------------------
    path("sort_products", views.sort_products, name="sort_products"),
    path("AdminViewAllProduct_sort_products", views.AdminViewAllProduct_sort_products, name="AdminViewAllProduct_sort_products"),
    path("EmployeeViewAllProduct_sort_products", views.EmployeeViewAllProduct_sort_products, name="EmployeeViewAllProduct_sort_products"),
    path("CustomerViewAllProduct_sort_products", views.CustomerViewAllProduct_sort_products, name="CustomerViewAllProduct_sort_products"),
    path("Employee_sort_products", views.Employee_sort_products, name="Employee_sort_products"),
    path("Customer_sort_products", views.Customer_sort_products, name="Customer_sort_products"),
    path("product_list", views.product_list, name="product_list"),
    path("product_list_shop", views.product_list_shop, name="product_list_shop"),
    path("AdminViewAll_product_list", views.AdminViewAll_product_list, name="AdminViewAll_product_list"),
    path("EmployeeViewAll_product_list", views.EmployeeViewAll_product_list, name="EmployeeViewAll_product_list"),
    path("CustomerViewAll_product_list", views.CustomerViewAll_product_list, name="CustomerViewAll_product_list"),
    path("Employee_product_list", views.Employee_product_list, name="Employee_product_list"),
    path("Customer_product_list", views.Customer_product_list, name="Customer_product_list"),

    # -------------------Admin Combo Section-------------------
    path("Combo", views.Combo, name="Combo"),
    path("combo_products", views.combo_products, name="combo_products"),
    path("HomeSortedManualCombo", views.HomeSortedManualCombo, name="HomeSortedManualCombo"),
    path("MakeMaualCombo", views.MakeMaualCombo, name="MakeMaualCombo"),
    path("Product_Manual_Combo_Del/<int:id>", views.Product_Manual_Combo_Del, name="Product_Manual_Combo_Del"),
    path("combo_product_list", views.combo_product_list, name="combo_product_list"),
    path("SortedManualCombofinal", views.SortedManualCombofinal, name="SortedManualCombofinal"),
    path("AddToManualCombo/<int:id>", views.AddToManualCombo, name="AddToManualCombo"),
    path("DeleteCombo", views.DeleteCombo, name="DeleteCombo"),
    path("auto_combo_submit", views.auto_combo_submit, name="auto_combo_submit"),
    path("combo_sort_products", views.combo_sort_products, name="combo_sort_products"),
    
    path("SortedCombo1", views.SortedCombo1, name="SortedCombo1"),
    path("SortedCombo2", views.SortedCombo2, name="SortedCombo2"),
    
    path("employee_SortedCombo1", views.employee_SortedCombo1, name="employee_SortedCombo1"),
    path("employee_SortedCombo2", views.employee_SortedCombo2, name="employee_SortedCombo2"),

    # -------------------PDF Section-------------------
    path("IntermediatePDFsection", views.IntermediatePDFsection, name="IntermediatePDFsection"),
    path('html_to_pdf', views.html_to_pdf, name='convert_to_pdf'),
    path('html_to_pdf_confirm', views.html_to_pdf_confirm, name='html_to_pdf_confirm'),

    # -------------------Employee Combo Section-------------------
    path("Employee_Combo", views.Employee_Combo, name="Employee_Combo"),
    path("Employee_combo_products", views.Employee_combo_products, name="Employee_combo_products"),
    path("Employee_HomeSortedManualCombo", views.Employee_HomeSortedManualCombo, name="Employee_HomeSortedManualCombo"),
    path("Employee_MakeMaualCombo", views.Employee_MakeMaualCombo, name="Employee_MakeMaualCombo"),
    path("Employee_Product_Manual_Combo_Del/<int:id>", views.Employee_Product_Manual_Combo_Del, name="Employee_Product_Manual_Combo_Del"),
    path("Employee_combo_product_list", views.Employee_combo_product_list, name="Employee_combo_product_list"),
    path("Employee_SortedManualCombofinal", views.Employee_SortedManualCombofinal, name="Employee_SortedManualCombofinal"),
    path("Employee_AddToManualCombo/<int:id>", views.Employee_AddToManualCombo, name="Employee_AddToManualCombo"),
    path("Employee_DeleteCombo", views.Employee_DeleteCombo, name="Employee_DeleteCombo"),
    path("Employee_auto_combo_submit", views.Employee_auto_combo_submit, name="Employee_auto_combo_submit"),
    path("Employee_combo_sort_products", views.Employee_combo_sort_products, name="Employee_combo_sort_products"),

    # -------------------Customer Combo Section-------------------
    path("Customer_Combo", views.Customer_Combo, name="Customer_Combo"),
    path("Customer_combo_products", views.Customer_combo_products, name="Customer_combo_products"),
    path("Customer_HomeSortedManualCombo", views.Customer_HomeSortedManualCombo, name="Customer_HomeSortedManualCombo"),
    path("Customer_MakeMaualCombo", views.Customer_MakeMaualCombo, name="Customer_MakeMaualCombo"),
    path("Customer_Product_Manual_Combo_Del/<int:id>", views.Customer_Product_Manual_Combo_Del, name="Customer_Product_Manual_Combo_Del"),
    path("Customer_combo_product_list", views.Customer_combo_product_list, name="Customer_combo_product_list"),
    path("Customer_SortedManualCombofinal", views.Customer_SortedManualCombofinal, name="Customer_SortedManualCombofinal"),
    path("Customer_AddToManualCombo/<int:id>", views.Customer_AddToManualCombo, name="Customer_AddToManualCombo"),
    path("Customer_DeleteCombo", views.Customer_DeleteCombo, name="Customer_DeleteCombo"),
    path("Customer_auto_combo_submit", views.Customer_auto_combo_submit, name="Customer_auto_combo_submit"),
    path("Customer_combo_sort_products", views.Customer_combo_sort_products, name="Customer_combo_sort_products"),
]
