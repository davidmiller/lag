from django.test import TestCase

from lag.items.models import Artifact, Treasure
from lag.players.models import PocketArtifact, PocketTreasure

class PocketArtifactTestCase(TestCase):
    "Artifacts that players have"
    fixtures = ['fixture.json']

    def test_desc(self):
        "Get the artifact's description"
        artifact = PocketArtifact(artifact=Artifact(flavour_text="Scarab"))
        self.assertEqual("Scarab", artifact.iten_desc)

    def test_name(self):
        """ get the artifact's name """
        artifact = PocketArtifact(artifact=Artifact(name="Scarab"))
        self.assertEqual("Scarab", artifact.item_name)



class PocketTreasureTestCase(TestCase):
    "Treasures that players have"
    fixtures = ['fixture.json']

    def test_desc(self):
        "Get the treasure's description"
        treasure = PocketTreasure(treasure=Treasure(flavour_text="Scarab"))
        self.assertEqual("Scarab", treasure.iten_desc)

    def test_name(self):
        """ get the treasure's name """
        treasure = PocketTreasure(treasure=Treasure(name="Scarab"))
        self.assertEqual("Scarab", treasure.item_name)



