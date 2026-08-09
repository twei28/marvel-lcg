import { ButtonSetting, Setting } from './settings.js';
import { Game } from './game.js';
import { Cards } from './cards.js';
import { Lib } from './lib.js';
import { Effect } from './effect.js';
import { HoverCard } from './hover.js';
import { copyToClipboard } from '../lib/clipboard.js';
import { ClassName } from './class_name.js';
import { AutoActivate } from './auto_activate.js';
import { Notify } from './notify.js';
function toPlayerCardDescriptorList(control_player, obj, parent_div_id, options = {}) {
    options.control_player = control_player;
    return toCardCardDescriptorList(obj, parent_div_id, options);
}
function toCardCardDescriptorList(obj, parent_div_id, options = {}) {
    return obj.map(x => {
        const card = Cards.getCard(x['id']);
        if (card) {
            card.update(x, parent_div_id, options);
            return card;
        }
        else {
            return new CardDescriptor(x, parent_div_id, options);
        }
    });
}
class CardDescriptorUI {
    constructor(effect_by_cards, effect_to_cards, crc, is_obligation) {
        this.effect_by_cards = effect_by_cards;
        this.effect_to_cards = effect_to_cards;
        this.crc = crc;
        this.is_obligation = is_obligation;
    }
    equals(other) {
        return Lib.array.equals(this.effect_by_cards, other.effect_by_cards) &&
            Lib.array.equals(this.effect_to_cards, other.effect_to_cards) &&
            this.crc === other.crc;
    }
}
export class CardDescriptor {
    get need_render() { return !this.lastRenderState || this.currentState != this.lastRenderState; }
    constructor(obj, parent_div_id, options, new_element = true) {
        this.updateInternal(obj, parent_div_id, options);
        let rate_super = 664;
        let rate_sparkles = 789;
        if (Setting.ssr_bonus) {
            rate_super = 64;
            rate_sparkles = 89;
        }
        if ((Number(this.card_id) + this.object_id) % rate_super == rate_super - 1) {
            console.log('ssr: super', this.object_id);
            this.is_ssr = 'super';
        }
        else if ((Number(this.card_id) + this.object_id) % rate_sparkles == rate_sparkles - 1) {
            console.log('ssr: ultra', this.object_id);
            this.is_ssr = 'ultra';
        }
        else {
            this.is_ssr = '';
        }
        if (new_element) {
            this.card_div = this.createDiv();
        }
        this.lastRenderState = "";
    }
    update(obj, parent_div_id, options) {
        this.updateInternal(obj, parent_div_id, options);
    }
    doRender() {
        this.lastRenderState = this.currentState;
    }
    updateInternal(obj, parent_div_id, options) {
        const { is_in_play = false, is_in_hand = false, is_dealt_card = false, is_obligation = false, control_player = -1 } = options;
        this.object_id = obj['id'];
        this.is_ready = obj['is_ready'];
        this.is_face_up = obj['is_face_up'];
        this.visible_for_players = obj['visible_for_players'];
        this.bind_object_id = obj['bind_object_id'];
        this.ui = new CardDescriptorUI(obj['effect_by_cards'], obj['effect_to_cards'], obj['crc'], is_obligation);
        this.game_area = obj['game_area'];
        this.name = obj['name'];
        this.card_type = obj['card_type'];
        this.info = obj['info'];
        this.traits = obj['traits'];
        this.buffs = obj['buffs'];
        this.card_id = obj['card_id'];
        this.pic_id = obj['pic_id'];
        this.down_card_id = obj['down_card_ids'][0];
        this.down_card_ids = obj['down_card_ids'];
        this.effects = obj['effects'];
        this.resources = obj['resources'];
        this.cost = obj['cost'];
        this.is_new = obj['is_new'];
        this.is_action = obj['is_action'];
        this.control_player = control_player;
        this.is_in_play = is_in_play;
        this.is_in_hand = is_in_hand;
        this.is_dealt_card = is_dealt_card;
        this.card_type_base = '';
        if (["Ally", "Minion", "EncounterVillain", "Hero", "AlterEgo"].includes(this.card_type)) {
            this.card_type_base = "Unit";
        }
        if (["MainScheme", "EncounterSideScheme", "PlayerSideScheme"].includes(this.card_type)) {
            this.card_type_base = "Scheme";
        }
        this.parent_div_id = parent_div_id ?? '';
        this.currentState = Lib.object.hashObjectFast(obj) + Lib.object.hashObjectFast(options);
    }
    isInPlay() {
        const num = this.object_id;
        const card_div = Cards.getDiv(num);
        return !card_div?.parentElement?.classList.contains('deck') && card_div?.parentElement?.id != "player-all-hand-cards";
    }
    isVisible() {
        if (ButtonSetting.show_all_hand_cards && this.is_in_hand) {
            return true;
        }
        if (Setting.is_hot_seat || Setting.is_watch || Game.world_descriptor.players[Setting.player_id]?.is_eliminated) {
            return [0, 1, 2, 3].some(player => this.visible_for_players.includes(player));
        }
        else {
            return this.visible_for_players.includes(Setting.player_id);
        }
    }
    createDiv() {
        const object_id = this.object_id;
        const card_div = document.createElement('div');
        card_div.classList.add('card');
        card_div.dataset.id = object_id.toString();
        Cards.cards[object_id] = this;
        card_div.onclick = (e) => {
            if (e.ctrlKey) {
                card_div.classList.toggle('clicked-top');
            }
            else {
                Effect.onCardClick(card_div, false, false, true);
            }
            e.stopPropagation();
            e.preventDefault();
        };
        card_div.oncontextmenu = (e) => {
            const currentTime = new Date().getTime();
            const lastTime = Cards.render.lastRightClickTimes.get(card_div.dataset.id) || 0;
            const DBL_RIGHT_CLICK_THRESHOLD = 300;
            if (currentTime - lastTime < DBL_RIGHT_CLICK_THRESHOLD) {
                if (card_div.parentElement?.classList.contains('area') &&
                    card_div.parentElement?.id != "player-all-hand-cards") {
                    toggleAutoActivateHelper(e);
                }
            }
            else if (e.shiftKey && e.ctrlKey) {
                const object_id = Number(card_div.dataset.id);
                const card_id = Cards.getCard(object_id).card_id;
                Setting.render_card_blacklist.toggle(card_id);
                Lib.cookie.setSet("render_card_blacklist", Setting.render_card_blacklist);
                const add = Setting.render_card_blacklist.has(card_id);
                Notify.showCommand(`${card_id} ${add ? "add to" : "remove from"} render_card_blacklist`);
                if (add) {
                    Cards.render.printCards();
                }
            }
            else if (e.ctrlKey) {
                const object_id = Number(card_div.dataset.id);
                const card_id = Cards.getCard(object_id).card_id;
                Setting.render_card_whitelist.toggle(card_id);
                Lib.cookie.setSet("render_card_whitelist", Setting.render_card_whitelist);
                const add = Setting.render_card_blacklist.has(card_id);
                Notify.showCommand(`${card_id} ${Setting.render_card_whitelist.has(card_id) ? "add to" : "remove from"} render_card_whitelist`);
                if (!add) {
                    Cards.render.printCards();
                }
            }
            else if (e.shiftKey) {
                const object_id = Number(card_div.dataset.id);
                const card_id = Cards.getCard(object_id).card_id;
                const text = card_id.toString();
                copyToClipboard(text);
            }
            else {
                HoverCard.flip();
            }
            Cards.render.lastRightClickTimes.set(card_div.dataset.id, currentTime);
            e.stopPropagation();
            e.preventDefault();
        };
        const createEvent = new CustomEvent('createCard', {
            detail: {
                div: card_div,
            }
        });
        window.dispatchEvent(createEvent);
        card_div.onmouseenter = function () {
            HoverCard.set(card_div);
        };
        card_div.onmouseleave = function () {
            HoverCard.set(null);
        };
        let card_bg = document.createElement('div');
        card_bg.classList.add('face');
        card_div.appendChild(card_bg);
        let card_image = document.createElement('div');
        card_image.classList.add('image');
        card_bg.appendChild(card_image);
        if (Cards.getCard(object_id).is_new) {
            let card_new = document.createElement('div');
            card_new.classList.add('badge-new');
            card_image.appendChild(card_new);
        }
        if (Setting.show_card_id) {
            let card_debug = document.createElement('div');
            card_debug.classList.add('debug-text');
            card_div.appendChild(card_debug);
        }
        let card_info = document.createElement('div');
        card_info.classList.add('info');
        card_bg.appendChild(card_info);
        let card_res = document.createElement('div');
        card_res.classList.add('info_pay');
        card_image.appendChild(card_res);
        let bind_image_info = document.createElement('div');
        bind_image_info.classList.add('bind-image-info');
        card_image.appendChild(bind_image_info);
        let card_target_equip = document.createElement('div');
        card_target_equip.classList.add('equip');
        card_bg.appendChild(card_target_equip);
        let auto_activate = document.createElement('div');
        auto_activate.classList.add('auto-activate-btn');
        auto_activate.innerHTML = `<i class="fa fa-check-circle-o" aria-hidden="true"></i>`;
        card_bg.appendChild(auto_activate);
        function toggleAutoActivateHelper(e) {
            const object_id = Number(card_div.dataset.id);
            const card_id = Cards.getCard(object_id).card_id;
            card_div.classList.toggle(ClassName.auto_activate);
            e.stopPropagation();
            e.preventDefault();
            if (card_div.classList.contains(ClassName.auto_activate)) {
                AutoActivate.config.add(card_id);
            }
            else {
                AutoActivate.config.delete(card_id);
            }
            AutoActivate.saveConfig();
        }
        auto_activate.onclick = toggleAutoActivateHelper;
        if (this.is_ssr == "super") {
            card_bg.classList.add('super-rare');
        }
        else if (this.is_ssr == "ultra") {
            card_bg.classList.add('ultra-rare');
        }
        if (AutoActivate.config.has(this.card_id)) {
            card_div.classList.add(ClassName.auto_activate);
        }
        return card_div;
    }
}
class PlayerDescriptor {
    constructor(obj, control_player) {
        this.area_hero = toPlayerCardDescriptorList(control_player, obj['area_hero'], "player-all-area-hero", { is_in_play: true });
        this.allies = toPlayerCardDescriptorList(control_player, obj['allies'], "player-all-allies", { is_in_play: true });
        this.supports = toPlayerCardDescriptorList(control_player, obj['supports'], "player-all-supports", { is_in_play: true });
        this.player_deck = toPlayerCardDescriptorList(control_player, obj['player_deck'], null);
        this.player_discard_pile = toPlayerCardDescriptorList(control_player, obj['player_discard_pile'], null);
        this.dealt_encounter_cards = toPlayerCardDescriptorList(control_player, obj['dealt_encounter_cards'], "player-all-area-hero", { is_dealt_card: true });
        this.hand_cards = toPlayerCardDescriptorList(control_player, obj['hand_cards'], "player-all-hand-cards", { is_in_hand: true });
        this.engaged_enemies = toPlayerCardDescriptorList(control_player, obj['engaged_enemies'], "player-all-engaged-minions", { is_in_play: true });
        this.set_aside_nemesis_sets = toPlayerCardDescriptorList(control_player, obj['set_aside_nemesis_sets'], "nemesis-pool");
        this.set_aside_deck = toPlayerCardDescriptorList(control_player, obj['set_aside_deck'], "area-removed");
        this.additional_deck = toPlayerCardDescriptorList(control_player, obj['additional_deck'], null);
        this.additional_discard_pile = toPlayerCardDescriptorList(control_player, obj['additional_discard_pile'], null);
        this.obligations_area = toPlayerCardDescriptorList(control_player, obj['obligations_area'], "player-all-area-hero", { is_in_play: true, is_obligation: true });
        this.environment_area = toPlayerCardDescriptorList(control_player, obj['environment_area'], "player-all-area-hero", { is_in_play: true, is_obligation: true });
        this.resources = obj['resources'];
        this.is_eliminated = obj['is_eliminated'];
        this;
    }
}
export class WorldDescriptor {
    constructor(obj) {
        this.render_id = obj['render_id'];
        this.round_id = obj['round_id'];
        this.phase = obj['phase'];
        this.prompt = obj['prompt'];
        this.event_name = obj['event_name'];
        this.prompt_last_text = obj['prompt_last_text'];
        this.sound_name = obj['sound_name'];
        this.max_card_object_id = obj['max_card_object_id'];
        this.active_card_ids = obj['active_card_ids'];
        this.area_schemes_main = toCardCardDescriptorList(obj['area_schemes_main'], "area-schemes-main", { is_in_play: true });
        this.main_schemes_deck = toCardCardDescriptorList(obj['main_schemes_deck'], "area-advanced");
        this.area_schemes_side = toCardCardDescriptorList(obj['area_schemes_side'], "area-schemes-side", { is_in_play: true });
        this.additional_decks = obj['additional_decks'].map((x) => toCardCardDescriptorList(x, null));
        this.additional_discard_piles = obj['additional_discard_piles'].map((x) => toCardCardDescriptorList(x, null));
        this.area_boost = toCardCardDescriptorList(obj['area_boost'], "area-play");
        this.area_environment = toCardCardDescriptorList(obj['area_environment'], "area-villain", { is_in_play: true });
        this.area_evidence = toCardCardDescriptorList(obj['area_evidence'], "area-removed", { is_in_play: true });
        this.area_rule = toCardCardDescriptorList(obj['area_rule'], "area-villain", { is_in_play: true });
        this.area_processing = toCardCardDescriptorList(obj['area_processing'], "area-play");
        this.area_revealing = toCardCardDescriptorList(obj['area_revealing'], "area-play");
        this.area_resources = toCardCardDescriptorList(obj['area_resources'], "area-play");
        this.area_removed = toCardCardDescriptorList(obj['area_removed'], "area-removed");
        this.area_insert = toCardCardDescriptorList(obj['area_insert'], "removed-pool");
        this.area_set_aside = toCardCardDescriptorList(obj['area_set_aside'], "area-removed");
        this.victory_display = toCardCardDescriptorList(obj['victory_display'], "victory-display");
        this.area_status_cards = toCardCardDescriptorList(obj['area_status_cards'], "removed-pool");
        this.players = obj['players'].map((x, index) => new PlayerDescriptor(x, index));
        this.area_villain = toCardCardDescriptorList(obj['area_villain'], "area-villain", { is_in_play: true });
        this.villain_deck = toCardCardDescriptorList(obj['villain_deck'], "area-advanced");
        this.encounter_deck = toCardCardDescriptorList(obj['encounter_deck'], "encounter-deck-0");
        this.encounter_discard_pile = toCardCardDescriptorList(obj['encounter_discard_pile'], "encounter-discard-pile-0");
    }
}
//# sourceMappingURL=descriptor.js.map