from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotAllowed
from django.urls import reverse
from django.utils.timezone import make_naive
from django.views.generic import ListView, TemplateView, FormView

from webapp.models import Tipe
from .forms import TipeForm, BROWSER_DATETIME_FORMAT, SimpleSearchForm
from .base_views import FormView as CustomFormView, ListView as CustomListView


class IndexView(ListView):
    template_name = 'index.html'
    context_object_name = 'tipes'
    paginate_by = 2
    paginate_orphans = 0

    def get_context_data(self, *, object_list=None, **kwargs):
        form = SimpleSearchForm(data=self.request.GET)
        if form.is_valid():
            search = form.cleaned_data['search']
            kwargs['search'] = search
        kwargs['form'] = form
        return super().get_context_data(object_list=object_list, **kwargs)

    def get_queryset(self):
        data = Tipe.objects.all()

        if not self.request.GET.get('is_admin', None):
            data = Tipe.objects.filter(status='In Progress')

        # http://localhost:8000/?search=ygjkjhg
        form = SimpleSearchForm(data=self.request.GET)
        if form.is_valid():
            search = form.cleaned_data['search']
            if search:
                data = data.filter(Q(title__icontains=search) | Q(author__icontains=search))

        return data.order_by('-created_at')


class TipeView(TemplateView):
    template_name = 'tipe_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs.get('pk')
        tipe = get_object_or_404(Tipe, pk=pk)

        context['tipe'] = tipe
        return context


class TipeCreateView(CustomFormView):
    template_name = 'tipe_create.html'
    form_class = TipeForm

    def form_valid(self, form):
        self.tipe = form.save()
        return super().form_valid(form)

    def get_redirect_url(self):
        return reverse('tipe_view', kwargs={'pk': self.tipe.pk})


class TipeUpdateView(FormView):
    template_name = 'tipe_update.html'
    form_class = TipeForm

    def dispatch(self, request, *args, **kwargs):
        self.tipe = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipe'] = self.tipe
        return context

    def get_initial(self):
        return {'publish_at': make_naive(self.tipe.publish_at)\
            .strftime(BROWSER_DATETIME_FORMAT)}

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.tipe
        return kwargs

    def form_valid(self, form):
        self.tipe = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tipe_view', kwargs={'pk': self.tipe.pk})

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Tipe, pk=pk)


def tipe_delete_view(request, pk):
    tipe = get_object_or_404(Tipe, pk=pk)
    if request.method == 'GET':
        return render(request, 'tipe_delete.html', context={'tipe': tipe})
    elif request.method == 'POST':
        tipe.delete()
        return redirect('index')
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])
