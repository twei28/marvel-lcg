from cards.pack import *

# ===========================================================================
# Helpers partages du set « Beta Ray Bill » (Rainy, set 158, prefixe `br`).
#
# ⚠ TOUT LE PACK TOURNE AUTOUR D'UNE SEULE AMELIORATION : br010 Stormbreaker.
# Elle est UNIQUE, Restreinte, coute 1, et SEPT des treize cartes la citent
# nommement :
#   - br001a « Worthy » la RAPPELLE EN MAIN, et frappe pour 3 si elle etait en
#     jeu ;
#   - br003 Hammer Throw l'INCLINE, frappe pour 6, puis la rappelle ;
#   - br004 Hammer Twirl l'INCLINE pour prevenir, et frappe si elle a PAYE ;
#   - br002 Eye of the Storm ignore la crise si elle a PAYE ;
#   - br008 Calm Before the Storm change de bonus selon qu'elle est EN JEU ;
#   - br010 elle-meme se DEFAUSSE pour payer un evenement ;
#   - br012 Unworthy la CACHE sous elle, et la rend introuvable.
# Le marteau fait donc l'aller-retour main <-> jeu en permanence, et c'est le
# moteur economique du heros.
#
# ⚠ LES DEUX FACES PORTENT LE MEME NOM. Beta Ray Bill n'a pas d'identite
# civile : `br001a` et `br001b` s'appellent toutes deux « * Beta Ray Bill ».
# Un `CardFinder(name=...)` ne distingue donc PAS les deux formes — il faut
# passer par le TYPE (`Hero` / `AlterEgo`) partout ou la forme compte.
# ===========================================================================

NOM_HEROS = "Beta Ray Bill"
NOM_MARTEAU = "Stormbreaker"
NOM_VAISSEAU = "Skuttlebutt"
NOM_STAR_JUMP = "Star Jump"
SET_HEROS: 'CardFace.SETNAMES' = "Beta Ray Bill"
COMPTEUR_INDIGNE: 'CardFace.COUNTER' = 'unworthy'


def JoueurDeCetteCarte(effect: 'Effect') -> 'Player|None':
    """Le joueur a qui appartient la carte qui agit.

    ⚠ NE PAS se rabattre sur `effect.GetInitiator()` en premier : il leve un
    assert quand l'initiateur n'est pas un joueur, et le moteur AVALE
    l'exception — la carte ne fait alors rien, et aucun outil ne le voit
    (leçon `Player.GetHero()`, pack lady_sif).

    ⚠ Passer le joueur EXPLICITEMENT quand la carte qui agit ne lui appartient
    pas : c'est le cas de l'obligation br012, carte de RENCONTRE donnee au
    joueur, pour laquelle ce helper ne rend rien (leçon yd013 / dr010 / tt020).
    """
    porteur = getattr(effect, "this", None)
    if porteur is not None:
        controleur = porteur.GetControlByOrOwner()
        if Player.IsType(controleur):
            return controleur
    initiateur = getattr(effect, "initiator", None)
    if initiateur is not None and Player.IsType(initiateur):
        return initiateur
    return None


def HerosDuJoueur(effect: 'Effect') -> 'CardFace|None':
    """La face HEROS de l'identite, ou None si le joueur est en civil.

    ⚠ LE FILTRE EST LE TYPE, PAS LE NOM : les deux faces s'appellent
    « Beta Ray Bill ».
    """
    joueur = JoueurDeCetteCarte(effect)
    if joueur is None:
        return None
    identite = joueur.GetIdentity()
    if identite is None or not Hero.IsType(identite):
        return None
    return identite


def MarteauEnJeu(effect: 'Effect') -> 'CardFace|None':
    """Stormbreaker sur le terrain, ou None.

    Lu par br008 (« while Stormbreaker is in play ») et par br001a, qui ne
    frappe que si le marteau QUITTE le jeu pour rejoindre la main.
    """
    return Worlds.FindCardOnField(effect, name=NOM_MARTEAU, card_type=Upgrade)


def VaisseauEnJeu(effect: 'Effect') -> 'CardFace|None':
    """Skuttlebutt sur le terrain, ou None (br005 le redresse)."""
    return Worlds.FindCardOnField(effect, name=NOM_VAISSEAU, card_type=Support)


def EstCarteDeBill(face: 'CardFace|None') -> bool:
    """« a Beta Ray Bill card » (br005 Star Jump).

    Le moteur a la primitive : `IsDeckBuildingClass` (card_player.py:169)
    verifie D'ABORD la classe `IdentitySpecific`, PUIS l'egalite litterale du
    `set_name`. Ne PAS comparer les noms a la main.
    """
    if face is None or not ClassCard.IsType(face):
        return False
    return face.IsDeckBuildingClass(SET_HEROS)


def MarteauAPaye(effect: 'Effect') -> bool:
    """« used Stormbreaker to pay for this card » (br002, br004).

    ⚠ CE N'EST PAS UNE COULEUR DE RESSOURCE, C'EST UNE CARTE. Le moteur garde
    les EFFETS qui ont paye dans `effect.context.paid_this_res_effects`
    (effect_context.py:33), et chacun porte sa carte sur `.this` — montage
    `dz036` (pack dazzler), qui compte les chansons ayant paye. Lire seulement
    `GetPaidResources()` (les couleurs, montage `47009`) ne dirait PAS d'ou
    elles viennent, et Stormbreaker genere du [wild] comme n'importe quelle
    autre carte.

    Lisible PENDANT la resolution, contrairement a `message.paid_res_effects`
    qui n'existe que sur `AfterPlayerPlayedCard`.
    """
    for res_effect in (getattr(effect.context, "paid_this_res_effects", None) or []):
        face = getattr(res_effect, "this", None)
        if face is not None and face.IsName(NOM_MARTEAU):
            return True
    return False


def ResoudreWorthy(effect: 'Effect', joueur: 'Player|None') -> None:
    """Le corps de la capacite « Worthy » de br001a, partage avec br008.

    br008 Calm Before the Storm dit « resolve your hero's Worthy ability
    (IGNORING ITS LIMIT) » : ecrire deux fois le meme effet ferait diverger
    les deux cartes des la premiere correction. Il vit donc ici.

    « Find Stormbreaker and add it to your hand. If it LEAVES PLAY this way,
    deal 3 damage to an enemy. » — les 3 degats ne tombent QUE si le marteau
    etait EN JEU.
    """
    if joueur is None:
        return
    marteau = MarteauEnJeu(effect)
    if marteau is not None:
        Faces.ReturnToHand([marteau], "Owner", effect)
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Deal 3 damage to an enemy",
                lambda cibles: effect.this.DealDamage(cibles, 3, effect),
            ).SetTarget(Enemy),
        )
        return
    face = Search.PlayerCard(
        effect, joueur,
        include_player_deck=True,
        include_discard_pile=True,
        name=NOM_MARTEAU,
        card_type=Upgrade,
    )
    if face is not None:
        joueur.GainCard(face, effect)
