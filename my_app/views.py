from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from .forms import BusinessInquiryForm
from .models import BusinessInquiry
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


def home(request):
    return render(request, 'inquiry_form.html')

# def business_inquiry(request):
#     if request.method == 'POST':
#         form = BusinessInquiryForm(request.POST)
#         if form.is_valid():
#             username = request.POST.get('username')
#             password = request.POST.get('password')

#             if not username or not password:
#                 messages.error(request, "Username and Password are required.")
#                 return redirect('business_inquiry')

#             if User.objects.filter(username=username).exists():
#                 messages.error(request, "Username already taken. Try a different one.")
#                 return redirect('business_inquiry')

#             user = User.objects.create_user(username=username, password=password)
#             inquiry = form.save(commit=False)
#             inquiry.user = user
#             inquiry.status = 'approved'  # Automatically approve new inquiries
#             inquiry.save()

#             messages.success(request, "User added successfully!")
#             return redirect('business_inquiry')

#     else:
#         form = BusinessInquiryForm()

#     return render(request, 'inquiry_form.html', {'form': form})

# 

@csrf_exempt
def business_inquiry(request):
    if request.method == 'POST':
        form = BusinessInquiryForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            if not username or not password:
                return JsonResponse({
                    "success": False,
                    "error": "Username and Password are required."
                }, status=200)

            if User.objects.filter(username=username).exists():
                return JsonResponse({
                    "success": False,
                    "error": "Username already taken. Try a different one."
                }, status=200)

            try:
                user = User.objects.create_user(username=username, password=password)
                inquiry = form.save(commit=False)
                inquiry.user = user
                inquiry.is_admin_created = False
                inquiry.save()

                return JsonResponse({
                    "success": True,
                    "message": "Wait for approval from admin."
                }, status=200)

            except Exception as e:
                return JsonResponse({
                    "success": False,
                    "error": str(e)
                }, status=200)

        else:
            return JsonResponse({
                "success": False,
                "error": form.errors
            }, status=200)

    else:
        return JsonResponse({
            "success": False,
            "error": "Invalid request method. Use POST."
        }, status=200)


@csrf_exempt
@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return JsonResponse({
            "success": False,
            "error": "Access denied!"
        }, status=200)

    inquiries = BusinessInquiry.objects.all().order_by('-created_at')
    data = [{
        'id': inquiry.id,
        'name': inquiry.name,
        'mobile': inquiry.mobile,
        'business_name': inquiry.business_name,
        'email': inquiry.email,
        'gstnumber': inquiry.gstnumber,
        'pannumber': inquiry.pannumber,
        'category': inquiry.category,
        'city': inquiry.city,
        'pin': inquiry.pin,
        'business_number': inquiry.business_number,
        'status': inquiry.status,
        'created_at': inquiry.created_at.strftime("%Y-%m-%d %H:%M:%S")
    } for inquiry in inquiries]
    
    return JsonResponse({
        "success": True,
        "inquiries": data
    })

@csrf_exempt
@login_required
def approve_inquiry(request, inquiry_id):
    if not request.user.is_superuser:
        return JsonResponse({
            "success": False,
            "error": "Access denied!"
        }, status=200)

    try:
        inquiry = BusinessInquiry.objects.get(id=inquiry_id)
        inquiry.status = 'approved'
        inquiry.save()
        return JsonResponse({
            "success": True,
            "message": "User Approved Successfully!",
            "inquiry_id": inquiry_id
        })
    except BusinessInquiry.DoesNotExist:
        return JsonResponse({
            "success": False,
            "error": "Inquiry not found"
        }, status=200)

@csrf_exempt
@login_required
def decline_inquiry(request, inquiry_id):
    if not request.user.is_superuser:
        return JsonResponse({
            "success": False,
            "error": "Access denied!"
        }, status=200)

    try:
        inquiry = BusinessInquiry.objects.get(id=inquiry_id)
        inquiry.status = 'declined'
        inquiry.save()
        return JsonResponse({
            "success": True,
            "message": "User Declined!",
            "inquiry_id": inquiry_id
        })
    except BusinessInquiry.DoesNotExist:
        return JsonResponse({
            "success": False,
            "error": "Inquiry not found"
        }, status=200)

@csrf_exempt
@login_required
def create_user(request):
    if not request.user.is_superuser:
        return JsonResponse({
            "success": False,
            "error": "Access denied!"
        }, status=200)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        business_name = request.POST.get('business_name')
        email = request.POST.get('email')
        gstnumber = request.POST.get('gstnumber')
        pannumber = request.POST.get('pannumber')
        category = request.POST.get('category')
        city = request.POST.get('city')
        pin = request.POST.get('pin')
        business_number = request.POST.get('business_number')
        if not all([username, password, name, mobile, address, business_name, email, gstnumber, pannumber, category, city, pin, business_number]):
            return JsonResponse({
                "success": False,
                "error": "All fields are required"
            }, status=200)

        if User.objects.filter(username=username).exists():
            return JsonResponse({
                "success": False,
                "error": "Username already exists!"
            }, status=200)

        try:
            user = User.objects.create_user(username=username, password=password)
            inquiry = BusinessInquiry.objects.create(
                user=user,
                name=name,
                mobile=mobile,
                address=address,
                business_name=business_name,
                email=email,
                gstnumber=gstnumber,
                pannumber=pannumber,
                category=category,
                city=city,
                pin=pin,
                business_number=business_number,
                status='approved',
                is_admin_created=True
            )
            return JsonResponse({
                "success": True,
                "message": "User created and approved successfully!",
                "user_id": user.id,
                "inquiry_id": inquiry.id
            })
        except Exception as e:
            return JsonResponse({
                "success": False,
                "error": str(e)
            }, status=200)

    return JsonResponse({
        "success": False,
        "error": "Invalid request method. Use POST."
    }, status=200)
    
@csrf_exempt
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_superuser:
            login(request, user)
            return JsonResponse({
                "success": True,
                "message": "Login successful",
                "is_superuser": True
            })
        else:
            return JsonResponse({
                "success": False,
                "message": "Invalid credentials or not an admin"
            }, status=200)
    
    return JsonResponse({
        "success": False,
        "error": "Only POST method allowed"
    }, status=200)