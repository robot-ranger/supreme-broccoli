"""
MTConnect Protocol Header

Header class for MTConnect response documents containing metadata about the
agent, timing, and sequence tracking information.

Reference: MTConnect Standard v2.6 - Protocol Specification
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from mtconnect.types.primitives import MTCDateTime, Version


@dataclass
class Header:
    """
    Header for MTConnect response documents.
    
    Contains metadata about the MTConnect agent, timing information, and
    sequence number tracking for data stream management. Present in all
    MTConnect response types (Devices, Streams, Assets, Error).
    
    Reference: https://model.mtconnect.org/#Package___19_0_3_68e0225_1622798866752_358680_13276
    """
    creation_time: MTCDateTime
    sender: str
    instance_id: int
    version: Version
    device_model_change_time: Optional[MTCDateTime] = None
    test_indicator: bool = False
    
    # Sequence tracking (for Streams responses)
    buffer_size: Optional[int] = None
    first_sequence: Optional[int] = None
    last_sequence: Optional[int] = None
    next_sequence: Optional[int] = None
    
    # Asset tracking (for Assets responses)
    asset_buffer_size: Optional[int] = None
    asset_count: Optional[int] = None
    
    def __post_init__(self):
        """Validate header after initialization"""
        if isinstance(self.creation_time, str):
            self.creation_time = MTCDateTime(self.creation_time)
        
        if isinstance(self.version, str):
            self.version = Version(self.version)
        
        if self.device_model_change_time and isinstance(self.device_model_change_time, str):
            self.device_model_change_time = MTCDateTime(self.device_model_change_time)
        
        if self.instance_id < 0:
            raise ValueError(f"Instance ID must be non-negative, got {self.instance_id}")
        
        # Validate sequence numbers are consistent
        if self.first_sequence is not None and self.last_sequence is not None:
            if self.first_sequence > self.last_sequence:
                raise ValueError(
                    f"first_sequence ({self.first_sequence}) cannot be greater than "
                    f"last_sequence ({self.last_sequence})"
                )
        
        if self.next_sequence is not None and self.last_sequence is not None:
            if self.next_sequence != self.last_sequence + 1:
                # Log warning but don't fail - some agents may have gaps
                pass
    
    def has_sequence_info(self) -> bool:
        """Check if header contains sequence tracking information"""
        return (
            self.buffer_size is not None and
            self.first_sequence is not None and
            self.last_sequence is not None
        )
    
    def available_sequence_range(self) -> Optional[tuple[int, int]]:
        """
        Get the range of available sequence numbers in the buffer.
        
        Returns:
            Tuple of (first, last) sequence numbers, or None if not available
        """
        if self.first_sequence is not None and self.last_sequence is not None:
            return (self.first_sequence, self.last_sequence)
        return None
    
    def observations_in_buffer(self) -> Optional[int]:
        """
        Calculate number of observations currently in buffer.
        
        Returns:
            Number of observations, or None if sequence info not available
        """
        if self.first_sequence is not None and self.last_sequence is not None:
            return self.last_sequence - self.first_sequence + 1
        return None
    
    def buffer_utilization_percent(self) -> Optional[float]:
        """
        Calculate buffer utilization as percentage.
        
        Returns:
            Percentage (0-100), or None if buffer info not available
        """
        if self.buffer_size and self.first_sequence is not None and self.last_sequence is not None:
            obs_count = self.observations_in_buffer()
            if obs_count is not None:
                return (obs_count / self.buffer_size) * 100.0
        return None
    
    def is_buffer_nearly_full(self, threshold_percent: float = 90.0) -> bool:
        """
        Check if buffer utilization exceeds threshold.
        
        Args:
            threshold_percent: Percentage threshold (default 90%)
        
        Returns:
            True if buffer utilization >= threshold, False otherwise
        """
        util = self.buffer_utilization_percent()
        return util is not None and util >= threshold_percent
    
    def sequence_is_available(self, sequence: int) -> bool:
        """
        Check if a specific sequence number is still in the buffer.
        
        Args:
            sequence: Sequence number to check
        
        Returns:
            True if sequence is within the buffer range, False otherwise
        """
        if self.first_sequence is None or self.last_sequence is None:
            return False
        return self.first_sequence <= sequence <= self.last_sequence
    
    def is_test_mode(self) -> bool:
        """Check if agent is in test mode"""
        return self.test_indicator
