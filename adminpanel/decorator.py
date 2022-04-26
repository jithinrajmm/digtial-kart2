

from django.shortcuts import redirect

# checking the admin is login or not
def adminlogin(check):
    def checkfunction(request):
        if 'id' in request.session:
            return redirect('adminhome')
        else:
            return check(request)
    return checkfunction

# for checking the user is logout or not
def logout(check_function):
    
    def check(request,*args,**kargs):
        if 'id' not in request.session:
            return redirect('adminLogin')
        else:
            return check_function(request,*args,**kargs)
    return check