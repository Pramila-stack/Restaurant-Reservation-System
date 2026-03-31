🔥 FULL FLOW (from click → available tables)

<!-- ✅ 1. User selects date & time -->
In your HTML:
<form method="GET">
    <input type="date" name="reservation_date">
    <input type="time" name="reservation_time">
    <button type="submit">Check Availability</button>
</form>
👉 User picks:
Date → 2026-03-26
Time → 21:00

<!-- ✅ 2. User clicks Check Availability -->
👉 Browser sends a GET request:
/reserve-table/?reservation_date=2026-03-26&reservation_time=21:00


<!-- ✅ 3. Django receives request -->
Now in your view:
self.request.GET
👉 becomes:
{
    'reservation_date': '2026-03-26',
    'reservation_time': '21:00'
}


<!-- ✅ 4. get_form_kwargs() runs -->
def get_form_kwargs(self):
    kwargs = super().get_form_kwargs()
    date = self.request.GET.get('reservation_date')
    time = self.request.GET.get('reservation_time')

    if date and time:
        kwargs['date'] = date
        kwargs['time'] = time

    return kwargs

👉 Now Django prepares the form like:
ReservationForm(date='2026-03-26', time='21:00')


<!-- ✅ 5. Form __init__() runs -->
def __init__(self, *args, **kwargs):
    date = kwargs.pop('date', None)
    time = kwargs.pop('time', None)

    super().__init__(*args, **kwargs)
👉 Form receives date & time from the view ✅



<!-- ✅ 6. Filter booked tables -->
booked_tables = Reservation.objects.filter(
    reservation_date=date,
    reservation_time=time,
    status__in=['pending', 'confirmed']
).values_list('table_id', flat=True)

👉 Finds tables already booked at that time



<!-- ✅ 7. Show only available tables -->
self.fields['table'].queryset = Table.objects.exclude(id__in=booked_tables)
👉 Dropdown now shows only free tables ✅



✅ 8. Page renders again
Now template loads with:

<select name="table">
    <option>Table 2</option>
    <option>Table 5</option>
</select>

👉 Only available tables are shown 🎉

<!-- ✅ 9. Input fields keep old values -->
value="{{ request.GET.reservation_date }}"

👉 So user still sees:
Date: 2026-03-26
Time: 21:00


🔥 FINAL FLOW (super simple)
User selects date/time
        ↓
Clicks "Check Availability"
        ↓
GET request sent (URL updated)
        ↓
View reads request.GET
        ↓
get_form_kwargs() passes data
        ↓
Form __init__ receives it
        ↓
Filter booked tables
        ↓
Dropdown shows available tables
        ↓
Page reloads with filtered results
🔥 One-line understanding

👉 User input → goes to URL → view reads it → sends to form → form filters data → shows available tables.