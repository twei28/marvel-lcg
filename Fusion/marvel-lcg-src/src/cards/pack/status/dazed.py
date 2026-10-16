from . import *

# Dazed (carte d'etat maison, pack TMNT, Baxter Stockman v3, scan Inkwire)
#
# Texte imprime : « The next time this character uses a basic power or
# activates, decrease that value by 2, then discard this status card. The next
# time this character would take any amount of damage, increase that value by
# 2, then discard this status card. »
#
# Insert « Dazed Rules » (meme zip) : « Daze X » = poser une carte d'etat Dazed
# sur X ; UNE seule Dazed par personnage sauf mention contraire (Steady et
# Stalwart n'y changent rien) ; les deux declencheurs sont EXCLUSIFS (« Can I
# defend with a Dazed card, -2 DEF and also +2 damage ? No ») : le premier qui
# arrive defausse la carte. Meme lecture que Cloaked (decision de l'utilisateur
# du 16/10/2026), a l'envers. Fiche : docs/reference/mots-cles/dazed.md.
#
# « Tough resolves before Cloaked, and Cloaked and Dazed resolve
# simultaneously » (insert) :
#  - Tough d'abord : un personnage Tough qui va subir des degats les voit
#    PREVENUS par Tough ; Dazed ne se declenche pas (la carte reste). Garde
#    `IsTough()` + `is_be_instead`, qui ne dependent pas de l'ordre des cartes.
#  - Cloaked et Dazed « en meme temps » : sur des degats, Dazed prend la
#    main : +2 puis -2 (Cloaked) d'un seul bloc, les DEUX cartes partent
#    (`cloaked.py` lui cede la place quand le personnage est Dazed). Sur un
#    pouvoir de base (+2 / -2) les deux modifications s'additionnent d'elles
#    memes.
#
# Modele : `cloaked.py` (meme dossier), forme identique.

def GetAbilities() -> Sequence['Ability']:

    def consommer(effect: 'Effect') -> None:
        from game.operate.faces import Faces
        this = effect.this.CastTo(StatusCard)
        Faces.DiscardAll([this], effect)

    def pas_ennemi(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> bool:
        return not Enemy.IsType(message.trigger)

    def pouvoir_de_base(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        message.GainValue(-2, effect)
        consommer(effect)

    def activation(effect: 'Effect', message: 'Message.WhenEnemyActivateAgainstYou') -> None:
        would = message.would_message
        if isinstance(would, Message.WhenUnitWouldAttack):
            would.GainATKForThisAttack(-2, effect)
        else:
            would.GainSCHForThisScheme(-2, effect)
        consommer(effect)

    def vraie_activation_de_base(effect: 'Effect', message: 'Message.WhenEnemyActivateAgainstYou') -> bool:
        if message.would_act_message is None:
            return False
        would = message.would_message
        if isinstance(would, Message.WhenUnitWouldAttack):
            return would.IsBasicAttack()
        return would.IsBasicScheme()

    def peut_se_declencher_sur_degats(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        unit = effect.this.CastTo(StatusCard).GetBindFace()
        if message.is_be_instead or message.IsBePrevent():
            return False
        # Tough d'abord : il va tout prevenir, Dazed attend le prochain coup.
        if not message.property.ignore_tough and unit.IsTough():
            return False
        return message.will_take_damage > 0

    def degats(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(StatusCard)
        unit = this.GetBindFace()
        # `inclure_overkill` : le personnage subit REELLEMENT ces degats.
        message.IncreaseDamage(2, effect, inclure_overkill=True)
        # Cloaked « en meme temps » : -2 dans le meme bloc, et la carte part.
        if unit.IsCloaked():
            message.ReduceDamage(min(2, message.will_take_damage), effect)
            unit.DiscardCloaked(effect, rule=1)
        consommer(effect)

    return [
        AbilityFactory.WhenUnitUseBasicPower(
            AbilityType.Status,
            "AttachedCharacter",
            pouvoir_de_base,
            conditions=[pas_ennemi],
        ),
        AbilityFactory.WhenEnemyActivateAgainstYou(
            AbilityType.Status,
            "AttachedEnemy",
            activation,
            conditions=[vraie_activation_de_base],
        ),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.Status,
            "AttachedCharacter",
            degats,
            conditions=[peut_se_declencher_sur_degats],
        ),
    ]
