from django.contrib import messages
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from apps.accounts.permissions import AdminRequiredMixin, EditorRequiredMixin
from .forms import FacultyForm
from .models import Faculty


class FacultyListView(ListView):
    template_name = 'public/faculty.html'
    context_object_name = 'faculty'
    paginate_by = 12

    def get_queryset(self):
        q = Faculty.objects.filter(is_active=True)
        if designation := self.request.GET.get('designation'):
            q = q.filter(designation=designation)
        return q


class ManageFacultyView(AdminRequiredMixin, ListView):
    template_name = 'admin_panel/manage-faculty.html'
    context_object_name = 'faculty'
    paginate_by = 10

    def get_queryset(self):
        q = Faculty.objects.all()
        if term := self.request.GET.get('search'):
            q = q.filter(Q(name__icontains=term) | Q(specialization__icontains=term) | Q(email__icontains=term))
        if designation := self.request.GET.get('designation'):
            q = q.filter(designation=designation)
        return q.order_by('display_order', 'name')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['designation_choices'] = Faculty.Designation.choices
        ctx['total_faculty'] = Faculty.objects.count()
        ctx['active_count'] = Faculty.objects.filter(is_active=True).count()
        return ctx


class AddFacultyView(EditorRequiredMixin, CreateView):
    template_name = 'admin_panel/add-faculty.html'
    form_class = FacultyForm
    success_url = reverse_lazy('faculty:manage')

    def form_valid(self, form):
        messages.success(self.request, 'Faculty profile saved successfully.')
        return super().form_valid(form)


class EditFacultyView(EditorRequiredMixin, UpdateView):
    template_name = 'admin_panel/add-faculty.html'
    model = Faculty
    form_class = FacultyForm
    success_url = reverse_lazy('faculty:manage')

    def form_valid(self, form):
        messages.success(self.request, 'Faculty profile updated successfully.')
        return super().form_valid(form)


class DeleteFacultyView(EditorRequiredMixin, DeleteView):
    model = Faculty
    success_url = reverse_lazy('faculty:manage')

    def form_valid(self, form):
        messages.success(self.request, 'Faculty profile deleted successfully.')
        return super().form_valid(form)
