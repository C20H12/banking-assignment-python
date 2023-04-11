const loginBtn = document.querySelector("#login");
const registerBtn = document.querySelector("#register");
const form = document.querySelector("#form");
const output = document.querySelector("#output-message")

form.addEventListener("submit", e => {
  e.preventDefault();
})

function getFormEntries() {
  const formData = new FormData(form);
  const formEntries = {}
  for (const [name, value] of formData) {
    formEntries[name] = value;
  }
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

