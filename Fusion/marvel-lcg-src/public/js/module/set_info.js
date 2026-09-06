export class SetInfo {
    constructor(obj = null) {
        this.name = '';
        this.scenarios = [];
        this.heroes = [];
        this.encounters = [];
        this.max_id = '';
        if (obj) {
            this.name = obj.name || '';
            this.scenarios = obj.scenarios || [];
            this.heroes = obj.heroes || [];
            this.encounters = obj.encounters || [];
            this.max_id = obj.max_id || '';
        }
    }
}
//# sourceMappingURL=set_info.js.map