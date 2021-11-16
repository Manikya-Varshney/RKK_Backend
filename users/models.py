from django.db import models

from django.core.validators import RegexValidator

from cbse.models import Board, Language, Standard, Subject

phone_regex = RegexValidator(regex = r'^\+\d{4,15}$', message = "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
otp_regex = RegexValidator(regex = r'^\d{4}')



class Profile(models.Model):
    phone_number = models.CharField(max_length = 17, validators = [phone_regex], verbose_name = 'Phone No.', unique = True)
    name = models.CharField(max_length = 200, null = True, blank = True)
    otp = models.IntegerField(validators = [otp_regex], null = True, blank = True)
    otp_timestamp = models.DateTimeField(auto_now = True, verbose_name = "OTP Created On")
    city = models.CharField(max_length=30, blank=True, null=True)
    state = models.CharField(max_length=20, blank=True, null=True)
    board = models.ForeignKey(to=Board, on_delete=models.CASCADE, null=True)
    language = models.ForeignKey(to=Language, on_delete=models.CASCADE, null=True)
    standard = models.ForeignKey(to=Standard, on_delete=models.CASCADE, null=True)
    subjects = models.ManyToManyField(to=Subject, related_name="Subjects", null=True)

    def __str__(self):
        return self.phone_number + ' - ' + self.id

    @classmethod
    def getAllAddresses(cls, id):
        profile = cls(pk = id)
        return profile.address_set.all()

    @classmethod
    def getAllScans(cls, user_id):
        profile = cls.objects.get(pk = user_id)
        return profile.scan_set.all()



    class Meta:
        verbose_name_plural = "Profiles"
