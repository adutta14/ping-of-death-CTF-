# include <stdio.h>
# include <string.h>
# include <stdlib.h>

// Function to be used to sanitize input params for OS command injection through ;
char * santizeSemicolon(char *input){
	int i=0;
	//printf("Input in function: %s\n", input);
	char * sanitizedInput = malloc(sizeof(input));
	while(input[i] != '\0'){
		if(input[i] == ';'){
			//printf("Semicolon found \n");
			//sanitizedInput[i++] = ';';
			sanitizedInput[i] = '\0';
			break;
		} else {
			sanitizedInput[i] = input[i];
		}
		i++;
	}
	return sanitizedInput;
}

// Function to be used to sanitize input params for path attacks through ../
char * santizeDotDot(char *input){
	int i=0, j=0;
	////printf("Input in function: %s\n", input);
	char * newInput = malloc(sizeof(input));
	int len = strlen(input);
	while(i < len){
		if(input[i] == '.' && input[i+1] == '.' && input[i+2] == '/'){
			//printf("../ found \n");
			i = i + 3;
		} else if(input[i] == '.' && input[i+1] == '.'){
			//printf(".. found \n");
			i = i + 2;
		} 
		else {
			//printf("%c\n", input[i]);
			newInput[j] = input[i];
			i++;
			j++;
		}
	}
	newInput[j] = '\0';
	//printf("j sanitizedInput after .. : %d %s\n", j, newInput);
	return newInput;
}

// '../command_injection.c;echo c'



// Test Stub
int main(int argc, char **argv) {
	char cat[] = "cat ";
	char *command;
	size_t commandLength;

	//printf("Input in main: %s\n", argv[1]);

	argv[1] = santizeSemicolon(argv[1]);
	printf("Input in main after Semicolon: %s\n", argv[1]);
	argv[1] = santizeDotDot(argv[1]);
	//printf("sanitizedInput after .. : %s\n", argv[1]);

	commandLength = strlen(cat) + strlen(argv[1]) + 1;
	command = (char *) malloc(commandLength);
	strncpy(command, cat, commandLength);
	strncat(command, argv[1], (commandLength - strlen(cat)) );

	system(command);
	return (0);
}