#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
#include <signal.h>

#define PIPE_IN		"/tmp/earth_in_pipe"
#define PIPE_OUT	"/tmp/earth_out_pipe"
#define CRAWLER 	"python crawler.py "
#define CRAWLERSIZE	20

int pipe_in, pipe_out;

void exit_signal_handler(int signal)
{
	if(signal == 2)
	{
		printf("\n\nExiting....");

		/* Close Connection */
		close(pipe_in);
		close(pipe_out);
		printf("\n..Done!\n\n");
		exit(0);
	}
}

int main()
{
	/* Signal stuff */
	struct sigaction sig_handler;

	char buff[100];

	/* Pipes stuff */
	ssize_t bytes_written;
	int pipe_in, pipe_out;
	int layers;
	char *link = NULL;
	char get[4];

	//Opening pipes
	pipe_in = open(PIPE_IN, O_RDWR);
	if(pipe_in < 0)
	{
		printf("Error openning ");
		puts(PIPE_IN);
		exit(1);
	}

	pipe_out = open(PIPE_OUT, O_RDWR);
	if(pipe_out < 0)
	{
		printf("Error openning ");
		puts(PIPE_OUT);
		exit(1);
	}
	
	while(42)
	{
		int bytes_read, layers;
		char *s_buff = NULL;

		bytes_read = read(pipe_out, buff, sizeof(char)*99);
		s_buff = (char*) malloc(bytes_read*sizeof(char));
		link = (char*) malloc(bytes_read*sizeof(char));
		strncpy(s_buff, buff, bytes_read);
		printf("bytes read: %d\n", bytes_read);
		printf("Pipe out = %s\n", s_buff);
		
		//Parsing command
		int res = strncmp(s_buff, "get", 3);
		if(res == 0)
		{
			FILE *crawler = fopen(CRAWLER, "r");
			strncpy(link, &s_buff[4], bytes_read - 4);
			printf("site: %s\n", link);
			char *callpy = NULL;
			callpy = (char*) malloc(
							(bytes_read + CRAWLERSIZE)*sizeof(char));
			callpy[0] = '\0';
			callpy = strcat(callpy, CRAWLER);
			callpy = strcat(callpy, link);
			printf("%s\n", callpy);
			system(callpy);
			system("chmod +x sedScript.sh");
			system("sh sedScript.sh");
			system("tar -zcf site.tar.gz remotefile* basefile.html");
			//copying to mars
			system("/home/ainsoph/devel/SpaceApp/dtn-2.9.0/apps/dtncp/dtncp site.tar.gz dtn://spaceapps.dtn");
			system("/home/ainsoph/devel/SpaceApp/dtn-2.9.0/apps/dtnsend/dtnsend -s dtn://spaceapps.dtn/me -d dtn://spaceapps.dtn/mars -t m -p \"snt\"");
			printf("%s done!\n", link);
		}
	}
}
