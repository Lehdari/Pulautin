//
// Created by {{AUTHOR}} on {{DATE}}.
//

#ifndef SDL_APP_HPP
#define SDL_APP_HPP


#include <SDL.h>
#include <string>


class SDLApp {
public:
    // Settings for the application
    struct Settings {
        std::string     windowName;
        int64_t         windowWidth;
        int64_t         windowHeight;
        int64_t         windowFramerateLimit;

        explicit Settings(
            const std::string& windowName = "",
            int64_t windowWidth = 800,
            int64_t windowHeight = 600,
            int64_t windowFramerateLimit = 60) :
            windowName             (windowName),
            windowWidth            (windowWidth),
            windowHeight           (windowHeight),
            windowFramerateLimit   (windowFramerateLimit)
        {}
    };

    explicit SDLApp(const Settings& settings = Settings());
    ~SDLApp();

    void loop(void);

private:
    Settings        _settings;
    SDL_Window*     _window;
    SDL_Surface*    _surface;
    bool            _quit; // flag for quitting the application

    // Window event handling loop
    void handleEvents(SDL_Event& event);
    void render(void);
};


#endif // SDL_APP_HPPs