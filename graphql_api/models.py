from gdstorage.storage import GoogleDriveStorage
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.mail import send_mail
import string
import random

def randompassword():
  chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
  size = random.randint(8, 12)
  return ''.join(random.choice(chars) for x in range(size))

SEXE = (
    ("1", ("M")),
    ("2", ("F")),
)

class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    class Meta:
        db_table = 'User'

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

class Temoin(User):
    class Meta:
        verbose_name = 'Témoin'
        verbose_name_plural = 'Témoins'
        db_table = 'Temoin'

class Medicin(User):
    class Meta:
        verbose_name = 'Médicin'
        verbose_name_plural = 'Médicins'
        db_table = 'Medicin'

    def save(self, **kwargs):
        password = randompassword()
        email = self.username
        Medicin.set_password(self, raw_password = password)
        send_mail('Registration in FirstAid App', 'Your identifier: {}\nYour password: {}'.format(email, password), 'estanislaumenezes9@gmail.com',
                  [email])
        super().save(**kwargs)


class Victime(models.Model):
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    sexe = models.CharField(max_length=1, null=True, blank=True, choices=SEXE)
    adresse = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'Victime'

    def __str__(self):
        return  "Victime du sexe {} et age {}".format(self.sexe, self.age)

class Cas(models.Model):
    date = models.DateTimeField(default=timezone.now())
    lieu = models.TextField(blank=True)
    adresse = models.TextField(blank=True)
    temoin = models.ForeignKey(Temoin, blank=True, null=True, on_delete=models.CASCADE)
    victime = models.ForeignKey(Victime, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = "Cas"
        verbose_name_plural = "Cas"

class Signes_N(models.Model):
    ouverture_yeux = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    reponse_verbale = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    reponse_motrice = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)])

    class Meta:
        db_table = "Signes Neurologiques"
        verbose_name = "Signes Neurologiques"
        verbose_name_plural = "Signes Neurologiques"

class Signes_F(models.Model):
    hemorragie = models.BooleanField(blank=True, null=True)
    dyspnee = models.BooleanField(blank=True, null=True)
    pouls = models.BooleanField(blank=True, null=True)

    class Meta:
        db_table = "Signes Fonctionnelles"
        verbose_name = "Signes Fonctionnelles"
        verbose_name_plural = "Signes Fonctionnelles"

class Cas_N(models.Model):
    cas = models.ForeignKey(Cas, blank=True, null=True, on_delete=models.CASCADE)
    neurologie = models.ForeignKey(Signes_N, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = "Neurologie"
        verbose_name = "Cas x Neurologie"
        verbose_name_plural = "Cas x Neurologie"

class Cas_F(models.Model):
    cas = models.ForeignKey(Cas, blank=True, null=True, on_delete=models.CASCADE)
    fonctionnelle = models.ForeignKey(Signes_F, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = "Fonctionnelles"
        verbose_name = "Cas x Signes Fonctionnelles"
        verbose_name_plural = "Cas x Signes Fonctionnelles"

class Message(models.Model):
    expediteur = models.ForeignKey(User, blank=True, null=True, related_name="expediteur", on_delete=models.CASCADE)
    destinateur = models.ForeignKey(User, blank=True, null=True, related_name="destinateur", on_delete=models.CASCADE)
    diffusion = models.BooleanField(default=False)
    contenu = models.TextField(blank=True, null=True)
    date = models.DateTimeField(default=timezone.now())

    class Meta:
        db_table = "Messages"

# Define Google Drive Storage
gd_storage = GoogleDriveStorage()

class Protocole(models.Model):
    type = models.TextField(blank=True, null=True, verbose_name="Protocole")
    cas_precis = models.TextField(blank=True, null=True, verbose_name="situation")
    img = models.ImageField(upload_to='protocole/', null=True, blank=True)
    data = models.JSONField()

    class Meta:
        db_table = "Protocole"
        unique_together = ['type', 'cas_precis']

    def __str__(self):
        return "Type: {}    Cas: {} ".format(self.type, self.cas_precis)
