from . import *

# Gunrunner's Warehouse (3A) — MANIGANCE PRINCIPALE.
# When Revealed : In player order, deal any cards attached to locations as facedown encounter cards. Set all locations aside. Reveal a random
#   CAPO villain from the set-aside area, reveal Gunrunner, and attach it to them. Set all other CAPOS aside.
#
# Cartes de reference : pu090a (`Villains.RevealNextVillain`, `Villains.SetActive`), `Faces.SetAside` (game/operate/faces.py), pu109 (« reveal
# and attach » : `Find` + `AttachTo2`), commun.py (`FaceCacheeAuJoueur`-style : carte distribuee face cachee).
# ⚠ « In player order, deal ... » : une carte attachee a un lieu a la fois, joueur apres joueur en partant du premier, jusqu'a epuisement ;
# « from the set-aside area » : un CAPO PAS en jeu (les 3 rangees sont deja en jeu : il s'agit des CAPO restes de cote) ; « set all other CAPOS
# aside » : les CAPO des rangees quittent le jeu ; FAQ du livret : « tous les CAPO qui ne sont pas en jeu sont mis de cote » ;
# « each player is considered to be in their turf » (3B) : tous les joueurs rejoignent la zone du CAPO Gunrunner et la ville disparait
# (plus de deplacement) : decision de mise en oeuvre.

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        premier = Worlds.GetFirstPlayer(effect)
        joueurs = TousLesJoueurs(effect)
        etat = Ville.Etat(effect)
        lieux = [] if etat is None else [etat.cases[c] for c in sorted(etat.cases)]

        # 1. cartes attachees aux lieux, distribuees face cachee en tournant
        attachees = [a for lieu in lieux for a in list(lieu.GetAttachedAttachments())]
        for i, carte in enumerate(attachees):
            joueur = joueurs[i % len(joueurs)]
            Faces.MoveAllTo([carte], joueur.dealt_encounter_cards, effect)

        # 2. les lieux sont mis de cote, la ville n'a plus de grille
        if lieux:
            Faces.SetAside(lieux, effect)
        if etat is not None:
            effect.world.ville = None

        # 3. un CAPO au hasard parmi ceux de cote, Gunrunner lui est attache ; les autres CAPO sont mis de cote
        anciens = [v for v in Worlds.GetAllVillains(effect) if v.HasTrait("CAPO")]
        capo = Villains.RevealNextVillain(premier, effect)
        autres = [v for v in anciens if v is not capo]
        if autres:
            Faces.SetAside(autres, effect)
        if capo is None:
            return
        zone = premier.GetIdentity().card.GetGameArea()
        if capo.card.GetGameArea() is not zone:
            zone.AddCard(capo.card)
        for joueur in joueurs:
            if joueur.GetIdentity().card.GetGameArea() is not zone:
                effect.world.MovePlayerToGameArea(joueur, zone)
        gun = Find.FindAndPutIntoPlay(effect, premier, name="Gunrunner", card_type=Attachment)
        if gun is not None:
            gun.AttachTo2(capo, effect)
            gun.Reveal(premier, effect)
        Villains.SetActive(capo, effect)
        Villains.SetRule(effect, Villains.Rule(the_villain="Active"))

    return [AbilityFactory.WhenThisRevealed(None, revele)]
