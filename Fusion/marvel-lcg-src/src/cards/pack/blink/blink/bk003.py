from . import *

# Assault Redirection (x2) — EVENEMENT, cout 1, [energy]. DEFENSE. SUPERPOWER.
# Hero Interrupt (defense): When a character would take any amount of damage
#   from an attack, prevent all of that damage. You may discard a [[PORTAL]]
#   upgrade attached to an enemy to deal damage to that enemy equal to the
#   amount prevented this way.
#
# CARTE DE REFERENCE
#  - `damage.py` `PreventAllDamageTo` / `message.PreventDamage("All", effect)`.
#
# TEXTE CONTRE CODE
#  « a CHARACTER » -> pas seulement l'identite : un allie protege aussi.
#  « ANY amount » + « prevent ALL » -> `PreventDamage("All")`, pas un montant.
#  « YOU MAY discard » -> la seconde moitie est FACULTATIVE.
#  « equal to the amount PREVENTED THIS WAY » -> on relit ce qui a reellement
#    ete prevenu, pas les degats annonces.


def GetAbilities() -> Sequence['Ability']:

    def redirection(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Event)
        prevenus = int(getattr(message, "will_take_damage", 0) or 0)
        message.PreventDamage("All", effect)
        if prevenus <= 0:
            return

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        candidats = [p for p in PortailsEnJeu(effect)
                     if Hote(p) is not None and Enemy.IsType(Hote(p))]
        if not candidats:
            return

        def renvoyer(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            portail = candidats[0]
            ennemi = Hote(portail)
            Faces.DiscardAll([portail], effect)
            if ennemi is not None:
                this.DealDamage([ennemi], prevenus, effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Discard a Portal to redirect the damage",
                renvoyer,
            ),
            AbilityFactory.ForChoiceAbility("Prevent the damage only"),
        )

    return [
        # ⚠ `who_deal_damage=Enemy` EST OBLIGATOIRE, ET C'EST UN CORRECTIF.
        #
        # Le texte dit « when A CHARACTER would take any amount of damage from
        # an attack » — plus large que le « you » des evenements de defense
        # officiels (`ma011`, `01003` Backflip). Pris a la lettre SANS borner
        # l'attaquant, « a character » inclut le VILAIN : le pilote a donc joue
        # Assault Redirection pour prevenir les degats que Blink infligeait
        # elle-meme a Klaw avec Hit and Run. Le journal disait « Blink defend
        # contre Blink », puis le moteur tombait sur
        # `assert being_atk_message.defense_messages == []`
        # (can_attack.py:427) : une defense restait ouverte au milieu d'une
        # attaque. 1 partie sur 16 en autoplay, le 04/09/2026.
        #
        # Le libelle `(defense)` dit la lecture juste : on defend contre une
        # attaque ENNEMIE. `Unit2` reste, lui, volontairement large — allies et
        # personnages des autres joueurs sont bien couverts, ce que « a
        # character » demande et ce que « you » exclurait.
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            Unit2,
            redirection,
            is_from_attack=True,
            who_deal_damage=Enemy,
        ).SetPlay().SetLabel('defense'),
    ]
