#ReserveForm ----> forms.py
<!-- Note -Dropdown is automatically created when used ForeignKey -->

<!-- widgets = {
    'reservation_time': forms.TimeInput(format='%H:%M', attrs={'type':'time'}),
    'reservation_date': forms.DateInput(attrs={'type':'date'}),
} -->
👉 This changes how inputs look in browser:
type="time" → shows time picker
type="date" → shows calendar picker


<!-- 🔹 What is __init__? -->

👉 It runs every time the form is created
Example:
form = ReservationForm()
👉 Django calls:
ReservationForm.__init__()

<!-- ✅ 2. Get custom values
date = kwargs.pop('date', None)
time = kwargs.pop('time', None) -->

👉 This is VERY important.
You passed date and time from the view
Example:
ReservationForm(date='2026-03-26', time='21:00')

<!-- 👉 kwargs.pop() means: -->

“Take date from kwargs”
Remove it so Django doesn’t get confused

👉 If not provided → None

<!-- ⚠️ Why pop? -->
Because Django form does NOT expect date and time by default.
If you don’t pop → ❌ error

<!-- ✅ 3. Call parent constructor
super().__init__(*args, **kwargs) -->

👉 This initializes the normal Django form:
creates fields
loads data
prepares validation
👉 Without this → ❌ form won’t work

<!-- ✅ 4. Check if date & time exist
if date and time: -->
👉 Only run filtering if user selected both

<!-- ✅ 5. Find already booked tables
booked_tables = Reservation.objects.filter(
    reservation_date=date,
    reservation_time=time,
    status__in=['pending', 'confirmed']
).values_list('table_id', flat=True) -->

👉 Meaning:
Get all reservations where:
same date
same time
status is pending OR confirmed
<!-- 
👉 Then:
.values_list('table_id', flat=True) -->
👉 returns only table IDs like:[1, 3, 5]

<!-- ✅ 6. Show only available tables
self.fields['table'].queryset = Table.objects.exclude(id__in=booked_tables) -->
👉 This is the magic line.
self.fields['table'] → the dropdown field
.queryset → controls what options appear

<!-- 👉 exclude(id__in=booked_tables) means: -->
❌ remove booked tables
✅ show only free tables



<!-- 🔹 What is self.fields? -->

Inside a Django form:
self.fields👉 is a dictionary that stores all the form fields
 
Example:

self.fields = {
    'table': <ModelChoiceField>,
    'guests': <IntegerField>,
    'reservation_date': <DateField>,
    'reservation_time': <TimeField>
}
🔹 Why not just use table directly?

❌ This will NOT work:
table.queryset = ...

Because:
table is just a name
<!-- Django stores actual fields inside self.fields -->

✅ So we must do:

self.fields['table']
🔹 Why is it needed in your case?
Because you want to change the dropdown options dynamically

👉 Default behavior:
Django shows all tables

👉 Your requirement:
Show only available tables
