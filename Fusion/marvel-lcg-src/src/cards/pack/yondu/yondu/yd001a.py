from . import *

# * Yondu — face HEROS. PV 10, ATQ 2, CTR 2, DEF 2, main 5.
# GUARDIAN. RAVAGER.
# D'ast Whistlin' — Interrupt: When the Yaka Arrow upgrade is attached to or
#   removed from an enemy, deal 1 damage to that enemy. When it is attached to
#   your identity, heal 1 damage from Yondu.
#
# LE MOTEUR DU PACK. Chaque DEPLACEMENT de la fleche devient un effet :
#   arrive sur un ennemi   -> 1 degat a cet ennemi
#   quitte un ennemi       -> 1 degat a cet ennemi
#   arrive sur l'identite  -> 1 soin sur Yondu
# Un aller-retour ennemi -> identite -> ennemi fait donc mal TROIS fois.
#
# Cartes de reference :
#  - **`al001a`** * Alligator Loki (pack alligator_loki) : le SEUL precedent du
#    depot d'un heros qui reagit aux attaches et aux detaches. Il a deja etabli
#    que `AttachTo2` / `DetachFrom2` emettent `AfterCardAttachTo` et
#    `AfterCardDetachFrom` (can_attach.py:49-104), et que `OnEvent.AttachedMove`
#    est ce qui les ecoute cote valeurs continues.
#  - `AbilityFactory.AfterCardAttachTo(type, which_card, to_which_card, op)`
#    (card_move.py:141) pour l'arrivee.
#  - ⚠ **AUCUNE FABRIQUE POUR LE DETACHEMENT** : `AfterCardDetachFrom` n'en a
#    pas. L'abilite est donc construite a la main avec `Ability(...)`, comme
#    `aa001b` * Agatha Harkness et `cd008` le font deja pour d'autres messages.
#  - `08013` / partout pour `DealDamage`, `42018` pour `HealthUnits`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « attached to **OR REMOVED FROM** an enemy » : DEUX declencheurs, donc
#    DEUX capacites — un seul `Ability` ne peut pas ecouter deux messages.
#    Oublier le retrait couperait la carte en deux, et c'est la moitie la plus
#    facile a oublier.
#  - « to **that** enemy » : l'ennemi concerne par le mouvement, jamais un
#    choix offert (piege `wd022`). Il se lit dans le message : `to_face` a
#    l'arrivee, `from_face` au depart.
#  - « an **ENEMY** » : vilain ou sbire. Une fleche qui se pose sur un ALLIE
#    ne fait rien — et c'est cohérent, le texte ne prevoit que trois
#    destinations : un ennemi, l'identite, la main.
#  - « heal 1 damage from **YONDU** » : un NOM PROPRE. Mais ici il designe
#    l'IDENTITE — la phrase precedente dit « attached to your identity » —, et
#    l'alter-ego s'appelle Yondu Udonta. Le soin vise donc la face qui porte
#    la fleche, c'est-a-dire l'identite courante.
#  - « **Interrupt** » : le texte annonce une interruption, mais le moteur
#    n'offre AUCUNE fenetre « would detach » (`DetachFrom2` n'emet
#    `AfterCardDetachFrom` qu'APRES coup, constat deja ecrit dans le pack
#    alligator_loki). ECART ASSUME : les deux capacites sont montees en
#    `AbilityType.Interrupt` sur des messages d'APRES-COUP. Sans consequence
#    de jeu ici — l'ennemi et le heros existent encore quand les 1 degat ou
#    1 soin tombent, et aucune autre carte ne s'intercale entre les deux.


def GetAbilities() -> Sequence['Ability']:

    def arrivee(effect: 'Effect', message: 'Message.AfterCardAttachTo') -> None:
        this = effect.this.CastTo(Hero)

        hote = message.to_face
        if hote is None:
            return

        if Enemy.IsType(hote):
            this.DealDamage([hote], 1, effect)
            return

        # « When it is attached to your identity, heal 1 damage from Yondu. »
        joueur = JoueurDeCetteCarte(effect)
        if joueur is not None and hote is joueur.GetIdentity():
            this.HealthUnits([hote], 1, effect)

    return [
        AbilityFactory.AfterCardAttachTo(
            AbilityType.Interrupt,
            CardFinder(name=NOM_FLECHE, card_type=Upgrade),
            None,
            arrivee,
        ).SetName("D'ast Whistlin'"),
    ]
