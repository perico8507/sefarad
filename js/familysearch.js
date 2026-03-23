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

        // Ejemplo de uso: (Se requiere estar autenticado primero)
        // fs.get('/platform/users/current', (error, response) => {
        //     if (error) {
        //         console.error('Error al obtener el usuario:', error);
        //     } else {
        //         console.log('Datos del usuario autenticado:', response.data);
        //     }
        // });
        
        // Exportar a nivel global por si necesitas llamarlo desde otros scripts o la consola
        window.fsApi = fs;
    } else {
        console.error("El SDK de FamilySearch no pudo ser cargado.");
    }
});