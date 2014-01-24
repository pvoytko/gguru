# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Group'
        db.create_table(u'gguru_group', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'gguru', ['Group'])


    def backwards(self, orm):
        # Deleting model 'Group'
        db.delete_table(u'gguru_group')


    models = {
        u'gguru.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['gguru']