# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Player.pickpocketings'
        db.add_column('players_player', 'pickpocketings', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Player.pickpocketings'
        db.delete_column('players_player', 'pickpocketings')


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
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
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
        'locations.lair': {
            'Meta': {'object_name': 'Lair'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'lair_createdby'", 'null': 'True', 'to': "orm['players.Player']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lon': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['locations.Region']", 'null': 'True', 'blank': 'True'})
        },
        'locations.region': {
            'Meta': {'object_name': 'Region'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lon': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'npcs.npcinteraction': {
            'Meta': {'object_name': 'NPCInteraction'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'players.player': {
            'Meta': {'object_name': 'Player'},
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'has_lair': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interactions_seen': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['npcs.NPCInteraction']", 'symmetrical': 'False'}),
            'lairs': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['locations.Lair']", 'null': 'True', 'symmetrical': 'False', 'blank': 'True'}),
            'pickpocketings': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'profile_pic': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'short_bio': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'players.pocket': {
            'Meta': {'object_name': 'Pocket'},
            'has_camera': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_compass': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_phone': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['players.Player']", 'unique': 'True'})
        },
        'players.pocketartifact': {
            'Meta': {'object_name': 'PocketArtifact'},
            'artifact': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['items.Artifact']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['players.Player']", 'null': 'True', 'blank': 'True'}),
            'qty': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'players.pockettreasure': {
            'Meta': {'object_name': 'PocketTreasure'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['players.Player']", 'null': 'True', 'blank': 'True'}),
            'qty': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'treasure': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['items.Treasure']"})
        }
    }

    complete_apps = ['players']
