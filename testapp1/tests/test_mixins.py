""" mixins tests """
from django.test import TestCase

from improved_permissions.exceptions import NotAllowed
from improved_permissions.models import RolePermission
from improved_permissions.roles import ALL_MODELS, Role, RoleManager
from improved_permissions.shortcuts import get_users
from improved_permissions.templatetags.roletags import has_perm as tg_has_perm
from improved_permissions.utils import dip_cache
from testapp1.models import Book, Chapter, MyUser, Paragraph
from testapp1.roles import Advisor, Author, Coordenator, Reviewer
from testapp2.models import Library
from testapp2.roles import LibraryOwner, LibraryWorker


class MixinsTest(TestCase):
    """ mixins test class """

    def setUp(self):
        self.john = MyUser.objects.create(username='john')
        self.bob = MyUser.objects.create(username='bob')
        self.mike = MyUser.objects.create(username='mike')

        self.library = Library.objects.create(title='Cool Library')
        self.book = Book.objects.create(title='Very Nice Book 1', library=self.library)
        self.chapter = Chapter.objects.create(title='Very Nice Chapter 1', book=self.book)
        self.paragraph = Paragraph.objects.create(content='Such Text 1', chapter=self.chapter)

        self.another_book = Book.objects.create(title='Very Nice Book 2', library=self.library)

        RoleManager.cleanup()
        RoleManager.register_role(Author)
        RoleManager.register_role(Advisor)
        RoleManager.register_role(Coordenator)
        RoleManager.register_role(Reviewer)
        RoleManager.register_role(LibraryOwner)
        RoleManager.register_role(LibraryWorker)
        dip_cache().clear()

    def test_inherit_permission(self):
        """ test if the inherit works fine """

        self.library.assign_role(self.john, LibraryOwner)
        self.book.assign_role(self.bob, Author)

        self.assertTrue(self.bob.has_role(Author))
        self.assertTrue(self.john.has_role(LibraryOwner))

        # Author role assigned to the book, but the chapter
        # and the paragraph are children of book.
        self.assertTrue(self.bob.has_permission('testapp1.add_book', self.book))
        self.assertTrue(self.bob.has_permission('testapp1.add_chapter', self.chapter))
        self.assertTrue(self.bob.has_permission('testapp1.add_paragraph', self.paragraph))

        # Another books are denied.
        self.assertFalse(self.bob.has_permission('testapp1.add_book', self.another_book))


        # As the role Author denies 'review', the
        # children will deny as well.
        self.assertFalse(self.bob.has_permission('testapp1.review', self.book))
        self.assertFalse(self.bob.has_permission('testapp1.review', self.chapter))
        self.assertFalse(self.bob.has_permission('testapp1.review', self.paragraph))

        # Reviewer role assigned to the book, but the chapter
        # and the paragraph are children of book.
        self.book.assign_role(self.mike, Reviewer)
        self.assertTrue(self.mike.has_permission('testapp1.review', self.book))
        self.assertTrue(self.mike.has_permission('testapp1.review', self.chapter))
        self.assertTrue(self.mike.has_permission('testapp1.review', self.paragraph))

        # Another books are denied.
        self.assertFalse(self.mike.has_permission('testapp1.review', self.another_book))

        # As the role Reviewer only allows 'review', the
        # children will deny as well.
        self.assertFalse(self.mike.has_permission('testapp1.add_book', self.book))

        # Check if the library owner inherits the permissions from all of them.
        self.assertTrue(self.john.has_permission('testapp1.change_book', self.book))
        self.assertTrue(self.john.has_permission('testapp1.change_book', self.chapter))
        self.assertTrue(self.john.has_permission('testapp1.change_book', self.paragraph))

        self.book.remove_role(self.bob, Author)
        self.library.remove_roles([self.john], LibraryOwner)

    def test_anyobject_permissions(self):
        """ test the has_permission function using any_object=True """
        self.john.assign_role(LibraryOwner, self.library)
        self.assertTrue(self.john.has_permission('testapp1.change_book', self.book))
        self.assertTrue(tg_has_perm(self.john, 'testapp1.change_book', self.book))

        # Without an object, we got a False.
        self.assertFalse(self.john.has_permission('testapp1.change_book'))
        self.assertFalse(tg_has_perm(self.john, 'testapp1.change_book'))

        # Using any_object=True we are allowing to bypass the instance check.
        self.assertTrue(self.john.has_permission('testapp1.change_book', any_object=True))
        self.assertTrue(tg_has_perm(self.john, 'testapp1.change_book', 'any'))

        # Provide an object and use any_object=True
        # at same time is not allowed.
        with self.assertRaises(NotAllowed):
            self.john.has_permission('testapp1.change_book', self.book, any_object=True)

    def test_persistent_permission(self):
        """ test permission behavior over persistent mode """
        self.john.assign_role(Coordenator)
        self.john.assign_role(Author, self.book)
        self.assertFalse(self.john.has_permission('testapp1.review', self.book))
        self.assertFalse(tg_has_perm(self.john, 'testapp1.review', self.book))
        self.assertFalse(tg_has_perm(self.john, 'testapp1.review', self.book, 'non-persistent'))

        # Using the templatetag option incorrectly.
        with self.assertRaises(NotAllowed):
            tg_has_perm(self.john, 'testapp1.review', self.book, 'i am not a option.')

        # Test persistent mode using the 'persistent' bypass kwarg.
        self.assertTrue(self.john.has_permission('testapp1.review', self.book, persistent=True))
        self.assertTrue(tg_has_perm(self.john, 'testapp1.review', self.book, 'persistent'))

        new_settings = {'PERSISTENT': True}
        with self.settings(IMPROVED_PERMISSIONS_SETTINGS=new_settings):
            # Test persistent mode using default settings.
            self.assertTrue(self.john.has_permission('testapp1.review', self.book))

            # Checking if the bypass still has preference.
            self.assertTrue(tg_has_perm(self.john, 'testapp1.review', self.book, 'persistent'))
            self.assertFalse(tg_has_perm(self.john, 'testapp1.review', self.book, 'non-persistent'))

            # Testing using a role with inherit=False in order to ignore it aswell.
            self.john.assign_role(LibraryWorker, self.library)
            self.assertTrue(self.john.has_permission('testapp1.review', self.book))

    def test_get_users(self):
        """ test if the get_user method works fine """

        # There is no user for the "library" yet.
        self.assertEqual(self.library.get_user(), None)

        self.book.assign_roles([self.bob], Author)
        self.john.assign_role(Advisor, self.bob)
        self.library.assign_role(self.mike, LibraryOwner)

        # Get single user instance.
        result = self.library.get_user()
        self.assertEqual(result, self.mike)

        # Get single user instance and role class.
        result = self.library.get_user(LibraryOwner)
        self.assertEqual(result, self.mike)

        # Try to get a user from a object with
        # Role class unique=False
        self.assertEqual(self.book.get_user(), None)

        # Get all users with who is Author of "book".
        self.book.assign_role(self.john, Author)
        result = self.book.get_users(Author)
        self.assertEqual(list(result), [self.bob, self.john])

        # Trying to use the reverse GerericRelation.
        reverse = list(self.book.roles.values_list('user', flat=True))
        self.assertEqual(reverse, [self.bob.id, self.john.id])

        # Get all users with any role to "library".
        result = self.library.get_users()
        self.assertEqual(list(result), [self.mike])

        # Try to get users list from a object
        # using a wrong Role class.
        with self.assertRaises(NotAllowed):
            self.library.get_users(Advisor)

        # Get all users with any role and any object.
        # As the result is a QuerySet, we use order_by()
        result = get_users().order_by('-username')
        self.assertEqual(list(result), [self.mike, self.john, self.bob])

        self.john.remove_role(Advisor)
        self.assertFalse(self.john.has_role(Advisor, self.bob))

    def test_get_user_roles_strings(self):
        """ test if the get_role and get_user_roles_strings methods work fine """
        self.book.assign_role(self.mike, Author)

        self.assertTrue(self.book.has_role(self.mike))
        self.assertTrue(self.book.has_role(self.mike, Author))

        # Check for single role class.
        self.assertEqual(self.mike.get_role(), Author)
        self.assertEqual(self.mike.get_role(self.book), Author)
        self.assertEqual(self.book.get_role(self.mike), Author)

        self.mike.assign_role(Reviewer, self.book)

        # Check for multiple role class.
        self.assertEqual(self.mike.get_user_roles_strings(), [Author, Reviewer])
        self.assertEqual(self.mike.get_user_roles_strings(self.book), [Author, Reviewer])
        self.assertEqual(self.book.get_user_roles_strings(self.mike), [Author, Reviewer])

    def test_remove_all(self):
        """ test if the remove_all shortcut works fine """
        self.book.assign_role(self.john, Author)
        self.book.assign_role(self.mike, Reviewer)

        self.assertEqual(list(self.book.get_users()), [self.john, self.mike])
        self.assertTrue(self.john.has_permission('testapp1.add_book', self.book))
        self.assertTrue(self.mike.has_permission('testapp1.review', self.book))

        # Remove all Authors from "book".
        self.book.remove_all(Author)
        self.assertEqual(list(self.book.get_users()), [self.mike])
        self.assertFalse(self.john.has_permission('testapp1.add_book', self.book))

        # Remove all Reviewers from "book".
        self.book.remove_all(Reviewer)
        self.assertEqual(list(self.book.get_users()), [])
        self.assertFalse(self.mike.has_permission('testapp1.review', self.book))

        # Assigning the roles again.
        self.book.assign_role(self.john, Author)
        self.book.assign_role(self.mike, Reviewer)

        self.assertEqual(list(self.book.get_users()), [self.john, self.mike])
        self.assertTrue(self.john.has_permission('testapp1.add_book', self.book))
        self.assertTrue(self.mike.has_permission('testapp1.review', self.book))

        # Remove any user of any role from "book".
        self.book.remove_all()
        self.assertEqual(list(self.book.get_users()), [])
        self.assertFalse(self.john.has_permission('testapp1.add_book', self.book))
        self.assertFalse(self.mike.has_permission('testapp1.review', self.book))

    def test_get_objects(self):
        """ test if the get_objects method works fine """
        self.book.assign_role(self.bob, Author)
        self.john.assign_role(Advisor, self.bob)
        self.library.assign_role(self.john, LibraryOwner)

        # Get all objects where john is "Advisor".
        result = self.john.get_objects(Advisor)
        self.assertEqual(result, [self.bob])

        # Get all objects of john for any Role.
        result = self.john.get_objects()
        self.assertEqual(result, [self.library, self.bob])

        # Get all objects of john but only of User model.
        result = self.john.get_objects(model=MyUser)
        self.assertEqual(result, [self.bob])
