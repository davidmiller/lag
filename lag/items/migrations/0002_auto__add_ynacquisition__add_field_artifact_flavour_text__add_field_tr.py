# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'YNAcquisition'
        db.create_table('items_ynacquisition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('artifact', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['items.Artifact'], null=True, blank=True)),
            ('treasure', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['items.Treasure'], null=True, blank=True)),
            ('dilemma', self.gf('django.db.models.fields.TextField')()),
            ('yes', self.gf('django.db.models.fields.TextField')()),
            ('no', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('items', ['YNAcquisition'])

        # Adding field 'Artifact.flavour_text'
        db.add_column('items_artifact', 'flavour_text', self.gf('django.db.models.fields.TextField')(null=True), keep_default=False)

        # Adding field 'Treasure.flavour_text'
        db.add_column('items_treasure', 'flavour_text', self.gf('django.db.models.fields.TextField')(null=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting model 'YNAcquisition'
        db.delete_table('items_ynacquisition')

        # Deleting field 'Artifact.flavour_text'
        db.delete_column('items_artifact', 'flavour_text')

        # Deleting field 'Treasure.flavour_text'
        db.delete_column('items_treasure', 'flavour_text')


    models = {
        'items.artifact': {
            'Meta': {'object_name': 'Artifact'},
            'created_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'flavour_text': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'released': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'released_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        'items.treasure': {
            'Meta': {'object_name': 'Treasure'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'created_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'flavour_text': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'released': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'released_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        'items.ynacquisition': {
            'Meta': {'object_name': 'YNAcquisition'},
            'artifact': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['items.Artifact']", 'null': 'True', 'blank': 'True'}),
            'dilemma': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'no': ('django.db.models.fields.TextField', [], {}),
            'treasure': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['items.Treasure']", 'null': 'True', 'blank': 'True'}),
            'yes': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['items']
