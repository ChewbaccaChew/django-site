from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User  # стандартная модель django

from captcha.fields import CaptchaField

from .models import *

# форма не связанная с моделью
# class AddPostForm(forms.Form):
#     title = forms.CharField(max_length=255, label='Заголовок', widget=forms.TextInput(attrs={'class': 'form-input'}))
#     # через widget прописываем стили для поля
#     slug = forms.SlugField(max_length=255, label='URL')
#     content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), label='Контент')
#     is_published = forms.BooleanField(label='Публикация', required=False, initial=True)
#     # required=False - поле не обязательно к заполнению; initial=True - по умолчанию ставится галочка
#     cat = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория', empty_label='Категория не выбрана')
#     # cat - поле со списком выбора, который формирует queryset


# форма связанная с моделью
class AddPostForm(forms.ModelForm):
    # конструктор
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # вызов конструктора базового класса
        self.fields['cat'].empty_lable = 'Категория не выбрана'

    class Meta:
        model = Women  # связываем форму с моделью
        # fields = '__all__'  # отобразить в форме все поля модели, кроме заполняемых автоматически
        # на практике лучше явно указывать поля, которые необходимо отобразить
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat']
        # в widgets прописываем стили для полей
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

    # пользовательский валидатор (сработает только после проверки стандартным валидатором)
    def clean_title(self):  # название формируется из clean_ и дальше идет название поля для которого производится валидация
        title = self.cleaned_data['title']  # получаем данные по заголовку из коллекции cleaned_data, доступной в экземпляре AddPostForm
        if len(title) > 200:
            # обязательная генерация исключения ValidationError
            raise ValidationError('Длина превышает 200 символов')

        return title


class RegisterUserForm(UserCreationForm):
    """Форма регистрации"""

    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    # с помощью widget определяем как отображать поле в браузере

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

        # такой синтаксис для полей password1 и password2 в django не работает
        # поэтому определили его с помощью переменных выше
        # widgets = {
        #     'username': forms.TextInput(attrs={'class': 'form-input'}),
        #     'password1': forms.PasswordInput(attrs={'class': 'form-input'}),
        #     'password2': forms.PasswordInput(attrs={'class': 'form-input'}),
        # }


class LoginUserForm(AuthenticationForm):
    """Форма авторизации"""

    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class ContactForm(forms.Form):
    """Форма для Обратной связи"""

    name = forms.CharField(label='Имя', max_length=255)
    email = forms.EmailField(label='Email')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    captcha = CaptchaField()  # подключаем к форме каптчу
