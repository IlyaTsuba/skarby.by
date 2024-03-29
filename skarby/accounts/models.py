from django.db import models

from users.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=80, unique=True, db_index=True, verbose_name='Slug')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Катэгорыя'
        verbose_name_plural = 'Катэгорыі'


def account_avatar_upload_to(instance, filename):
    """
    This method creates a new path for upload_to in Account model. Params instance and filename are identified in
    FileField class.
    :param instance: Class object. In this case instance is a class Account object.
    :param filename: Example filename.jpg.
    :return: New path for avatar upload_to.
    """
    # get account name through ForeignKey to Account. Same as Account.name
    account_name = instance.name
    return f"accounts/{account_name}/avatar/{filename}"


class Account(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Чарнавік',
        PUBLISHED = 1, 'Апублікавана'

    name = models.CharField(max_length=70, verbose_name='Імя/Назва')
    slug = models.SlugField(max_length=80, unique=True, db_index=True, verbose_name='Slug')
    description = models.TextField(verbose_name='Апісанне')
    avatar = models.ImageField(upload_to=account_avatar_upload_to, verbose_name='Аватар')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Катэгорыя')
    is_published = models.BooleanField(choices=Status.choices, default=Status.DRAFT)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Акаўнт'
        verbose_name_plural = 'Акаўнты'


class SocialMedia(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='account_social_media')
    instagram = models.CharField(max_length=50, null=True, blank=True)
    telegram = models.CharField(max_length=50, blank=True, null=True)
    youtube = models.CharField(max_length=50, blank=True, null=True)
    tiktok = models.CharField(max_length=50, blank=True, null=True)
    site = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.account.name

    class Meta:
        verbose_name = 'Сацыяльнае медыя'
        verbose_name_plural = 'Сацыяльныя медыя'


class AccountLikes(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Падабайка'
        verbose_name_plural = 'Падабайкі'


def account_photos_upload_to(instance, filename):
    """
    This method creates a new path for upload_to in Photo model. Params instance and filename are identified in
    FileField class.
    :param instance: Class object. In this case instance is a class Photos object.
    :param filename: Example filename.jpg.
    :return: New path for photo upload_to.
    """
    # get account name through ForeignKey to Account. Same as Photos.accounts.name
    account_name = instance.accounts.name
    return f"accounts/{account_name}/account_photos/{filename}"


class Photos(models.Model):
    accounts = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='account_photos',
                                 verbose_name='Аккаўнт')
    photo = models.ImageField(upload_to=account_photos_upload_to, verbose_name='Фота')

    def __str__(self):
        return self.photo.name

    class Meta:
        verbose_name = 'Фота'
        verbose_name_plural = 'Фота'


class SavedAccount(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
