import datetime
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView
from apps.accounts.permissions import AdminRequiredMixin, EditorRequiredMixin
from .forms import EventForm, ScheduleItemForm
from .models import Event, ScheduleItem


# ==============================================================================
# Public Event Views
# ==============================================================================

class EventListView(ListView):
    template_name = 'public/events.html'
    context_object_name = 'events'
    paginate_by = 9

    def get_queryset(self):
        q = Event.objects.all()
        if status := self.request.GET.get('status'):
            q = q.filter(status=status)
        if category := self.request.GET.get('category'):
            q = q.filter(category=category)
        return q


class PublicCalendarView(TemplateView):
    """
    Dedicated Public Academic Calendar page for students to browse monthly/yearly schedules.
    """
    template_name = 'public/calendar.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['schedule_categories'] = ScheduleItem.Category.choices
        ctx['upcoming_schedules'] = ScheduleItem.objects.filter(
            is_published=True,
            start_date__gte=datetime.date.today()
        ).order_date_range() if hasattr(ScheduleItem.objects, 'order_date_range') else ScheduleItem.objects.filter(
            is_published=True,
            start_date__gte=datetime.date.today()
        ).order_by('start_date', 'start_time')[:10]
        return ctx


class ScheduleJsonFeedView(View):
    """
    Returns calendar schedules in JSON format for the interactive homepage and calendar widget.
    Filters by month, year, or category.
    """
    def get(self, request, *args, **kwargs):
        year = request.GET.get('year')
        month = request.GET.get('month')
        category = request.GET.get('category')

        queryset = ScheduleItem.objects.filter(is_published=True)

        if year and year.isdigit():
            y = int(year)
            if month and month.isdigit():
                m = int(month)
                # Schedules that occur in or span into this month
                queryset = queryset.filter(
                    Q(start_date__year=y, start_date__month=m) |
                    Q(end_date__year=y, end_date__month=m)
                )
            else:
                queryset = queryset.filter(
                    Q(start_date__year=y) | Q(end_date__year=y)
                )

        if category and category != 'all':
            queryset = queryset.filter(category=category)

        queryset = queryset.order_by('start_date', 'start_time')

        events_data = []
        for item in queryset:
            events_data.append({
                'id': item.id,
                'title': item.title,
                'category': item.category,
                'category_display': item.get_category_display(),
                'category_color': item.category_color,
                'start_date': item.start_date.isoformat(),
                'end_date': item.end_date.isoformat() if item.end_date else None,
                'start_time': item.start_time.strftime('%I:%M %p') if item.start_time else None,
                'end_time': item.end_time.strftime('%I:%M %p') if item.end_time else None,
                'venue': item.venue,
                'description': item.description,
                'registration_link': item.registration_link,
                'attachment_url': item.attachment.url if item.attachment else None,
                'is_academic_calendar': item.is_academic_calendar,
                'is_multi_day': item.is_multi_day,
                'is_from_event': bool(item.source_event_id),
            })

        return JsonResponse({
            'status': 'success',
            'count': len(events_data),
            'schedules': events_data,
        })


# ==============================================================================
# Admin Event Views
# ==============================================================================

class ManageEventsView(AdminRequiredMixin, ListView):
    template_name = 'admin_panel/manage-events.html'
    context_object_name = 'events'
    paginate_by = 10

    def get_queryset(self):
        q = Event.objects.all()
        if term := self.request.GET.get('search'):
            q = q.filter(Q(title__icontains=term) | Q(venue__icontains=term) | Q(description__icontains=term))
        if category := self.request.GET.get('category'):
            q = q.filter(category=category)
        if status := self.request.GET.get('status'):
            q = q.filter(status=status)
        return q.order_by('-event_date', '-event_time')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = Event.Category.choices
        ctx['status_choices'] = Event.Status.choices
        ctx['total_events'] = Event.objects.count()
        ctx['upcoming_count'] = Event.objects.filter(status=Event.Status.UPCOMING).count()
        return ctx


class AddEventView(EditorRequiredMixin, CreateView):
    template_name = 'admin_panel/add-event.html'
    form_class = EventForm
    success_url = reverse_lazy('events:manage')

    def form_valid(self, form):
        messages.success(self.request, 'Event published and synchronized with Academic Calendar.')
        return super().form_valid(form)


class EditEventView(EditorRequiredMixin, UpdateView):
    template_name = 'admin_panel/add-event.html'
    model = Event
    form_class = EventForm
    success_url = reverse_lazy('events:manage')

    def form_valid(self, form):
        messages.success(self.request, 'Event updated and synchronized with Academic Calendar.')
        return super().form_valid(form)


class DeleteEventView(EditorRequiredMixin, DeleteView):
    model = Event
    success_url = reverse_lazy('events:manage')

    def form_valid(self, form):
        messages.success(self.request, 'Event deleted successfully.')
        return super().form_valid(form)


# ==============================================================================
# Admin Schedule / Academic Calendar Management Views
# ==============================================================================

class ManageSchedulesView(AdminRequiredMixin, ListView):
    template_name = 'admin_panel/manage-schedules.html'
    context_object_name = 'schedules'
    paginate_by = 15

    def get_queryset(self):
        q = ScheduleItem.objects.all()
        if term := self.request.GET.get('search'):
            q = q.filter(Q(title__icontains=term) | Q(venue__icontains=term) | Q(description__icontains=term))
        if category := self.request.GET.get('category'):
            q = q.filter(category=category)
        if academic := self.request.GET.get('academic'):
            if academic == 'true':
                q = q.filter(is_academic_calendar=True)
            elif academic == 'false':
                q = q.filter(is_academic_calendar=False)
        return q.order_by('-start_date')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = ScheduleItem.Category.choices
        ctx['total_schedules'] = ScheduleItem.objects.count()
        ctx['academic_schedules'] = ScheduleItem.objects.filter(is_academic_calendar=True).count()
        ctx['event_schedules'] = ScheduleItem.objects.filter(source_event__isnull=False).count()
        return ctx


class AddScheduleView(EditorRequiredMixin, CreateView):
    template_name = 'admin_panel/schedule-form.html'
    form_class = ScheduleItemForm
    success_url = reverse_lazy('events:admin_schedules')

    def form_valid(self, form):
        messages.success(self.request, 'Schedule item successfully added to the Academic Calendar.')
        return super().form_valid(form)


class EditScheduleView(EditorRequiredMixin, UpdateView):
    template_name = 'admin_panel/schedule-form.html'
    model = ScheduleItem
    form_class = ScheduleItemForm
    success_url = reverse_lazy('events:admin_schedules')

    def form_valid(self, form):
        messages.success(self.request, 'Schedule item successfully updated.')
        return super().form_valid(form)


class DeleteScheduleView(EditorRequiredMixin, DeleteView):
    model = ScheduleItem
    success_url = reverse_lazy('events:admin_schedules')

    def form_valid(self, form):
        messages.success(self.request, 'Schedule item removed from calendar.')
        return super().form_valid(form)
