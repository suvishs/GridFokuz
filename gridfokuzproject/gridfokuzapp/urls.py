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
    path("update_product/<int:id>", views.update_product, name="update_product"),
    path("delete_product/<int:id>", views.delete_product, name="delete_product"),
    
    # -------------------Filtering Section-------------------
    path("sort_products", views.sort_products, name="sort_products"),
    path("product_list", views.product_list, name="product_list"),
    
    # -------------------Combo Section-------------------
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
]
