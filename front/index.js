const loginFormBtns = document.querySelectorAll("[data-login-form-btn]");
const inputFields = document.querySelectorAll("[data-login-input-field]");
const output = document.querySelector("#output-message");
const transacLogArea = document.querySelector("#transac-log-area");


function getAccountData() {
  const formEntries = {}
  inputFields.forEach(inputField => {
    formEntries[inputField.name] = inputField.value;
  })
  return formEntries;
}

function updateTransacLogs(transacArr) {
  transacLogArea.innerHTML = "";
  for (const entry of transacArr) {
    const row = document.createElement("div");
    row.classList.add("row");
    for (const value of Object.values(entry)) {
      const col = document.createElement("span");
      col.classList.add("col");
      col.innerText = value;
      row.appendChild(col);
    }
    transacLogArea.appendChild(row);
  }
}

loginFormBtns.forEach(btn => {
  btn.addEventListener("click", () => {
    console.log("btn clicked", btn.value)
    fetch("/account", {
      method: "POST",
      headers: {'Content-Type': 'application/json'}, 
      body: JSON.stringify({
        action: btn.value, 
        data: null,
        accountInfo: getAccountData()
      })
    })
    .then(res => res.json())
    .then(res => {
      console.log("Request complete:", res);
      output.value = res.message;
      if (res.data) {
        updateTransacLogs(res.data);
      }
    })
    .catch(err => {
      console.warn("Request error:", err);
    })
  })
})


const actionAreas = document.querySelectorAll("[data-action-area]");
actionAreas.forEach(area => {
  const inputs = area.querySelectorAll("input");
  const btn = area.querySelector("button");
  const actionOutput = area.querySelector("output");
  btn.addEventListener("click", () => {
    const data = {}
    inputs.forEach(input => {
      data[input.id] = input.value;
    })
    fetch("/account", {
      method: "POST",
      headers: {'Content-Type': 'application/json'}, 
      body: JSON.stringify({
        action: btn.value, 
        data: data,
        accountInfo: getAccountData()
      })
    })
    .then(res => res.json())
    .then(res => {
      console.log("Request complete:", res);
      actionOutput.value = res.message;
      if (res.data) {
        updateTransacLogs(res.data);
      }
    })
    .catch(err => {
      console.warn("Request error:", err);
    })
  })
})


