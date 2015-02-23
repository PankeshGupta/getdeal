# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Preferences'
        db.create_table(u'profiles_preferences', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('send_emails', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('view_settings', self.gf('django.db.models.fields.TextField')(default='{}')),
            ('newsletter_frequency', self.gf('django.db.models.fields.CharField')(default='0', max_length=1)),
            ('paused_until', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('profiles', ['Preferences'])

        # Adding model 'Steps'
        db.create_table(u'profiles_steps', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tutorial_finished', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('hide_getting_started', self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True)),
            ('has_setup_feeds', self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True)),
            ('has_found_friends', self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True)),
        ))
        db.send_create_signal('profiles', ['Steps'])

        # Adding model 'ProfileStats'
        db.create_table(u'profiles_profilestats', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('profile', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stats', to=orm['profiles.Profile'])),
            ('nbr_following', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('nbr_followers', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('nbr_unfollowed', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('nbr_shared_deals', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('nbr_rated_deals', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('nbr_positive_deals', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('nbr_negative_deals', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('nbr_viewed_deals', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('nbr_wished_deals', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('nbr_bought_deals', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('nbr_claimed_deals', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('nbr_buried_deals', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('nbr_visits', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('nbr_subscriptions', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('nbr_ips', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('last_visit_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('last_visit_ip', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('counter', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('previous', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profiles.ProfileStats'], null=True, blank=True)),
        ))
        db.send_create_signal('profiles', ['ProfileStats'])

        # Adding model 'Profile'
        db.create_table(u'profiles_profile', (
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='profile', unique=True, primary_key=True, to=orm['auth.User'])),
            ('gender', self.gf('django.db.models.fields.CharField')(default='0', max_length=1)),
            ('timezone', self.gf('django.db.models.fields.CharField')(default='UCT', max_length=5)),
            ('token', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['authtoken.Token'], null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(default='profile.png', max_length=100, null=True, blank=True)),
            ('thumbnail', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('preferences', self.gf('django.db.models.fields.related.OneToOneField')(related_name='profile', unique=True, to=orm['profiles.Preferences'])),
            ('steps', self.gf('django.db.models.fields.related.OneToOneField')(related_name='profile', unique=True, to=orm['profiles.Steps'])),
            ('current_stats', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='+', unique=True, null=True, to=orm['profiles.ProfileStats'])),
        ))
        db.send_create_signal(u'profiles', ['Profile'])

        # Adding M2M table for field location on 'Profile'
        m2m_table_name = db.shorten_name(u'profiles_profile_location')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('profile', models.ForeignKey(orm[u'profiles.profile'], null=False)),
            ('city', models.ForeignKey(orm['addresses.city'], null=False))
        ))
        db.create_unique(m2m_table_name, ['profile_id', 'city_id'])


    def backwards(self, orm):
        # Deleting model 'Preferences'
        db.delete_table(u'profiles_preferences')

        # Deleting model 'Steps'
        db.delete_table(u'profiles_steps')

        # Deleting model 'ProfileStats'
        db.delete_table(u'profiles_profilestats')

        # Deleting model 'Profile'
        db.delete_table(u'profiles_profile')

        # Removing M2M table for field location on 'Profile'
        db.delete_table(db.shorten_name(u'profiles_profile_location'))


    models = {
        'addresses.city': {
            'Meta': {'object_name': 'City'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['addresses.Country']"}),
            'current_stats': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'+'", 'unique': 'True', 'null': 'True', 'to': "orm['addresses.CityStats']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        'addresses.citystats': {
            'Meta': {'ordering': "['city', '-counter']", 'object_name': 'CityStats'},
            'avg_rating_deals': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stats'", 'to': "orm['addresses.City']"}),
            'counter': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nbr_active_deals': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'nbr_active_subscribers': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'nbr_bought_deals': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'nbr_buried_deals': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'nbr_claimed_deals': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'nbr_negative_deals': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'nbr_new_deals': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'nbr_positive_deals': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'nbr_rated_deals': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'nbr_shared_deals': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'nbr_subscribers': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'nbr_viewed_deals': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'nbr_wished_deals': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'previous': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['addresses.CityStats']", 'null': 'True', 'blank': 'True'}),
            'score': ('django.db.models.fields.FloatField', [], {'default': '0.0'})
        },
        'addresses.country': {
            'Meta': {'object_name': 'Country'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'authtoken.token': {
            'Meta': {'object_name': 'Token'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '40', 'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'auth_token'", 'unique': 'True', 'to': u"orm['auth.User']"})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'profiles.preferences': {
            'Meta': {'object_name': 'Preferences'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'newsletter_frequency': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'}),
            'paused_until': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'send_emails': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'view_settings': ('django.db.models.fields.TextField', [], {'default': "'{}'"})
        },
        u'profiles.profile': {
            'Meta': {'object_name': 'Profile'},
            'current_stats': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'+'", 'unique': 'True', 'null': 'True', 'to': "orm['profiles.ProfileStats']"}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'default': "'profile.png'", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['addresses.City']", 'null': 'True', 'blank': 'True'}),
            'preferences': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': "orm['profiles.Preferences']"}),
            'steps': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': "orm['profiles.Steps']"}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'timezone': ('django.db.models.fields.CharField', [], {'default': "'UCT'", 'max_length': '5'}),
            'token': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['authtoken.Token']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['auth.User']"})
        },
        'profiles.profilestats': {
            'Meta': {'object_name': 'ProfileStats'},
            'counter': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_visit_ip': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'last_visit_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'nbr_bought_deals': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'nbr_buried_deals': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'nbr_claimed_deals': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'nbr_followers': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'nbr_following': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'nbr_ips': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'nbr_negative_deals': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'nbr_positive_deals': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'nbr_rated_deals': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'nbr_shared_deals': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'nbr_subscriptions': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'nbr_unfollowed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'nbr_viewed_deals': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'nbr_visits': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'nbr_wished_deals': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'previous': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.ProfileStats']", 'null': 'True', 'blank': 'True'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stats'", 'to': u"orm['profiles.Profile']"})
        },
        'profiles.steps': {
            'Meta': {'object_name': 'Steps'},
            'has_found_friends': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'has_setup_feeds': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'hide_getting_started': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tutorial_finished': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['profiles']