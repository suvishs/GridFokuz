from django.urls import path
from .import views

urlpatterns = [
    
    # -------------------General Section-------------------
    path("", views.Index, name="index"),
    path("Usrlogin", views.Usrlogin, name="Usrlogin"),
    path("Register", views.Register, name="Register"),
    path("home", views.home, name="home"),
    path("GridHome", views.GridHome, name="GridHome"),
    path("SemiAdminHome", views.SemiAdminHome, name="SemiAdminHome"),
    path("EmployeeHome", views.EmployeeHome, name="EmployeeHome"),
    path("logout", views.logout, name="logout"),
    
    # -------------------Vendor Section-------------------
    path("addventors", views.addventors, name="addventors"),
    
    # -------------------Product Section-------------------
    path("addproducts", views.addproducts, name="addproducts"),
    path("product_detail/<int:id>", views.product_detail, name="product_detail"),
    path("Employee_product_detail/<int:id>", views.Employee_product_detail, name="Employee_product_detail"),
    
    path("update_product/<int:id>", views.update_product, name="update_product"),
    path("delete_product/<int:id>", views.delete_product, name="delete_product"),
    
    # -------------------Filtering Section-------------------
    path("sort_products", views.sort_products, name="sort_products"),
    path("Employee_sort_products", views.Employee_sort_products, name="Employee_sort_products"),
    
    path("product_list", views.product_list, name="product_list"),
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
    
    # -------------------PDF Section-------------------
    path("IntermediatePDFsection", views.IntermediatePDFsection, name="IntermediatePDFsection"),
    path('html_to_pdf', views.html_to_pdf, name='convert_to_pdf'),
    
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

]
