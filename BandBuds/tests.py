from django.test import TestCase
from bba.models import UserProfile

class UserProfileTestCase(TestCase):
    def setUp(self):
        UserProfile.objects.create(user="joel", smokes="yes")
        UserProfile.objects.create(user="cat", smokes="no")

    def test_animals_can_speak(self):
        """profiles"""
        joel = UserProfile.objects.get(name="joel")
        pet = UserProfile.objects.get(name="cat")
        self.assertEqual(joel.speak(), 'The user name is "roar"')
        self.assertEqual(pet.speak(), 'Her pet says "meow"')



class UserProfileMethodTests(TestCase):

    def test_ensure_gender_are_positive(self):

        """
                ensure_views_are_positive should results True for categories where views are zero or positive
        """
        user = UserProfile(name='gender',gender=-1)
        user.save()
        self.assertEqual((user.gender >= 0), True)


def test_slug_line_creation(self):
    """
    slug_line_creation checks to make sure that when we add a category an appropriate slug line is created
    i.e. "Random Category String" -> "random-category-string"
    """

    cat = UserProfile('Random Category String')
    cat.save()
    self.assertEqual(cat.slug, 'random-category-string')

from django.core.urlresolvers import reverse

class user_profileViewTests(TestCase):

    def test_user_profile_view_with_no_categories(self):
        """
        If no questions exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('user_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no categories present.")
        self.assertQuerysetEqual(response.context['categories'], [])




def test_index_view_with_categories(self):
    """
    If no questions exist, an appropriate message should be displayed.
    """

    add_cat('test',1,1)
    add_cat('temp',1,1)
    add_cat('tmp',1,1)
    add_cat('tmp test temp',1,1)

    response = self.client.get(reverse('index'))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "tmp test temp")

    num_cats =len(response.context['categories'])
    self.assertEqual(num_cats , 4)

