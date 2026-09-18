from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from .models import Ad
from .serializers import AdSerializer


User = get_user_model()


class AdSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='seller@example.com',
            password='password123',
            first_name='Иван',
            last_name='Петров',
            phone_number='+79990000000',
        )
        self.ad_data = {
            'title': 'Ремонт',
            'city': 'Москва',
            'phone_number': '+79991111111',
            'description': 'Описание',
            'price': '1000.00',
            'currency': 'RUB',
        }

    def test_author_name_is_available_for_ad_list_and_detail_serialization(self):
        ad = Ad.objects.create(author=self.user, **self.ad_data)

        serialized_ad = AdSerializer(ad).data
        serialized_detail = AdSerializer(Ad.objects.get(pk=ad.pk)).data

        self.assertEqual(serialized_ad['author'], 'Иван Петров')
        self.assertEqual(serialized_ad['author_name'], 'Иван Петров')
        self.assertEqual(serialized_detail['author'], 'Иван Петров')
        self.assertEqual(serialized_detail['author_name'], 'Иван Петров')

    def test_create_uses_author_passed_by_view(self):
        serializer = AdSerializer(data=self.ad_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

        ad = serializer.save(author=self.user)

        self.assertEqual(ad.author, self.user)

    def test_create_without_author_is_rejected(self):
        serializer = AdSerializer(data=self.ad_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

        with self.assertRaises(ValidationError):
            serializer.save()
