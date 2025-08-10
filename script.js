document.querySelector("form").addEventListener("submit", function(e) {
  const emailsField = document.getElementById("emails");
  const emails = emailsField.value.split(",");
  

  // Add emails as hidden inputs for backend
  emailsField.remove();
  const form = document.querySelector("form");
  emails.forEach(email => {
    const input = document.createElement("input");
    input.type = "hidden";
    input.name = "emails";
    input.value = email.trim();
    form.appendChild(input);
  });
});
