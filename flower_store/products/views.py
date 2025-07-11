from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from .models import Comment
from django.shortcuts import get_object_or_404
from .forms import CommentCreateForm
from django.contrib import messages
from django.shortcuts import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from orders.forms import CartAddForm
from .models import Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class ProductDetailView(View):
    form_class = CommentCreateForm

    def setup(self, request, *args, **kwargs):
        self.product = get_object_or_404(Product, slug=kwargs['slug_product'])
        self.comments = self.product.product_comments.filter(is_reply=False)
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        purchase_form = CartAddForm
        return render(request, 'products/product.html',
                      context={'product': self.product, 'comments': self.comments, 'form': self.form_class,
                               'purchase_form': purchase_form})

    @method_decorator(login_required)
    def post(self, request, slug_product):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.product = self.product
            new_comment.save()
            messages.success(request, 'your comment submitted successfully', 'success')
            return redirect(reverse('products:detail_view', args=(slug_product,)))
        return render(request, 'products/product.html',
                      context={'product': self.product, 'comments': self.comments, 'form': self.form_class})


class ProductReplyCommentView(LoginRequiredMixin, View):
    def post(self, request, product_id, comment_id):
        form_class = CommentCreateForm
        product = get_object_or_404(Product, id=product_id)
        comment = get_object_or_404(Comment, id=comment_id)
        all_comment = product.product_comments.filter(is_reply=False)
        form = form_class(request.POST)
        if form.is_valid():
            reply_comment = form.save(commit=False)
            reply_comment.user = request.user
            reply_comment.product = product
            reply_comment.reply = comment
            reply_comment.is_reply = True
            reply_comment.save()
            messages.success(request, 'your answer was successfully registered', 'success')
            return redirect(reverse('products:detail_view', args=(product.slug,)))
        return render(request, 'products/product.html',
                      context={'form': form, 'product': product, 'comments': all_comment})


class ShowAllProducts(View):
    def get(self, request):
        products = Product.objects.all()
        paginator = Paginator(products, 3)
        page = request.GET.get('page', 1)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        return render(request, "products/show-all-products.html",
                      context={'products': products, 'paginator': paginator})
