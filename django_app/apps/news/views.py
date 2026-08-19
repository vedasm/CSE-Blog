from django.contrib import messages
from django.db.models import F, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from apps.accounts.permissions import AdminRequiredMixin, EditorRequiredMixin
from .forms import NewsForm
from .models import NewsItem


# -------------------- Public Views -------------------- #

class NewsListView(ListView):
    template_name = 'public/news-list.html'
    context_object_name = 'news_items'
    paginate_by = 10

    def get_queryset(self):
        qs = NewsItem.objects.filter(is_published=True)
        if search := self.request.GET.get('search'):
            qs = qs.filter(
                Q(title__icontains=search) |
                Q(summary__icontains=search) |
                Q(content__icontains=search)
            )
        if category := self.request.GET.get('category'):
            qs = qs.filter(category=category)
        return qs.order_by('-is_pinned', '-published_at', '-created_at')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = NewsItem.Category.choices
        ctx['selected_category'] = self.request.GET.get('category', '')
        ctx['search_term'] = self.request.GET.get('search', '')
        ctx['pinned_count'] = NewsItem.objects.filter(is_published=True, is_pinned=True).count()
        return ctx


class NewsDetailView(DetailView):
    template_name = 'public/news-detail.html'
    model = NewsItem
    context_object_name = 'news'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return NewsItem.objects.filter(is_published=True)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        # Increment views atomically
        NewsItem.objects.filter(pk=obj.pk).update(views_count=F('views_count') + 1)
        obj.refresh_from_db(fields=['views_count'])
        return obj

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['recent_news'] = NewsItem.objects.filter(
            is_published=True
        ).exclude(pk=self.object.pk).order_by('-published_at')[:4]
        return ctx


class NewsJsonFeedView(View):
    """JSON feed for fluid instant client-side filtering on the homepage."""
    def get(self, request, *args, **kwargs):
        category = request.GET.get('category')
        limit = int(request.GET.get('limit', 8))
        qs = NewsItem.objects.filter(is_published=True)
        if category and category != 'all':
            if category == 'urgent':
                qs = qs.filter(is_pinned=True)
            else:
                qs = qs.filter(category=category)
        qs = qs.order_by('-is_pinned', '-published_at', '-created_at')[:limit]

        data = []
        for item in qs:
            data.append({
                'id': item.id,
                'title': item.title,
                'slug': item.slug,
                'category': item.category,
                'category_display': item.get_category_display(),
                'summary': item.summary or item.content[:160],
                'content': item.content,
                'is_pinned': item.is_pinned,
                'has_attachment': bool(item.attachment),
                'attachment_url': item.attachment.url if item.attachment else '',
                'external_link': item.external_link,
                'published_at': item.published_at.strftime('%d %b %Y') if item.published_at else '',
                'detail_url': f"/news/{item.slug}/",
            })
        return JsonResponse({'news': data})


# -------------------- Admin Views -------------------- #

class ManageNewsView(AdminRequiredMixin, ListView):
    template_name = 'admin_panel/manage-news.html'
    context_object_name = 'news_items'
    paginate_by = 12

    def get_queryset(self):
        qs = NewsItem.objects.all()
        if term := self.request.GET.get('search'):
            qs = qs.filter(
                Q(title__icontains=term) |
                Q(summary__icontains=term)
            )
        if cat := self.request.GET.get('category'):
            qs = qs.filter(category=cat)
        return qs.order_by('-is_pinned', '-published_at', '-created_at')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['total_news'] = NewsItem.objects.count()
        ctx['pinned_news'] = NewsItem.objects.filter(is_pinned=True).count()
        ctx['published_news'] = NewsItem.objects.filter(is_published=True).count()
        ctx['categories'] = NewsItem.Category.choices
        return ctx


class AddNewsView(EditorRequiredMixin, CreateView):
    template_name = 'admin_panel/add-news.html'
    form_class = NewsForm
    success_url = reverse_lazy('news:manage')

    def form_valid(self, form):
        messages.success(self.request, 'News bulletin published successfully.')
        return super().form_valid(form)


class EditNewsView(EditorRequiredMixin, UpdateView):
    template_name = 'admin_panel/edit-news.html'
    model = NewsItem
    form_class = NewsForm
    success_url = reverse_lazy('news:manage')

    def form_valid(self, form):
        messages.success(self.request, 'News bulletin updated successfully.')
        return super().form_valid(form)


class DeleteNewsView(EditorRequiredMixin, DeleteView):
    model = NewsItem
    success_url = reverse_lazy('news:manage')

    def form_valid(self, form):
        messages.success(self.request, 'News bulletin removed.')
        return super().form_valid(form)


class TogglePinNewsView(EditorRequiredMixin, View):
    def post(self, request, pk):
        item = get_object_or_404(NewsItem, pk=pk)
        item.is_pinned = not item.is_pinned
        item.save(update_fields=['is_pinned'])
        status_msg = 'pinned as urgent' if item.is_pinned else 'unpinned'
        messages.success(request, f'News "{item.title}" {status_msg}.')
        return redirect('news:manage')
