document.addEventListener("DOMContentLoaded", function () {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
      setTimeout(() => {
        const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
        bsAlert.close();
      }, 3000);
    });
  });

  function togglePassword() {
    const input = document.getElementById("passwordInput");
    input.type = input.type === "password" ? "text" : "password";
  }
  