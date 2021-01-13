from django.http import HttpResponseForbidden, HttpResponse
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views import generic
from app.models import vehicle, insurance, orders
from django.contrib.auth.models import User
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView, FormView, FormMixin
import app.forms as frm
import datetime
import razorpay
from io import BytesIO
from reportlab.pdfgen import canvas
import smtplib
from email.message import EmailMessage
from django.conf import settings
from django.core.mail import send_mail



class HomePageView(TemplateView):
    template_name = 'index.html'

class Profile(TemplateView):
    template_name = 'profile.html'


def UserOrder(request):
    app_list=orders.objects.filter(username=request.user)
    return render(request,'userorder.html',{"app_list":app_list})


class payment_confirmation(TemplateView):
    template_name = 'payment_confirmation.html'


def signup(request):
    if request.method == 'POST':
        form = frm.SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            User = authenticate(username=username, password=raw_password)
            login(request, User)
            subject = 'Welcome to Borderless Insurance'
            message = f'Hi {User.username}, thank you for registering with us.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [User.email, ]
            send_mail(subject, message, email_from, recipient_list)
            return redirect('home')
    else:
        form = frm.SignUpForm()
    return render(request, 'signup.html', {'form': form})


def AddVehicleForm(request):
    if request.method == 'POST':
        form = frm.VehicleForm(request.POST, request.FILES)
        if form.is_valid():
            if not vehicle.objects.filter(vehicle_number=form.cleaned_data['vehicle_number']):
                # print(form.cleaned_data['vehicle_number'])
                form.instance.full_name = request.user
                # print(request.user)
                form.save()
                return redirect('home')
            else:
                return render(request, 'addvehicle.html', {'msg': "Vehicle Number Already Exsits", 'form': form})
    else:
        form = frm.VehicleForm()
    return render(request, 'addvehicle.html', {'form': form})


def AddInsuranceForm(request):
    if request.method == 'POST':
        form = frm.InsuranceForm(request.POST, request.FILES)
        if form.is_valid():
            if not insurance.objects.filter(insurance_name=form.cleaned_data['insurance_name'],
                                            insurance_type=form.cleaned_data['insurance_type']):
                form.save()
                return redirect('home')
            else:
                return render(request, 'addinsurance.html', {'msg': "Insurance Name Already Exsits", 'form': form})
    else:
        form = frm.InsuranceForm()
    return render(request, 'addinsurance.html', {'form': form})



class InsuranceListView(generic.ListView):
    model = insurance
    context_object_name = 'app_list'
    template_name = 'insurance_profile.html'

    def get_queryset(self):
        return insurance.objects.all()


class InsuranceDelete(DeleteView):
    model = insurance
    template_name = 'delete_insurance.html'
    success_url = reverse_lazy('insurance_profile')


def UserInsuranceView(request):
    wheeler = request.POST.get('wheeler')
    print(type(wheeler))
    model = insurance
    app_list = {}
    app_list = insurance.objects.filter(insurance_type=wheeler)
    test_list = list(insurance.objects.filter(insurance_type=wheeler))
    for i in range(len(test_list)):
        print(test_list[i])
    return render(request, 'insurance_view.html', {"app_list": app_list})


class SelectedInsurance(FormMixin, generic.DetailView):
    template_name = 'user_insurance.html'
    # context_object_name = 'selected_insurance'
    model = insurance
    form_class = frm.VehicleForm

    def get_success_url(self):
        return reverse_lazy('payment')

    def post(self, request, *args, **kwargs):
        insu_data = []
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        insu = list(insurance.objects.filter(id=self.kwargs.get('pk')))
        for i in insu:
            insu_data.append(i.insurance_basic_price)
            insu_data.append(i.insurance_name)
            insu_data.append(i.insurance_type)
        f = open("payment-logs.txt","w")
        datatowrite=str(insu_data[0])+ "\n" + str(insu_data[1])+ "\n" + str(insu_data[2])
        f.write(datatowrite)
        f.close()
        form.instance.full_name = self.request.user
        form.instance.insurance_type = insu_data[2]
        form.instance.insurance_name = insu_data[1]
        form.instance.insurance_price = int(insu_data[0])
        if form.is_valid():
            form.save()
            print(form.errors)
            return self.form_valid(form)
        else:
            print(form.errors)
            return self.form_invalid(form)
    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SelectedInsurance, self).get_context_data(**kwargs)
        context['form'] = frm.VehicleForm()
        return context


def payment(request):
    empty_list=[]
    with open("payment-logs.txt") as f:
        empty_list=([line.rstrip() for line in f])
    context = {}
    client = razorpay.Client(auth=("rzp_test_EXjbUEDybwsOhO", "UlTOik00OQcCXKmKvJU7BROz"))
    response = client.order.create(data={"amount": int(empty_list[0])*100, "currency": "INR"})
    order_id = response["id"]
    order_status = response["status"]
    if order_status == "created":
        context["order_id"] = order_id
        context["insurance_name"] = empty_list[1]  # vehicle
        context["price"] = empty_list[0]  # insurace_basic_pay * bike valued amount
        context["username"] = request.user.username  # user
        obj = orders(orderid=order_id,insurance_name=empty_list[1],price=empty_list[0],username=request.user.username)
        obj.save()
        return render(request, 'payment.html', context)

class OrdersListView(generic.ListView):
    model = orders
    context_object_name = 'app_list'
    template_name = 'orders.html'

    def get_queryset(self):
        return orders.objects.all()

def payment_status(request):
    response = request.POST
    print(response)
    empty_list = []
    with open("payment-logs.txt") as f:
        empty_list = ([line.rstrip() for line in f])
    subject = 'Welcome to Borderless Insurance'
    message = f'Hi {request.user.username}, thank you for purchasing insurance with us.' \
              f' Insurance Price :{empty_list[0]}' \
              f' Insurance Name: {empty_list[1]}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [request.user.email, ]
    send_mail(subject, message, email_from, recipient_list)
    params_dict = {
        'razorpay_payment_id': response['razorpay_payment_id'],
        'razorpay_order_id': response['razorpay_order_id'],
        'razorpay_signature': response['razorpay_signature']
    }

    print(params_dict)

    # VERIFYING SIGNATURE
    try:
        status = client.utility.verify_payment_signature(params_dict)
        print(status)
        return render(request, 'order_summary.html', {'status': 'Payment Successful'})
    except:
        return redirect('payment_confirmation')



