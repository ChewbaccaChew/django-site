from django.db import models


class Women(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)  # blank=True означает, что поле может быть пустым
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')  # для работы поля требуется установить Pillow
    # в upload_to передаем шаблон пути, по которому будем сохранять загруженные фото
    time_create = models.DateTimeField(auto_now_add=True)
    # auto_now_add определяет текущее время в момент добавления записи и больше никогда не изменяется
    time_update = models.DateTimeField(auto_now=True)
    # auto_now будет обновлять дату на текущую при каждом изменении записи
    is_published = models.BooleanField(default=True)

    # магический метод, выводит заголовок экземпляра вместо Women_object_(1)
    def __str__(self):
        return self.title
