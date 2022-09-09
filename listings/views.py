from django.http import HttpResponse
from django.shortcuts import render, redirect
from listings.models import Product, Alternative
from listings.forms import RegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist


def hello(request):
    return HttpResponse('<h1>Hello Django!</h1>')


def home(request):
    """home page"""
    return render(request, 'pages/index.html')


def search(request):
    """Research page :
    if 1 product match the research, display it with it's alternative
    if no product match the research, try to find result containing research
    if 1 product match the new research, display it with it's alternative
    if several product match the new research, display them all
    if no product match the new research, display no product found
    """
    try:
        search = request.GET['name']
        product = Product.objects.get(name__iexact=search)
        context = {'product': product}
    except Product.DoesNotExist:
        products = Product.objects.filter(name__icontains=search)
        if not products:
            context = {'error': 'Aucun produit correspondant'}
        elif len(products) == 1:
            context = {'product': products[0]}
        else:
            context = {'products': products}
    except:
        context = {'error': 'Aucun produit correspondant'}
    """if we got only one product, let's find his alternative products"""
    try:
        product = context['product']
    except:
        pass
    else:
        try:
            alternatives = Product.objects.filter(nutriscore__lt=product.nutriscore,
                                                  category=product.category
                                                  ).order_by('nutrigrade', 'name')
            if request.user.is_authenticated:
                saved = Alternative.objects.filter(user=request.user).values('product')
                alternatives = alternatives.exclude(pk__in=saved)
            if alternatives:
                context['alternatives'] = alternatives
            else:
                raise Exception()
        except:
            context['no_alternatives'] = 'Aucun meilleur produit trouvé'
    return render(request, 'pages/search.html', context)


def product(request, product_name):
    """Product page"""
    name = product_name
    try:
        product = Product.objects.get(name__iexact=name)
        context = {'product': product}
    except Product.DoesNotExist:
        context = {'error': 'Ce produit n\'est pas dans la base de données.'}
    else:
        try:
            alternatives = Product.objects.filter(nutriscore__lt=product.nutriscore,
                                                  category=product.category
                                                  ).order_by('nutrigrade', 'name')
            if request.user.is_authenticated:
                saved = Alternative.objects.filter(user=request.user).values('product')
                alternatives = alternatives.exclude(pk__in=saved)
            if alternatives:
                context['alternatives'] = alternatives
            else:
                raise Exception()
        except:
            context['no_alternatives'] = 'Aucun meilleur produit trouvé'

    return render(request, 'pages/product.html', context)


def save_alt(request):
    """save a product for the active user"""
    if request.method == 'POST':
        product_id = request.POST['product_id']
        user = request.user
        product = Product.objects.get(pk=product_id)
        alternative = Alternative(user=user, product=product)
        alternative.save()
    return HttpResponse('')


def registration(request):
    """Page to create an account"""
    print("ça marche")
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            print(username, password)
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = RegistrationForm()
    context = {'form': form}
    return render(request, 'pages/registration.html', context)


def connection(request):
    """page to log in"""
    context = {}

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        print(form.is_valid())
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        print(username, password)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            context['error'] = 'Mauvais mot de passe ou pseudo.'

    else:
        form = AuthenticationForm()
    context['form'] = form
    return render(request, 'pages/connexion.html', context)


def disconnection(request):
    """Please, the name is clear enough"""
    logout(request)
    return redirect('home')


def account(request):
    """page that display the information of the accont"""
    return render(request, 'pages/account.html')


def aliments(request):
    """display every registered aliments for the connected user"""
    if request.user.is_authenticated:
        try:
            alternatives = Alternative.objects.filter(user=request.user)
            if alternatives:
                context = {'alternatives': alternatives}
            else:
                raise Exception()
        except:
            context = {'error': 'Aucun produits enregistrés'}
    else:
        context = {'error': 'Vous n\'êtes pas connecter'}
    return render(request, 'pages/aliments.html', context)


def mentions(request):
    """Legales mentions page"""
    return render(request, 'pages/mentions.html')


def contact(request):
    """page with contact information"""
    return render(request, 'pages/contact.html')

def handler404(request, exception):
    """Error page 404"""
    return render(request, 'errors/error404.html', status=404)

def handler500(request):
    """Error page 500"""
    return render(request, 'errors/error500.html')
# Create your views here.
