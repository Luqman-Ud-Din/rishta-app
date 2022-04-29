# Generated by Django 4.0.2 on 2022-04-29 18:42

import backend.users.managers
import backend.users.models
from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('contact_number', models.CharField(blank=True, max_length=16, verbose_name='contact number')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('date_of_birth', models.DateField(default=backend.users.models.current_date, verbose_name='date of birth')),
                ('time_of_birth', models.TimeField(default=backend.users.models.current_time, verbose_name='time of birth')),
                ('city_of_birth', models.CharField(blank=True, max_length=64, null=True, verbose_name='city of birth')),
                ('country', models.CharField(blank=True, max_length=64, null=True, verbose_name='country')),
                ('city', models.CharField(blank=True, max_length=64, null=True, verbose_name='city')),
                ('zip_code', models.CharField(blank=True, max_length=32, null=True, verbose_name='zip code')),
                ('residency_status', models.CharField(blank=True, max_length=64, null=True, verbose_name='residency status')),
                ('highest_qualification', models.CharField(blank=True, max_length=128, null=True, verbose_name='highest qualification')),
                ('employer', models.CharField(blank=True, max_length=128, null=True, verbose_name='employer')),
                ('designation', models.CharField(blank=True, max_length=128, null=True, verbose_name='employer')),
                ('annual_income', models.IntegerField(default=0, verbose_name='annual income')),
                ('religion', models.CharField(choices=[('CHRISTIANITY', 'Christianity'), ('ISLAM', 'Islam'), ('ATHEIST', 'Atheist'), ('HINDUISM', 'Hinduism'), ('BUDDHISM', 'Buddhism'), ('SIKHISM', 'Sikhism'), ('SPIRITISM', 'Spiritism'), ('JUDAISM', 'Judaism'), ('OTHER', 'Other')], default='OTHER', max_length=32, verbose_name='religion')),
                ('mother_tongue', models.CharField(blank=True, max_length=64, null=True, verbose_name='mother tongue')),
                ('community', models.CharField(blank=True, max_length=64, null=True, verbose_name='community')),
                ('sub_community', models.CharField(blank=True, max_length=64, null=True, verbose_name='sub-community')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('U', 'Unknown')], default='U', max_length=1, verbose_name='gender')),
                ('marital_status', models.CharField(choices=[('S', 'Single'), ('M', 'Married'), ('D', 'Divorced'), ('O', 'Other')], default='S', max_length=1, verbose_name='marital status')),
                ('looking_for', models.CharField(choices=[('S', 'Single'), ('M', 'Married'), ('D', 'Divorced'), ('N', 'No Preference')], default='N', max_length=1, verbose_name='looking for')),
                ('blood_group', models.CharField(choices=[('AB-', 'AB-'), ('AB+', 'AB+'), ('A-', 'A-'), ('A+', 'A+'), ('B-', 'B-'), ('B+', 'B+'), ('O-', 'O-'), ('O+', 'O+'), ('U', 'Unknown')], default='U', max_length=3, verbose_name='blood group')),
                ('created_by', models.CharField(choices=[('SELF', 'Self'), ('PARENT', 'Parent'), ('GUARDIAN', 'Guardian'), ('SIBLING', 'Sibling'), ('FRIEND', 'Friend'), ('OTHER', 'Other')], default='SELF', max_length=8, verbose_name='created by')),
                ('height', models.PositiveSmallIntegerField(default=0, help_text='height in centimeters', verbose_name='height')),
                ('has_disability', models.BooleanField(default=False, verbose_name='has disability')),
                ('is_father_alive', models.BooleanField(default=True, verbose_name='is father alive')),
                ('is_mother_alive', models.BooleanField(default=True, verbose_name='is mother alive')),
                ('children_count', models.PositiveSmallIntegerField(default=0, verbose_name='children count')),
                ('brothers_count', models.PositiveSmallIntegerField(default=0, verbose_name='brothers count')),
                ('sisters_count', models.PositiveSmallIntegerField(default=0, verbose_name='sisters count')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatar')),
                ('about_self', models.CharField(blank=True, max_length=2048, null=True, verbose_name='about self')),
                ('about_family', models.CharField(blank=True, max_length=2048, null=True, verbose_name='about family')),
                ('about_partner', models.CharField(blank=True, max_length=2048, null=True, verbose_name='about partner')),
                ('about_likes', models.CharField(blank=True, max_length=1024, null=True, verbose_name='about likes')),
                ('about_dislikes', models.CharField(blank=True, max_length=1024, null=True, verbose_name='about dislikes')),
                ('about_lifestyle', models.CharField(blank=True, max_length=1024, null=True, verbose_name='about lifestyle')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', backend.users.managers.CustomUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ProfileView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created at')),
                ('viewee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='viewee', to=settings.AUTH_USER_MODEL)),
                ('viewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='viewer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sentiment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sentiment', models.CharField(choices=[('L', 'LIKE'), ('D', 'DISLIKE'), ('N', 'NEUTRAL')], default='N', max_length=1, verbose_name='sentiment')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('sentiment_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sentiments_from', to=settings.AUTH_USER_MODEL)),
                ('sentiment_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sentiments_to', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('sentiment_to', 'sentiment_from')},
            },
        ),
    ]
