# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'NewsItem.datetime'
        db.add_column('news_newsitem', 'datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'NewsItem.datetime'
        db.delete_column('news_newsitem', 'datetime')


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
        'locations.place': {
            'Meta': {'object_name': 'Place'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['players.Player']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'items_found': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lon': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'placetype': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['locations.PlaceType']", 'null': 'True', 'blank': 'True'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['locations.Region']", 'null': 'True', 'blank': 'True'}),
            'unique_visitors': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'visits': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'locations.placetype': {
            'Meta': {'object_name': 'PlaceType'},
            'artifact_percentage': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'doctor_percentage': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'epic_percentage': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mythic_percentage': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'philosopher_percentage': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'soothsayer_percentage': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'wizard_percentage': ('django.db.models.fields.IntegerField', [], {'default': '10'})
        },
        'locations.region': {
            'Meta': {'object_name': 'Region'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lon': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'news.newsitem': {
            'Meta': {'object_name': 'NewsItem'},
            'artifact': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['items.Artifact']", 'null': 'True', 'blank': 'True'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'newstype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['news.NewsType']"}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['locations.Place']"}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['players.Player']"}),
            'treasure': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['items.Treasure']", 'null': 'True', 'blank': 'True'})
        },
        'news.newstype': {
            'Meta': {'object_name': 'NewsType'},
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
            'profile_pic': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'short_bio': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['news']
