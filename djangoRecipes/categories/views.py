from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from rest_framework.generics import UpdateAPIView, DestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated

from djangoRecipes.categories.forms import CategoryForm
from djangoRecipes.categories.models import Category
from djangoRecipes.categories.serializers import CategorySerializer
from djangoRecipes.common.forms import SearchForm


class AddCategoryView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "categories/add-category-view.html"
    success_url = reverse_lazy("list-categories")

    def form_valid(self, form):
        category = form.save(commit=False)
        category.user = self.request.user

        return super().form_valid(form)


class CategoryListView(ListView):
    model = Category
    template_name = "categories/list-categories-views.html"


class CategoryEditDeleteView(UpdateAPIView, DestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        category_id = self.kwargs.get('pk')
        return get_object_or_404(Category, pk=category_id)

    # def update(self, request, *args, **kwargs):
    #     comment = self.get_object()
    #
    #     if request.user != comment.user:
    #         return Response({'success': False, 'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    #
    #     serializer = CommentSerializer(comment, data=request.data, partial=True)
    #
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({'success': True, 'description': serializer.data['description']})
    #
    #     return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CategoryRecipesView(ListView):
    template_name = "recipes/dashboard.html"
    context_object_name = 'recipes'
    paginate_by = 4

    def get_queryset(self):
        category = get_object_or_404(Category, pk=self.kwargs['pk'])
        queryset = category.recipes.all()

        search_query = self.request.GET.get('search_criteria', '').strip()
        if search_query:
            queryset = queryset.filter(recipe_name__icontains=search_query)

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recipes"] = context["page_obj"]
        context['search_form'] = SearchForm(self.request.GET)

        return context