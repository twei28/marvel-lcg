from . import *

# Double Defense — amelioration d'aspect PROTECTION, x1. PREPARATION. TACTIC.
# Cout 1, ressource [physical]. Max 1 par joueur.
# Max 1 per player.
# Hero Response: When a character other than your identity would take any
#   amount of damage from an attack, discard Double Defense -> reduce that
#   amount by your hero's DEF.
#
# Cartes de reference :
#  - **`im007`** Energy Shield (pack iron_man_model_42) et `01098` Armored
#    Rhino Suit : `WhenUnitWouldTakeDamage(..., op, is_from_attack=True)` puis
#    `message.PreventDamage(n, effect)`.
#  - `08018` Spycraft / `im011` pour `CostFunc.Discard("This")`.
#  - `08007` Black Widow's Gauntlet pour une PREPARATION jouee en avance et
#    defaussee pour son effet.
#
# ⚠ TEXTE IMPRIME CONTRADICTOIRE, ARBITRE PAR L'UTILISATEUR (03/09/2026).
# La carte annonce « **Hero Response** » (apres coup) mais decrit
# « **When** a character ... **would take** » (avant coup). Les deux ne
# peuvent pas coexister : une fois les degats subis, il n'y a plus de
# « that amount » a reduire. Decision : on suit le DECLENCHEUR, la carte est
# une INTERRUPTION (`AbilityType.HeroInterrupt`). C'est aussi ce que font les
# trois cartes officielles au meme texte. Meme famille de piege que « The
# Made Men » (« Forced Interrupt : After Maniac schemes »).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « a character **other than your identity** » : un allie a vous ou a un
#    autre joueur, l'identite d'un autre joueur, et meme un sbire ou le
#    vilain — le texte ne restreint pas le camp. Ce qui est exclu, c'est
#    VOTRE identite, et elle seule : as001a Armor Protection est deja la
#    pour celle-la, les deux cartes se completent sans se recouvrir.
#  - « **any amount** of damage **from an attack** » : toute instance issue
#    d'une attaque. Une traitrise ou un degat indirect ne declenchent rien.
#    `is_from_attack=True`.
#  - « reduce that amount by **your hero's DEF** » : la DEF COURANTE du
#    heros au moment de la resolution, bonus compris (as002b la baisse de 1,
#    as012 ne touche que la CTR, as017 la monte de 3). Lire `heros.defense`,
#    jamais la valeur imprimee.
#  - « **your hero's** » : la carte ne marche donc qu'en forme heros, ce que
#    le prefixe `Hero` du type de capacite impose deja. Garde `IsHero()`
#    quand meme : `Player.GetHero()` leve un assert hors forme heros, et le
#    moteur AVALE l'exception (leçon ls014, 03/09/2026).
#  - « **Max 1 per player.** » : base automatique lue dans `desc.MaxPerUnit`,
#    AUCUN script (`HasMaxPer`). Ne rien recoder.
#  - « **discard** Double Defense -> » : la fleche en fait un COUT. La carte
#    part meme si la DEF vaut 0 — c'est le texte, et le joueur reste libre de
#    ne pas declencher.


def GetAbilities() -> Sequence['Ability']:

    def autre_que_mon_identite(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return False
        identite = joueur.GetIdentity()
        return identite is not None and message.trigger is not identite

    def double_defense(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None or not joueur.IsHero():
            return
        heros = joueur.GetIdentity()
        if heros is None:
            return

        reduction = heros.defense
        if reduction <= 0:
            return
        message.PreventDamage(reduction, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            None,
            double_defense,
            is_from_attack=True,
            conditions=[autre_que_mon_identite],
        ).SetCostFunc(CostFunc.Discard("This")),
    ]
