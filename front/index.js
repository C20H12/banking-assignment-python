const loginBtn = document.querySelector("#login");
const registerBtn = document.querySelector("#register");
const output = document.querySelector("#output-message");
const inputFields = document.querySelectorAll("[data-input-field]");


function getFormEntries() {
  const formEntries = {}
  inputFields.forEach(inputField => {
    formEntries[inputField.name] = inputField.value;
  })
  return formEntries;
}

loginBtn.addEventListener("click", () => {
  fetch("/", {
    method: "POST",
    headers: {'Content-Type': 'application/json'}, 
    body: JSON.stringify({
      action: "login", 
      data: getFormEntries()
    })
  })
  .then(res => res.json())
  .then(res => {
    console.log("Request complete! response:", res);
  });
})

registerBtn.addEventListener("click", () => {
  fetch("/", {
    method: "POST",
    headers: {'Content-Type': 'application/json'}, 
    body: JSON.stringify({
      action: "register", 
      data: getFormEntries()
    })
  })
  .then(res => res.json())
  .then(res => {
    console.log("Request complete! response:", res);
  });
})

