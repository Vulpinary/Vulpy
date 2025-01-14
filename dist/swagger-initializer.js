 url: "https://vulpinary.github.io/Vulpy/",
  dom_id: '#swagger-ui',
  deepLinking: true,
  presets: [
    SwaggerUIBundle.presets.apis,
     SwaggerUIStandalonePreset
  ],
     layout: "StandaloneLayout",
  customOptions: {
    swaggerUi: {
       url: "https://vulpinary.github.io/Vulpy/",
        dom_id: '#swagger-ui',
        deepLinking: true,
        presets: [
            SwaggerUIBundle.presets.apis,
            SwaggerUIStandalonePreset
        ],
        layout: "StandaloneLayout",
        configUrl: null,
        showCommonExtensions: false,
        showExtensions: true
    }
  }
};
