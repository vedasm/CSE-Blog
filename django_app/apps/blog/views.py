from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from apps.accounts.permissions import AdminRequiredMixin, EditorRequiredMixin, StudentRequiredMixin
from .forms import BlogForm, StudentBlogForm
from .models import Blog

class BlogListView(ListView):
    template_name='public/blogs.html'; context_object_name='blogs'; paginate_by=6
    def get_queryset(self):
        q=Blog.objects.filter(status='published').select_related('category','author')
        if term:=self.request.GET.get('search'): q=q.filter(Q(title__icontains=term)|Q(content__icontains=term)|Q(tags__icontains=term))
        if category:=self.request.GET.get('category'): q=q.filter(category__slug=category)
        return q
class BlogDetailView(DetailView):
    template_name='public/blog-details.html'; context_object_name='blog'; slug_field='slug'
    def get_queryset(self): return Blog.objects.filter(status='published').select_related('category','author')
    def get_object(self, queryset=None):
        obj=super().get_object(queryset); Blog.objects.filter(pk=obj.pk).update(views_count=obj.views_count+1); obj.views_count += 1; return obj
    def get_context_data(self, **kwargs):
        c=super().get_context_data(**kwargs); c['related_blogs']=Blog.objects.filter(status='published', category=self.object.category).exclude(pk=self.object.pk)[:3] if self.object.category else []; return c
class ManageBlogsView(AdminRequiredMixin, ListView):
    template_name = 'admin_panel/manage-blogs.html'
    context_object_name = 'blogs'
    paginate_by = 10

    def get_queryset(self):
        q = Blog.objects.select_related('category', 'author')
        if term := self.request.GET.get('search'):
            q = q.filter(Q(title__icontains=term) | Q(tags__icontains=term) | Q(content__icontains=term))
        if category := self.request.GET.get('category'):
            q = q.filter(category__slug=category)
        if status := self.request.GET.get('status'):
            q = q.filter(status=status)
        return q.order_by('-published_at', '-created_at')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from .models import Category
        ctx['categories'] = Category.objects.all()
        ctx['total_blogs'] = Blog.objects.count()
        ctx['published_count'] = Blog.objects.filter(status='published').count()
        ctx['draft_count'] = Blog.objects.filter(status='draft').count()
        ctx['pending_count'] = Blog.objects.filter(status='pending').count()
        ctx['approved_count'] = Blog.objects.filter(status='approved').count()
        ctx['rejected_count'] = Blog.objects.filter(status='rejected').count()
        return ctx

class AdminBlogDetailView(AdminRequiredMixin, DetailView):
    template_name = 'admin_panel/blog_review.html'
    model = Blog
    context_object_name = 'blog'

class AdminBlogApproveView(EditorRequiredMixin, View):
    def post(self, request, pk):
        blog = get_object_or_404(Blog, pk=pk)
        if blog.status == 'pending':
            blog.status = 'approved'
            blog.save()
            messages.success(request, 'Blog approved successfully.')
        else:
            messages.error(request, 'Only pending blogs can be approved.')
        return redirect('blog:detail', pk=pk)

class AdminBlogRejectView(EditorRequiredMixin, View):
    def post(self, request, pk):
        blog = get_object_or_404(Blog, pk=pk)
        reason = request.POST.get('rejection_reason', '').strip()
        if not reason:
            messages.error(request, 'A rejection reason is required.')
            return redirect('blog:detail', pk=pk)
        if blog.status == 'pending':
            blog.status = 'rejected'
            blog.rejection_reason = reason
            blog.save()
            messages.success(request, 'Blog has been rejected and student notified.')
        else:
            messages.error(request, 'Only pending blogs can be rejected.')
        return redirect('blog:detail', pk=pk)

class AdminBlogPublishView(EditorRequiredMixin, View):
    def post(self, request, pk):
        blog = get_object_or_404(Blog, pk=pk)
        if blog.status == 'approved':
            blog.status = 'published'
            if not blog.published_at:
                blog.published_at = timezone.now()
            blog.save()
            messages.success(request, 'Blog published successfully!')
        else:
            messages.error(request, 'Only approved blogs can be published.')
        return redirect('blog:detail', pk=pk)

class AdminBlogUnpublishView(EditorRequiredMixin, View):
    def post(self, request, pk):
        blog = get_object_or_404(Blog, pk=pk)
        if blog.status == 'published':
            blog.status = 'approved'
            blog.save()
            messages.success(request, 'Blog has been unpublished and reverted to approved.')
        else:
            messages.error(request, 'Only published blogs can be unpublished.')
        return redirect('blog:detail', pk=pk)
class AddBlogView(EditorRequiredMixin, CreateView):
    template_name='admin_panel/add-blog.html'; form_class=BlogForm; success_url=reverse_lazy('blog:manage')
    def form_valid(self, form):
        if not form.instance.author: form.instance.author=self.request.user
        messages.success(self.request,'Blog saved successfully.'); return super().form_valid(form)
class EditBlogView(EditorRequiredMixin, UpdateView):
    template_name='admin_panel/edit-blog.html'; form_class=BlogForm; model=Blog; success_url=reverse_lazy('blog:manage')
    def form_valid(self, form): messages.success(self.request,'Blog updated successfully.'); return super().form_valid(form)
class DeleteBlogView(EditorRequiredMixin, DeleteView):
    model=Blog; success_url=reverse_lazy('blog:manage')
    def post(self, request, *args, **kwargs): messages.success(request,'Blog deleted.'); return super().post(request,*args,**kwargs)

class StudentBlogListView(StudentRequiredMixin, ListView):
    template_name = 'student/student_dashboard.html'
    context_object_name = 'blogs'
    paginate_by = 10

    def get_queryset(self):
        return Blog.objects.filter(author=self.request.user).select_related('category').order_by('-updated_at', '-created_at')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['total_blogs'] = Blog.objects.filter(author=self.request.user).count()
        ctx['draft_count'] = Blog.objects.filter(author=self.request.user, status='draft').count()
        ctx['pending_count'] = Blog.objects.filter(author=self.request.user, status='pending').count()
        ctx['published_count'] = Blog.objects.filter(author=self.request.user, status='published').count()
        ctx['rejected_count'] = Blog.objects.filter(author=self.request.user, status='rejected').count()
        return ctx

class StudentBlogCreateView(StudentRequiredMixin, CreateView):
    template_name = 'student/student_blog_form.html'
    form_class = StudentBlogForm
    success_url = reverse_lazy('public_blog:my_blogs')

    def form_valid(self, form):
        form.instance.author = self.request.user
        action = self.request.POST.get('action', 'draft')
        if action == 'submit':
            form.instance.status = 'pending'
            messages.success(self.request, 'Blog submitted for review successfully!')
        else:
            form.instance.status = 'draft'
            messages.success(self.request, 'Blog draft saved successfully.')
        return super().form_valid(form)

class StudentBlogUpdateView(StudentRequiredMixin, UpdateView):
    template_name = 'student/student_blog_form.html'
    form_class = StudentBlogForm
    model = Blog
    success_url = reverse_lazy('public_blog:my_blogs')

    def get_queryset(self):
        return Blog.objects.filter(author=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.status not in {'draft', 'rejected'}:
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied("You can only edit draft or rejected blogs.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        action = self.request.POST.get('action', 'draft')
        if action == 'submit':
            form.instance.status = 'pending'
            messages.success(self.request, 'Blog updated and submitted for review!')
        else:
            form.instance.status = 'draft'
            messages.success(self.request, 'Blog updates saved as draft.')
        return super().form_valid(form)

class StudentBlogSubmitView(StudentRequiredMixin, View):
    def post(self, request, pk):
        blog = get_object_or_404(Blog, pk=pk, author=request.user)
        if blog.status in {'draft', 'rejected'}:
            blog.status = 'pending'
            blog.save()
            messages.success(request, 'Blog submitted for review successfully!')
        else:
            messages.error(request, 'Only draft or rejected blogs can be submitted.')
        return redirect('public_blog:my_blogs')

class StudentBlogDetailView(StudentRequiredMixin, DetailView):
    template_name = 'student/student_blog_detail.html'
    context_object_name = 'blog'

    def get_queryset(self):
        return Blog.objects.filter(author=self.request.user)
