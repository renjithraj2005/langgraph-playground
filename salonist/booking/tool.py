from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from langchain.tools import BaseTool
from pydantic import PrivateAttr

class AvailabilityTool(BaseTool):
    """Tool for checking and managing appointment availability."""
    
    name: str = "check_availability"
    description: str = """Use this tool to check appointment availability.
    Input can be:
    - A specific date in YYYY-MM-DD format (e.g., "2024-03-28")
    - "today" for today's availability
    - "tomorrow" for tomorrow's availability
    - "next_week" for availability next week
    Returns available time slots for that date."""
    
    _availability: Dict[str, List[str]] = PrivateAttr(default_factory=dict)
    
    def __init__(self, **data):
        """Initialize the booking tool with hardcoded data."""
        super().__init__(**data)
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
    
    def _get_date_for_query(self, query: str) -> str:
        """Convert relative date queries to actual dates.
        
        Args:
            query: Date string or relative date query
            
        Returns:
            Date string in YYYY-MM-DD format
        """
        today = datetime.now()
        
        if query == "today":
            return today.strftime("%Y-%m-%d")
        elif query == "tomorrow":
            tomorrow = today + timedelta(days=1)
            return tomorrow.strftime("%Y-%m-%d")
        elif query == "next_week":
            next_week = today + timedelta(days=7)
            return next_week.strftime("%Y-%m-%d")
        else:
            # Assume it's a YYYY-MM-DD format date
            return query
    
    def _run(self, query: str) -> str:
        """Check availability for a specific date.
        
        Args:
            query: Date string or relative date query
            
        Returns:
            String containing available time slots
        """
        date_str = self._get_date_for_query(query)
        
        if date_str not in self._availability:
            return f"No availability found for date {date_str}"
        
        slots = self._availability[date_str]
        if not slots:
            return f"No available slots for date {date_str}"
        
        return f"Available slots for {date_str}: {', '.join(slots)}"
    
    def _arun(self, query: str) -> str:
        """Async version of _run."""
        raise NotImplementedError("Async version not implemented")

tool = AvailabilityTool()

