from . import *

# Whirling Debris — AMELIORATION, cout 2, [physical]. SUPERPOWER.
# Texas Twister gains retaliate 1.
# Hero Interrupt: When you make a basic attack, exhaust Whirling Debris ->
#   damage from this attack may be divided among enemies as you choose.
#
# CARTES DE REFERENCE
#  - `06009` Mjolnir : `GiveKeywordToAttached`, ici avec `retaliate=1`.
#  - `13006` Wasp Sting et `cd005` Lightforce Daggers : l'idiome du depot pour
#    des degats REPARTIS — `SetTarget(Enemy, range=(1, N),
#    repeat_rules="Health")` puis UN degat par attribution.
#
# MOT-CLE : RETALIATE — fiche `docs/reference/mots-cles/retaliate.md`, lue
# avant d'ecrire. Trois cas ou il ne part PAS, tous dans `ResolveRetaliate` :
# attaque a DISTANCE, attaquant ou defenseur deja vaincu, et attaque qui
# ignore le mot-cle. Aucun script n'est requis pour le mot-cle lui-meme : ici
# il est ACCORDE, donc `GiveKeywordToAttached(retaliate=1)`, exactement comme
# `03009` Captain America's Shield, que la fiche cite pour ce piege precis.
#
# ⚠ ECART ASSUME, ET SA RAISON — LA MOITIE « REPARTITION » N'EST PAS UNE
# INTERRUPTION.
# Le texte imprime interrompt une attaque de base DEJA CIBLEE : quand
# `WhenUnitUseBasicPower` part, la cible unique de l'attaque est choisie
# depuis longtemps (elle l'est a la selection de la capacite, avant meme le
# paiement du cout). Le moteur ne sait REPARTIR des degats que si les cibles
# multiples sont choisies AU MOMENT DE LA SELECTION : c'est ce que fait
# `ThisCanAttack(canbe_divided=True)` (`cd002a` Dagger, `13001c` Wasp), qui
# REMPLACE la definition meme du pouvoir ATQ et ne peut donc pas etre allumee
# en cours de route.
# La carte est donc rendue en HERO ACTION dediee, qui coute l'inclinaison de
# Whirling Debris ET celle de l'identite — c'est-a-dire exactement ce que
# coute une attaque de base plus la carte. Valeur de jeu identique, forme
# differente. La question est posee a l'auteur plutot que masquee.


def GetAbilities() -> Sequence['Ability']:

    def atq_du_heros(effect: 'Effect') -> int:
        """Le nombre de degats a repartir : l'ATQ COURANTE du heros.

        ⚠ COURANTE ET NON IMPRIMEE : tout le pack empile des +1 ATQ (tt001a,
        tt003, tt009). Lire l'imprime ferait de cette carte la seule du set a
        ignorer le moteur du heros.
        """
        heros = HerosDuJoueur(effect)
        return max(1, int(getattr(heros, "attack", 1) or 1)) if heros is not None else 1

    def debris_tourbillonnants(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        # UN degat par attribution : le joueur a choisi N fois une cible, en
        # repetant la meme pour concentrer. Montage `13006` / `cd005`.
        this.DealDamage(effect.targets, 1, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(name=NOM_HEROS),
            retaliate=1,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            debris_tourbillonnants,
        ).SetLabel('attack')
        .SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Exhaust("YourIdentity"))
        .SetTarget(Enemy, range=(1, atq_du_heros), repeat_rules="Health"),
    ]
