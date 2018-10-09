//
// Created by {{AUTHOR}} on {{DATE}}.
//

#include "SDLApp.hpp"


int main(int argv, char** args) {

    SDLApp app(SDLApp::Settings("{{EXECUTABLE_NAME}}"));
    app.loop();

    return 0;
}
