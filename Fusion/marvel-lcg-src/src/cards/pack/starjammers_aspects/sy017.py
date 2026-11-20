from . import *
# * Korvus Rook'shir (Aggression, allie 3 [physical], 1*/1*, PV 3). PSIONIC. SHI'AR. STARJAMMER.
# Response: After Korvus Rook'shir enters play, find Blade of the Phoenix and attach it to him.
#
# Cartes de reference : tk101 / ul040 (carte `Linked` : `desc.Linked` sur sy018 la fait fabriquer MISE DE COTE des que Korvus est cree,
# fiche linked.md ; on la lit par `Worlds.GetSetAsideAreaCards`) ; nt016 (`this.AttachTo2(cible, effect)`) ; valk/valkyrie (« find X and
# attach » : recherche dans le set-aside, puis en jeu).
# « find » : la lame vit dans la zone mise de cote ; aucune lame disponible (deja attachee ou defaussee) : rien ne se passe.
def GetAbilities() -> Sequence['Ability']:
    def korvus(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        lames = [f for f in Worlds.GetSetAsideAreaCards(effect) if getattr(f.paper, "card_id", None) == "sy018"]
        if not lames:
            return
        lames[0].AttachTo2(this, effect)
    def une_lame_de_cote(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> bool:
        return any(getattr(f.paper, "card_id", None) == "sy018" for f in Worlds.GetSetAsideAreaCards(effect))
    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            korvus,
            conditions=[une_lame_de_cote],
        ),
    ]
