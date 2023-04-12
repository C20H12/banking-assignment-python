const loginFormBtns = document.querySelectorAll("[data-login-form-btn]");
const inputFields = document.querySelectorAll("[data-login-input-field]");
const output = document.querySelector("#output-message");


function getAccountData() {
  const formEntries = {}
  inputFields.forEach(inputField => {
    formEntries[inputField.name] = inputField.value;
  })
  return formEntries;
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
    });
  })
})




