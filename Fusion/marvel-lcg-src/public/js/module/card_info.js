export class Card {
    constructor(card_id, type, name, subtitle, desc, setName, traits, package_name, full_link_id, text) {
        this.card_id = card_id;
        this.type = type;
        this.name = name;
        this.subtitle = subtitle;
        this.cost = undefined;
        this.hp = undefined;
        this.boost = undefined;
        this.atk = undefined;
        this.thw = undefined;
        this.uses = undefined;
        this.incite = undefined;
        this.class = '';
        this.toughness = undefined;
        this.retaliate = undefined;
        this.restricted = undefined;
        this.nemesis = undefined;
        this.guard = undefined;
        this.patrol = undefined;
        this.villainous = undefined;
        this.victory = undefined;
        this.alliance = undefined;
        this.quickstrike = undefined;
        this.sch = undefined;
        this.surge = undefined;
        this.peril = undefined;
        this.desc = desc;
        this.package_name = package_name;
        this.full_link_id = full_link_id;
        this.text = text;
        // CORRECTIF : nom de l'auteur pour une carte fan-made, "" sinon.
        // Renseigne par CardStatistics.createCardObjects depuis cards.json.
        this.custom = "";
        if (desc) {
            if ("Cost" in desc) {
                this.cost = desc.Cost;
            }
            if ("Class" in desc) {
                this.class = desc.Class.split(";")[0];
            }
            if ("ATK" in desc) {
                this.atk = desc.ATK;
            }
            if ("THW" in desc) {
                this.thw = desc.THW;
            }
            if ("HP" in desc) {
                this.hp = desc.HP;
            }
            if ("Boost" in desc) {
                this.boost = desc.Boost;
            }
            if ("Uses" in desc) {
                this.uses = desc.Uses;
            }
            if ("Incite" in desc) {
                this.incite = desc.Incite;
            }
            if ("Toughness" in desc) {
                this.toughness = desc.Toughness;
            }
            if ("Retaliate" in desc) {
                this.retaliate = desc.Retaliate;
            }
            if ("Restricted" in desc) {
                this.restricted = desc.Restricted;
            }
            if ("Nemesis" in desc) {
                this.nemesis = desc.Nemesis;
            }
            if ("Guard" in desc) {
                this.guard = desc.Guard;
            }
            if ("Surge" in desc) {
                this.surge = desc.Surge;
            }
            if ("Peril" in desc) {
                this.peril = desc.Peril;
            }
            if ("Patrol" in desc) {
                this.patrol = desc.Patrol;
            }
            if ("Villainous" in desc) {
                this.villainous = desc.Villainous;
            }
            if ("Permanent" in desc) {
                this.permanent = desc.Permanent;
            }
            if ("Victory" in desc) {
                this.victory = desc.Victory;
            }
            if ("Alliance" in desc) {
                this.alliance = desc.Alliance;
            }
            if ("Quickstrike" in desc) {
                this.quickstrike = desc.Quickstrike;
            }
            if ("SCH" in desc) {
                this.sch = desc.SCH;
            }
        }
        this.rotate = ["PlayerSideScheme", "EncounterSideScheme", "MainScheme", "Status", "Insert"].includes(type);
        this.set_name = setName;
        this.traits = traits;
    }
}
//# sourceMappingURL=card_info.js.map