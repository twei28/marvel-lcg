import { Lib } from './lib.js';
import { Game } from './game.js';
import { MouseSync } from './mouse.js';
const search_params = new URLSearchParams(window.location.search);
export class Setting {
    static showAllCards() {
        return Setting.show_all_cards || Setting.cheat_show_all_cards;
    }
    static getPlayerIds() {
        let player_ids = `${Setting.player_id}`;
        if (Setting.is_hot_seat) {
            function createList(X, Y) {
                let list = [];
                for (let i = X; i <= Y; i++) {
                    list.push(i);
                }
                return list;
            }
            player_ids = createList(0, Game.total_players - 1).join(",");
        }
        return player_ids;
    }
}
Setting.is_debug = search_params.has('debug');
Setting.show_achievement = search_params.has('show_achievement') || Setting.is_debug;
Setting.hide_bug_report = search_params.has('hide_bug_report');
Setting.show_res_id = Setting.is_debug;
Setting.is_auto_test = search_params.has('auto_test');
Setting.ssr_bonus = search_params.has('ssr_bonus');
Setting.no_tilt = !search_params.has('3d_card');
Setting.statistics_off = search_params.has('notification') && search_params.get('notification') == '0';
Setting.statistics_first = !search_params.has('notification') || search_params.has('notification') && search_params.get('notification') == '1';
Setting.statistics_all = search_params.has('notification') && search_params.get('notification') == '2';
Setting.is_hot_seat = search_params.has('hot_seat');
Setting.is_watch = search_params.has('watch');
Setting.show_all_cards = search_params.has('show_all_cards');
Setting.show_card_id = search_params.has('show_card_id') || Setting.is_debug;
Setting.player_id = search_params.has('p') ? Number(search_params.get('p')) : 0;
Setting.ver = 1;
Setting.scene_3d = search_params.has('3d_scene') || search_params.has('3d');
Setting.is_remote = search_params.has('remote');
(() => {
    if (window.location.pathname == '/marvel2.html') {
        Setting.ver = 2;
    }
    ;
    if (!Setting.is_hot_seat) {
        MouseSync.init();
    }
})();
Setting.cheat_show_all_cards = false;
Setting.auto_effect_black_list = [];
Setting.render_card_whitelist = new Set([]);
Setting.render_card_blacklist = new Set([]);
Setting.render_under_card_whitelist = new Set([]);
(() => {
    Setting.render_card_whitelist = Lib.cookie.getSet("render_card_whitelist", ["32020", "36023", "16142"]);
    Setting.render_under_card_whitelist = Lib.cookie.getSet("render_under_card_whitelist", ["53021"]);
    Setting.render_card_blacklist = Lib.cookie.getSet("render_card_blacklist", ["03019"]);
})();
(() => {
    Game.forced_on_player = Setting.player_id;
    const no_animation = search_params.has('disable_animations');
    if (no_animation) {
        Setting.no_tilt = true;
        Lib.loader.loadCSS('./public/css/disable-animation.css');
    }
})();
export class ButtonSetting {
}
ButtonSetting.enable_enhance_fx = Number(!search_params.has('disable_enhance_fx'));
ButtonSetting.sort_hand_cards = Number(search_params.has('sort_hand_cards') || Setting.is_debug);
ButtonSetting.sort_area_cards = 1;
ButtonSetting.sort_discard_pile_cards = 0;
ButtonSetting.new_badge = 1;
ButtonSetting.enable_preview = Number(!search_params.has('disable_preview'));
ButtonSetting.auto_target = 1;
ButtonSetting.auto_target_forced = 0;
ButtonSetting.show_image_text = 0;
ButtonSetting.is_replay = Number(search_params.has('replay'));
ButtonSetting.music_on = 1;
ButtonSetting.show_all_players = 1;
ButtonSetting.show_all_hand_cards = Setting.is_hot_seat ? 1 : 0;
ButtonSetting.always_show_minions_belong = 1;
ButtonSetting.hide_no_action_cards = 1;
ButtonSetting.players_pin = 1;
ButtonSetting.show_auto_activate = 0;
ButtonSetting.auto_activate = 1;
ButtonSetting.pause_when_reveal_or_boost = 1;
ButtonSetting.card_tilt = 0;
window.Setting = Setting;
window.ButtonSetting = ButtonSetting;
//# sourceMappingURL=settings.js.map