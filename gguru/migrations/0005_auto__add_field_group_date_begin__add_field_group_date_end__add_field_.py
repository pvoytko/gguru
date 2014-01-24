# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Group.date_begin'
        db.add_column(u'gguru_group', 'date_begin',
                      self.gf('django.db.models.fields.DateField')(default='2014-01-25'),
                      keep_default=False)

        # Adding field 'Group.date_end'
        db.add_column(u'gguru_group', 'date_end',
                      self.gf('django.db.models.fields.DateField')(default='2014-01-25'),
                      keep_default=False)

        # Adding field 'Group.place_type'
        db.add_column(u'gguru_group', 'place_type',
                      self.gf('django.db.models.fields.CharField')(default='ship', max_length=5),
                      keep_default=False)

        # Adding field 'Group.ship'
        db.add_column(u'gguru_group', 'ship',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Group.hotel'
        db.add_column(u'gguru_group', 'hotel',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Group.other_place'
        db.add_column(u'gguru_group', 'other_place',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Member.group'
        db.delete_column(u'gguru_member', 'group_id')


    def backwards(self, orm):
        # Deleting field 'Group.date_begin'
        db.delete_column(u'gguru_group', 'date_begin')

        # Deleting field 'Group.date_end'
        db.delete_column(u'gguru_group', 'date_end')

        # Deleting field 'Group.place_type'
        db.delete_column(u'gguru_group', 'place_type')

        # Deleting field 'Group.ship'
        db.delete_column(u'gguru_group', 'ship')

        # Deleting field 'Group.hotel'
        db.delete_column(u'gguru_group', 'hotel')

        # Deleting field 'Group.other_place'
        db.delete_column(u'gguru_group', 'other_place')


        # User chose to not deal with backwards NULL issues for 'Member.group'
        raise RuntimeError("Cannot reverse this migration. 'Member.group' and its values cannot be restored.")

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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pasp_nom': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'pasp_srok': ('django.db.models.fields.DateField', [], {})
        }
    }

    complete_apps = ['gguru']