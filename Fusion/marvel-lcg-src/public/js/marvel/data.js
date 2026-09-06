import { Lib } from "./lib.js";
export class EffectDescriptor {
    constructor(obj) {
        this.id = obj?.['id'] ?? -1;
        this.name = obj?.['name'] ?? "";
        if (this.name.startsWith("p_")) {
            let src = this.name.replace(/^p_/, '');
            this.name_with_space = `<img class=${this.name} src=${src}></img>`;
        }
        else {
            this.name_with_space = this.name.replaceAll("_", " ");
        }
        this.bind_id = obj?.['bind_id'] ?? "";
        this.bind_player_id = obj?.['bind_player_id'] ?? 0;
        this.all_legal_targets = structuredClone(obj?.['all_legal_targets']);
        this.target_num_range = structuredClone(obj?.['target_num_range']);
        if (this.target_num_range && this.target_num_range[1] == 0) {
            this.all_legal_targets = [];
        }
        this.target_payment = Object.entries(obj?.['target_payment'] ?? {}).reduce((acc, [key, value]) => {
            acc[Number(key)] = new EffectDescriptor.Payment(value);
            return acc;
        }, {});
        this.select_rule = obj?.['select_rule'];
        this.select_rule_param = structuredClone(obj['select_rule_param']);
        this.target_must_include_traits = structuredClone(obj['target_must_include_traits']);
        this.failure_reason = obj?.['failure_reason'];
        this.resources = [];
        this.selected_targets = [];
        this.is_search = obj?.['is_search'];
        let start_x = false;
        if (this.all_legal_targets) {
            for (const target of this.all_legal_targets) {
                if (Lib.array.occurrence(this.all_legal_targets, target) > 1) {
                    start_x = true;
                    break;
                }
            }
        }
        this.start_x = start_x;
    }
    clear() {
        this.id = -1;
        this.name = '';
        this.name_with_space = '';
        this.bind_id = -1;
        this.bind_player_id = undefined;
        this.all_legal_targets = [];
        this.target_num_range = [0, 0];
        this.target_payment = {};
        this.select_rule = '';
        this.target_must_include_traits = [];
        this.failure_reason = '';
        this.resources = [];
        this.selected_targets = [];
        this.is_search = false;
        this.start_x = false;
    }
    getN() {
        let n = 0;
        if (this.selected_targets.length > 0) {
            n = this.selected_targets[0];
        }
        else if (this.all_legal_targets.length > 0) {
            n = this.all_legal_targets[0];
        }
        if (!(n in this.target_payment)) {
            n = 0;
        }
        return n;
    }
    getCost() {
        if (this.selected_targets.length > 0 || this.all_legal_targets.length === 0) {
            let n = this.getN();
            return this.target_payment[n]?.cost || "";
        }
        else {
            let last_cost = "";
            const keys = Object.keys(this.target_payment);
            if (keys.length === 1) {
                return this.target_payment[Number(keys[0])].cost || "";
            }
            for (let n of this.all_legal_targets) {
                if (n in this.target_payment) {
                    const cost = this.target_payment[n].cost;
                    if (last_cost && cost !== last_cost) {
                        return "?";
                    }
                    last_cost = cost;
                }
            }
            return last_cost;
        }
    }
    getRule(rule) {
        if (this.selected_targets.length > 0 || this.all_legal_targets.length === 0) {
            let n = this.getN();
            return this.target_payment[n]?.rule?.includes(rule) || false;
        }
        return false;
    }
    isCostRuleUpTo() {
        return this.getRule("UpTo");
    }
    isCostRuleSameType() {
        return this.getRule("SameType");
    }
    isCostRuleDifferentType() {
        return this.getRule("DifferentType");
    }
    getResources() {
        let n = this.getN();
        return this.target_payment[n]?.payment.map(y => y.effect_id) || [];
    }
    getResText() {
        let n = this.getN();
        return this.target_payment[n]?.payment.map(y => y.res_text) || [];
    }
}
(function (EffectDescriptor) {
    class Payment {
        constructor(obj) {
            this.payment = (obj['payment'] || []).map((y) => new EffectPay(y));
            this.cost = obj['cost'];
            this.rule = obj['rule'];
        }
    }
    EffectDescriptor.Payment = Payment;
    class EffectPay {
        constructor(obj = null) {
            if (obj && 'effect_id' in obj) {
                this.effect_id = obj.effect_id;
                this.res_text = obj.res_text;
                if (isNaN(this.effect_id)) {
                    console.error('Invalid effect_id:', this.effect_id);
                }
            }
            else if (obj) {
                const key = Object.keys(obj)[0];
                this.effect_id = Number(key);
                this.res_text = obj[key];
                if (isNaN(this.effect_id)) {
                    console.error('Invalid effect_id:', this.effect_id);
                }
            }
            else {
                this.effect_id = 0;
                this.res_text = '';
            }
        }
    }
    EffectDescriptor.EffectPay = EffectPay;
})(EffectDescriptor || (EffectDescriptor = {}));
export class AskOptionPayload {
    constructor(obj) {
        this.options = [];
        for (let x of JSON.parse(obj.options_json)) {
            this.options.push(new EffectDescriptor(x));
        }
        this.event_name = obj.event_name;
        this.prompt_text = obj.prompt_text;
        this.show_cancel = obj.show_cancel;
        this.replay_input = obj.replay_input;
        this.ability_type = obj.ability_type;
        this.is_ex_effect = ["WhenPlayerChooseAbility", "WhenResolveSpecialAbility", "End Turn"].includes(this.event_name);
    }
}
//# sourceMappingURL=data.js.map