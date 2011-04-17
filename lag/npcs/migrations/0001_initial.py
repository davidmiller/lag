# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'NPCInteraction'
        db.create_table('npcs_npcinteraction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('level', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('npcs', ['NPCInteraction'])

        # Adding model 'SoothSayer'
        db.create_table('npcs_soothsayer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('icon', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('npcs', ['SoothSayer'])

        # Adding M2M table for field interactions on 'SoothSayer'
        db.create_table('npcs_soothsayer_interactions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('soothsayer', models.ForeignKey(orm['npcs.soothsayer'], null=False)),
            ('npcinteraction', models.ForeignKey(orm['npcs.npcinteraction'], null=False))
        ))
        db.create_unique('npcs_soothsayer_interactions', ['soothsayer_id', 'npcinteraction_id'])

        # Adding model 'Wizard'
        db.create_table('npcs_wizard', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('icon', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('npcs', ['Wizard'])

        # Adding M2M table for field interactions on 'Wizard'
        db.create_table('npcs_wizard_interactions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('wizard', models.ForeignKey(orm['npcs.wizard'], null=False)),
            ('npcinteraction', models.ForeignKey(orm['npcs.npcinteraction'], null=False))
        ))
        db.create_unique('npcs_wizard_interactions', ['wizard_id', 'npcinteraction_id'])

        # Adding model 'Doctor'
        db.create_table('npcs_doctor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('icon', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('npcs', ['Doctor'])

        # Adding M2M table for field interactions on 'Doctor'
        db.create_table('npcs_doctor_interactions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('doctor', models.ForeignKey(orm['npcs.doctor'], null=False)),
            ('npcinteraction', models.ForeignKey(orm['npcs.npcinteraction'], null=False))
        ))
        db.create_unique('npcs_doctor_interactions', ['doctor_id', 'npcinteraction_id'])

        # Adding model 'Philosopher'
        db.create_table('npcs_philosopher', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('icon', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('npcs', ['Philosopher'])

        # Adding M2M table for field interactions on 'Philosopher'
        db.create_table('npcs_philosopher_interactions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('philosopher', models.ForeignKey(orm['npcs.philosopher'], null=False)),
            ('npcinteraction', models.ForeignKey(orm['npcs.npcinteraction'], null=False))
        ))
        db.create_unique('npcs_philosopher_interactions', ['philosopher_id', 'npcinteraction_id'])


    def backwards(self, orm):
        
        # Deleting model 'NPCInteraction'
        db.delete_table('npcs_npcinteraction')

        # Deleting model 'SoothSayer'
        db.delete_table('npcs_soothsayer')

        # Removing M2M table for field interactions on 'SoothSayer'
        db.delete_table('npcs_soothsayer_interactions')

        # Deleting model 'Wizard'
        db.delete_table('npcs_wizard')

        # Removing M2M table for field interactions on 'Wizard'
        db.delete_table('npcs_wizard_interactions')

        # Deleting model 'Doctor'
        db.delete_table('npcs_doctor')

        # Removing M2M table for field interactions on 'Doctor'
        db.delete_table('npcs_doctor_interactions')

        # Deleting model 'Philosopher'
        db.delete_table('npcs_philosopher')

        # Removing M2M table for field interactions on 'Philosopher'
        db.delete_table('npcs_philosopher_interactions')


    models = {
        'npcs.doctor': {
            'Meta': {'object_name': 'Doctor'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interactions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['npcs.NPCInteraction']", 'symmetrical': 'False'})
        },
        'npcs.npcinteraction': {
            'Meta': {'object_name': 'NPCInteraction'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'npcs.philosopher': {
            'Meta': {'object_name': 'Philosopher'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interactions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['npcs.NPCInteraction']", 'symmetrical': 'False'})
        },
        'npcs.soothsayer': {
            'Meta': {'object_name': 'SoothSayer'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interactions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['npcs.NPCInteraction']", 'symmetrical': 'False'})
        },
        'npcs.wizard': {
            'Meta': {'object_name': 'Wizard'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interactions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['npcs.NPCInteraction']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['npcs']
