const loginFormBtns = document.querySelectorAll("[data-login-form-btn]");
const loginInputFields = document.querySelectorAll("[data-login-input-field]");
const loginOutput = document.querySelector("#login-output-message");
const transacLogArea = document.querySelector("#transac-logs");


function getAccountData() {
  const formEntries = {}
  loginInputFields.forEach(inputField => {
    formEntries[inputField.name] = inputField.value;
  })
  return formEntries;
}

function clearAccountData() {
  loginInputFields.forEach(inputField => {
    inputField.value = "";
    inputField.removeAttribute("disabled")
  })
  loginOutput.value = "";
  loginFormBtns.forEach(btn => {
    btn.removeAttribute("disabled");
  })
  loginOutput.value = "You have been logged out";
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

function hasEmptyFields(fields) {
  for (const input of fields) {
    if (input.value === "") {
      return true;
    }
  }
  return false;
}


loginFormBtns.forEach(btn => {
  btn.addEventListener("click", () => {
    if (hasEmptyFields(loginInputFields)) {
      actionOutput.value = "One or more fields are empty"
      return;
    }
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
      loginOutput.value = res.message;
      if (btn.value === "login" && res.data) {
        updateTransacLogs(res.data);

        [...loginFormBtns, ...loginInputFields].forEach(element => {
          element.setAttribute("disabled", "true");
        })
      }
    })
    .catch(err => {
      console.warn("Request error:", err);
    })
  })
})


const actionAreas = document.querySelectorAll("[data-action-area]");
actionAreas.forEach(area => {
  const actionInputs = area.querySelectorAll("input");
  const btn = area.querySelector("button");
  const actionOutput = area.querySelector("output");
  btn.addEventListener("click", () => {
    if (hasEmptyFields(actionInputs)) {
      actionOutput.value = "One or more fields are empty"
      return;
    }
    console.log("btn clicked", btn.value)
    const data = {}
    actionInputs.forEach(input => {
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
        if (res.message === "Account deleted") {
          clearAccountData()
        }
      }
    })
    .catch(err => {
      console.warn("Request error:", err);
    })
  })
})

const logoutBtn = document.querySelector("#logout-btn");
logoutBtn.addEventListener("click", clearAccountData)

