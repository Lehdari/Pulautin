#include <cstdio>

#include "Types.hpp"


int main(void) {
	MyType projName = "{{PROJECT_NAME}}";

    printf("Hello %s!\n", projName.c_str());

    return 0;
}
