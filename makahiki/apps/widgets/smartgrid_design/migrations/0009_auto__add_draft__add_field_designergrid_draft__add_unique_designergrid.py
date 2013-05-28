# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Removing unique constraint on 'DesignerAction', fields ['slug']
        db.delete_unique('smartgrid_design_designeraction', ['slug'])

        # Removing unique constraint on 'DesignerColumnGrid', fields ['name', 'level']
        db.delete_unique('smartgrid_design_designercolumngrid', ['name_id', 'level_id'])

        # Adding model 'Draft'
        db.create_table('smartgrid_design_draft', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
        ))
        db.send_create_signal('smartgrid_design', ['Draft'])

        # Adding field 'DesignerGrid.draft'
        db.add_column('smartgrid_design_designergrid', 'draft', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['smartgrid_design.Draft'], null=True, blank=True), keep_default=False)

        # Adding unique constraint on 'DesignerGrid', fields ['column', 'action', 'row', 'draft', 'level']
        db.create_unique('smartgrid_design_designergrid', ['column', 'action_id', 'row', 'draft_id', 'level_id'])

        # Adding field 'DesignerColumnGrid.draft'
        db.add_column('smartgrid_design_designercolumngrid', 'draft', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['smartgrid_design.Draft'], null=True, blank=True), keep_default=False)

        # Adding unique constraint on 'DesignerColumnGrid', fields ['draft', 'name', 'level']
        db.create_unique('smartgrid_design_designercolumngrid', ['draft_id', 'name_id', 'level_id'])

        # Adding field 'DesignerLevel.draft'
        db.add_column('smartgrid_design_designerlevel', 'draft', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['smartgrid_design.Draft'], null=True, blank=True), keep_default=False)

        # Adding field 'DesignerQuestionChoice.draft'
        db.add_column('smartgrid_design_designerquestionchoice', 'draft', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['smartgrid_design.Draft'], null=True, blank=True), keep_default=False)

        # Adding field 'DesignerTextPromptQuestion.draft'
        db.add_column('smartgrid_design_designertextpromptquestion', 'draft', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['smartgrid_design.Draft'], null=True, blank=True), keep_default=False)

        # Adding field 'DesignerAction.draft'
        db.add_column('smartgrid_design_designeraction', 'draft', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['smartgrid_design.Draft'], null=True, blank=True), keep_default=False)

        # Adding unique constraint on 'DesignerAction', fields ['draft', 'slug']
        db.create_unique('smartgrid_design_designeraction', ['draft_id', 'slug'])

        # Adding field 'DesignerColumnName.draft'
        db.add_column('smartgrid_design_designercolumnname', 'draft', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['smartgrid_design.Draft'], null=True, blank=True), keep_default=False)

        # Changing field 'DesignerColumnName.name'
        db.alter_column('smartgrid_design_designercolumnname', 'name', self.gf('django.db.models.fields.CharField')(max_length=50))


    def backwards(self, orm):
        
        # Removing unique constraint on 'DesignerAction', fields ['draft', 'slug']
        db.delete_unique('smartgrid_design_designeraction', ['draft_id', 'slug'])

        # Removing unique constraint on 'DesignerColumnGrid', fields ['draft', 'name', 'level']
        db.delete_unique('smartgrid_design_designercolumngrid', ['draft_id', 'name_id', 'level_id'])

        # Removing unique constraint on 'DesignerGrid', fields ['column', 'action', 'row', 'draft', 'level']
        db.delete_unique('smartgrid_design_designergrid', ['column', 'action_id', 'row', 'draft_id', 'level_id'])

        # Deleting model 'Draft'
        db.delete_table('smartgrid_design_draft')

        # Deleting field 'DesignerGrid.draft'
        db.delete_column('smartgrid_design_designergrid', 'draft_id')

        # Deleting field 'DesignerColumnGrid.draft'
        db.delete_column('smartgrid_design_designercolumngrid', 'draft_id')

        # Adding unique constraint on 'DesignerColumnGrid', fields ['name', 'level']
        db.create_unique('smartgrid_design_designercolumngrid', ['name_id', 'level_id'])

        # Deleting field 'DesignerLevel.draft'
        db.delete_column('smartgrid_design_designerlevel', 'draft_id')

        # Deleting field 'DesignerQuestionChoice.draft'
        db.delete_column('smartgrid_design_designerquestionchoice', 'draft_id')

        # Deleting field 'DesignerTextPromptQuestion.draft'
        db.delete_column('smartgrid_design_designertextpromptquestion', 'draft_id')

        # Deleting field 'DesignerAction.draft'
        db.delete_column('smartgrid_design_designeraction', 'draft_id')

        # Adding unique constraint on 'DesignerAction', fields ['slug']
        db.create_unique('smartgrid_design_designeraction', ['slug'])

        # Deleting field 'DesignerColumnName.draft'
        db.delete_column('smartgrid_design_designercolumnname', 'draft_id')

        # Changing field 'DesignerColumnName.name'
        db.alter_column('smartgrid_design_designercolumnname', 'name', self.gf('django.db.models.fields.CharField')(max_length=255))


    models = {
        'smartgrid_design.designeraction': {
            'Meta': {'unique_together': "(('slug', 'draft'),)", 'object_name': 'DesignerAction'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'draft': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['smartgrid_design.Draft']", 'null': 'True', 'blank': 'True'}),
            'embedded_widget': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'expire_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'point_value': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pub_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(2013, 5, 3)'}),
            'related_resource': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'social_bonus': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'unlock_condition': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'unlock_condition_text': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'video_id': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'video_source': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        'smartgrid_design.designeractivity': {
            'Meta': {'object_name': 'DesignerActivity', '_ormbases': ['smartgrid_design.DesignerAction']},
            'admin_note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'confirm_prompt': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'confirm_type': ('django.db.models.fields.CharField', [], {'default': "'text'", 'max_length': '20'}),
            'designeraction_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['smartgrid_design.DesignerAction']", 'unique': 'True', 'primary_key': 'True'}),
            'expected_duration': ('django.db.models.fields.IntegerField', [], {}),
            'point_range_end': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'point_range_start': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'smartgrid_design.designercolumngrid': {
            'Meta': {'unique_together': "(('level', 'name', 'draft'),)", 'object_name': 'DesignerColumnGrid'},
            'column': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'draft': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['smartgrid_design.Draft']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['smartgrid_design.DesignerLevel']"}),
            'name': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['smartgrid_design.DesignerColumnName']"})
        },
        'smartgrid_design.designercolumnname': {
            'Meta': {'object_name': 'DesignerColumnName'},
            'draft': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['smartgrid_design.Draft']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'})
        },
        'smartgrid_design.designercommitment': {
            'Meta': {'object_name': 'DesignerCommitment', '_ormbases': ['smartgrid_design.DesignerAction']},
            'commitment_length': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'designeraction_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['smartgrid_design.DesignerAction']", 'unique': 'True', 'primary_key': 'True'})
        },
        'smartgrid_design.designerevent': {
            'Meta': {'object_name': 'DesignerEvent', '_ormbases': ['smartgrid_design.DesignerAction']},
            'designeraction_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['smartgrid_design.DesignerAction']", 'unique': 'True', 'primary_key': 'True'}),
            'event_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'event_location': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'event_max_seat': ('django.db.models.fields.IntegerField', [], {'default': '1000'}),
            'expected_duration': ('django.db.models.fields.IntegerField', [], {})
        },
        'smartgrid_design.designerfiller': {
            'Meta': {'object_name': 'DesignerFiller', '_ormbases': ['smartgrid_design.DesignerAction']},
            'designeraction_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['smartgrid_design.DesignerAction']", 'unique': 'True', 'primary_key': 'True'})
        },
        'smartgrid_design.designergrid': {
            'Meta': {'ordering': "('draft', 'level', 'column', 'row')", 'unique_together': "(('draft', 'level', 'column', 'row', 'action'),)", 'object_name': 'DesignerGrid'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['smartgrid_design.DesignerAction']"}),
            'column': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'draft': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['smartgrid_design.Draft']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['smartgrid_design.DesignerLevel']"}),
            'row': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'smartgrid_design.designerlevel': {
            'Meta': {'ordering': "('priority',)", 'object_name': 'DesignerLevel'},
            'draft': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['smartgrid_design.Draft']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'unlock_condition': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'unlock_condition_text': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'})
        },
        'smartgrid_design.designerquestionchoice': {
            'Meta': {'object_name': 'DesignerQuestionChoice'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['smartgrid_design.DesignerAction']"}),
            'choice': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'draft': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['smartgrid_design.Draft']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['smartgrid_design.DesignerTextPromptQuestion']"})
        },
        'smartgrid_design.designertextpromptquestion': {
            'Meta': {'object_name': 'DesignerTextPromptQuestion'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['smartgrid_design.DesignerAction']"}),
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'draft': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['smartgrid_design.Draft']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.TextField', [], {})
        },
        'smartgrid_design.draft': {
            'Meta': {'object_name': 'Draft'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        }
    }

    complete_apps = ['smartgrid_design']
