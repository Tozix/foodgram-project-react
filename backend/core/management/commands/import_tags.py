from django.core.management import BaseCommand
from recipes.models import Tag


class Command(BaseCommand):
    help = 'Создаем тэги'

    def handle(self, *args, **kwargs):
        data = [
            {'name': 'Завтрак', 'color': '#F1A816', 'slug': 'breakfast'},
            {'name': 'Обед', 'color': '#9E16F1', 'slug': 'lunch'},
            {'name': 'Ужин', 'color': '#F11623', 'slug': 'dinner'}]
        Tag.objects.bulk_create(Tag(**tag) for tag in data)
        self.stdout.write(self.style.SUCCESS('Все тэги загружены!'))
