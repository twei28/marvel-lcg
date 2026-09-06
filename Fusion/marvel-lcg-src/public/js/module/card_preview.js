"use strict";
import { copyToClipboard } from '../lib/clipboard.js';
export class CardPreview {
    constructor(const_card_dict) {
        this.lastClickCardDiv = null;
        this.statisticsJson = {};
        this.constCardDict = const_card_dict;
        this.previewImg = document.createElement('img');
        this.previewImg.id = 'preview-img';
        this.previewImg.src = '';
        this.previewImg.alt = 'Preview';
        this.previewCardIdDiv = document.createElement('div');
        this.previewCardIdDiv.id = 'preview-card-id';
        this.previewDiv = this.createPreviewContainer();
    }
    createPreviewContainer() {
        const div = document.createElement('div');
        div.id = 'preview';
        div.setAttribute('tabindex', '0');
        div.onkeydown = this.handleKeyDown.bind(this);
        div.onclick = this.killPreview.bind(this);
        document.body.appendChild(div);
        const previewContentDiv = document.createElement('div');
        previewContentDiv.id = 'preview-content';
        previewContentDiv.appendChild(this.previewImg);
        previewContentDiv.appendChild(this.previewCardIdDiv);
        const nextButton = this.createButton('next', 'fa-arrow-circle-o-right', this.showNextCard.bind(this));
        const prevButton = this.createButton('prev', 'fa-arrow-circle-o-left', this.showPreviousCard.bind(this));
        div.appendChild(prevButton);
        div.appendChild(previewContentDiv);
        div.appendChild(nextButton);
        return div;
    }
    createButton(id, iconClass, onClick) {
        const buttonDiv = document.createElement('div');
        buttonDiv.id = id;
        buttonDiv.onclick = onClick;
        buttonDiv.innerHTML = `<i class="fa ${iconClass}" aria-hidden="true"></i>`;
        return buttonDiv;
    }
    handleKeyDown(event) {
        if (this.lastClickCardDiv) {
            if (event.key === 'ArrowLeft') {
                event.preventDefault();
                this.showPreviousCard();
            }
            else if (event.key === 'ArrowRight') {
                event.preventDefault();
                this.showNextCard();
            }
        }
        if (event.key === "Escape") {
            this.killPreview();
            event.preventDefault();
        }
    }
    killPreview() {
        if (this.previewDiv) {
            this.previewDiv.style.display = 'none';
        }
    }
    showPreviousCard(e = null) {
        if (e) {
            e.stopPropagation();
        }
        const div = this.lastClickCardDiv?.previousElementSibling;
        this.previewCard(div);
    }
    showNextCard(e = null) {
        if (e) {
            e.stopPropagation();
        }
        const div = this.lastClickCardDiv?.nextElementSibling;
        this.previewCard(div);
    }
    getDivIndex(divElement) {
        if (!(divElement instanceof HTMLDivElement)) {
            throw new Error("The provided element is not a valid <div> element.");
        }
        const parent = divElement.parentElement;
        if (!parent) {
            throw new Error("The provided <div> element has no parent.");
        }
        const children = Array.from(parent.children);
        return children.indexOf(divElement);
    }
    previewCard(cardDiv, statisticsJson) {
        if (!cardDiv) {
            return;
        }
        if (statisticsJson) {
            this.statisticsJson = statisticsJson;
        }
        else {
            statisticsJson = this.statisticsJson;
        }
        const cardId = cardDiv.getAttribute('data-card-id');
        const cardName = this.constCardDict[cardId].name;
        this.lastClickCardDiv = cardDiv;
        this.previewImg.src = cardId;
        const fullLinkId = this.constCardDict[cardId].full_link_id;
        const index = `${this.getDivIndex(cardDiv) + 1}/${cardDiv.parentNode?.children.length}`;
        this.previewCardIdDiv.innerHTML = `
            <span class='preview-key'>(${index})</span><br/>
            <span class='preview-key' id='copy-card-name'>
                <i class="fa fa-clipboard preview-key" aria-hidden="true" style='padding-right: .4rem'></i>Name</span><br/>
            <span id='copy-card-id'>
                <i class="fa fa-clipboard preview-key" aria-hidden="true" style='padding-right: .4rem'></i>${cardId}</span><br/>
            <br/>
        `;
        if (fullLinkId) {
            this.previewCardIdDiv.innerHTML += `
                <span class='preview-key'>Related</span><br/>
                ${fullLinkId}<br/>
                <br/>
            `;
        }
        if (statisticsJson && cardId in statisticsJson) {
            this.previewCardIdDiv.innerHTML += `
                <hr style="color: black"/>
                <span class='preview-key'>Resolve</span><br/>
                ${statisticsJson[cardId].resolve}<br/>
                <span class='preview-key'>Play</span><br/>
                ${statisticsJson[cardId].play}<br/>
                <span class='preview-key'>Defeated</span><br/>
                ${statisticsJson[cardId].defeated}<br/>
            `;
        }
        else {
        }
        const copyCardNameElement = document.getElementById('copy-card-name');
        if (copyCardNameElement) {
            copyCardNameElement.onclick = (e) => {
                this.copyToClipboard(cardName);
            };
        }
        const copyCardIdElement = document.getElementById('copy-card-id');
        if (copyCardIdElement) {
            copyCardIdElement.onclick = (e) => {
                this.copyToClipboard(cardId);
            };
        }
        if (this.constCardDict[cardId].rotate) {
            this.previewImg.classList.add('rotate');
        }
        else {
            this.previewImg.classList.remove('rotate');
        }
        if (this.previewDiv) {
            this.previewDiv.style.display = 'flex';
            this.previewDiv.focus();
        }
    }
    copyToClipboard(text) {
        copyToClipboard(text);
    }
}
//# sourceMappingURL=card_preview.js.map