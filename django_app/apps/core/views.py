import datetime
import json
from django.contrib import messages
from django.db.models import Q, Sum
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from apps.accounts.permissions import AdminRequiredMixin, EditorRequiredMixin
from apps.blog.models import Blog
from apps.events.models import Event, ScheduleItem
from apps.faculty.models import Faculty
from apps.contact.models import ContactMessage
from apps.news.models import NewsItem
from .forms import DepartmentDocumentForm, PlacementStatForm, DepartmentMilestoneForm, DepartmentLabForm
from .models import SiteSettings, DepartmentDocument, PlacementStat, DepartmentLab, DepartmentMilestone


class HomeView(TemplateView):
    template_name = 'public/index.html'

    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        today = datetime.date.today()
        c.update(
            featured_blog=Blog.objects.filter(status='published').order_by('-published_at').first(),
            latest_blogs=Blog.objects.filter(status='published').order_by('-published_at')[:4],
            upcoming_events=Event.objects.filter(status='upcoming').order_by('event_date')[:3],
            settings=SiteSettings.current(),
            faculty=Faculty.objects.filter(is_active=True).order_by('display_order')[:4],
            latest_news=NewsItem.objects.filter(is_published=True).order_by('-is_pinned', '-published_at', '-created_at')[:8],
            pinned_news=NewsItem.objects.filter(is_published=True, is_pinned=True).order_by('-published_at', '-created_at')[:3],
            news_categories=NewsItem.Category.choices,
            upcoming_schedules=ScheduleItem.objects.filter(is_published=True, start_date__gte=today).order_by('start_date', 'start_time')[:6],
            schedule_categories=ScheduleItem.Category.choices,

            # Official Department Information & Milestones
            department_milestones=DepartmentMilestone.objects.filter(is_active=True).order_by('display_order'),
            placement_stats=PlacementStat.objects.filter(is_published=True).order_by('year'),
            recent_placement_stats=PlacementStat.objects.filter(is_published=True).order_by('-year')[:5],
            research_documents=DepartmentDocument.objects.filter(category=DepartmentDocument.Category.RESEARCH, is_published=True).order_by('display_order')[:4],
            achievement_documents=DepartmentDocument.objects.filter(category=DepartmentDocument.Category.ACHIEVEMENT, is_published=True).order_by('display_order')[:4],
            department_labs=DepartmentLab.objects.all().order_by('display_order')[:6],
            alumni_documents=DepartmentDocument.objects.filter(category=DepartmentDocument.Category.ALUMNI, is_published=True).order_by('display_order')[:4],
        )
        return c


class PlacementsView(TemplateView):
    template_name = 'public/placements.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        records = PlacementStat.objects.filter(is_published=True).order_by('year')
        total_students = records.aggregate(total=Sum('students_placed'))['total'] or 0
        latest_record = records.last()

        # Chart JSON data
        chart_data = {
            'labels': [str(r.year) for r in records],
            'placed': [r.students_placed for r in records],
            'offers': [r.total_offers or r.students_placed for r in records]
        }

        ctx.update(
            placement_records=records.reverse(),
            chart_data_json=json.dumps(chart_data),
            total_students_placed=total_students,
            latest_record=latest_record,
            placement_documents=DepartmentDocument.objects.filter(category=DepartmentDocument.Category.PLACEMENT, is_published=True),
            milestones=DepartmentMilestone.objects.filter(is_active=True).order_by('display_order')
        )
        return ctx


class ResearchView(TemplateView):
    template_name = 'public/research.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['research_documents'] = DepartmentDocument.objects.filter(
            category=DepartmentDocument.Category.RESEARCH,
            is_published=True
        ).order_by('display_order')
        ctx['centre_document'] = DepartmentDocument.objects.filter(
            category=DepartmentDocument.Category.RESEARCH,
            title__icontains='Centre'
        ).first()
        return ctx


class AchievementsView(TemplateView):
    template_name = 'public/achievements.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['achievement_documents'] = DepartmentDocument.objects.filter(
            category=DepartmentDocument.Category.ACHIEVEMENT,
            is_published=True
        ).order_by('display_order')
        ctx['milestones'] = DepartmentMilestone.objects.filter(is_active=True).order_by('display_order')
        return ctx


class InfrastructureView(TemplateView):
    template_name = 'public/infrastructure.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['labs'] = DepartmentLab.objects.all().order_by('display_order')
        ctx['library_doc'] = DepartmentDocument.objects.filter(
            category=DepartmentDocument.Category.LIBRARY,
            is_published=True
        ).first()
        return ctx


class AlumniView(TemplateView):
    template_name = 'public/alumni.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['alumni_documents'] = DepartmentDocument.objects.filter(
            category=DepartmentDocument.Category.ALUMNI,
            is_published=True
        ).order_by('display_order')
        return ctx


class DashboardView(AdminRequiredMixin, TemplateView):
    template_name = 'admin_panel/dashboard.html'

    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        c.update(
            total_blogs=Blog.objects.count(),
            published_blogs=Blog.objects.filter(status='published').count(),
            pending_blogs=Blog.objects.filter(status='pending').count(),
            total_events=Event.objects.count(),
            upcoming_events=Event.objects.filter(status='upcoming').count(),
            total_faculty=Faculty.objects.filter(is_active=True).count(),
            total_news=NewsItem.objects.count(),
            pinned_news=NewsItem.objects.filter(is_pinned=True).count(),
            total_schedules=ScheduleItem.objects.count(),
            total_documents=DepartmentDocument.objects.count(),
            unread_messages=ContactMessage.objects.filter(is_read=False).count(),
            recent_blogs=Blog.objects.order_by('-created_at')[:5],
            recent_news=NewsItem.objects.order_by('-created_at')[:5],
            recent_messages=ContactMessage.objects.order_by('-created_at')[:5]
        )
        return c


# ==============================================================================
# Admin Document & Department Archive Management Views
# ==============================================================================

class ManageDocumentsView(AdminRequiredMixin, ListView):
    template_name = 'admin_panel/manage-documents.html'
    context_object_name = 'documents'
    paginate_by = 15

    def get_queryset(self):
        q = DepartmentDocument.objects.all()
        if term := self.request.GET.get('search'):
            q = q.filter(Q(title__icontains=term) | Q(academic_year__icontains=term) | Q(description__icontains=term))
        if category := self.request.GET.get('category'):
            q = q.filter(category=category)
        return q.order_by('category', 'display_order', '-created_at')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = DepartmentDocument.Category.choices
        ctx['total_docs'] = DepartmentDocument.objects.count()
        ctx['research_count'] = DepartmentDocument.objects.filter(category=DepartmentDocument.Category.RESEARCH).count()
        ctx['achievement_count'] = DepartmentDocument.objects.filter(category=DepartmentDocument.Category.ACHIEVEMENT).count()
        return ctx


class AddDocumentView(EditorRequiredMixin, CreateView):
    template_name = 'admin_panel/document-form.html'
    form_class = DepartmentDocumentForm
    success_url = reverse_lazy('core_admin:manage_documents')

    def form_valid(self, form):
        messages.success(self.request, 'Department document uploaded successfully.')
        return super().form_valid(form)


class EditDocumentView(EditorRequiredMixin, UpdateView):
    template_name = 'admin_panel/document-form.html'
    model = DepartmentDocument
    form_class = DepartmentDocumentForm
    success_url = reverse_lazy('core_admin:manage_documents')

    def form_valid(self, form):
        messages.success(self.request, 'Department document updated successfully.')
        return super().form_valid(form)


class DeleteDocumentView(EditorRequiredMixin, DeleteView):
    model = DepartmentDocument
    success_url = reverse_lazy('core_admin:manage_documents')

    def form_valid(self, form):
        messages.success(self.request, 'Department document deleted successfully.')
        return super().form_valid(form)


class ManagePlacementsView(AdminRequiredMixin, ListView):
    template_name = 'admin_panel/manage-placements.html'
    model = PlacementStat
    context_object_name = 'placements'


class AddPlacementView(EditorRequiredMixin, CreateView):
    template_name = 'admin_panel/placement-form.html'
    form_class = PlacementStatForm
    success_url = reverse_lazy('core_admin:manage_placements')

    def form_valid(self, form):
        messages.success(self.request, 'Placement record added successfully.')
        return super().form_valid(form)


class EditPlacementView(EditorRequiredMixin, UpdateView):
    template_name = 'admin_panel/placement-form.html'
    model = PlacementStat
    form_class = PlacementStatForm
    success_url = reverse_lazy('core_admin:manage_placements')

    def form_valid(self, form):
        messages.success(self.request, 'Placement record updated successfully.')
        return super().form_valid(form)


class DeletePlacementView(EditorRequiredMixin, DeleteView):
    model = PlacementStat
    success_url = reverse_lazy('core_admin:manage_placements')

    def form_valid(self, form):
        messages.success(self.request, 'Placement record deleted successfully.')
        return super().form_valid(form)


class ManageLabsView(AdminRequiredMixin, ListView):
    template_name = 'admin_panel/manage-labs.html'
    model = DepartmentLab
    context_object_name = 'labs'


class AddLabView(EditorRequiredMixin, CreateView):
    template_name = 'admin_panel/lab-form.html'
    form_class = DepartmentLabForm
    success_url = reverse_lazy('core_admin:manage_labs')

    def form_valid(self, form):
        messages.success(self.request, 'Laboratory record added successfully.')
        return super().form_valid(form)


class EditLabView(EditorRequiredMixin, UpdateView):
    template_name = 'admin_panel/lab-form.html'
    model = DepartmentLab
    form_class = DepartmentLabForm
    success_url = reverse_lazy('core_admin:manage_labs')

    def form_valid(self, form):
        messages.success(self.request, 'Laboratory record updated successfully.')
        return super().form_valid(form)


class DeleteLabView(EditorRequiredMixin, DeleteView):
    model = DepartmentLab
    success_url = reverse_lazy('core_admin:manage_labs')

    def form_valid(self, form):
        messages.success(self.request, 'Laboratory record deleted successfully.')
        return super().form_valid(form)
