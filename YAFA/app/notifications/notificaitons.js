document.addEventListener("DOMContentLoaded", () => {
    const buttons = document.querySelectorAll(".btn-dismiss");

    buttons.forEach(button => {
        button.addEventListener("click", async () => {
            const notificationId = button.getAttribute("data-id");

            try {
                const response = await fetch(`/notifications/dismiss/${notificationId}`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": getCookie("csrf_token"),
                    },
                });

                if (response.ok) {
                    // Remove the notification item from the UI
                    button.closest(".notification-item").remove();
                } else {
                    alert("Failed to dismiss notification.");
                }
            } catch (error) {
                console.error("Error dismissing notification:", error);
                alert("Error occurred.");
            }
        });
    });
});

// Helper function to get CSRF token cookie for Flask-WTF
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
}
