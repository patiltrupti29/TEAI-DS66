import heapq
import time
from typing import List, Dict, Any

# ==========================================
# Priority Weight Configuration
# placement > result > event
# ==========================================

WEIGHT_MAPPING = {
    "placement": 3,
    "result": 2,
    "event": 1
}

# ==========================================
# Calculate Priority Tuple
# ==========================================

def get_priority_tuple(notification: Dict[str, Any]) -> tuple:

    notification_type = notification.get("type", "event")

    weight = WEIGHT_MAPPING.get(notification_type, 1)

    timestamp = notification.get("timestamp", 0)

    notification_id = notification.get("id", 0)

    return (weight, timestamp, notification_id)


# ==========================================
# Maintain Top N Notifications Using Min Heap
# ==========================================

def maintain_priority_inbox(
    notification_stream,
    n: int = 10
) -> List[Dict[str, Any]]:

    min_heap = []

    print(f"\nProcessing Notification Stream...")
    print(f"Maintaining Top {n} Notifications\n")

    for notification in notification_stream:

        priority_score = get_priority_tuple(notification)

        heapq.heappush(
            min_heap,
            (priority_score, notification)
        )

        # Keep heap size fixed to N
        if len(min_heap) > n:
            removed = heapq.heappop(min_heap)

            print(
                f"Removed Lowest Priority -> "
                f"{removed[1]['message']}"
            )

    # Extract notifications only
    top_notifications = [
        item[1]
        for item in min_heap
    ]

    # Sort highest priority first
    top_notifications.sort(
        key=lambda x: get_priority_tuple(x),
        reverse=True
    )

    return top_notifications


# ==========================================
# Mock Notification API Stream
# ==========================================

def mock_notification_api_stream():

    current_time = int(time.time())

    return [

        {
            "id": 101,
            "type": "event",
            "message": "User logged in",
            "timestamp": current_time - 50
        },

        {
            "id": 102,
            "type": "result",
            "message": "Test execution passed",
            "timestamp": current_time - 40
        },

        {
            "id": 103,
            "type": "placement",
            "message": "Placement drive announced",
            "timestamp": current_time - 30
        },

        {
            "id": 104,
            "type": "event",
            "message": "System health check",
            "timestamp": current_time - 20
        },

        {
            "id": 105,
            "type": "placement",
            "message": "Premium company hiring",
            "timestamp": current_time - 10
        },

        {
            "id": 106,
            "type": "result",
            "message": "Semester results published",
            "timestamp": current_time - 5
        },

        {
            "id": 107,
            "type": "event",
            "message": "Button clicked",
            "timestamp": current_time
        },

        {
            "id": 108,
            "type": "placement",
            "message": "Amazon placement registration open",
            "timestamp": current_time + 5
        },

        {
            "id": 109,
            "type": "result",
            "message": "Compilation completed",
            "timestamp": current_time + 10
        },

        {
            "id": 110,
            "type": "event",
            "message": "File downloaded",
            "timestamp": current_time + 15
        },

        {
            "id": 111,
            "type": "placement",
            "message": "Microsoft interview shortlist released",
            "timestamp": current_time + 20
        },

        {
            "id": 112,
            "type": "event",
            "message": "Background sync completed",
            "timestamp": current_time + 25
        }

    ]


# ==========================================
# Main Execution
# ==========================================

if __name__ == "__main__":

    api_stream = mock_notification_api_stream()

    top_10_notifications = maintain_priority_inbox(
        api_stream,
        n=10
    )

    print("\n==========================================")
    print("       TOP 10 PRIORITY NOTIFICATIONS")
    print("==========================================\n")

    for rank, notification in enumerate(
        top_10_notifications,
        start=1
    ):

        notification_type = notification["type"].upper()

        message = notification["message"]

        timestamp = notification["timestamp"]

        print(
            f"Rank {rank:02d} | "
            f"Type: {notification_type:<10} | "
            f"Timestamp: {timestamp} | "
            f"Message: {message}"
        )

    print("\n==========================================")