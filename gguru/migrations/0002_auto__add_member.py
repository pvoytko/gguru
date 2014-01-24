# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Member'
        db.create_table(u'gguru_member', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gguru.Group'])),
            ('fio', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('grazd', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('dr', self.gf('django.db.models.fields.DateField')()),
            ('pasp_srok', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'gguru', ['Member'])


    def backwards(self, orm):
        # Deleting model 'Member'
        db.delete_table(u'gguru_member')


    models = {
        u'gguru.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'gguru.member': {
            'Meta': {'object_name': 'Member'},
            'dr': ('django.db.models.fields.DateField', [], {}),
            'fio': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'grazd': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gguru.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pasp_srok': ('django.db.models.fields.DateField', [], {})
        }
    }

    complete_apps = ['gguru']