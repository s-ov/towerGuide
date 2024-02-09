from typing import Any, Dict
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.views.generic.edit import DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView

from .utils import DataMixin
from .forms import NodeForm, LoginUserForm
from .filters import NodeFilter
from .models import (DistributiveSubstation as DS,
                     MotorControlCenter as MCC, 
                     Node)


class HomeView(DataMixin, ListView):
    template_name = 'locator/base.html'
    context_object_name = 'substations'
    title_page = 'Гoлoвна'

    def get_queryset(self) -> QuerySet[Any]:
        return DS.objects.all()
    

class SubstationView(DataMixin, ListView):
    template_name = 'locator/mcc.html'
    context_object_name = 'rooms'

    def get_queryset(self):
        return MCC.objects.filter(substation__id=self.kwargs['sub_num'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        substation = DS.objects.get(id=self.kwargs['sub_num'])
        context['title'] = substation.title
        return context


class MCCView(DataMixin, ListView):
    template_name = 'locator/nodes.html'
    context_object_name = 'nodes'

    def get_queryset(self) -> QuerySet[Any]:
        # mcc__slug=self.kwargs['mcc_slug']
        return Node.objects.filter(mcc__slug=self.kwargs['mcc_slug'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mcc = MCC.objects.get(slug=self.kwargs['mcc_slug'])
        context['title'] = f'{mcc.title}(PП-{mcc.substation_id + 3})'
        return context
    

class NodeView(DetailView):
    template_name = 'locator/node.html'
    context_object_name = 'node'
    slug_url_kwarg = 'slug'

    def get_object(self):
        return get_object_or_404(Node, slug=self.kwargs[self.slug_url_kwarg])
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        node = Node.objects.get(slug=self.kwargs['slug'])
        context['title'] = f'{node.title}_{node.slug}'
        return context
    

class AddNodeView(PermissionRequiredMixin, DataMixin, CreateView):
    model = Node
    form_class = NodeForm 
    template_name = 'locator/add_node.html'
    success_url = reverse_lazy('home')

    title_page = 'Сторінка форми'
    permission_required = 'locator.add_node' 
 

class UpdateNodeView(PermissionRequiredMixin, DataMixin, UpdateView):
    model = Node
    form_class = NodeForm
    template_name = 'locator/add_node.html'
    success_url = reverse_lazy('home')
    
    title_page = 'Сторінка редагування'
    permission_required = 'locator.change_node'


class SearchNodeView(PermissionRequiredMixin, DataMixin, ListView):
    queryset = Node.objects.all()
    template_name = 'locator/search_node.html'
    context_object_name = 'node'
    title_page = 'Сторінка пошуку'
    permission_required = 'locator.view_node'

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        self.filterset = NodeFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form'] = self.filterset.form
        return context
    

class NodeDeleteView(DeleteView):
    model = Node
    template_name = 'locator/delete_node.html'
    success_url = reverse_lazy('home')
    slug_url_kwarg = 'slug'
    context_object_name = 'node_instance'

    def get_object(self, queryset=None):
        # Use slug parameter for lookup
        slug = self.kwargs.get('slug')
        return get_object_or_404(Node, slug=slug)

    def form_valid(self, form):
        self.object = self.get_object()
        self.object.delete()
        return redirect('node_delete_confirm')
    

class NodeDeleteConfirmView(TemplateView):
    template_name = 'locator/node_confirm_delete.html'


class LoginUserView(LoginView):
    form_class = LoginUserForm
    template_name = 'locator/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Вхід у застосунок'
        return context

    # def get_success_url(self):
    #     return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')
