import json
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404,redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView,ListView
from apps.accounts.permissions import AdminRequiredMixin,EditorRequiredMixin
from .forms import GalleryUploadForm
from .models import GalleryImage
class ManageGalleryView(AdminRequiredMixin,ListView):
    template_name='admin_panel/manage-gallery.html';context_object_name='images';paginate_by=24
    def get_queryset(self):
        q=GalleryImage.objects.all()
        if category:=self.request.GET.get('category'):q=q.filter(category__iexact=category)
        return q
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs);context['categories']=GalleryImage.objects.values_list('category',flat=True).distinct();context['upload_form']=GalleryUploadForm();return context
class UploadImageView(EditorRequiredMixin,View):
    def post(self,request):
        form=GalleryUploadForm(request.POST,request.FILES)
        if form.is_valid():
            for image in request.FILES.getlist('images'):GalleryImage.objects.create(title=image.name.rsplit('.',1)[0],image=image,category=form.cleaned_data['category'],uploaded_by=request.user)
            messages.success(request,'Gallery images uploaded.')
        else:messages.error(request,form.errors.as_text())
        return redirect('gallery:manage')
class EditImageView(EditorRequiredMixin,View):
    def patch(self,request,pk):
        image=get_object_or_404(GalleryImage,pk=pk)
        try:data=json.loads(request.body)
        except ValueError:return JsonResponse({'detail':'Invalid JSON.'},status=400)
        image.title=data.get('title',image.title).strip();image.category=data.get('category',image.category).strip();image.save(update_fields=['title','category'])
        return JsonResponse({'id':image.pk,'title':image.title,'category':image.category})
class DeleteImageView(EditorRequiredMixin,DeleteView):model=GalleryImage;success_url=reverse_lazy('gallery:manage')
