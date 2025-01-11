const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");

sign_up_btn.addEventListener("click", () => {
  container.classList.add("sign-up-mode");
});

sign_in_btn.addEventListener("click", () => {
  container.classList.remove("sign-up-mode");
});

async function loginReq()
{
  const emailVal = document.getElementById("email_login").value;
  const passVal = document.getElementById("password_login").value;
  fetch("/login", {
    method: "POST",
    body: JSON.stringify({
      email: emailVal,
      password: passVal,
    }),
    headers: {
      "Content-type": "application/json; charset=UTF-8"
    }
  });
  
}