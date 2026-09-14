from . import *
def GetAbilities() -> Sequence['Ability']:
    def big_mistake(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        alias = Worlds.FindCardOnField(effect, name='Alias Investigations')
        player = effect.GetInitiator()
        if alias and alias.GetCounters('evidence') >= 1:
            def boosted(_targets: Sequence['CardFace']):
                alias.RemoveCountersInternal(1, 'evidence', effect)
                # ⚠ AUCUN IMPORT ICI. Il y avait `from game.element.attack_property
                # import AttackProperty`, un module qui N'EXISTE PAS (la classe
                # vit dans `game/card/face/attribute/can_attack.py`) et que
                # `from . import *`, en tete de fichier, apporte deja.
                #
                # L'import etait DANS la fonction, donc dans la seule branche
                # « je paie une preuve » : la carte marchait parfaitement sans
                # preuve et ne faisait RIEN avec. Rapporte en jeu le 14/09/2026 :
                # « j'ai paye une preuve et il n'a meme pas fait de degats du
                # tout, la carte est partie dans le vide ; sans la preuve il
                # fait bien les 3 degats ». Le moteur avale l'exception et
                # defausse la carte.
                def with_overkill(_t: Sequence['CardFace']):
                    this.AttackDamage(effect.targets, 5, effect, property=AttackProperty(overkill=True))
                def with_piercing(_t: Sequence['CardFace']):
                    this.AttackDamage(effect.targets, 5, effect, property=AttackProperty(piercing=True))
                player.ChooseAbilities(
                    effect,
                    AbilityFactory.ForChoiceAbility('Overkill', with_overkill),
                    AbilityFactory.ForChoiceAbility('Piercing', with_piercing),
                )
            def unboosted(_targets: Sequence['CardFace']):
                this.AttackDamage(effect.targets, 3, effect)
            player.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility('Remove 1 evidence counter from Alias Investigations to deal 2 additional damage and gain overkill or piercing', boosted),
                AbilityFactory.ForChoiceAbility('Deal 3 damage', unboosted),
            )
        else:
            this.AttackDamage(effect.targets, 3, effect)
    return [AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, big_mistake).SetPlay().SetLabel('attack').SetTarget(Enemy)]
