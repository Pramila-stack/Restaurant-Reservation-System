# Admin/staff sees all reservations
@method_decorator(staff_member_required, name='dispatch')
class ManageReservationsView(ListView):
    model = Reservation
    template_name = 'manage_reservations.html'
    context_object_name = 'reservations'
    ordering = ['-reservation_date']

<!-- @method_decorator(staff_member_required, name='dispatch')
class ManageReservationsView(ListView): -->
This is a Django class-based view (CBV) that shows a list of reservations to staff/admin users only.

<!-- 1️⃣ @method_decorator(staff_member_required, name='dispatch') -->
staff_member_required → built-in Django decorator
Only staff users (users with is_staff=True) can access this view
<!-- For that you have to mark the staff status when creating the users for admin or staff in admin panel -->
method_decorator(..., name='dispatch') → allows decorators to work on class-based views
✅ Meaning:
Only staff/admin can see this page. Normal users will get redirected to login.

<!-- 2️⃣ class ManageReservationsView(ListView): -->
ListView → CBV for displaying lists of objects from a model
Here, we are listing Reservation objects


<!-- Below is a Django CBV (View) for admin/staff to confirm a reservation: -->

Automatically assigns a table based on availability
Updates the reservation status
Sends a confirmation email to the user
Redirects back to the admin reservations page

<!-- # Admin confirms reservation -->
# Admin confirms reservation
@method_decorator(staff_member_required, name='dispatch')
class ConfirmReservationView(View):
    def get(self, request, pk, *args, **kwargs):
        res = get_object_or_404(Reservation, pk=pk)
        # Assign table automatically
        already_boooked = Reservation.objects.filter(
            table = res.table
            reservation_date=res.reservation_date,
            reservation_time=res.reservation_time,
            status='confirmed'
        ).exists()
        

        if already_boooked:
            return redirect("manage-reservations")
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

<!-- @method_decorator(staff_member_required, name='dispatch') -->
Only staff users can access this view
Normal users will be redirected to login
dispatch → makes the decorator work for all HTTP methods (GET, POST, etc.)

2️⃣ Class Declaration
<!-- class ConfirmReservationView(View): -->
Inherits View (generic class-based view)
We manually define what happens for each HTTP method (get, post, etc.)

<!-- def get(self, request, pk, *args, **kwargs): -->
Handles GET requests
pk = primary key of the reservation to confirm
Example URL: /confirm-reservation/5/ → confirms reservation with ID 5

<!-- res = get_object_or_404(Reservation, pk=pk) -->
Try to get reservation by pk
If not found → return 404 error

<!-- Note -->
res = get_object_or_404(Reservation, pk=pk)
👉 gives you one full Reservation object (all its model fields)



<!-- already_booked = Reservation.objects.filter(
    table=res.table,
    reservation_date=res.reservation_date,
    reservation_time=res.reservation_time,
    status='confirmed'
).exists() -->
👉 This checks:“Is this SAME table already confirmed at SAME date & time?”

<!-- send_mail(
    subject='Your Reservation is Confirmed',
    message=f"Hi {res.user.username}, your reservation for {res.guests} guests on {res.reservation_date} at {res.reservation_time} is confirmed. Table: {res.table.number}.",
    from_email=settings.DEFAULT_FROM_EMAIL,
    recipient_list=[res.user.email],
) -->
Email user with confirmation details:
Guests
Date & Time
Table number

<!-- return redirect('manage-reservations') -->
After confirming, go back to Manage Reservations page

<!-- 🧠 Summary (Flow) -->
Admin clicks “Confirm”
Fetch reservation by pk
see if the table is booked
If not,Mark reservation as confirmed
Save reservation to the database.
Send confirmation email to the user
Redirect back to the admin view