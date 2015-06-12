/****************************************************/
/************* datetime Example Client **************/
/****************************************************/

#include "datetime.h"

int main( int argc , char * * argv )
{
	int sockfd , n ;
    int time_server; // 服务器传来的时间（单位：s）
    int time1; // 向服务器发送请求前的本机时间（单位：s）
    int time2; // 收到服务器数据时的本机时间（单位：s）
    int time_syn; // 处理传输时延后，最终用于同步的时间（单位：s）
	char recvline[ MAXLINE + 1];
	struct sockaddr_in servaddr;

	if( argc != 2 )  {
		printf( "usage : a.out <IP address>\n" );
		exit( 1 );
	}

	if( ( sockfd = socket( AF_INET , SOCK_STREAM , 0 ) ) < 0 ) {
		printf( "socket error\n" );
		exit( 1 );
	}

	memset( &servaddr , 0 , sizeof( servaddr ) );
	servaddr.sin_family = AF_INET;
	servaddr.sin_port = htons( 1113 );

	if( inet_pton( AF_INET , argv[ 1 ] , &servaddr.sin_addr ) <= 0 )  {
		printf( "inet_pton error for %s\n" , argv[ 1 ] );
		exit( 1 );
	}

    time1 = time(NULL);
	if( connect( sockfd , (struct sockaddr *)&servaddr , sizeof( servaddr ) ) < 0 )  {
		//printf( "connect error\n" );
        perror( "connect error: " );
		exit( 1 );
	}

	while( ( n = read( sockfd , recvline , MAXLINE ) ) > 0 )  {
		recvline[ n ] = 0;
		if( fputs( recvline , stdout ) == EOF ) {
			printf( "fputs error\n" );
			exit( 1 );
		}
        time2 = time(NULL);
        memcpy(&time_server, recvline, 4);
	}
    time_syn = time_server + (time2 - time1) / 2;
    printf( "总传输时延：%d，服务器时间：%d，实际使用的同步时间：%d\n",
            (time2 - time1), time_server, time_syn );

	if( n < 0 )  {
		printf( "read error\n" );
		exit( 1 );
	}
	exit( 0 );
}
