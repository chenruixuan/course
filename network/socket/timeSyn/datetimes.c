/****************************************************/
/************* datetime Example Server **************/
/****************************************************/
#include "datetime.h"

int
main( int argc , char * * argv )
{
	int listenfd , connfd;
	struct sockaddr_in servaddr;
    pid_t pid;
	char buff[ MAXLINE ];
	//time_t ticks;
    int ticks;
    int len = sizeof( struct sockaddr );

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
        if ( (pid = fork()) == 0 ) {
            // 显示连接的客户端和服务器的IP地址
            struct sockaddr_in serv, guest;
            char serv_ip[20];
            char guest_ip[20];
            int serv_len = sizeof(serv);
            int guest_len = sizeof(guest);
            getsockname(connfd, (struct sockaddr *)&serv, &serv_len);
            getpeername(connfd, (struct sockaddr *)&guest, &guest_len);
            inet_ntop(AF_INET, &serv.sin_addr, serv_ip, sizeof(serv_ip));
            inet_ntop(AF_INET, &guest.sin_addr, guest_ip, sizeof(guest_ip));
            printf("host %s:%d guest %s:%d\n", serv_ip, ntohs(serv.sin_port),
                    guest_ip, ntohs(guest.sin_port));

            // 向客户端发送服务器时间
            ticks = (int)time( NULL );
            //snprintf( buff , sizeof( buff ) , "%.24s\r\n" , ctime( &ticks ) );
            //strncpy( buff, ctime( &ticks ), MAXLINE );
            memcpy( buff, &ticks, 4 );
            write( connfd , buff , strlen( buff ) );
            close( connfd );


        }
        close( connfd );
	}
}
