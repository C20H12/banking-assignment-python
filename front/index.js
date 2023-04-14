const loginFormBtns = document.querySelectorAll("[data-login-form-btn]");
const loginInputFields = document.querySelectorAll("[data-login-input-field]");
const loginOutput = document.querySelector("#login-output-message");

const transacArea = document.querySelector("div.transactions");
const actionArea = document.querySelector('div.actions');

const transacLogArea = document.querySelector("#transac-logs");
const actionAreas = document.querySelectorAll("[data-action-area]");


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
  transacArea.classList.add('hidden')
  actionArea.classList.add('hidden')
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

function validateFields(fields) {
  for (const input of fields) {
    if (input.value === "") {
      return [false, "One or more fields are empty"];
    }
    const inputStr = input.value.toString()
    const decimalPlaces = inputStr.split(".")[1];
    if (input.type === "number" && (inputStr === '0' || decimalPlaces?.length > 2)) {
      return [false, "Invalid number"];
    }
  }
  return [true, ''];
}


loginFormBtns.forEach(btn => {
  btn.addEventListener("click", () => {
    const [isValid, invalidMsg] = validateFields(loginInputFields);
    if (!isValid) {
      loginOutput.value = invalidMsg;
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
        transacArea.classList.remove('hidden');
        actionArea.classList.remove('hidden');
      }
    })
    .catch(err => {
      console.warn("Request error:", err);
    })
  })
})


actionAreas.forEach(area => {
  const actionInputs = area.querySelectorAll("input");
  const btn = area.querySelector("button");
  const actionOutput = area.querySelector("output");
  btn.addEventListener("click", () => {
    const [isValid, invalidMsg] = validateFields(actionInputs);
    if (!isValid) {
      actionOutput.value = invalidMsg;
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
      if (actionOutput) {
        actionOutput.value = res.message;
      }
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

