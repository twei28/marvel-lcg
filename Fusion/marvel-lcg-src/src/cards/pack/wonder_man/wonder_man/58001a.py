from . import *
def GetAbilities() -> Sequence['Ability']:
    def tucked_count(effect: 'Effect', ui: List['CardFace']) -> int:
        faces = GetTuckedCards(effect, effect.this.GetControlByPlayer())
        ui.extend(faces)
        return len(faces)
    def after_basic_attack(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Hero)
        faces = GetTuckedCards(effect, this.GetControlByPlayer())
        if faces:
            Faces.DiscardAll(faces, effect)
    # « Wonder Man gagne +1 ATK par carte glissee sous Ionic Physiology. »
    #
    # CORRECTIF (5/8/2026) : la construction d'origine etait
    # `GiveKeywordToAttached(..., get_new_value=tucked_count)`. Avec
    # `get_new_value`, l'assistant passe par `asset_helper.check_fn`, qui fait
    # `effect.this.CastTo(CanAttach)` : pose sur l'IDENTITE, qui ne s'attache a
    # rien, cela levait « AssertionError: face_type=CanAttach » et la creation
    # de partie de Wonder Man etait IMPOSSIBLE. Changer la cible n'y faisait
    # rien, c'est `get_new_value` qui impose le chemin attachement.
    #
    # `ThisGainKeyword` est la fabrique prevue pour un bonus dynamique porte
    # par la carte elle-meme (modele Madame Web 69001a et Negative Zone Prison
    # 56064b). `OnEvent.TuckUnder` la fait recalculer a chaque carte glissee ou
    # retiree ; « Identity » et non « Here » parce que les cartes sont glissees
    # sous Ionic Physiology, pas sous l'identite.
    return [AbilityFactory.ThisGainKeyword(
                tucked_count,
                attack=1,
                change_on_event=OnEvent.TuckUnder("Identity"),
            ).SetName("Power Recycling"),
            AbilityFactory.AfterUnitUseBasicPower(AbilityType.ForcedResponse, 'This', after_basic_attack, powers=['ATK'])]
