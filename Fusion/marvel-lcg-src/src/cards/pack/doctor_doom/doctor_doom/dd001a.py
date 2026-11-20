from . import *

# * Doctor Doom — heros. LATVERIA. MYSTIC. CTR 3 / ATQ 1 / DEF 2, MNG 5, 11 PV.
# Power Syphon — Response: After you pay for a SPELL event using a [mental]
#   resource, place 1 power counter here (to a maximum of 3).
# Overwhelming Power — Action: Remove 3 power counters -> you gain villainous
#   until the end of the round. Ignore any boost effects on boost cards dealt
#   to you.
#
# Cartes de reference :
#  - « After you pay for a <type> using a [X] resource » :
#    `AfterPlayerPlayedCard(type, "You", CardFinder2("SPELL", Event), op)`
#    (play.py:275). Son message porte `paid_resources` (sender_player.py:204),
#    donc la couleur payee se relit sans passer par `effect.GetPaidResources()`,
#    qui designerait le paiement de CETTE capacite et non celui de l'evenement.
#    C'est la difference avec 01013 Photonic Blast, ou la carte payee EST la
#    carte qui teste.
#  - compteurs plafonnes sur sa propre identite : bt023 / aos/campaign.py,
#    `PlaceCountersInternal(n, 'power', effect, maximum=3)`. Le compteur
#    `power` existait DEJA dans l'enum COUNTER, rien a ajouter.
#  - depense de compteurs en cout : 23016 Command Team,
#    `CostFunc.Counter("This", 3, 'power')`.
#  - mot-cle temporaire : ab003 / 12016, `GainUntilRoundEnd(effect, ...)`.
#
# ⚠ EXTENSION MOTEUR pour « you gain villainous » (01/09/2026, voir le
# __init__.py du pack) : `HasVillainous` etait reserve aux SBIRES et la classe
# `Hero` n'en heritait pas ; `GainUntilRoundEnd` n'acceptait pas le parametre.
# Les deux ont ete corriges, plus un garde `num <= 0` dans `can_boost.py` sans
# lequel TOUS les heros plantaient a chaque attaque de base. Choix valide par
# l'utilisateur, et confirme par l'arrivee annoncee d'un heros OFFICIEL
# (Elektra) portant le meme effet.
#
# ⚠⚠ A LIRE AVANT DE PORTER ELEKTRA (ou toute carte « gain villainous » /
# « give [heros] a boost card ») : Doom s'en sort parce que SON texte dit
# explicitement « Ignore any boost effects on boost cards dealt to you » — il
# n'a donc jamais besoin que la carte de boost serve a quoi que ce soit. Le
# 04/11/2026, `ca009` Klyntar Bond (Carnage, « you may give him a boost card »
# SANS cette clause d'ignorer) a ete trouve CASSE en partie reelle pour cette
# raison exacte : `Faces.GiveFacedownBoostCards` pose la carte dans la pile
# `CanBoost`, mais RIEN ne la resout pour un pouvoir de base d'un HEROS en
# DEFENSE ou en RECUPERATION (seuls `can_attack.py` et `can_scheme.py`
# appellent `ResolveBoostCards` ; aucun fichier equivalent ne le fait pour
# CTR/DEF), et les effets [star] Boost d'une carte de rencontre ne se
# declenchent de toute facon QUE sur une activation d'ENNEMI, jamais sur
# celle d'un heros, attaque ou manigance comprise. SI Elektra (ou une future
# carte) veut un VRAI effet de la carte de boost donnee (pas juste
# l'ignorer), NE PAS reprendre `Faces.GiveFacedownBoostCards` : utiliser le
# modele `ca009` (corrige) / `bc002` / `14002` — `Worlds.
# DiscardEncounterTopCard` (ou `DiscardEncounterCards`) + `FacesCounter.
# CountTotalBoostIcons` + `message.GainValue(valeur, effect)` sur le message
# `WhenUnitUseBasicPower` — qui fonctionne pour les QUATRE pouvoirs de base
# (ATQ, CTR, DEF, RECUPERATION), sans dependre de la pile `CanBoost` cassee
# pour ce cas. Preuve par substitution de ca009 : `tools/cas/carnage.py`.
#
# ⚠ « to a MAXIMUM of 3 » : plafond passe a `PlaceCountersInternal`, pas verifie
# a la main — sinon deux Response simultanees pourraient depasser.
#
# ⚠ « using a [mental] resource », PAS « using ONLY [mental] resources » : le
# reste du pack emploie l'autre tournure (dd004, dd005, dd006). D'ou
# `HasColor("B")` ici, et `OnlyHasColor("B")` la-bas.
#
# ⚠ « Ignore any boost effects on boost cards dealt to you » : non code. Le
# moteur ne distribue de cartes de boost a un heros que par la voie ouverte
# ci-dessus, et les effets [star] Boost d'une carte de rencontre ne se
# declenchent que sur une activation d'ENNEMI. Ecart assume, documente au §4 du
# journal de portage.

def GetAbilities() -> Sequence['Ability']:

    def power_syphon(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Hero)

        if not message.paid_resources.HasColor("B"):
            return
        this.CastTo(CanPlaceCounter).PlaceCountersInternal(1, 'power', effect, maximum=3)

    def overwhelming_power(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Hero)
        Unused(message)

        this.GainUntilRoundEnd(effect, villainous=1)

    return [
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.Response,
            "You",
            CardFinder2("SPELL", Event),
            power_syphon,
        ).SetName("Power Syphon"),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            overwhelming_power,
        ).SetName("Overwhelming Power")
        .SetCostFunc(CostFunc.Counter("This", 3, 'power')),
    ]
