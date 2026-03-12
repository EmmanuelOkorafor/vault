//C:\Users\EMMANUEL\Documents\Projects\Other\Practise

#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include<ctype.h>
#include<math.h>

int main(void)
{
    long long Visa13 = 4199249241981;
    long long Visa16 = 4638342752323293;
    long long MasterCard = 5174934221929994;
    long long Amex = 347948486715354;
    long long creditCardNumber = MasterCard;
    int count = 0;
    long long digits = creditCardNumber;
    long long length = creditCardNumber;

    while ( length > 0)
    {
        length = length / 10;
        count++;
    }

    if( ( count != 13 ) && ( count != 15 ) && ( count != 16 ) )
    {
        printf("INVALID / INCOMPLETE CARD NUMBER\n");
    }

    int number[count];

    for( int i = 0; i < count; i++)
    {
        number[i] = creditCardNumber % 10;
        creditCardNumber = creditCardNumber / 10;
    }


    int cardarray[count];
    for ( int i = 1; i < count; i++ )
    {
        cardarray[i] = number[i];
    }

    for ( int i = 1; i < count; i+=2 )
    {
        number[i] = number[i] * 2;
    }


    int accumulator = 0;
    int sumdigits;
       
    if ( count == 13 )
    {
        for ( int i = 0; i < count; i++ )
        {
            sumdigits = ( number[i] % 10 ) + ( number[i] / 10 % 10);
            accumulator = accumulator + sumdigits;
        }

        if ( cardarray[12] == 4 && accumulator % 10 == 0 )
        {
            printf("VISA-13\n");
        }

        else
        {
            printf("INVALID\n");
        }

    }

    if ( count == 15 )
    {
        for ( int i = 0; i < count; i++ )
        {
            sumdigits = ( number[i] % 10 ) + ( number [i] / 10 % 10 );
            accumulator = accumulator + sumdigits;
        }

        if ( cardarray [14] == 3 && accumulator % 10 == 0 && ( cardarray[13] == 4 || cardarray[13] == 7 ) )
        {
            printf("AMEX\n");
        }

        else
        {
            printf("INVALID\n");
        }
    }

    if ( count == 16 )
    {
        for ( int i = 0; i < count; i++ )
        {
            sumdigits = ( number[i] % 10 ) + ( number[i] / 10 % 10 );
            accumulator = accumulator + sumdigits;
        }

        if ( cardarray[15] == 4 && accumulator % 10 == 0 )
        {
            printf("VISA-16\n");
        }

        else if ( cardarray[15] == 5 && accumulator % 10 == 0 && ( cardarray[14] == 1 || cardarray[14] == 2 || cardarray[14] == 3 || cardarray[14] == 4 || cardarray[14] == 5))
        {
            printf("MASTERCARD\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }

    return 0;
}