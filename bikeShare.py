import time
import pandas as pd
import numpy as np
import datetime as dt

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = None  # type: str
    month = None  # type: str
    day = None  # type: str
    choice = None  # type: str or tuple
    
    cityOption = ['chicago', 'new york city', 'washington']
    monthOption = ['january', 'february', 'march', 'april', 'may', 'june']
    choiceOption = ['month', 'day', 'none', 'both']

    # TO DO: get user input for month (all, january, february, ... , june)
    while city not in cityOption:
        city = str(input('Would you like to see data for Chicago, '
        'New York City, or Washington?')).lower().strip()

    while choice not in choiceOption:
        choice = str(input("Would you like to filter the data by month, day, both or not at all? "
                           "Type \"none\" for no time filter. ")).lower().strip()

    # for choice is none no filtering is required
    if choice == "none":
        month = "all"
        day = "all"

    # for choice is both input month and day
    if choice == "both":
        choice = 'month','day'

    # get user input for month (all, january, february, ... , june)
    if 'month' in choice:
        while month not in monthOption:
            month = str(input('Which month? January, February, March, April, May or June. ')).lower().strip()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    if 'day' in choice:
        while day not in ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']:
            day = str(input('Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday. ')).lower().strip()

    if day == None:
        day="all"

    if month == None:
        month="all"

    print('-' * 40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    if month == 'all':
        #Add a new column for month as month
        df['month']=df['Start Time'].dt.month
    else:
        # filter by month
        monthOption = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6}
        df = df[df['Start Time'].dt.month == monthOption[month]]
    
    if day == 'all':
        #Add a new column for day of week as day
        df['day']=df['Start Time'].dt.weekday_name

    elif day != None:
        #filter by day of week
        df = df[df['Start Time'].dt.weekday_name == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    if 'month' in df.columns:
        popular_month = df['month'].mode()[0]
        count = df['month'].value_counts(dropna=True)[popular_month]
        print("Most popular month:",popular_month," Count:",count)

    # display the most common day of week
    if 'day' in df.columns:
        popular_day = df['day'].mode()[0]
        count = df['day'].value_counts(dropna=True)[popular_day]
        print("Most popular day of week:",popular_day.title()," Count:",count)


    # TO DO: display the most common start hour
    # display the most common start hour
    popular_hour = df['Start Time'].dt.hour.mode()[0]
    count = df['Start Time'].dt.hour.value_counts(dropna=True)[popular_hour]
    print("Most popular hour:",popular_hour," Count:",count)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
  
    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    count = df['Start Station'].value_counts(dropna=True)[popular_start_station]
    print("Most popular start station:",popular_start_station.title()," Count:",count)


    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    count = df['End Station'].value_counts(dropna=True)[popular_end_station]
    print("Most popular end station:",popular_end_station.title()," Count:",count)


    # TO DO: display most frequent combination of start station and end station trip
    df['Trip']=df['Start Station']+' - '+df['End Station']
    popular_trip = df['Trip'].mode()[0]
    count = df['Trip'].value_counts(dropna=True)[popular_trip]
    print("Most popular trip:",popular_trip.title()," Count:",count)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum(skipna=True)
    count=df['Trip Duration'].count()


    # TO DO: display mean travel time
    average_travel_time = total_travel_time/(count)
    print("Total Duration:",total_travel_time," Count:",count,
    " Average Duration:",average_travel_time)



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count=df['User Type'].value_counts(dropna=True)
    subscriber=count['Subscriber']
    customer=count['Customer']
    print("Subscriber:",subscriber," Customer:",customer)



    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        gender=df['Gender'].value_counts(dropna=True)
        male=gender['Male']
        female=gender['Female']
        print("Male:",male," Female:",female)


    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        #Display earliest birth year
        earliest_year=df['Birth Year'].min(skipna=True)
        count = df['Birth Year'].value_counts(dropna=True)[earliest_year]
        print("Earliest year:",earliest_year," Count:",count)

        #Display most recent year
        recent_year=df['Birth Year'].max(skipna=True)
        count = df['Birth Year'].value_counts(dropna=True)[recent_year]
        print("Recent year:",recent_year," Count:",count)

        #Display most popular Year
        popular_year=df['Birth Year'].mode()[0]
        count = df['Birth Year'].value_counts(dropna=True)[popular_year]
        print("Popular year:",popular_year," Count:",count)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
