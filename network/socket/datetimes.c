/****************************************************/
/************* datetime Example Server **************/
/****************************************************/
#include "datetime.h"
#include <time.h>

int
main( int argc , char * * argv )
{
	int listenfd , connfd;
	struct sockaddr_in servaddr;
	char buff[ MAXLINE ];
	time_t ticks;

	listenfd = socket( AF_INET , SOCK_STREAM , 0 );

	memset( &servaddr , 0 , sizeof( servaddr ) );
	servaddr.sin_family = AF_INET;
	servaddr.sin_addr.s_addr = htonl( INADDR_ANY );
	servaddr.sin_port = htons( 1113 );

	bind( listenfd , (struct sockaddr *)&servaddr , sizeof( servaddr ) );
	listen( listenfd , 1024 );

	for( ; ; )
	{
        printf("Before Accept...\n");
		connfd = accept( listenfd , (struct sockaddr *)NULL , NULL );
        printf( "%d\n", connfd );
		ticks = time( NULL );
		//snprintf( buff , sizeof( buff ) , "%.24s\r\n" , ctime( &ticks ) );
        strncpy( buff, ctime( &ticks ), MAXLINE );
		write( connfd , buff , strlen( buff ) );
		close( connfd );
	}
}
