from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView,ListView,View
from django.contrib.auth.mixins import LoginRequiredMixin

from reservation.forms import ReservationForm, SignupForm
from reservation.models import MenuItem, Profile, Reservation, Table
from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.
class SignupView(CreateView):
    template_name = "registration/signup.html"
    form_class = SignupForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        # Save the user first
        response = super().form_valid(form)
        # Save the email to the user
        self.object.email = form.cleaned_data['email']
        self.object.save()
        # Create customer profile
        Profile.objects.create(user=self.object, role="customer")
        return response

class HomeView(ListView):
    model = MenuItem
    template_name = "home.html"
    context_object_name = "menu_items"

    def get_queryset(self):
        return MenuItem.objects.filter(available=True)
    
class ReserveTableView(LoginRequiredMixin,CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = "reserve_table.html"
    success_url = reverse_lazy("my-reservations")

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = "pending"

        if form.instance.user.email:
            send_mail(
                subject="Reservation request received.",
                message=f"Hi {form.instance.user.username},your reservation requests for {form.instance.guests} on {form.instance.reservation_date} at {form.instance.reservation_time} is pending confirmation.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[form.instance.user.email]
            )
        return super().form_valid(form)
    

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
    ordering = ['-reservation_date']

# Admin confirms reservation
@method_decorator(staff_member_required, name='dispatch')
class ConfirmReservationView(View):
    def get(self, request, pk, *args, **kwargs):
        res = get_object_or_404(Reservation, pk=pk)
        # Assign table automatically
        tables = Table.objects.filter(seats__gte=res.guests)
        reserved_tables = Reservation.objects.filter(
            reservation_date=res.reservation_date,
            reservation_time=res.reservation_time,
            status='confirmed'
        ).values_list('table_id', flat=True)
        available_tables = tables.exclude(id__in=reserved_tables)

        if available_tables.exists():
            res.table = available_tables.first()
            res.status = 'confirmed'
            res.save()
            # Send confirmation email
            send_mail(
                subject='Your Reservation is Confirmed',
                message=f"Hi {res.user.username}, your reservation for {res.guests} guests on {res.reservation_date} at {res.reservation_time} is confirmed. Table: {res.table.number}.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[res.user.email],
            )
        return redirect('manage-reservations')

# Admin cancels reservation
@method_decorator(staff_member_required, name='dispatch')
class CancelReservationView(View):
    def get(self, request, pk, *args, **kwargs):
        res = get_object_or_404(Reservation, pk=pk)
        res.status = 'cancelled'
        res.save()
        # Send cancellation email
        send_mail(
            subject='Your Reservation is Cancelled',
            message=f"Hi {res.user.username}, your reservation for {res.guests} guests on {res.reservation_date} at {res.reservation_time} has been cancelled.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[res.user.email],
        )
        return redirect('manage-reservations')
    