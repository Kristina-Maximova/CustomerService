from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from ..forms import AddresseeForm
from ..models import Addressee


class AddresseeCreateView(LoginRequiredMixin, CreateView):
    """ Отображение получателя почты"""
    model = Addressee
    form_class = AddresseeForm
    template_name = 'sender/addressee/addressee_form.html'
    success_url = reverse_lazy('sender:addressees_list')

    def form_valid(self, form):
        addressee = form.save()
        user = self.request.user
        addressee.owner = user
        addressee.save()

        return super().form_valid(form)


class AddresseeUpdateView(LoginRequiredMixin, UpdateView):
    model = Addressee
    form_class = AddresseeForm
    template_name = 'sender/addressee/addressee_form.html'
    success_url = reverse_lazy('sender:addressees_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not (self.request.user == obj.owner):
            raise PermissionDenied("У вас нет прав редактировать адресата.")
        return obj


class AddresseeDetailView(LoginRequiredMixin, DetailView):
    model = Addressee
    template_name = 'sender/addressee/addressee_detail.html'
    context_object_name = 'addressee'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not (self.request.user == obj.owner or self.request.user.groups.filter(name='manager').exists()):
            raise PermissionDenied("У вас нет прав просматривать информацию об адресатах.")
        return obj


class AddresseeDeleteView(LoginRequiredMixin, DeleteView):
    model = Addressee
    template_name = 'sender/addressee/addressee_confirm_delete.html'
    success_url = reverse_lazy('sender:addressees_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not (self.request.user == obj.owner):
            raise PermissionDenied("У вас нет прав удалять адресата.")
        return obj


class AddresseeListView(LoginRequiredMixin, ListView):
    model = Addressee
    template_name = 'sender/addressee/addressees_list.html'
    context_object_name = 'addressees'

    def get_queryset(self):
        if self.request.user.groups.filter(name='Managers').exists() or self.request.user.is_superuser:
            queryset = cache.get('addressee_queryset')
            if not queryset:
                queryset = super().get_queryset()
                cache.set('addressee_queryset', queryset, 15)
            return queryset
        else:
            return super().get_queryset().filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['is_manager'] = self.request.user.groups.filter(name='Managers').exists()
        return context
