# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Player'
        db.create_table('players_player', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('short_bio', self.gf('django.db.models.fields.CharField')(max_length=400, null=True, blank=True)),
            ('profile_pic', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('has_lair', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('players', ['Player'])

        # Adding M2M table for field lairs on 'Player'
        db.create_table('players_player_lairs', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('player', models.ForeignKey(orm['players.player'], null=False)),
            ('lair', models.ForeignKey(orm['locations.lair'], null=False))
        ))
        db.create_unique('players_player_lairs', ['player_id', 'lair_id'])

        # Adding model 'Pocket'
        db.create_table('players_pocket', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['players.Player'], unique=True)),
            ('has_phone', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_camera', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_compass', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('players', ['Pocket'])

        # Adding model 'PocketArtifact'
        db.create_table('players_pocketartifact', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['players.Player'], null=True, blank=True)),
            ('qty', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('artifact', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['items.Artifact'])),
        ))
        db.send_create_signal('players', ['PocketArtifact'])

        # Adding model 'PocketTreasure'
        db.create_table('players_pockettreasure', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['players.Player'], null=True, blank=True)),
            ('qty', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('treasure', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['items.Treasure'])),
        ))
        db.send_create_signal('players', ['PocketTreasure'])


    def backwards(self, orm):
        
        # Deleting model 'Player'
        db.delete_table('players_player')

        # Removing M2M table for field lairs on 'Player'
        db.delete_table('players_player_lairs')

        # Deleting model 'Pocket'
        db.delete_table('players_pocket')

        # Deleting model 'PocketArtifact'
        db.delete_table('players_pocketartifact')

        # Deleting model 'PocketTreasure'
        db.delete_table('players_pockettreasure')


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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'released': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'released_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        'locations.lair': {
            'Meta': {'object_name': 'Lair'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
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
        'players.player': {
            'Meta': {'object_name': 'Player'},
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'has_lair': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lairs': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['locations.Lair']", 'null': 'True', 'symmetrical': 'False', 'blank': 'True'}),
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
