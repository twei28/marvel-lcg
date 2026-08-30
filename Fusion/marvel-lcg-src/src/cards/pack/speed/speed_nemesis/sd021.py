from . import *

# Magic Chains — ATTACHEMENT nemesis, custom « CptScorp »
# `ATK+ "1"`, 1 icone de bonus, traits WEAPON / MYSTIC.
# Attach to Coat of Arms, if able. If you cannot, attach to the villain.
# Forced Response: After the attached enemy attacks, if the attack deals
#   damage, stun your hero -> discard this card.
#
# ⚠ LA CLE DE DONNEES EST `ATK+`, JAMAIS `ATK`. « +1 ATK » sur un attachement
# est un BONUS donne a la carte porteuse, pas une valeur d'attaque propre :
# `ATK` ferait de l'attachement une carte a 1 d'ATQ, ce qui n'a aucun sens.
# La cle est lue nativement, rien a coder ici (verifie dans cards.json).
#
# ---------------------------------------------------------------------------
# L'ATTACHE CONDITIONNELLE -> `AbilityFactory.AttachToFaceWhenPutIntoPlay(
# CardFinder(name="Coat of Arms"), if_cannot_attach_to=Villain)`. Modeles
# exacts : `04029` Crossfire's Rifle et `04064` Crossbones' Machine Gun, qui
# impriment la meme tournure (« Attach to X. Otherwise, attach to the
# villain »).
#
# La recherche par nom est ici sans danger : « Coat of Arms » est un nom
# unique du catalogue, et il appartient a ce set nemesis. (Le piege du `*`
# d'unicite est evite : la constante `NOM_COAT_OF_ARMS` est ecrite SANS
# l'etoile, `cards/paper.py:45` la retirant du nom effectif.)
#
# ---------------------------------------------------------------------------
# LE FORCED RESPONSE -> `AbilityFactory.AfterUnitAttackUnit(AbilityType
# .ForcedResponse, "AttachedEnemy", None, ..., dealt_damage=True)`.
#
# `"AttachedEnemy"` est une cible-chaine du moteur
# (condition/card_type.py:38 et 184) : elle designe l'ennemi PORTEUR de cet
# attachement, donc Coat of Arms ou le vilain selon ou la carte a atterri.
# C'est bien « THE ATTACHED enemy » et non « un ennemi ».
#
# `dealt_damage=True` rend « IF THE ATTACK DEALS DAMAGE » : une attaque
# entierement defendue ou prevenue ne declenche rien.
#
# ---------------------------------------------------------------------------
# « STUN YOUR HERO -> DISCARD THIS CARD » :
#
# - « YOUR hero » = le heros du joueur que l'ennemi attache vient d'attaquer,
#   lu sur `message.to_player` (et non `message.GetToPlayer()`, dont le repli
#   contient un assert cable sur la carte 44014 : voir le commentaire de
#   sd019).
#
# - LA FLECHE EST UN COUT -> UN EFFET, arbitrage de l'utilisateur du
#   30/08/2026 (« on suit la regle »). C'est la regle officielle : a gauche de
#   la fleche le COUT, a droite l'EFFET, et la capacite ne se declenche que si
#   le cout est integralement payable. Elle vaut aussi pour une capacite
#   FORCEE, comme le montrent les seules cartes rencontre du depot qui
#   impriment une fleche dans un Forced : `11014` Temporal Shield (« discard
#   Temporal Shield -> prevent all damage »), `11031` Chitauri Soldier et
#   `16074` Biogram Image. Quand une carte veut DEUX consequences, elle les
#   relie par « and » SANS fleche : `02021` Pumpkin Bombs (« discard Pumpkin
#   Bombs AND take 2 indirect damage »).
#
#   Ici : cout = « stun your hero », effet = « discard this card ».
#   Cout impayable => RIEN ne se passe, ni etourdissement ni defausse, et
#   l'attachement RESTE en jeu avec son +1 ATQ. Deux cas concrets :
#     * le joueur est en identite civile : il n'a aucun heros a etourdir ;
#     * le heros est DEJA etourdi (ou Stalwart) : `CanbeStunned()` est faux,
#       un personnage ne pouvant pas porter deux fois le meme statut.
#   La premiere version de ce module defaussait la carte dans tous les cas :
#   c'etait la lecture inverse, et elle rendait les chaines a usage unique.
#
# ⚠ Si sd018 The Real Question est en jeu, cet attachement a gagne PERMANENT
# et la defausse est bloquee par le moteur (`HasPermanent.OnWhenCardLeavePlay`).
# Contrairement a la Hero Action de sd020, il n'y a RIEN a conditionner ici :
# c'est un Forced Response, il doit partir de toute facon, et le blocage de
# sortie de jeu est une regle du mot-cle, pas une erreur. La carte reste alors
# attachee et pourra etourdir de nouveau — consequence directe et voulue de
# Permanent.


def GetAbilities() -> Sequence['Ability']:

    def magic_chains(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this.CastTo(Attachment)

        joueur = message.to_player
        if not Player.IsType(joueur):
            return

        heros = joueur.GetHero()
        # Le COUT d'abord : s'il n'est pas payable, l'effet n'a pas lieu.
        if heros is None or not heros.CanbeStunned():
            return

        Faces.GiveStatus([heros], "Stunned", effect)
        Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(name=NOM_COAT_OF_ARMS),
            if_cannot_attach_to=Villain,
        ),
        AbilityFactory.AfterUnitAttackUnit(
            AbilityType.ForcedResponse,
            "AttachedEnemy",
            None,
            magic_chains,
            dealt_damage=True,
        ),
    ]
