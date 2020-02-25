from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404

from .forms import ProductForm, RawProductForm
from .models import Product

def product_list_view(request):
	queryset = Product.objects.all()
	context = {
		"object_list": queryset
	}
	return render(request, "product_list.html", context)

def dynamic_lookup_view(request, id):
	# obj = Product.objects.get(id=id)
	# obj = get_object_or_404(Product, id=id)
	try:
		obj = Product.objects.get(id=id)
	except Product.DoesNotExist:
		raise Http404
	context = {
		"object": obj
	}
	return render(request, "product_detail.html", context)

def product_delete_view(request, id):
	obj = get_object_or_404(Product, id=id)

	if request.method == "POST":
		obj.delete()
		return redirect('../../')
	obj.delete()
	context = {
		"object": obj
	}
	return render(request, "product_delete.html", context)

def render_initial_form(request):
	initial_data = {
		'title': "My this awesome title"
	}
	obj = Product.objects.get(id=1)
	form = RawProductForm(request.POST or None, instance=obj)
	if form.is_valid():
		form.save()
	context = {
		'form': form
	}
	return render(request, 'product_create.html', context)

# Create your views here.
def product_create_view(request):
	form = ProductForm(request.POST or None)
	if form.is_valid():
		form.save()
		form = ProductForm()

	context = {
		'form': form
	}
	return render(request, "product_create.html", context)

# def product_create_view(request):
# 	context = {}
# 	title = request.POST.get('title')
# 	print(title)
# 	# Product.objects.create(title=my_new_title)

# 	return render(request, "product_create.html", context)

# def product_create_view(request):
# 	form = RawProductForm()
# 	if request.method == "POST":
# 		form = RawProductForm(request.POST)
# 		if form.is_valid():
# 			# now the data is good
# 			print(form.cleaned_data)

# 		else:
# 			print(form.errors)
# 	context = {
# 		"form": form
# 	}
# 	# Product.objects.create(title=my_new_title)

# 	return render(request, "product_create.html", context)

# Create your views here.
def product_detail_view(request):
	obj = Product.objects.get(id=1)
	context = {
		'object': obj
	}
	return render(request, "product_detail.html", context)