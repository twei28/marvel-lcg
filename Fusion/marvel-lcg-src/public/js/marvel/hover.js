var _a;
import { Lib } from './lib.js';
import { ButtonSetting, Setting } from './settings.js';
import { Game } from './game.js';
import { UI } from './ui.js';
import { Cards } from './cards.js';
import { convertScenePosToWindowPos, Scene } from './scene.js';
import { ClassName } from './class_name.js';
import { CardAnimation } from './card_animation.js';
import { Button } from './buttons.js';
export class HoverCard {
    static showPreview(show) {
        if (show) {
            HoverCard.preview_left.parentElement.classList.remove("display-none");
            HoverCard.preview_right.parentElement.classList.remove("display-none");
        }
        else {
            HoverCard.preview_left.parentElement.classList.add("display-none");
            HoverCard.preview_right.parentElement.classList.add("display-none");
        }
    }
    static updateRect() {
        HoverCard.rect_left = Lib.client.getOffsetClient(HoverCard.preview_left);
        HoverCard.rect_right = Lib.client.getOffsetClient(HoverCard.preview_right);
    }
    static getPreviewRect() {
        if (HoverCard.using_left) {
            return HoverCard.rect_left;
        }
        else {
            return HoverCard.rect_right;
        }
    }
    static getPreview() {
        if (CardAnimation.animation_name == "center_flip") {
            return HoverCard.center_preview.preview_center;
        }
        if (HoverCard.using_left) {
            return HoverCard.preview_left;
        }
        else {
            return HoverCard.preview_right;
        }
    }
    static pause() {
        if (HoverCard.timer_id) {
            HoverCard.has_reveal = 0;
            clearTimeout(this.timer_id);
        }
    }
    static unPause() {
        HoverCard.setReveal(null);
        HoverCard.center_preview.hide();
    }
    static update() {
        if (HoverCard.timer_id) {
            HoverCard.has_reveal = 0;
            clearTimeout(this.timer_id);
        }
        HoverCard.set(HoverCard.hover_card, false, HoverCard.hover_card_image);
    }
    static onMouseMove(x, y, w, h) {
        let is_overlap = Lib.isOverlapping(x, y, w, h, HoverCard.rect_left.left, HoverCard.rect_left.top, HoverCard.rect_left.width, HoverCard.rect_left.height);
        if (is_overlap) {
            if (HoverCard.using_left) {
                HoverCard.hide();
                HoverCard.using_left = false;
                HoverCard.update();
            }
        }
        else {
            if (!HoverCard.using_left) {
                HoverCard.hide();
                HoverCard.using_left = true;
                HoverCard.update();
            }
        }
    }
    static updateHoverEffects(object_id, add) {
        const card = Cards.getCard(object_id);
        if (add) {
            for (let id of card.ui.effect_to_cards) {
                Cards.getDiv(id)?.classList.add('hover_effected_to');
            }
            for (let id of card.ui.effect_by_cards) {
                Cards.getDiv(id)?.classList.add('hover_effected_by');
            }
        }
        else {
            for (let id of card.ui.effect_by_cards) {
                Cards.getDiv(id)?.classList.remove('hover_effected_by');
            }
            for (let id of card.ui.effect_to_cards) {
                Cards.getDiv(id)?.classList.remove('hover_effected_to');
            }
        }
    }
    static setTilt(card_div, is_log, hide_glare) {
        if (!Setting.no_tilt) {
            if (HoverCard.getPreview().vanillaTilt) {
                HoverCard.getPreview().vanillaTilt.destroy();
                HoverCard.getPreview().querySelectorAll('.js-tilt-glare').forEach(e => {
                    e.parentNode.removeChild(e);
                });
            }
            if (!is_log) {
                let background_image = "";
                if (card_div.querySelector('.face').classList.contains('super-rare')) {
                    background_image = UI.background_image_super_rare;
                }
                if (card_div.querySelector('.face').classList.contains('ultra-rare')) {
                    background_image = UI.background_image_ultra_rare;
                }
                VanillaTilt.init(HoverCard.getPreview(), {
                    reverse: true,
                    max: 10,
                    speed: 400,
                    glare: true,
                    "max-glare": .5,
                    "mouse-event-element": card_div,
                    reset: false,
                    "reset-to-start": false,
                    "glare-background-image": background_image
                });
            }
        }
        if (hide_glare) {
            HoverCard.getPreview().classList.add("hide-glare");
        }
        else {
            HoverCard.getPreview().classList.remove("hide-glare");
        }
        HoverCard.getPreview().classList.remove('super-rare');
        HoverCard.getPreview().classList.remove('ultra-rare');
        if (card_div.querySelector('.face').classList.contains('super-rare')) {
            HoverCard.getPreview().classList.add('super-rare');
        }
        if (card_div.querySelector('.face').classList.contains('ultra-rare')) {
            HoverCard.getPreview().classList.add('ultra-rare');
        }
    }
    static setReveal(card_div, timeout = 0) {
        if (card_div) {
            if (!HoverCard.hover_card) {
                HoverCard.setTilt(card_div, false, false);
                if (!HoverCard.getPreview().parentElement.classList.contains('hide')) {
                    HoverCard.hide();
                }
                let bg_image = card_div.style.getPropertyValue('--bg-image');
                let rotate_times = getComputedStyle(card_div.querySelector('.face')).getPropertyValue('--rotate-times');
                const offset = Lib.client.getOffset2(card_div);
                let x = offset.left;
                let y = offset.top;
                let max_v = card_div.offsetWidth * Scene.scale;
                const pos = convertScenePosToWindowPos(x, y);
                HoverCard.onMouseMove(pos.x, pos.y, max_v, max_v);
                HoverCard.set2(card_div, bg_image);
                HoverCard.has_reveal += 1;
                HoverCard.timer_id = setTimeout(function () {
                    HoverCard.has_reveal -= 1;
                    if (HoverCard.has_reveal == 0) {
                        HoverCard.setReveal(null);
                    }
                }, timeout);
            }
        }
        else {
            HoverCard.onMouseMove(0, 0, 0, 0);
            if (!HoverCard.hover_card) {
                HoverCard.hide();
            }
        }
    }
    static set2(card_div, bg_image) {
        const card_id = /url\((.*?)\)$/.exec(bg_image)[1].replace(/"/g, '');
        HoverCard.set3(card_div, card_id);
    }
    static set3(card_div, card_id) {
        let rotate_times = "";
        let debug_text = "";
        let is_new = false;
        let name = "";
        let text = "";
        let type = "";
        rotate_times = getComputedStyle(card_div.querySelector('.face')).getPropertyValue('--rotate-times');
        if (['player', 'enccounter', 'villain'].includes(card_id)) {
            text = "";
        }
        else {
            const object_id = Number(card_div.dataset.id);
            const card = Cards.getCard(object_id);
            if (Setting.is_debug && Setting.cheat_show_all_cards) {
                debug_text = card_div.querySelector('.debug-text').innerHTML;
            }
            is_new = card_div.querySelector('.badge-new') != undefined;
            name = card.name;
            text = Cards.getText(card_id);
            text = Lib.game.cleanResText(text);
            type = card.card_type;
        }
        HoverCard.show(`url("${card_id}")`, name, type, text, rotate_times, debug_text, is_new);
    }
    static set(card_div, is_log = false, forced_bg_image = '') {
        let bg_image = "";
        if (UI.hold_ctrl) {
            card_div = null;
        }
        if (card_div) {
            HoverCard.setTilt(card_div, is_log, true);
            if (!is_log) {
                HoverCard.hover_card = card_div;
            }
            const object_id = Number(card_div.dataset.id);
            HoverCard.updateHoverEffects(object_id, true);
            if (Setting.showAllCards()
                || Cards.getCard(object_id).isVisible()
                || card_div.classList.contains(ClassName.being_searching)
                || Game.game_over
                || forced_bg_image
                || is_log
                || (card_div.parentElement.classList.contains('clicked') && Setting.is_debug)) {
                if (forced_bg_image) {
                    bg_image = forced_bg_image;
                }
                else {
                    bg_image = card_div.style.getPropertyValue('--bg-image-true');
                }
            }
            HoverCard.hover_card_image = bg_image;
        }
        else {
            if (HoverCard.hover_card) {
                const object_id = Number(HoverCard.hover_card.dataset.id);
                HoverCard.updateHoverEffects(object_id, false);
                HoverCard.hover_card = null;
                HoverCard.hover_card_image = "";
            }
        }
        if (card_div && bg_image) {
            HoverCard.set2(card_div, bg_image);
        }
        else {
            HoverCard.show(bg_image, "", "", "", "", "", false);
        }
    }
    static showLogImage(object_id, bg_image) {
        bg_image = `url("${bg_image}")`;
        const card_div = Cards.getDiv(object_id);
        HoverCard.set(card_div, true, bg_image);
    }
    static whenCardActive(card_div) {
        if (!HoverCard.is_showing) {
            return;
        }
        if (HoverCard.is_overlay) {
            return;
        }
        const rect = Lib.client.getOffset(card_div);
        const pos = convertScenePosToWindowPos(rect.left, rect.top);
        const w = card_div.offsetWidth * Scene.scale;
        const preview_rect = HoverCard.getPreviewRect();
        const is_overlay = Lib.isOverlapping(pos.x, pos.y, w, w, preview_rect.left, preview_rect.top, preview_rect.width, preview_rect.height);
        if (is_overlay) {
            HoverCard.whenOverlay();
        }
    }
    static whenOverlay() {
        if (HoverCard.is_overlay) {
            return;
        }
        HoverCard.is_overlay = true;
        HoverCard.getPreview().classList.add('opacity');
    }
    static hide() {
        HoverCard.show("", "", "", "", "", "", false);
    }
    static show(bg_image, name, type, text, rotate_times, debug_text, is_new) {
        const preview_div = HoverCard.getPreview();
        preview_div.classList.remove('opacity');
        HoverCard.is_overlay = false;
        if (bg_image) {
            HoverCard.is_showing = true;
            preview_div.style.transform = "none";
            preview_div.style.setProperty('--rotate-times', rotate_times);
            preview_div.style.setProperty('--bg-image', bg_image);
            if (ButtonSetting.show_image_text) {
                preview_div.parentElement.querySelector('.image-preview-name').innerHTML = name;
                preview_div.parentElement.querySelector('.image-preview-text').innerHTML = text;
            }
            else {
                preview_div.parentElement.querySelector('.image-preview-name').innerHTML = "";
                preview_div.parentElement.querySelector('.image-preview-text').innerHTML = "";
            }
            preview_div.parentElement.querySelector('.image-preview-debug-text').innerHTML = debug_text;
            preview_div.parentElement.classList.remove('hide');
            if (is_new) {
                preview_div.classList.add('badge-new');
            }
            else {
                preview_div.classList.remove('badge-new');
            }
            if (text && ButtonSetting.show_image_text) {
                preview_div.classList.remove('hide-text');
            }
            else {
                preview_div.classList.add('hide-text');
            }
            Lib.game.removeTypeClasses(preview_div);
            Lib.game.addTypeClass(preview_div, type);
        }
        else {
            HoverCard.is_showing = false;
            HoverCard.preview_left.parentElement.classList.add('hide');
            HoverCard.preview_right.parentElement.classList.add('hide');
        }
    }
    static flip() {
        if (HoverCard.hover_card) {
            const object_id = Number(HoverCard.hover_card.dataset.id);
            const card = Cards.getCard(object_id);
            if (card.down_card_ids.length > 1) {
                if (HoverCard.back_face_index >= card.down_card_ids.length) {
                    HoverCard.back_face_index = 0;
                }
                const card_id = card.down_card_ids[HoverCard.back_face_index];
                HoverCard.set3(HoverCard.hover_card, card_id);
                HoverCard.back_face_index += 1;
            }
            else if (card.isVisible()) {
                let bg_image = HoverCard.hover_card.style.getPropertyValue('--bg-image-true');
                if (HoverCard.getPreview().style.getPropertyValue('--bg-image') == bg_image) {
                    bg_image = HoverCard.hover_card.style.getPropertyValue('--bg-image-false');
                }
                HoverCard.set2(HoverCard.hover_card, bg_image);
            }
        }
    }
    static rotate(value) {
        if (HoverCard.hover_card) {
            let rotate_times_str = HoverCard.getPreview().style.getPropertyValue('--rotate-times');
            let rotate_times = Number(rotate_times_str);
            rotate_times += value;
            HoverCard.getPreview().style.setProperty('--rotate-times', rotate_times.toString());
        }
    }
}
HoverCard.hover_card_image = "";
HoverCard.preview_left = document.querySelector('#image-preview-div-left .image-preview');
HoverCard.preview_right = document.querySelector('#image-preview-div-right .image-preview');
HoverCard.timer_id = 0;
HoverCard.has_reveal = 0;
HoverCard.using_left = true;
HoverCard.is_showing = false;
HoverCard.is_overlay = false;
HoverCard.back_face_index = 0;
HoverCard.center_preview = (_a = class CenterPreview {
        static set(card_div, is_log = true) {
            CenterPreview.has_image = true;
            let bg_image = card_div.style.getPropertyValue('--bg-image-true');
            HoverCard.set2(card_div, bg_image);
        }
        static hide() {
            CenterPreview.has_image = false;
            CenterPreview.preview_center.parentElement.classList.add('hide');
        }
    },
    _a.has_image = false,
    _a.preview_center = document.querySelector('#image-preview-div-center .image-preview'),
    (() => {
        _a.preview_center.onclick = () => {
            Button.disablePause(true);
        };
    })(),
    _a);
(() => {
    HoverCard.updateRect();
})();
window.HoverCard = HoverCard;
//# sourceMappingURL=hover.js.map