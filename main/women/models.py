from django.db import models
from django.urls import reverse


class Women(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = models.TextField(blank=True, verbose_name='Текст статьи')  # blank=True означает, что поле может быть пустым
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото')  # для работы поля требуется установить Pillow
    # в upload_to передаем шаблон пути, по которому будем сохранять загруженные фото
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    # auto_now_add определяет текущее время в момент добавления записи и больше никогда не изменяется
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    # auto_now будет обновлять дату на текущую при каждом изменении записи
    is_published = models.BooleanField(default=True, verbose_name='Публикация')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория', null=True)

    # магический метод, выводит заголовок экземпляра вместо Women_object_(1)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.pk})

    class Meta:
        verbose_name = 'Известные женщины'
        verbose_name_plural = 'Известные женщины'
        ordering = ['-time_create', 'title']  # сортировка экземпляров


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_id': self.pk})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']
