"""
Learning Extension Plugin - Adaptive learning and improvement
"""
from typing import Dict, List, Any
from dataclasses import dataclass
import time

@dataclass
class LearningEvent:
    event_type: str
    timestamp: float
    success: bool
    data: Dict[str, Any]

class LearningExtension:
    def __init__(self):
        self.events: List[LearningEvent] = []
        self.patterns: Dict[str, List[str]] = {}
        self.success_rates: Dict[str, float] = {}
    
    def record_event(self, event_type: str, success: bool, data: Dict[str, Any] = None) -> None:
        """Record a learning event"""
        event = LearningEvent(
            event_type=event_type,
            timestamp=time.time(),
            success=success,
            data=data or {}
        )
        self.events.append(event)
        self._update_success_rate(event_type, success)
    
    def _update_success_rate(self, event_type: str, success: bool) -> None:
        """Update success rate for event type"""
        if event_type not in self.success_rates:
            self.success_rates[event_type] = 1.0 if success else 0.0
        else:
            # Running average
            current = self.success_rates[event_type]
            self.success_rates[event_type] = (current * 0.9) + (1.0 if success else 0.0) * 0.1
    
    def identify_patterns(self) -> Dict[str, Any]:
        """Identify patterns in learning events"""
        patterns = {}
        
        # Analyze success patterns
        for event_type, rate in self.success_rates.items():
            if rate > 0.8:
                patterns[event_type] = "highly_successful"
            elif rate < 0.3:
                patterns[event_type] = "needs_improvement"
        
        return patterns
    
    def get_recommendations(self) -> List[str]:
        """Get learning-based recommendations"""
        recommendations = []
        patterns = self.identify_patterns()
        
        for event_type, pattern in patterns.items():
            if pattern == "needs_improvement":
                recommendations.append(f"Focus on improving: {event_type}")
            elif pattern == "highly_successful":
                recommendations.append(f"Leverage strength in: {event_type}")
        
        return recommendations
