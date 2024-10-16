# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)





class Clients(models.Model):
    id = models.SmallIntegerField(blank=True, null=True)
    idclient = models.CharField(db_column='idClient', max_length=10, blank=True, null=True)  # Field name made lowercase.
    clientname = models.CharField(db_column='clientName', max_length=44, blank=True, null=True)  # Field name made lowercase.
    packet = models.CharField(max_length=12, blank=True, null=True)
    mainbandwidth = models.IntegerField(db_column='mainBandwidth', blank=True, null=True)  # Field name made lowercase.
    backupbandwidth = models.SmallIntegerField(db_column='backupBandwidth', blank=True, null=True)  # Field name made lowercase.
    remoteaddress = models.CharField(db_column='remoteAddress', max_length=13, blank=True, null=True)  # Field name made lowercase.
    portclient = models.IntegerField(db_column='portClient', blank=True, null=True)  # Field name made lowercase.
    mainlinkaddress = models.CharField(db_column='mainLinkAddress', max_length=13, blank=True, null=True)  # Field name made lowercase.
    backuplinkaddress = models.CharField(db_column='backupLinkAddress', max_length=11, blank=True, null=True)  # Field name made lowercase.
    activator = models.CharField(max_length=6, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clients'


class DatabasesUserdevice(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.CharField(max_length=100)
    password = models.CharField(max_length=1000)
    group = models.CharField(max_length=100)
    published = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'databases_userdevice'


class Devices(models.Model):
    id = models.IntegerField(blank=True, null=True)
    identity = models.CharField(max_length=37, blank=True, null=True)
    ipdevice = models.CharField(db_column='ipDevice', max_length=13, blank=True, null=True)  # Field name made lowercase.
    portdevice = models.IntegerField(db_column='portDevice', blank=True, null=True)  # Field name made lowercase.
    activator = models.CharField(max_length=6, blank=True, null=True)
    location = models.CharField(max_length=34, blank=True, null=True)
    layer = models.CharField(max_length=12, blank=True, null=True)
    routerpop = models.CharField(db_column='routerPOP', max_length=5, blank=True, null=True)  # Field name made lowercase.
    os = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'devices'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Graphtraffic(models.Model):
    id = models.SmallIntegerField(blank=True, null=True)
    hostname = models.CharField(max_length=47, blank=True, null=True)
    address = models.CharField(max_length=13, blank=True, null=True)
    ports = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'graphTraffic'


class Periodiccheckbandwidth(models.Model):
    id = models.IntegerField(blank=True, null=True)
    linkname = models.CharField(db_column='linkName', max_length=33, blank=True, null=True)  # Field name made lowercase.
    linkid = models.CharField(db_column='linkID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    deviceserverbtest = models.CharField(db_column='deviceServerBTest', max_length=13, blank=True, null=True)  # Field name made lowercase.
    interface = models.CharField(max_length=8, blank=True, null=True)
    deviceremotebtest = models.CharField(db_column='deviceRemoteBTest', max_length=13, blank=True, null=True)  # Field name made lowercase.
    initialbandwidth = models.SmallIntegerField(db_column='initialBandwidth', blank=True, null=True)  # Field name made lowercase.
    linktype = models.CharField(db_column='linkType', max_length=107, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'periodicCheckBandwidth'


class Servers(models.Model):
    id = models.IntegerField(blank=True, null=True)
    hostname = models.CharField(max_length=31, blank=True, null=True)
    ipserver = models.CharField(db_column='ipServer', max_length=11, blank=True, null=True)  # Field name made lowercase.
    role = models.CharField(max_length=9, blank=True, null=True)
    portserver = models.IntegerField(db_column='portServer', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'servers'


class SqliteSequence(models.Model):
    name = models.CharField(blank=True, null=True)
    seq = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sqlite_sequence'


class Staffne(models.Model):
    id = models.SmallIntegerField(blank=True, null=True)
    email = models.CharField(max_length=24, blank=True, null=True)
    name = models.CharField(max_length=21, blank=True, null=True)
    position = models.CharField(max_length=16, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'staffNe'
