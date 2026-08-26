const specialCostButton = document.getElementById('specialCostButton')
const historyList = document.getElementById('history_list')
const extrasList = document.getElementById('extras_list')

function getAddress() {
    return 'http://' + window.location.hostname
}

const card_history = new Array();
const card_extras = new Array();

class Card {
    constructor(oracle_id, name) {
        this.oracle_id = oracle_id;
        this.name = name;
    }
}

class Extra {
    constructor(oracle_id, display_name, name, type, stats) {
        this.oracle_id = oracle_id;
        this.display_name = display_name;
        this.name = name;
        this.stats = stats;
    }
}

async function openError(error_message) {
    let message_field = document.getElementById('error_message');
    message_field.innerText = error_message;

    let myCollapse = document.getElementById('error_section');
    let col = new bootstrap.Collapse(myCollapse);
    col.show();
}

function createHistoryListItem(name, oracle_id) {
    const listElement = document.createElement("li");
    listElement.classList.add('list-group-item');
    listElement.classList.add('d-flex');
    listElement.classList.add('justify-content-between');
    listElement.classList.add('align-items-center');
    const textNode = document.createTextNode(name);
    const printNode = document.createElement("button")
    printNode.classList.add("btn");
    printNode.classList.add("btn-primary");
    printNode.addEventListener("click", function() { printCardById(oracle_id); });
    printNode.appendChild(document.createTextNode("print"));
    listElement.appendChild(textNode);
    listElement.appendChild(printNode);
    return listElement
}

async function setPaperStatus() {
    const response = await fetch(getAddress() + '/api/status');
    if (!response.ok) {
        paper_label.innerText = 'something went wrong?';
        return;
    }
    const data = await response.json();
    paper_label.innerText = data.paper;
}

async function printRandomCard(button) {
    let response = await fetch(getAddress() + '/api/print/random/' + button.innerText, { method: "post" });
    if (!response.ok) {
        const data = await response.json();
        await openError(data.message);
        return
    }

    appendHistory(await response.json());
    outputHistory();
    outputExtras();
}

async function printCardById(oracle_id) {
    let response = await fetch(getAddress() + '/api/print/oid/' + oracle_id, { method: "post" });
    if (!response.ok) {
        const data = await response.json();
        await openError(data.message);
        return
    }
}

function appendHistory(responseJson) {
    let res = responseJson;
    let card_json = res.card;
    let card = new Card(card_json.oracle_id, card_json.name);
    card_history.push(card);
    
    res.extras.forEach(e => {
        let extra = new Extra(e.oracle_id, e.extra_name, e.name, e.type, e.stats);
        card_extras.push(extra);
    });
}

function outputHistory() {
    if (card_history.length == 0) {
        return;
    }

    historyList.innerHTML = '';

    card_history.forEach(card => {
        const listElement = createHistoryListItem(card.name, card.oracle_id);
        historyList.insertBefore(listElement, historyList.children[0]);
    });
}

function outputExtras() {
    if (card_extras.length == 0) {
        return;
    }

    extrasList.innerHTML = '';

    card_extras.forEach(card => {
        const listElement = createHistoryListItem(card.display_name, card.oracle_id);
        extrasList.insertBefore(listElement, extrasList.children[0]);
    });
}

function increaseSpecialCost() {
    let value = Number(specialCostButton.innerText);
    value += 1;
    if (value > 20) {
        value = 20;
    }
    specialCostButton.innerText = value;
}

function decreaseSpecialCost() {
    let value = Number(specialCostButton.innerText);
    value -= 1;
    if (value < 0) {
        value = 0;
    }

    specialCostButton.innerText = value;
}
