from core import *
from game.card.face import *
from game.effect import *
from game.card.face.model.base import ModelBase

class ModelTrait(ModelBase):
    def GetInfoTraits(self) -> Dict[str, int]:
        info: Dict[str, int] = {}
        # for trait in ['AERIAL', 'GIANT', 'GUARDIAN', 'WEB-WARRIOR', 'ICE', 'METAL', 'WOOD', 'STONE']:
        for trait in self.traits_internal:
            if self.HasTrait(trait):
                text = trait.replace(' ', '_').replace('!', '')
                info |= {f't_{text}': len(self.traits_internal[trait])}
        return info

    def OnInitModel(self):
        self.ResetTrait()
        return super().OnInitModel()

    def OnResetModel(self):
        self.ResetTrait()
        return super().OnResetModel()

    ################################################################################
    # Trait
    @final
    def ResetTrait(self):
        this = self.GetThis()
        self.traits_internal: Dict["CardFace.TRAITS", List['CardFace']] = {}
        self.traits_lost: Dict["CardFace.TRAITS", int] = {}
        for trait in this.paper.traits:
            self.traits_internal[trait] = [this]
    @property
    def traits(self) -> List["CardFace.TRAITS"]:
        return [x for x in self.traits_internal
                if len(self.traits_internal[x]) > 0 and self.traits_lost.get(x, 0) <= 0]
    @property
    def traits_str(self) -> str:
        name = ""
        for trait in self.traits_internal:
            name += trait + " "
        return name

    @final
    def FindHasTrait(self, *traits: "CardFace.TRAITS") -> List["CardFace.TRAITS"]:
        has_traits: List["CardFace.TRAITS"] = []
        for trait in traits:
            if self.HasTrait(trait):
                has_traits.append(trait)
        return has_traits
    @final
    # or
    def HasTrait(self, *traits: "CardFace.TRAITS") -> bool:
        this = self.GetThis()
        for trait in traits:
            if self.traits_lost.get(trait, 0) > 0:
                continue
            if trait in self.traits_internal and self.traits_internal[trait] != [] or \
                this.IsConsiderAs(trait=trait):
                return True
        return False
    @final
    def SuppressTrait(self, diff: int, trait: "CardFace.TRAITS"):
        """AJOUT (09/10/2026, pack hunting_season) : « loses the X trait » TEMPORAIRE.
        Compteur par trait : tant qu'il est > 0, `HasTrait` repond non, quelle que soit la
        source du trait. Remis a zero avec la face (`ResetTrait`)."""
        self.traits_lost[trait] = max(0, self.traits_lost.get(trait, 0) + diff)
    @final
    def ShareTrait(self, face: 'CardFace') -> bool:
        return self.HasTrait(*list(face.traits_internal.keys()))
    @final
    def GetShareTraitNum(self, face: 'CardFace') -> int:
        return len(self.GetShareTrait(face))
    @final
    def GetShareTrait(self, face: 'CardFace') -> List['CardFace.TRAITS']:
        traits: List['CardFace.TRAITS'] = []
        for trait in face.traits_internal:
            if self.HasTrait(trait):
                traits.append(trait)
        return traits
    @final
    def GainTraitInternal(self, diff: int, trait: "CardFace.TRAITS", by_effect: 'Effect'):
        face = by_effect.this
        if diff == 1:
            if trait in self.traits_internal:
                # assert face not in self.traits_internal[trait]
                self.traits_internal[trait].append(face)
            else:
                self.traits_internal[trait] = [face]
        elif diff == -1:
            self.traits_internal[trait].remove(face)
            if self.traits_internal[trait] == []:
                del self.traits_internal[trait]
        else:
            assert False
    @final
    def GainTraits(self, diff: int, traits: "CardFace.TRAITS"|List["CardFace.TRAITS"], by_effect: 'Effect'):
        from game.message import Message
        this = self.GetThis()
        the_traits: List["CardFace.TRAITS"] = []

        if isinstance(traits, list):
            the_traits = traits
        else:
            the_traits = [traits]

        for trait in the_traits:
            this.GainTraitInternal(diff, trait, by_effect)

        Message.WhenCardUpdateTrait_Text(this, diff, the_traits, by_effect)

    @final
    def CopyTrait(self, face: 'CardFace', by_effect: 'Effect'):
        self.GainTraits(+1, face.traits, by_effect)

    def GetTraitsTotalCount(self) -> int:
        value = 0
        for trait in self.traits:
            value += len(self.traits_internal[trait])
        return value

    def GetTraitsTotalCount2(self) -> int:
        return len(self.traits)

