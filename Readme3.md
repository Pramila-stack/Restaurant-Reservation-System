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


<!-- def get(self, request, pk, *args, **kwargs): -->
Handles GET requests
pk → primary key of the reservation to cancel

4️⃣ Fetch reservation
<!-- res = get_object_or_404(Reservation, pk=pk) -->
Gets the reservation by pk
Returns 404 error if reservation does not exist

<!-- res.status = 'cancelled' -->
<!-- res.save() -->
Updates reservation status in the database to cancelled
Saves changes


<!-- Send cancellation email
send_mail(
    subject='Your Reservation is Cancelled',
    message=f"Hi {res.user.username}, your reservation for {res.guests} guests on {res.reservation_date} at {res.reservation_time} has been cancelled.",
    from_email=settings.DEFAULT_FROM_EMAIL,
    recipient_list=[res.user.email],
) -->

Sends an email to the user
Message includes:
Username
Guests
Date & Time of reservation
Uses settings.DEFAULT_FROM_EMAIL as sender
7️⃣ Redirect back to admin page
return redirect('manage-reservations')
After cancelling, admin is sent back to Manage Reservations page