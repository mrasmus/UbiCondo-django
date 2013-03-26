# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Adding model 'Device'
        db.create_table('MainControl_device', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('deviceType', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('x', self.gf('django.db.models.fields.FloatField')()),
            ('y', self.gf('django.db.models.fields.FloatField')()),
            ('z', self.gf('django.db.models.fields.FloatField')()),
            ('address', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('toggleStatus', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('onString', self.gf('django.db.models.fields.CharField')(default='on', max_length=32)),
            ('offString', self.gf('django.db.models.fields.CharField')(default='off', max_length=32)),
        ))
        db.send_create_signal('MainControl', ['Device'])

        # Adding model 'Sensor'
        db.create_table('MainControl_sensor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hwid', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('MainControl', ['Sensor'])

        # Adding model 'PointGesture'
        db.create_table('MainControl_pointgesture', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('px', self.gf('django.db.models.fields.FloatField')()),
            ('py', self.gf('django.db.models.fields.FloatField')()),
            ('pz', self.gf('django.db.models.fields.FloatField')()),
            ('dx', self.gf('django.db.models.fields.FloatField')()),
            ('dy', self.gf('django.db.models.fields.FloatField')()),
            ('dz', self.gf('django.db.models.fields.FloatField')()),
            ('note', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('MainControl', ['PointGesture'])

        # Adding model 'Interaction'
        db.create_table('MainControl_interaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('target', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['MainControl.Device'])),
            ('complete', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('result', self.gf('django.db.models.fields.TextField')()),
            ('interType', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('MainControl', ['Interaction'])


    def backwards(self, orm):
        # Deleting model 'Device'
        db.delete_table('MainControl_device')

        # Deleting model 'Sensor'
        db.delete_table('MainControl_sensor')

        # Deleting model 'PointGesture'
        db.delete_table('MainControl_pointgesture')

        # Deleting model 'Interaction'
        db.delete_table('MainControl_interaction')


    models = {
        'MainControl.device': {
            'Meta': {'object_name': 'Device'},
            'address': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'deviceType': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'offString': ('django.db.models.fields.CharField', [], {'default': "'off'", 'max_length': '32'}),
            'onString': ('django.db.models.fields.CharField', [], {'default': "'on'", 'max_length': '32'}),
            'toggleStatus': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'x': ('django.db.models.fields.FloatField', [], {}),
            'y': ('django.db.models.fields.FloatField', [], {}),
            'z': ('django.db.models.fields.FloatField', [], {})
        },
        'MainControl.interaction': {
            'Meta': {'object_name': 'Interaction'},
            'complete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interType': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'result': ('django.db.models.fields.TextField', [], {}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['MainControl.Device']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'MainControl.pointgesture': {
            'Meta': {'object_name': 'PointGesture'},
            'dx': ('django.db.models.fields.FloatField', [], {}),
            'dy': ('django.db.models.fields.FloatField', [], {}),
            'dz': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'px': ('django.db.models.fields.FloatField', [], {}),
            'py': ('django.db.models.fields.FloatField', [], {}),
            'pz': ('django.db.models.fields.FloatField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'MainControl.sensor': {
            'Meta': {'object_name': 'Sensor'},
            'hwid': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['MainControl']