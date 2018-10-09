//
// Created by {{AUTHOR}} on {{DATE}}.
//

#include "SDLApp.hpp"


SDLApp::SDLApp(const SDLApp::Settings &settings) :
    _settings   (settings),
    _window     (nullptr),
    _surface    (nullptr),
    _quit       (false)
{
    // Initialize SDL
    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
        printf("Error: Could not initialize SDL!\n");
        return;
    }

    _window = SDL_CreateWindow(
         _settings.windowName.c_str(),
         SDL_WINDOWPOS_UNDEFINED,
         SDL_WINDOWPOS_UNDEFINED,
         (int)_settings.windowWidth,
         (int)_settings.windowHeight,
         SDL_WINDOW_SHOWN);

    if (_window == nullptr) {
        printf("Error: SDL Window could not be created! SDL_Error: %s\n", SDL_GetError());
        return;
    }

    _surface = SDL_GetWindowSurface(_window);
}

SDLApp::~SDLApp()
{
    // Destroy window and quit SDL subsystems
    SDL_DestroyWindow(_window);
    SDL_Quit();
}

void SDLApp::loop(void)
{
    // Application main loop
    while (!_quit) {
        SDL_Event event;
        while (SDL_PollEvent(&event) != 0)
            handleEvents(event);

        render();

        SDL_UpdateWindowSurface(_window);
    }
}


void SDLApp::handleEvents(SDL_Event& event)
{
    // Handle SDL events
    switch (event.type) {
        case SDL_QUIT:
            _quit = true;
            break;

        case SDL_KEYDOWN:
            switch (event.key.keysym.sym) {
                case SDLK_ESCAPE:
                    _quit = true;
                    break;

                default:
                    break;
            }
            break;

        default:
            break;
    }
}

void SDLApp::render(void)
{
    //  Render OpenGL stuff here
}