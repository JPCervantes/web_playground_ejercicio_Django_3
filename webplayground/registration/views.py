from .forms import UserCreationFormWithEmail, ProfileForm, EmailForm
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .models import Profile
from django import forms

# Create your views here.
class SignUpView(CreateView):
    form_class = UserCreationFormWithEmail
    template_name = 'registration/signup.html'

    def get_success_url(self):
        return reverse_lazy('login') + '?register'

    def get_form(self, form_class=None):
        form = super(SignUpView, self).get_form()
        # Aquí vamos a editar en tiempo real el formulario. Lo anterior lo recupera.
        form.fields['username'].widget = forms.TextInput(attrs= {'class':'form-control mb-2', 'placeholder':'Nombre de usuario'} )
        form.fields['email'].widget = forms.EmailInput(attrs= {'class':'form-control mb-2', 'placeholder':'Email'} )
        form.fields['password1'].widget = forms.TextInput(attrs= {'class':'form-control mb-2', 'placeholder':'Contraseña'} )
        form.fields['password2'].widget = forms.TextInput(attrs= {'class':'form-control mb-2', 'placeholder':'Repite la contraseña'} )
        return form

@method_decorator(login_required, name = 'dispatch')
class ProfileUpdate(UpdateView):
    form_class = ProfileForm
    success_url = reverse_lazy('profile')
    template_name='registration/profile_form.html'

    def get_object(self):
        #Recuperamos el objeto que se va a editar
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile


@method_decorator(login_required, name = 'dispatch')
class EmailUpdate(UpdateView):
    form_class = EmailForm
    success_url = reverse_lazy('profile')
    template_name='registration/profile_email_form.html'

    def get_object(self):
        #Recuperamos el objeto que se va a editar
        return self.request.user

    def get_form(self, form_class=None):
        form = super(EmailUpdate, self).get_form()
        # Aquí vamos a editar en tiempo real el formulario. Lo anterior lo recupera.
        form.fields['email'].widget = forms.EmailInput(attrs= {'class':'form-control mb-2', 'placeholder':'Email'} )
        return form
