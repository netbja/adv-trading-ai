// Logique JavaScript pour la page de connexion
console.log('Login JS chargé');

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const errorMessageDiv = document.getElementById('error-message');

    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const usernameInput = document.getElementById('username');
            const passwordInput = document.getElementById('password');
            
            if (!usernameInput || !passwordInput) {
                console.error("Les champs username ou password n'ont pas été trouvés");
                if(errorMessageDiv) {
                    errorMessageDiv.textContent = 'Erreur interne du formulaire.';
                    errorMessageDiv.style.display = 'block';
                }
                return;
            }

            const username = usernameInput.value;
            const password = passwordInput.value;
            
            if (errorMessageDiv) {
                errorMessageDiv.style.display = 'none'; // Cacher ancien message d'erreur
            }

            try {
                const response = await fetch('/api/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username, password })
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    // Stocker le token de session dans les cookies
                    // Le backend devrait renvoyer le token avec les bonnes options (HttpOnly, Secure, SameSite)
                    // Ici, le JS le met juste pour que les requêtes suivantes l'incluent.
                    // Le backend doit aussi s'assurer de la durée de vie du cookie.
                    document.cookie = `session_token=${result.session_token}; path=/; max-age=86400; SameSite=Lax`; // Max-age 1 jour
                    window.location.reload(); // Recharge la page, le backend servira le dashboard
                } else {
                    if (errorMessageDiv) {
                        errorMessageDiv.textContent = result.detail || 'Erreur de connexion. Veuillez vérifier vos identifiants.';
                        errorMessageDiv.style.display = 'block';
                    }
                }
            } catch (error) {
                console.error('Erreur de connexion au serveur:', error);
                if (errorMessageDiv) {
                    errorMessageDiv.textContent = 'Erreur de connexion au serveur. Veuillez réessayer plus tard.';
                    errorMessageDiv.style.display = 'block';
                }
            }
        });
    } else {
        console.error("Le formulaire de login avec l'ID 'login-form' n'a pas été trouvé.");
    }
}); 