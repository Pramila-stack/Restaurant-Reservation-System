class SignupView(CreateView):
    template_name = "registration/signup.html"
    form_class = SignupForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
<!-- # Save the user first -->
        response = super().form_valid(form)
<!-- # Save the email to the user -->
        self.object.email = form.cleaned_data['email']
        self.object.save()
<!-- # Create customer profile -->
        Profile.objects.create(user=self.object, role="customer")
        return response

<!-- self.object.email = form.cleaned_data['email'] -->
👉 cleaned_data is a dictionary of validated (clean) input data from a form.
That means:✅ Data user entered,✅ Checked (validated) by Django,✅ Safe to use

<!-- self.object.email = form.cleaned_data['email']
self.object.save() -->

👉 Why this?Because:
Default Django UserCreationForm does NOT save email automatically
So you manually:Get email from form,Assign it to user,Save again


<!-- Profile.objects.create(user=self.object, role="customer") -->

👉 You are creating a Profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20)


<!-- response = super().form_valid(form) -->
Saves the user
Sets self.object = saved user
Creates redirect (response)
<!-- Imp -->
self.object exists only after super().form_valid(form)
If you try to access self.object before calling super(), it will be None

<!-- ReserveTableView -->
def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = "pending"

        response = super().form_valid(form)

        if form.instance.user.email:
            send_mail(
                subject="Reservation request received.",
                message=f"Hi {form.instance.user.username},your reservation requests for {form.instance.guests} on {form.instance.reservation_date} at {form.instance.reservation_time} is pending confirmation.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[form.instance.user.email]
            )
        return response

<!-- This function says:
“Before saving → add user & status
After saving → send email
Then redirect user” -->

form.instance.user = self.request.user
<!-- 👉 Meaning:“Set the reservation’s user = currently logged-in user” -->

✅ 3. Set default status
form.instance.status = "pending"

<!-- 👉 Meaning:
Every new reservation starts as pending -->

<!-- 🧩 How form.instance works
When user submits the form: -->
form = ReservationForm(request.POST)
form holds the submitted data
form.instance is the Reservation object that will be saved

<!-- 🧠 Now after this line: -->
👉 self.object EXISTS ✅
👉 Reservation is SAVED ✅

✅ 5. Check email
<!-- if self.object.user.email: -->
👉 If user has email → continue

<!-- send_mail(
    subject="Reservation request received.", -->
👉 Email subject

<!-- message=f"Hi {self.object.user.username}, your reservation request..." -->
👉 Message uses:username,reservation info

<!-- 
from_email=settings.DEFAULT_FROM_EMAIL,
recipient_list=[self.object.user.email] -->
👉 Sends email to user

<!-- ✅ 7. Return response -->
return response
👉 Sends user to:
/my-reservations/

<!-- Note -->
<!-- form.instance.user = self.request.user and form.instance.status = "pending" assign the logged-in user and default status to the reservation object before saving, and response = super().form_valid(form) saves the object and generates the redirect response. -->

<!-- Imp -->
self.object exists only after super().form_valid(form)
If you try to access self.object before calling super(), it will be None