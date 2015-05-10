#include <stdio.h>
#include <sys/time.h>
int main(void)
{
    time_t t;
    t = time(NULL);
    printf("The number of seconds since January 1, 1970 is %d\n", (int)t);
    return 0;
}
