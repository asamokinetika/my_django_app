# Generated by Django 3.2.15 on 2022-09-09 11:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import sns.models


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
                ('email', models.EmailField(max_length=50, unique=True)),
                ('name', models.CharField(max_length=50)),
                ('img', models.ImageField(blank=True, null=True, upload_to=sns.models.upload_path)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auth', models.BooleanField()),
                ('invitee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitee_friend', to=settings.AUTH_USER_MODEL)),
                ('inviter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inviter_friend', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=100)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GroupMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=1000)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('Group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_receiver_group', to='sns.group')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_owner_group', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='GroupInvitation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auth', models.BooleanField()),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group', to='sns.group')),
                ('invitee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitee_group', to=settings.AUTH_USER_MODEL)),
                ('inviter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inviter_group', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FriendMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=1000)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_owner_friend', to=settings.AUTH_USER_MODEL)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_receiver_friend', to='sns.friend')),
            ],
            options={
                'ordering': ('-pub_date',),
            },
        ),
    ]
