from . import *

# Burning Hands — EVENEMENT, cout 2, [energy]. FIRE. SUPERPOWER. THWART. x3.
# Requirement ([energy]).
# Hero Action (thwart): Remove 3 threat from a scheme. Choose an attachment
#   with the text "Hero Action" or "Hero Response" and discard it. Otherwise,
#   attach a set-aside copy of Burning to an enemy.
#
# MOT-CLE : REQUIREMENT — fiche `docs/reference/mots-cles/requirement.md`.
# BASE AUTOMATIQUE : `desc.Requirement = "Y"`, le moteur exige l'energie au
# paiement. AUCUN SCRIPT. Modeles `27006` Web Binding (`Requirement: "B"`) et
# `28013` No Quarter (`"R"`).
#
# CARTES DE REFERENCE
#  - `42006` Natural Flight : « Hero Action (thwart): Remove N threat from a
#    scheme » -> `SetPlay().SetLabel('thwart').SetTarget(Scheme2)`.
#  - `bc004` / `bc010` (pack black_cat, la veille) : la selection d'un
#    attachement PAR SON TEXTE, brique 3 du plan de portage.
#
# TEXTE CONTRE CODE
#  ⚠ « Choose an attachment ... » SANS « attached to that enemy » : c'est LA
#    difference imprimee avec `sf005` Solar Blast. Ici on regarde TOUT le
#    terrain, la-bas seulement l'ennemi vise. Ne pas harmoniser.
#  ⚠ « OTHERWISE » n'est PAS un choix : le repli tombe quand il n'y a AUCUN
#    attachement eligible. Mot-piege releve a l'etape 5 (deja paye sur
#    `sn013`). La joueuse ne peut pas preferer la brulure.
#  ⚠ La brulure du repli va sur « AN enemy », au choix : la carte ne dit pas
#    lequel, et il n'y a pas de cible imprimee pour elle.
#  « Remove 3 threat » -> inconditionnel, avant tout le reste.


def GetAbilities() -> Sequence['Ability']:

    def mains_brulantes(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        this.RemoveThreatFromSchemes(effect.targets, 3, effect)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return

        # ⚠ TOUT le terrain, pas seulement un ennemi : voir l'encadre.
        candidats = [f for f in Worlds.GetOnFieldCards(effect)
                     if AttachementAvecActionDeHeros(f)]
        if candidats:
            choisi = joueur.AskChooseFace(candidats, effect)
            if choisi is not None:
                Faces.DiscardAll([choisi], effect)
                return

        # « OTHERWISE, attach a set-aside copy of Burning to an enemy. »
        ennemis = list(Worlds.GetOnFieldEnemies(effect))
        if not ennemis:
            return
        cible = joueur.AskChooseFace(ennemis, effect)
        AttacherUneBrulure(effect, cible, joueur)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            mains_brulantes,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
