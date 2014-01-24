# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Member.group'
        db.add_column(u'gguru_member', 'group',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=2, to=orm['gguru.Group']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Member.group'
        db.delete_column(u'gguru_member', 'group_id')


    models = {
        u'gguru.group': {
            'Meta': {'object_name': 'Group'},
            'date_begin': ('django.db.models.fields.DateField', [], {}),
            'date_end': ('django.db.models.fields.DateField', [], {}),
            'hotel': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'other_place': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'place_type': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'req_number': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ship': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
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