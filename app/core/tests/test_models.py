# we have to use this function to get user model (not directly User)
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase

from core import models


def sample_user(email='test@londonappdev.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = "test@example.com"
        password = "Testpass123"

        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """
        Test the email for a new user is normalized
        Just for tutorial. (Don't works for me without normalizing anyway)
        """
        email = "test@EXAMPLE.COM"
        user = get_user_model().objects.create_user(
            email=email,
            password='password',
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        # means everything we run here should raise ValueError.
        # If it doesnt - test will fail
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email="",
                password="password",
            )

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=None,
                password="password",
            )

    def test_create_new_superuser(self):
        """Test creating new superuser"""
        user = get_user_model().objects.create_superuser(
            email="admin@admin.com",
            password="password",
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Test the recipe string representation"""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Steak and mushroom sauce',
            time_minutes=5,
            price=5.00
        )

        self.assertEqual(str(recipe), recipe.title)

    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the correct location"""
        # UUID universally unique identifier
        # we want to mock uuid
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        # this means any time we call uuid4 ! function
        # that is triggered from our test it will override the default
        # behaviour and return 'test-uuid'
        # this allows us to reliably test how our function works

        # first parameter is instance but we dont need it right now
        # generate the file path
        file_path = models.recipe_image_file_path(None, 'my-image.jpg')

        # expected path
        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
