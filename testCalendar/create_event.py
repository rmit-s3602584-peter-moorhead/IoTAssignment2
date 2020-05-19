from datetime import datetime, timedelta
from cal_setup import get_calendar_service


def main():
    # creates one hour event tomorrow 10 AM IST
    service = get_calendar_service()

    d = datetime.now().date()
    #change this for the amount of 
    numDayBook = 1
    endBook = datetime(d.year, d.month, d.day, 10)+timedelta(days=1)
    start = d.isoformat()
    end = (endBook + timedelta(hours=1)).isoformat()

    event_result = service.events().insert(calendarId='primary',
        body={ 
            "summary": 'Car booking', 
            "description": 'This is the calendar event created for your car booking',
            "start": {"dateTime": start, "timeZone": 'Australia/Sydney'}, 
            "end": {"dateTime": end, "timeZone": 'Australia/Sydney'},
        }
    ).execute()

    print("created event")
    print("id: ", event_result['id'])
    print("summary: ", event_result['summary'])
    print("starts at: ", event_result['start']['dateTime'])
    print("ends at: ", event_result['end']['dateTime'])

if __name__ == '__main__':
    main()
