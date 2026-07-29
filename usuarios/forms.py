from django import forms
from .models import Usuario, Rol


class LoginForm(forms.Form):

    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Usuario"
            }
        )
    )


    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Contraseña"
            }
        )
    )


class UsuarioCrearForm(forms.ModelForm):

    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Contraseña inicial",
                "required": True,
            }
        )
    )

    class Meta:
        model = Usuario
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "rol",
            "telefono",
            "is_active",
        ]
        labels = {
            "username": "Nombre de Usuario",
            "first_name": "Nombres",
            "last_name": "Apellidos",
            "email": "Correo Electrónico",
            "rol": "Rol de Usuario",
            "telefono": "Teléfono",
            "is_active": "Usuario Activo",
        }
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ej: jgarcia"}
            ),
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Juan"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "García"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "correo@ejemplo.com"}
            ),
            "rol": forms.Select(
                attrs={"class": "form-control"}
            ),
            "telefono": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "+58 412-1234567"}
            ),
            "is_active": forms.CheckboxInput(
                attrs={"style": "width: 18px; height: 18px; cursor: pointer;"}
            ),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


class UsuarioEditarForm(forms.ModelForm):

    password_nueva = forms.CharField(
        label="Nueva Contraseña (opcional)",
        required=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Dejar en blanco para mantener la contraseña actual",
            }
        )
    )

    class Meta:
        model = Usuario
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "rol",
            "telefono",
            "is_active",
        ]
        labels = {
            "username": "Nombre de Usuario",
            "first_name": "Nombres",
            "last_name": "Apellidos",
            "email": "Correo Electrónico",
            "rol": "Rol de Usuario",
            "telefono": "Teléfono",
            "is_active": "Usuario Activo",
        }
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "first_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control"}
            ),
            "rol": forms.Select(
                attrs={"class": "form-control"}
            ),
            "telefono": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "is_active": forms.CheckboxInput(
                attrs={"style": "width: 18px; height: 18px; cursor: pointer;"}
            ),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password_nueva")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user