const ssid_select_list = document.getElementById("select_ssid");
const ssid_connected = document.getElementById("currently_connected");
const ssid_input = document.getElementById("hidden_network_input");
const ssid_password = document.getElementById("ssid_password");
const hidden_network_input = document.getElementById("hidden_network");

function getAddress() {
    return 'http://' + window.location.hostname
}

async function refreshSSIDs() {
    updateSSIDs("Loading...", []);
    const response = await fetch(getAddress() + '/settings/ssids');
    if (!response.ok) {
        updateSSIDs("Unknown", []);
        return;
    }

    const data = await response.json();
    updateSSIDs(data.connected_to, data.available);
}

function updateSSIDs(connected, nearby_list) {
    ssid_connected.innerText = connected;
    ssid_select_list.innerHTML = '';
    nearby_list.forEach(ssid => {
        let element = document.createElement('option');
        element.textContent = ssid;
        ssid_select_list.appendChild(element);
        ssid_select_list.disabled = false;
    });

    if (nearby_list.length < 1) {
        let element = document.createElement('option');
        element.textContent = "No networks nearby";
        ssid_select_list.appendChild(element);
        ssid_select_list.disabled = true;
    }
}

function swapHiddenNetworkTextbox(checked) {
    if (checked) {
        ssid_select_list.style.display = "none";
        ssid_input.style.display = "block";
    } else {
        ssid_select_list.style.display = "block";
        ssid_input.style.display = "none";
    }
}

async function connectNewNetwork() {
    let network_hidden = "false";
    let ssid = "";
    let password = ssid_password.value;

    if (hidden_network_input.checked) {
        network_hidden = "true";
        ssid = ssid_input.value;
    } else {
        if (ssid_select_list.style.disabled == true) {
            return;
        }
        ssid = ssid_select_list.options[ssid_select_list.selectedIndex].text;
    }

    await fetch(getAddress() + '/settings/changeNetwork', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ssid: ssid, password: password, hidden: network_hidden})
    });

    await refreshSSIDs();
}

window.onload = function() {
    refreshSSIDs();
    swapHiddenNetworkTextbox(hidden_network_input.checked);
};