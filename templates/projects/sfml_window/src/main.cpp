#include "Window.hpp"


int main(void) {
    Window window(Window::Settings("{{PROJECT_NAME}}"));

    window.loop();

    return 0;
}
