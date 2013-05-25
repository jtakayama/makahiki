# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'GccSettings'
        db.create_table('smartgrid_mgr_gccsettings', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('check_pub_dates', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('check_event_dates', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('check_unlock_dates', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('check_unreachable', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('check_false_unlocks', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('check_mismatched_levels', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('check_description_urls', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('smartgrid_mgr', ['GccSettings'])


    def backwards(self, orm):
        
        # Deleting model 'GccSettings'
        db.delete_table('smartgrid_mgr_gccsettings')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 24, 14, 38, 11, 36964)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 24, 14, 38, 11, 36886)'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'smartgrid_mgr.gccsettings': {
            'Meta': {'object_name': 'GccSettings'},
            'check_description_urls': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'check_event_dates': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'check_false_unlocks': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'check_mismatched_levels': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'check_pub_dates': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'check_unlock_dates': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'check_unreachable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['smartgrid_mgr']
