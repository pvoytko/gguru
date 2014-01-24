# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Group.number'
        db.delete_column(u'gguru_group', 'number')

        # Adding field 'Group.req_number'
        db.add_column(u'gguru_group', 'req_number',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Group.number'
        raise RuntimeError("Cannot reverse this migration. 'Group.number' and its values cannot be restored.")
        # Deleting field 'Group.req_number'
        db.delete_column(u'gguru_group', 'req_number')


    models = {
        u'gguru.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'req_number': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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