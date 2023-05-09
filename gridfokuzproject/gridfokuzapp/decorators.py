from django.shortcuts import redirect

def Admin_only(view_func):
    def wrapper_func(request,*args,**kwargs):
        group = None
        if request.user.groups.all().exists():
            group = request.user.groups.all()[0].name
        
        if group == "SemiAdmin":
            return redirect("semiadminhome")
        
        if group == "Employee":
            return redirect("employeehome")
        
        if group == "Customer":
            return redirect("customerhome")
        
        else:
            return view_func(request,*args,**kwargs)

    return wrapper_func