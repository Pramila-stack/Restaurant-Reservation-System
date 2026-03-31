<!-- Views.py- ReserveTableView -->

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        date = self.request.GET.get('reservation_date')
        time = self.request.GET.get('reservation_time')
        if date and time:
            kwargs['date'] = date
            kwargs['time'] = time
        return kwargs

<!-- 🔹 What is get_form_kwargs()? -->

👉 It is a method used by Django CreateView to:
“Send data from the view → into the form”

<!-- Flow (VERY IMPORTANT)
User clicks Check Availability
URL becomes: -->
/reserve-table/?reservation_date=2026-03-26&reservation_time=21:00
Django calls:
<!-- get_form_kwargs() -->
Data is passed to your form:
ReservationForm(date=..., time=...)


<!-- kwargs = super().get_form_kwargs() -->

👉 This gets default data Django already sends to the form:
Example:
kwargs = {
    'data': request.POST or None,
    'files': request.FILES or None,
    'instance': None
}
👉 Think of it as:
“Start with normal form data”

<!-- ✅ 2. Get date from URL
date = self.request.GET.get('reservation_date') -->

👉 Reads from URL:
?reservation_date=2026-03-26
👉 So:
date = "2026-03-26"

<!-- ✅ 3. Get time from URL
time = self.request.GET.get('reservation_time') -->
👉 From:
?reservation_time=21:00
👉 So:
time = "21:00"


<!-- ✅ 4. Check if both exist
if date and time: -->
👉 Only continue if user selected both

<!-- ✅ 5. Add custom data to kwargs
kwargs['date'] = date
kwargs['time'] = time -->

👉 Now kwargs becomes:

kwargs = {
    'data': None,
    'files': None,
    'date': '2026-03-26',
    'time': '21:00'
}

👉 You are adding extra custom values

✅ 6. Return kwargs
return kwargs

<!-- 👉 Django now calls your form like: -->

ReservationForm(date='2026-03-26', time='21:00')
🔹 How it connects to your form

<!-- In your form: -->

date = kwargs.pop('date', None)
time = kwargs.pop('time', None)

👉 This is where the data you passed is received


<!-- Reservetbale.html-templates -->
About how value came
    <input type="date" name="reservation_date" value="{{ request.GET.reservation_date }}" required>

🔹 Step-by-step flow (VERY CLEAR)

<!-- ✅ 1. User selects date + clicks button -->
Form sends request like:
<!-- /reserve-table/?reservation_date=2026-03-26&reservation_time=21:00 -->
👉 This is a GET request

✅ 2. Django stores it in request.GET

<!-- Django creates a dictionary-like object: -->

request.GET = {
    'reservation_date': '2026-03-26',
    'reservation_time': '21:00'
}

✅ 3. Template accesses it

In template:

<!-- {{ request.GET.reservation_date }} -->

👉 means:
request.GET['reservation_date']

👉 Output:
2026-03-26

✅ 4. It goes inside value

So HTML becomes:

<input type="date" name="reservation_date" value="2026-03-26">
🔹 Why this is used

👉 Without this:

User selects date → submits → page reloads
Input becomes empty ❌

👉 With this:

Input keeps previous value ✅