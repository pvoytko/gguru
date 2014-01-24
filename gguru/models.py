# -*- coding: utf-8 -*-

from django.db import models

# Чтобы в дебаг-репортах было видно ID.
class GGuruModel(models.Model):

    class Meta:
        abstract=True

    def __str__(self):
        return "{0} #{1}".format(super(GGuruModel, self).__str__(), self.id)


# Группа
class Group(GGuruModel):

    PLACE_TYPE_SHIP = 'ship'
    PLACE_TYPE_HOTEL = 'hotel'
    PLACE_TYPE_OTHER = 'other'
    PLACE_TYPE_CHOICES = (
        (PLACE_TYPE_SHIP, u'Корабль'),
        (PLACE_TYPE_HOTEL, u'Отель'),
        (PLACE_TYPE_OTHER, u'Иное'),
    )

    SHIP_CHOICES = (
        (1, "Adventure of the Seas"),
        (2, "Adonia"),
        (3, "AIDAbella"),
        (4, "AIDAblu"),
        (5, "AIDAmar"),
        (6, "AIDAsol"),
        (7, "Albatros"),
        (8, "Amadea"),
        (9, "Arcadia"),
        (10, "Artania"),
        (11, "Athena"),
        (12, "Aurora"),
        (13, "Azamara Journey"),
        (14, "Azura"),
        (15, "Balmoral"),
        (16, "Black Watch"),
        (17, "Boudicca"),
        (18, "Braemar"),
        (19, "Brilliance of the Seas"),
        (20, "Carnival Legend"),
        (21, "Century"),
        (22, "Constellation"),
        (23, "Costa Atlantica"),
        (24, "Costa Deliziosa"),
        (25, "Costa Fortuna"),
        (26, "Costa Luminosa"),
        (27, "Costa Magica"),
        (28, "Costa Marina"),
        (29, "Costa Mediterranea"),
        (30, "Costa NeoRomantica"),
        (31, "Costa Pacifica"),
        (32, "Crown Princess"),
        (33, "Crystal Serenity"),
        (34, "Crystal Symphony"),
        (35, "Discovery"),
        (36, "Disney Magic"),
        (37, "Eclipse"),
        (38, "Emerald Princess"),
        (39, "Empress"),
        (40, "Eurodam"),
        (41, "Europa"),
        (42, "Grand Mistral"),
        (43, "Grand Princess"),
        (44, "Insignia"),
        (45, "Jewel of the Seas"),
        (46, "Legend of the Seas"),
        (47, "Marco Polo"),
        (48, "Marina"),
        (49, "Mein Schiff"),
        (50, "Minerva"),
        (51, "MSC Lirica"),
        (52, "MSC Magnifica"),
        (53, "MSC Musica"),
        (54, "MSC Opera"),
        (55, "MSC Orchestra"),
        (56, "MSC Poesia"),
        (57, "MV Explorer"),
        (58, "Nautica"),
        (59, "Norwegian Star"),
        (60, "Norwegian Sun"),
        (61, "Ocean Countess"),
        (62, "Ocean Princess"),
        (63, "Oriana"),
        (64, "Princess Anastasia"),
        (65, "Princess Daphne"),
        (66, "Princess Maria"),
        (67, "Prinsendam"),
        (68, "Queen Elizabeth"),
        (69, "Queen Victoria"),
        (70, "Regatta"),
        (71, "Rotterdam"),
        (72, "Royal Princess"),
        (73, "Ryndam"),
        (74, "Saga Pearl"),
        (75, "Saga Ruby"),
        (76, "Saga Sapphire"),
        (77, "Seabourn Legend"),
        (78, "Seabourn Pride"),
        (79, "Seabourn Quest"),
        (80, "Seabourn Sojourn"),
        (81, "SeaDream"),
        (82, "Seven Seas Voyager"),
        (83, "Silja Festival"),
        (84, "Silver Cloud"),
        (85, "Silver Whisper"),
        (86, "Star Flyer"),
        (87, "Star Princess"),
        (88, "Tahitian Princess"),
        (89, "Thomson Spirit"),
        (90, "Viking Star"),
        (91, "Vision of the Seas"),
        (92, "Wind Spirit"),
        (93, "Wind Surf"),
    )

    req_number = models.CharField(max_length=100)
    date_begin = models.DateField()
    date_end = models.DateField()
    place_type = models.CharField(max_length=5, choices=PLACE_TYPE_CHOICES)
    ship = models.IntegerField(choices=SHIP_CHOICES, null=True, blank=True)
    hotel = models.CharField(max_length=255, null=True, blank=True)
    other_place = models.CharField(max_length=255, null=True, blank=True)

    def getPlaceDescr(self):
        import gg_json
        place = ""
        if self.place_type == self.PLACE_TYPE_SHIP:
            place = gg_json.choiceToText(self.ship, self.SHIP_CHOICES)
        if self.place_type == self.PLACE_TYPE_HOTEL:
            place = self.hotel
        if self.place_type == self.PLACE_TYPE_OTHER:
            place = self.other_place
        return gg_json.choiceToText(self.place_type, self.PLACE_TYPE_CHOICES) + ": " + place


# Участинк
class Member(GGuruModel):
    group = models.ForeignKey(Group)
    fio = models.CharField(max_length=255)
    grazd = models.CharField(max_length=255)
    dr = models.DateField()
    pasp_srok = models.DateField()
    pasp_nom = models.CharField(max_length=100)

    def getGroupName(self):
        return self.group.req_number + " " + self.group.getPlaceDescr()
