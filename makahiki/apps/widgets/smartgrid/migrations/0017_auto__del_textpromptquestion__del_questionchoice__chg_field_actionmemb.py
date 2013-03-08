# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'TextPromptQuestion'
        db.delete_table('smartgrid_textpromptquestion')

        # Deleting model 'QuestionChoice'
        db.delete_table('smartgrid_questionchoice')

        # Changing field 'ActionMember.question'
        db.alter_column('smartgrid_actionmember', 'question_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['smartgrid_library.LibraryTextPromptQuestion'], null=True))

        # Adding field 'Commitment.libCommitment'
        db.add_column('smartgrid_commitment', 'libCommitment', self.gf('django.db.models.fields.related.ForeignKey')(default=2, to=orm['smartgrid_library.LibraryCommitment']), keep_default=False)

        # Deleting field 'Action.image'
        db.delete_column('smartgrid_action', 'image')

        # Deleting field 'Action.description'
        db.delete_column('smartgrid_action', 'description')

        # Deleting field 'Action.title'
        db.delete_column('smartgrid_action', 'title')

        # Deleting field 'Action.type'
        db.delete_column('smartgrid_action', 'type')

        # Deleting field 'Action.video_source'
        db.delete_column('smartgrid_action', 'video_source')

        # Deleting field 'Action.libAction'
        db.delete_column('smartgrid_action', 'libAction_id')

        # Deleting field 'Action.embedded_widget'
        db.delete_column('smartgrid_action', 'embedded_widget')

        # Deleting field 'Action.slug'
        db.delete_column('smartgrid_action', 'slug')

        # Deleting field 'Action.name'
        db.delete_column('smartgrid_action', 'name')

        # Deleting field 'Action.video_id'
        db.delete_column('smartgrid_action', 'video_id')

        # Adding field 'Event.libEvent'
        db.add_column('smartgrid_event', 'libEvent', self.gf('django.db.models.fields.related.ForeignKey')(default=2, to=orm['smartgrid_library.LibraryEvent']), keep_default=False)

        # Deleting field 'Activity.admin_note'
        db.delete_column('smartgrid_activity', 'admin_note')

        # Deleting field 'Activity.confirm_type'
        db.delete_column('smartgrid_activity', 'confirm_type')

        # Deleting field 'Activity.confirm_prompt'
        db.delete_column('smartgrid_activity', 'confirm_prompt')

        # Adding field 'Activity.libActivity'
        db.add_column('smartgrid_activity', 'libActivity', self.gf('django.db.models.fields.related.ForeignKey')(default=2, to=orm['smartgrid_library.LibraryActivity']), keep_default=False)

        # Deleting field 'Category.name'
        db.delete_column('smartgrid_category', 'name')

        # Deleting field 'Category.slug'
        db.delete_column('smartgrid_category', 'slug')


    def backwards(self, orm):
        
        # Adding model 'TextPromptQuestion'
        db.create_table('smartgrid_textpromptquestion', (
            ('action', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['smartgrid.Action'])),
            ('answer', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('question', self.gf('django.db.models.fields.TextField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('smartgrid', ['TextPromptQuestion'])

        # Adding model 'QuestionChoice'
        db.create_table('smartgrid_questionchoice', (
            ('action', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['smartgrid.Action'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['smartgrid.TextPromptQuestion'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('choice', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('smartgrid', ['QuestionChoice'])

        # Changing field 'ActionMember.question'
        db.alter_column('smartgrid_actionmember', 'question_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['smartgrid.TextPromptQuestion'], null=True))

        # Deleting field 'Commitment.libCommitment'
        db.delete_column('smartgrid_commitment', 'libCommitment_id')

        # Adding field 'Action.image'
        db.add_column('smartgrid_action', 'image', self.gf('django.db.models.fields.files.ImageField')(max_length=255, null=True, blank=True), keep_default=False)

        # Adding field 'Action.description'
        db.add_column('smartgrid_action', 'description', self.gf('django.db.models.fields.TextField')(default='foo'), keep_default=False)

        # Adding field 'Action.title'
        db.add_column('smartgrid_action', 'title', self.gf('django.db.models.fields.CharField')(default='foo', max_length=200), keep_default=False)

        # Adding field 'Action.type'
        db.add_column('smartgrid_action', 'type', self.gf('django.db.models.fields.CharField')(default='foo', max_length=20), keep_default=False)

        # Adding field 'Action.video_source'
        db.add_column('smartgrid_action', 'video_source', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True), keep_default=False)

        # Adding field 'Action.libAction'
        db.add_column('smartgrid_action', 'libAction', self.gf('django.db.models.fields.related.ForeignKey')(default=2, to=orm['smartgrid_library.LibraryAction']), keep_default=False)

        # Adding field 'Action.embedded_widget'
        db.add_column('smartgrid_action', 'embedded_widget', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True), keep_default=False)

        # Adding field 'Action.slug'
        db.add_column('smartgrid_action', 'slug', self.gf('django.db.models.fields.SlugField')(default='foo', max_length=50, unique=True, db_index=True), keep_default=False)

        # Adding field 'Action.name'
        db.add_column('smartgrid_action', 'name', self.gf('django.db.models.fields.CharField')(default='foo', max_length=20), keep_default=False)

        # Adding field 'Action.video_id'
        db.add_column('smartgrid_action', 'video_id', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True), keep_default=False)

        # Deleting field 'Event.libEvent'
        db.delete_column('smartgrid_event', 'libEvent_id')

        # Adding field 'Activity.admin_note'
        db.add_column('smartgrid_activity', 'admin_note', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Activity.confirm_type'
        db.add_column('smartgrid_activity', 'confirm_type', self.gf('django.db.models.fields.CharField')(default='text', max_length=20), keep_default=False)

        # Adding field 'Activity.confirm_prompt'
        db.add_column('smartgrid_activity', 'confirm_prompt', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)

        # Deleting field 'Activity.libActivity'
        db.delete_column('smartgrid_activity', 'libActivity_id')

        # Adding field 'Category.name'
        db.add_column('smartgrid_category', 'name', self.gf('django.db.models.fields.CharField')(default='foo', max_length=255), keep_default=False)

        # Adding field 'Category.slug'
        db.add_column('smartgrid_category', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=50, null=True, db_index=True), keep_default=False)


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
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 3, 8, 7, 49, 51, 672899)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 3, 8, 7, 49, 51, 672814)'}),
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
        'notifications.usernotification': {
            'Meta': {'object_name': 'UserNotification'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'contents': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'display_alert': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {'default': '20'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'unread': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'score_mgr.pointstransaction': {
            'Meta': {'ordering': "('-transaction_date',)", 'unique_together': "(('user', 'transaction_date', 'message'),)", 'object_name': 'PointsTransaction'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'points': ('django.db.models.fields.IntegerField', [], {}),
            'transaction_date': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'smartgrid.action': {
            'Meta': {'ordering': "('level', 'category', 'priority')", 'object_name': 'Action'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['smartgrid.Category']", 'null': 'True', 'blank': 'True'}),
            'expire_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['smartgrid.Level']", 'null': 'True', 'blank': 'True'}),
            'point_value': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '1000'}),
            'pub_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(2013, 3, 8)'}),
            'related_resource': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'social_bonus': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'unlock_condition': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'unlock_condition_text': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'through': "orm['smartgrid.ActionMember']", 'symmetrical': 'False'})
        },
        'smartgrid.actionmember': {
            'Meta': {'unique_together': "(('user', 'action', 'submission_date'),)", 'object_name': 'ActionMember'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['smartgrid.Action']"}),
            'admin_comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'admin_link': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'approval_status': ('django.db.models.fields.CharField', [], {'default': "'pending'", 'max_length': '20'}),
            'award_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'completion_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '1024', 'blank': 'True'}),
            'points_awarded': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['smartgrid_library.LibraryTextPromptQuestion']", 'null': 'True', 'blank': 'True'}),
            'response': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'social_bonus_awarded': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'social_email': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'submission_date': ('django.db.models.fields.DateTimeField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'smartgrid.activity': {
            'Meta': {'ordering': "('level', 'category', 'priority')", 'object_name': 'Activity', '_ormbases': ['smartgrid.Action']},
            'action_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['smartgrid.Action']", 'unique': 'True', 'primary_key': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {}),
            'libActivity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['smartgrid_library.LibraryActivity']"}),
            'point_range_end': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'point_range_start': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'smartgrid.category': {
            'Meta': {'ordering': "('priority',)", 'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'libCategory': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['smartgrid_library.LibraryCategory']"}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'smartgrid.commitment': {
            'Meta': {'ordering': "('level', 'category', 'priority')", 'object_name': 'Commitment', '_ormbases': ['smartgrid.Action']},
            'action_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['smartgrid.Action']", 'unique': 'True', 'primary_key': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'libCommitment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['smartgrid_library.LibraryCommitment']"})
        },
        'smartgrid.confirmationcode': {
            'Meta': {'object_name': 'ConfirmationCode'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['smartgrid.Action']"}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 3, 8, 7, 47, 54, 234696)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'printed_or_distributed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'smartgrid.emailreminder': {
            'Meta': {'unique_together': "(('user', 'action'),)", 'object_name': 'EmailReminder'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['smartgrid.Action']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email_address': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'send_at': ('django.db.models.fields.DateTimeField', [], {}),
            'sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'smartgrid.event': {
            'Meta': {'ordering': "('level', 'category', 'priority')", 'object_name': 'Event', '_ormbases': ['smartgrid.Action']},
            'action_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['smartgrid.Action']", 'unique': 'True', 'primary_key': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {}),
            'event_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'event_location': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'event_max_seat': ('django.db.models.fields.IntegerField', [], {'default': '1000'}),
            'is_excursion': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'libEvent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['smartgrid_library.LibraryEvent']"})
        },
        'smartgrid.filler': {
            'Meta': {'ordering': "('level', 'category', 'priority')", 'object_name': 'Filler', '_ormbases': ['smartgrid.Action']},
            'action_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['smartgrid.Action']", 'unique': 'True', 'primary_key': 'True'})
        },
        'smartgrid.level': {
            'Meta': {'ordering': "('priority',)", 'object_name': 'Level'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'unlock_condition': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'unlock_condition_text': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'})
        },
        'smartgrid.textreminder': {
            'Meta': {'unique_together': "(('user', 'action'),)", 'object_name': 'TextReminder'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['smartgrid.Action']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'send_at': ('django.db.models.fields.DateTimeField', [], {}),
            'sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'text_carrier': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'text_number': ('django.contrib.localflavor.us.models.PhoneNumberField', [], {'max_length': '20'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'smartgrid_library.libraryaction': {
            'Meta': {'object_name': 'LibraryAction'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'embedded_widget': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'point_value': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'social_bonus': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'subtype': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'unlock_condition': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'unlock_condition_text': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'video_id': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'video_source': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        'smartgrid_library.libraryactivity': {
            'Meta': {'object_name': 'LibraryActivity', '_ormbases': ['smartgrid_library.LibraryAction']},
            'admin_note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'confirm_prompt': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'confirm_type': ('django.db.models.fields.CharField', [], {'default': "'text'", 'max_length': '20'}),
            'duration': ('django.db.models.fields.IntegerField', [], {}),
            'libraryaction_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['smartgrid_library.LibraryAction']", 'unique': 'True', 'primary_key': 'True'}),
            'point_range_end': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'point_range_start': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'smartgrid_library.librarycategory': {
            'Meta': {'ordering': "('name',)", 'object_name': 'LibraryCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'})
        },
        'smartgrid_library.librarycommitment': {
            'Meta': {'object_name': 'LibraryCommitment', '_ormbases': ['smartgrid_library.LibraryAction']},
            'duration': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'libraryaction_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['smartgrid_library.LibraryAction']", 'unique': 'True', 'primary_key': 'True'})
        },
        'smartgrid_library.libraryevent': {
            'Meta': {'object_name': 'LibraryEvent', '_ormbases': ['smartgrid_library.LibraryAction']},
            'duration': ('django.db.models.fields.IntegerField', [], {}),
            'is_excursion': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'libraryaction_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['smartgrid_library.LibraryAction']", 'unique': 'True', 'primary_key': 'True'})
        },
        'smartgrid_library.librarytextpromptquestion': {
            'Meta': {'object_name': 'LibraryTextPromptQuestion'},
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'libraryaction': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['smartgrid_library.LibraryAction']"}),
            'question': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['smartgrid']
