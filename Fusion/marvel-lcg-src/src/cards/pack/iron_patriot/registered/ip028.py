from . import *

# * Taskmaster — SBIRE du deck REGISTERED (15/20). 4 PV, ATQ 0, MNG 0,
# boost 3. AVENGER. ELITE. MERCENARY.
# Guard.
# [star] Taskmaster gets +1 SCH and +1 ATK for each REGISTERED character you
#   control (to a maximum of 3).
# Initiative Trainer — Special: Resolve the "Special" ability on 1 minion in
#   the REGISTERED deck discard pile.
#
# ⚠⚠ ATQ 0 ET MNG 0 IMPRIMES : Taskmaster ne vaut QUE par l'armee autour de
# lui. Sbire isole, il ne fait rien ; allie au milieu de quatre autres, il
# frappe a 3. C'est la carte qui recompense la strategie du pack.
#
# ⚠⚠ ET C'EST LA SEULE CARTE QUI ATTEINT LA DEFAUSSE DU DECK REGISTERED. Un
# allie vaincu y retourne (regle de l'insert, cf. `ip001b`) : Taskmaster
# rejoue donc son « Special » une derniere fois, depuis la tombe.
#
# CARTES DE REFERENCE
#  - `ip003` / `ip004` : `GiveKeywordToInPlayWhenApplyThis` avec
#    `get_new_value` pour un bonus qui se recalcule.
#  - `ip001b` Norman Osborn : `face.ResolveSpecialAbility(joueur, effect)`.
#
# TEXTE CONTRE CODE
#  ⚠ « for each REGISTERED CHARACTER you control » : Iron Patriot lui-meme
#    porte le trait et compte. Taskmaster aussi, une fois allie.
#  ⚠ « (to a MAXIMUM of 3) » : plafond sur le BONUS, pas sur le compte.
#  ⚠⚠ DEUX CAPACITES, PAS UNE. ATQ et MNG ne peuvent pas voyager ensemble :
#    une seule des deux existe sur la face du moment (le gabarit d'allie n'a
#    pas de MNG), et `unit.Gain` sort alors sans RIEN appliquer, +1 ATQ
#    compris. Meme piege que `ip029` Venom, mesure du 09/09/2026.
#  ⚠⚠ ET IL FAUT UN `change_on_event`. Sans lui, le bonus est fige a
#    l'inscription : Taskmaster recrute reste a ATQ 0 alors qu'il vient lui-
#    meme de rejoindre l'armee. On recalcule des qu'un personnage REGISTERED
#    entre ou sort du terrain.
#  ⚠ « on 1 MINION in the REGISTERED deck DISCARD PILE » : un sbire, dans la
#    defausse du deck additionnel — pas dans le deck, pas en defausse de
#    rencontre. `DefausseRegistered`.
#  ⚠ La carte visee resout son « Special » SANS revenir en jeu. Elle reste en
#    defausse.


def GetAbilities() -> Sequence['Ability']:

    def bonus(effect: 'Effect', ui: List['CardFace']) -> int:
        joueur = JoueurQuiControle(effect.this)
        if joueur is None:
            return 0
        personnages = [f for f in joueur.GetControlCharacters()
                       if f is not None and f.HasTrait(TRAIT_REGISTERED)]
        ui.extend(personnages)
        return min(3, len(personnages))

    def formateur(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        Unused(message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        sbires = [f for f in DefausseRegistered(joueur).Get()
                  if f is not None and Minion.IsType(f)]
        if not sbires:
            return
        choisi = joueur.AskChooseFaces(
            sbires, (1, 1), effect,
            prompt="Resolve the \"Special\" ability on 1 minion in the REGISTERED deck discard pile")
        for face in choisi:
            face.ResolveSpecialAbility(joueur, effect)

    def bonus_en_sbire(effect: 'Effect', ui: List['CardFace']) -> int:
        return bonus(effect, ui) if Minion.IsType(effect.this) else 0

    RECALCUL = OnEvent.CardInPlay(
        CardFinder(card_type=Unit2, trait=TRAIT_REGISTERED))

    return [
        AbilityFactory.ThisGainKeyword(
            bonus,
            attack=1,
            change_on_event=RECALCUL,
        ),
        AbilityFactory.ThisGainKeyword(
            bonus_en_sbire,
            scheme=1,
            change_on_event=RECALCUL,
        ),
        SpecialRegistered("Initiative Trainer", formateur),
    ]
