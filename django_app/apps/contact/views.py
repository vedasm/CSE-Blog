from django.contrib import messages
from django.shortcuts import redirect,render
from django.utils import timezone
from django.views import View
from django.views.generic import ListView
from apps.accounts.permissions import AdminRequiredMixin
from .forms import ContactForm
from .models import ContactMessage
from .tasks import send_contact_notification
class ContactView(View):
    template_name='public/contact.html'
    def get(self,request):return render(request,self.template_name,{'form':ContactForm()})
    def post(self,request):
        form=ContactForm(request.POST)
        if form.is_valid():
            message=form.save();send_contact_notification.delay(message.pk);messages.success(request,"Message sent! We'll get back to you soon.");return redirect('contact:contact')
        return render(request,self.template_name,{'form':form})
class MessagesView(AdminRequiredMixin,ListView):
    template_name='admin_panel/messages.html';context_object_name='messages_list';paginate_by=20;queryset=ContactMessage.objects.all()
    def post(self,request,*args,**kwargs):
        item=ContactMessage.objects.get(pk=request.POST['message_id']);item.is_read=True;item.replied_at=timezone.now();item.save(update_fields=['is_read','replied_at']);messages.success(request,'Message marked as read.');return self.get(request,*args,**kwargs)
