import math
import datetime

def placeholders(integer, target):
    """
    Pads a base-10 integer to match a specified number of places.
    Raises: 
        1. ValueError if target or integer do not have valid values, 
            or if integer already has at least the target number of 
            places.
    Parameters:
        1. integer: The integer that needs to be padded with zeroes. 
            (Must be >= 0)
        2. target: The number of places "integer" needs to be padded 
            out to. (Must be > 0)
    """
    # Convert parameters to integers (may raise a ValueError)
    int_integer = int(integer)
    int_target = int(target)
    # Error handling
    if (int_integer < 0 or int_target <= 0):
        if int_integer < 0:
            raise ValueError("In function \"placeholders\":\ninteger must be >= 0")
        elif int_target <= 0:
            raise ValueError("In function \"placeholders\":\ntarget number of places must be > 0")
    else:
        target_pow_10 = int_target - 1
        # Special case: math.log10(0) will fail, so just pad 0 out to the 
        # target number of places
        if int_integer == 0:
            i = 0
            result = str(integer)
            while i < target_pow_10:
                result = "0" + result
                i = i + 1
            return result
        # Error: Integer has same number of places as the target value
        elif math.log10(float(int_integer)) == target_pow_10:
            raise ValueError("In function \"placeholders\":\nInteger %s already has %s places. No placeholders can be added." % (integer, target))
        # Error: Integer has more places than the target value
        elif math.log10(float(int_integer)) > target_pow_10:
            raise ValueError("In function \"placeholders\":\nInteger %s has more than %s places. No placeholders can be added." % (integer, target))
        # Pad integer out to target number of places
        elif math.log10(float(int_integer)) < target_pow_10:
            i = 0
            result = str(integer)
            while i < (target_pow_10 - int(math.log10(float(int_integer)))):
                result = "0" + result
                i = i + 1
            return result

def datestring(datetime_datetime):
    """
    Given a datetime.datetime, returns the current time in the format 
    YmdHMSf:
    Y: Year (4 places - not compatible with years >= 10000)
    m: month (2 places)
    d: day (2 places)
    H: minute (2 places)
    M: minute (2 places)
    S: second (2 places)
    f: microsecond (6 places)
    
    Raises: 
        1. TypeError if datetime_datetime is not a datetime.datetime object
        2. ValueError if year is > 10000 
    Parameters:
        1. datetime_datetime: A datetime.datetime object.
    """
    if (datetime_datetime is not datetime.datetime):
        raise TypeError("In function \"datestring\": %s is not a datetime object." % datetime_datetime)
    current = datetime_datetime.now()
    year = -1
    month = -1
    day = -1
    hour = -1
    minute = -1
    second = -1
    microsec = -1
    
    # Year
    if current.year < 1000:
        year = placeholders(current.year, 4)
    elif current.year >= 10000:
        raise ValueError("In function \"datestring\": Year %s >= 10000, function assumes years <= 9999" % current.year)
    else:
        year = str(current.year)
    
    # Month
    if current.month < 10:
        month = placeholders(current.month, 2)
    else:
        month = str(current.month)
    
    # Day
    if current.day < 10:
        day = placeholders(current.day, 2)
    else:
        day = str(current.day)
    
    # Hour
    if current.hour < 10:
        hour = placeholders(current.hour, 2)
    else:
        hour = str(current.hour)
    
    # Minute
    if current.minute < 10:
        minute = placeholders(current.day, 2)
    else:
        minute = str(current.minute)
    
    # Second
    if current.second < 10:
        second = placeholders(current.second, 2)
    else:
        second = str(current.second)
    
    # Microsecond
    if current.microsecond < 100000:
        microsec = placeholders(current.microsecond, 6)
    else:
        microsec = str(current.microsecond)
    
    return year + month + day + hour + minute + second + microsec