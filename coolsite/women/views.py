from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView

from women.forms import AddPostForm, UploadFileForm
from women.models import Women, Category, TagPost, UploadFiles
from women.utils import DataMixin


class WomenHome(DataMixin, ListView):
    # model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'
    cat_selected = 0

    def get_queryset(self):
        return Women.published.all().select_related('cat')

    # Для передачи динамических полей через get
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Главная страница'
    #     context['menu'] = menu
    #     context['posts'] = Women.published.all().select_related('cat')
    #     context['cat_selected'] = int(self.request.GET.get('cat_id', 0))
    #     return context

@login_required
def about(request):
    contact_list = Women.published.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # if request.method == 'POST':
    #     # handle_uploaded_file(request.FILES['file_upload'])
    #     form = UploadFileForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         upload_files = UploadFiles(file=form.cleaned_data['file'])
    #         upload_files.save()
    # else:
    #     form = UploadFileForm()
    return render(request, 'women/about.html',
                  {'title': 'О сайте', 'page_obj': page_obj})


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#
#     data = {
#         'title': post.title,
#         # 'menu': menu,
#         'post': post,
#         'cat_selected': 1
#     }
#     return render(request, 'women/post.html', data)

class ShowPost(DataMixin, DetailView):
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])


class AddPage(LoginRequiredMixin,DataMixin,CreateView):
    form_class = AddPostForm  # ссылка на класс
    template_name = 'women/add_page.html'
    title_page = 'Добавление статьи'

    def form_valid(self, form):
        w = form.save(commit=False)  # объект новой записи для БД без занесения в БД
        w.author = self.request.user  # объект текущего пользователя
        return super().form_valid(form)



class UpdatePage(DataMixin, UpdateView):
    model = Women
    fields = ['title', 'content', 'photo', 'is_published', 'cat']  # все обязательные поля должны быть
    template_name = 'women/add_page.html'
    success_url = reverse_lazy('home')  # маршрут выстраивается не сразу, а только когда необходим
    title_page = 'Редактирование статьи'


class DeletePage(DataMixin, DeleteView):
    model = Women
    fields = '__all__'  # все обязательные поля должны быть
    template_name = 'women/delete.html'
    success_url = reverse_lazy('home')  # маршрут выстраивается не сразу, а только когда необходим
    title_page = 'Удаление записей'


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


class WomenCategory(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context,
                                      title='Категория - ' + cat.name,
                                      cat_selected=cat.pk)


# def show_tag_postlist(request, tag_slug):
#     tag = get_object_or_404(TagPost, slug=tag_slug)
#     posts = tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related('cat')
#
#     data = {
#         'title': f'Тег: {tag.tag}',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': None,  # Синим не отображается выбранная категория
#     }
#
#     return render(request, 'women/index.html', context=data)

class TagPostList(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False
    # tag = get_object_or_404(TagPost, slug=tag_slug)

    def get_queryset(self):
        return Women.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title=f'Тег: {tag.tag}')
