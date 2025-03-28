from typing import List, Dict, Any
from datetime import datetime, timedelta

class BookingTool:
    """Tool for checking and managing appointment availability."""
    
    def __init__(self):
        """Initialize the booking tool with hardcoded data."""
        # Generate some hardcoded availability for the next 7 days
        self._availability = self._generate_hardcoded_availability()
    
    def _generate_hardcoded_availability(self) -> Dict[str, List[str]]:
        """Generate hardcoded availability data for demo purposes."""
        availability = {}
        today = datetime.now()
        
        # Generate slots for the next 7 days
        for i in range(7):
            day = today + timedelta(days=i)
            date_str = day.strftime("%Y-%m-%d")
            
            # Create slots from 9 AM to 5 PM, every 30 minutes
            slots = []
            for hour in range(9, 17):
                for minute in [0, 30]:
                    # Skip some slots to simulate unavailability
                    if (hour == 12 and minute == 0) or (hour == 13 and minute == 0):
                        continue
                    
                    # Make some days have fewer slots
                    if i == 2 and hour >= 14:
                        continue
                    if i == 5 and hour <= 11:
                        continue
                    
                    time_str = f"{hour:02d}:{minute:02d}"
                    slots.append(time_str)
            
            availability[date_str] = slots
        
        return availability
    
    def get_available_dates(self) -> List[str]:
        """Get a list of dates with available slots."""
        return list(self._availability.keys())
    
    def get_available_slots(self, date_str: str) -> List[str]:
        """Get available time slots for a specific date.
        
        Args:
            date_str: Date string in YYYY-MM-DD format
            
        Returns:
            List of available time slots in HH:MM format
        """
        return self._availability.get(date_str, [])
    
    def check_availability(self, date_str: str, time_str: str) -> bool:
        """Check if a specific date and time slot is available.
        
        Args:
            date_str: Date string in YYYY-MM-DD format
            time_str: Time string in HH:MM format
            
        Returns:
            True if the slot is available, False otherwise
        """
        slots = self._availability.get(date_str, [])
        return time_str in slots
    
    def book_appointment(self, date_str: str, time_str: str) -> Dict[str, Any]:
        """Book an appointment at the specified date and time.
        
        Args:
            date_str: Date string in YYYY-MM-DD format
            time_str: Time string in HH:MM format
            
        Returns:
            Appointment details or error message
        """
        if not self.check_availability(date_str, time_str):
            return {
                "success": False,
                "message": f"The slot at {date_str} {time_str} is not available."
            }
        
        # Remove the slot from availability to simulate booking
        self._availability[date_str].remove(time_str)
        
        return {
            "success": True,
            "appointment": {
                "date": date_str,
                "time": time_str,
                "confirmation_code": f"BOOK-{hash(date_str + time_str) % 10000:04d}"
            }
        }
