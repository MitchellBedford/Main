#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

//impliment the game
int game(char you, char computer)
{
    //if choise is the same
    if (you == computer)
        return -1;
    
    // If user's choice is rock and computer's choice is paper
    if (you == 's' && computer == 'p')
        return 0;
 
    // If user's choice is paper and computer's choice is rock
    else if (you == 'p' && computer == 's') 
        return 1;
 
    // If user's choice is rock and computer's choice is scissor
    if (you == 's' && computer == 'r')
        return 1;
 
    // If user's choice is scissor and computer's choice is rock
    else if (you == 'r' && computer == 's')
        return 0;
 
    // If user's choice is paper and computer's choice is scissor
    if (you == 'p' && computer == 'r')
        return 0;
 
    // If user's choice is scissor and computer's choice is paper
    else if (you == 'r' && computer == 'p')
        return 1;
}

int main()
{
    //computer makes selection
    int choice = (rand() % 3) + 1;

    printf("%d", choice);

    char you, computer, result;

    //choose a random number every time
    srand(time(NULL));

    //assign the random number with either rock, paper or scissors
    if (choice == 1)
        computer = 's';

    else if (choice == 2)
        computer = 'p';

    else if (choice == 3)
        computer = 'r';

    printf("Enter r for ROCK, p for PAPER and s for \n");

    //input from user
    scanf("%c", &you);

    //call function to play game
    result = game(you, computer);

    if (result == -1) {
        printf("Game Draw!\n");
    }
    else if (result == 1) {
        printf("Wow! You have won the game!\n");
    }
    else {
        printf("Oh! You have lost the game!\n");
    }
        printf("YOu choose : %c and Computer choose : %c\n",you, computer);
 
    return 0;

}