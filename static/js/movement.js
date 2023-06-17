let loginForm = document.getElementById("loginForm");
console.log(loginForm);
loginForm.addEventListener("submit", (e) => {
  e.preventDefault();
  let name = document.getElementById("name").value;
  let email = document.getElementById("email").value;
  let msg = document.getElementById("msg").value;
  let data = { name: name, email: email, msg: msg };
  data = JSON.stringify(data);
  console.log(data);
  fetch("/submit", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: data,
  })
    .then((res) => {
      let loginForm = document.getElementById("loginForm");
      const div = document.createElement("div");
      div.className = "form-success";
      div.innerHTML = "Form submitted";
      div.id = "form-result";
      loginForm.replaceWith(div);
      console.log("Request complete! response:");
      const timeoutReplace = setTimeout(renewForm, 2000);
    })
    .catch((error) => {});
});

function renewForm() {
  let formResult = document.getElementById("form-result");
  formResult.replaceWith(loginForm);
  let name = document.getElementById("name");
  name.value = "";
  let email = document.getElementById("email");
  email.value = "";
  let msg = document.getElementById("msg");
  msg.value = "";
}
