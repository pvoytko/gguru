# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Member.pasp_nom'
        db.add_column(u'gguru_member', 'pasp_nom',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Member.pasp_nom'
        db.delete_column(u'gguru_member', 'pasp_nom')


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
            'pasp_nom': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'pasp_srok': ('django.db.models.fields.DateField', [], {})
        }
    }

    complete_apps = ['gguru']