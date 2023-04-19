// login and register buttons
const loginFormBtns = document.querySelectorAll("[data-login-form-btn]");
// username and password input fields
const loginInputFields = document.querySelectorAll("[data-login-input-field]");
// output message
const loginOutput = document.querySelector("#login-output-message");

// the section for transactions
const transacArea = document.querySelector("div.transactions");
// the div containing the logs
const transacLogs = document.querySelector("#transac-logs");

// the div containing the action areas
const actionArea = document.querySelector('div.actions');
// the areas each with their input fields and buttons
const actionAreas = document.querySelectorAll("[data-action-area]");

/**
 * get the username and password from the input fields
 * @returns {{username: string, password: string}} an object containing the username and password
 */
function getAccountData() {
  const formEntries = {}
  loginInputFields.forEach(inputField => {
    formEntries[inputField.name] = inputField.value;
  })
  return formEntries;
}

/**
 * reset the page
 * clear the input fields and output message on the login form and action areas
 * so the user can login again
 */
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
  transacArea.classList.add('hidden');
  actionArea.classList.add('hidden');
  actionAreas.forEach(action => {
    action.querySelectorAll("input,output").forEach(field => {
      field.value = "";
    })
  })
}

/**
 * replace the logs with a new array of elements constructed from the transaction array
 * @param {Object[]} transacArr the transaction data
 */
function updateTransacLogs(transacArr) {
  transacLogs.innerHTML = "";
  for (const entry of transacArr) {
    const row = document.createElement("div");
    row.classList.add("row");
    for (const value of Object.values(entry)) {
      const col = document.createElement("span");
      col.classList.add("col");
      col.innerText = value;
      row.appendChild(col);
    }
    transacLogs.appendChild(row);
  }
}

/**
 * validate the input fields
 * @param {HTMLInputElement[]} fields the input fields to validate
 * @returns {[boolean, string]} an array with the first element being a boolean indicating whether the fields are valid
 * and the second element being a message indicating the reason for invalidity
 */
function validateFields(fields) {
  for (const input of fields) {
    if (input.value === "") {
      return [false, "One or more fields are empty"];
    }
    const inputStr = input.value.toString()

    // check if the input is a number and if it has more than 2 decimal places
    const decimalPlaces = inputStr.split(".")[1];
    if (input.type === "number" && 
         (inputStr === '0' || 
           decimalPlaces?.length > 2 || 
           isNaN(parseFloat(inputStr)) || 
           inputStr.startsWith('-'))) {
      return [false, "Invalid number"];
    }
  }
  return [true, ''];
}


loginFormBtns.forEach(btn => {
  btn.addEventListener("click", () => {
    console.log("btn clicked", btn.value)

    // check if the input fields are valid
    const [isValid, invalidMsg] = validateFields(loginInputFields);
    if (!isValid) {
      loginOutput.value = invalidMsg;
      return;
    }
    
    // send a request to the server
    // the server responds with a json object with a message
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

      // display the message
      loginOutput.value = res.message;

      // the server sends the data only if the login suceeded
      // if login is successful, disable the login form and show the transaction logs and action areas
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
  // each action area has input fields, a GO button and an output field
  const actionInputs = area.querySelectorAll("input");
  const btn = area.querySelector("button");
  const actionOutput = area.querySelector("output");

  btn.addEventListener("click", () => {
    console.log("btn clicked", btn.value);

    // check if the input fields are valid
    const [isValid, invalidMsg] = validateFields(actionInputs);
    if (!isValid) {
      actionOutput.value = invalidMsg;
      return;
    }

    // gather the data from the input fields
    const data = {}
    actionInputs.forEach(input => {
      data[input.id] = input.value;
    });
    
    // send a request to the server
    // the server responds with a json object with a message and the updated transaction logs
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

      // display the message
      actionOutput.value = res.message;

      // the server sends the data only if the action was successful
      // if the action was successful, update the transaction logs
      if (res.data) {
        updateTransacLogs(res.data);

        // if the account was deleted, clear the page
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

// clear the page when the logout button is clicked
const logoutBtn = document.querySelector("#logout-btn");
logoutBtn.addEventListener("click", clearAccountData)

