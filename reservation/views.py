from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView,ListView,View
from django.contrib.auth.mixins import LoginRequiredMixin

import reservation
from reservation.forms import ReservationForm, SignupForm
from reservation.models import MenuItem, Profile, Reservation, Table
from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login

# Create your views here.
class SignupView(CreateView):
    template_name = "registration/signup.html"
    form_class = SignupForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        # Save the user first
        response = super().form_valid(form)
        # Save the email to the user
        self.object.email = form.cleaned_data['email']
        self.object.save()
        # Create customer profile
        Profile.objects.create(user=self.object, role="customer")
        login(self.request, self.object)
        return response

class HomeView(ListView):
    model = MenuItem
    template_name = "home.html"
    context_object_name = "menu_items"

    def get_queryset(self):
        return MenuItem.objects.filter(available=True).order_by("-id")
    

class ReserveTableView(LoginRequiredMixin, CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = "reserve_table.html"
    success_url = reverse_lazy("my-reservations")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        date = self.request.GET.get('reservation_date')
        time = self.request.GET.get('reservation_time')
        if date and time:
            kwargs['date'] = date
            kwargs['time'] = time
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = "pending"
        response = super().form_valid(form)

        if form.instance.user.email:
            send_mail(
                subject="Reservation request received",
                message=f"Hi {form.instance.user.username}, your reservation for {form.instance.guests} guests on {form.instance.reservation_date} at {form.instance.reservation_time} is pending confirmation.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[form.instance.user.email]
            )
        return response
    
    
class MyReservationView(LoginRequiredMixin,ListView):
    model = Reservation
    template_name = "my_reservations.html"
    context_object_name = "reservations"

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user).order_by("-reservation_date")
        
    
    
# Admin/staff sees all reservations
@method_decorator(staff_member_required, name='dispatch')
class ManageReservationsView(ListView):
    model = Reservation
    template_name = 'manage_reservations.html'
    context_object_name = 'reservations'
    # ordering = ['-reservation_date','reservation_time']
    ordering = ['-id']

# Admin confirms reservation
@method_decorator(staff_member_required,name="dispatch")
class ConfirmReservationView(View):
    def get(self,request,pk,*args,**kwargs):
        res = get_object_or_404(Reservation,pk=self.kwargs['pk'])

        already_booked = Reservation.objects.filter(
            table = res.table,
            reservation_date = res.reservation_date,
            reservation_time = res.reservation_time,
            status = 'confirmed'
        ).exists()

        if already_booked:
            return redirect('manage-reservations')
        res.status = 'confirmed'
        res.save()
#sends confirmation email.
        send_mail(
            subject='Your reservation is Confirmed',
            message=f"Hi{res.user.username},Your reservation for {res.guests} guest at {res.reservation_date} on {res.reservation_time} is confirmed.Table: {res.table.number}.",
            from_email= settings.DEFAULT_FROM_EMAIL,
            recipient_list=[res.user.email]
        )
        return redirect("manage-reservations")

# Admin cancels reservation
@method_decorator(staff_member_required,name="dispatch")
class CancelReservationView(View):
    def get(self,request,pk,*args,**kwargs):
        res = get_object_or_404(Reservation,pk=pk)
        res.status = 'cancelled'
        res.save()

        #send cancellation email.
        send_mail(
            subject='Your reservation is cancelled',
            message=f"Hi {res.user.username },Your reservation for {res.guests} guests at {res.reservation_date} on {res.reservation_time} has been cancelled.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[res.user.email],
        )
        return redirect('manage-reservations')
    