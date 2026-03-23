// Configuración inicial de FamilySearch API
document.addEventListener('DOMContentLoaded', () => {
    console.log("Inicializando FamilySearch API SDK...");

    // Se asume que el objeto FamilySearch está disponible gracias al CDN de fs-js-lite
    if (typeof FamilySearch !== 'undefined') {
        const fs = new FamilySearch({
            // Debes reemplazar 'YOUR_APP_KEY' con el App Key real otorgado por FamilySearch Developer Center
            appKey: 'YOUR_APP_KEY', 
            // La URI a donde FamilySearch redireccionará después de autenticarse
            redirectUri: window.location.origin + '/oauth-redirect.html',
            // Usa 'integration' para pruebas y sandbox, o 'production' para el entorno en vivo
            environment: 'integration', 
            // Opcional: configurar auto-renovación de sesión u otros parámetros
            saveAccessToken: true
        });

        console.log("FamilySearch API lista para usarse:", fs);

        // Función para iniciar el inicio de sesión
        const login = (e) => {
            if (e) e.preventDefault();
            console.log("Iniciando flujo de autorización OAuth2...");
            // El SDK se encarga de construir la URL con client_id, redirect_uri, response_type=code, etc.
            fs.oauthRedirect();
        };

        // Vincular al enlace "Acceder" de la interfaz estilo Wikipedia
        const loginLink = document.getElementById('pt-login');
        if (loginLink) {
            loginLink.addEventListener('click', login);
        }

        // Verificar si ya estamos autenticados al cargar la página
        if (fs.getAccessToken()) {
            console.log("Sesión activa detectada.");
            const userStatus = document.getElementById('pt-userpage');
            if (userStatus) {
                userStatus.innerHTML = '<a href="#">Sesión Iniciada</a>';
            }
            const loginItem = document.getElementById('pt-login');
            if (loginItem) {
                loginItem.innerHTML = '<a href="#">Cerrar Sesión</a>';
                loginItem.addEventListener('click', (e) => {
                    e.preventDefault();
                    fs.deleteAccessToken();
                    window.location.reload();
                });
            }
        }
        
        // Exportar a nivel global
        window.fsApi = fs;
        window.fsLogin = login;
    } else {
        console.error("El SDK de FamilySearch no pudo ser cargado.");
    }
});